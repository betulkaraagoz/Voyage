from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views import View
from .models import Hotel, Room, Reservation, Review, AdditionalImages
from .forms import ReviewForm, ReservationForm
from django.forms import modelformset_factory


class Home(View):
    def get(self, request):
        return render(request, 'index.html')


class Hotels(View):
    def get(self, request):
        hotels = Hotel.objects.filter(owner=request.user.id)

        return render(request, 'hotels.html', {'hotels': hotels})


class HotelHomePage(View):
    def get(self, request, hotel_id):
        form = ReservationForm()
        rooms = Room.objects.filter(assoc_hotel_id=hotel_id)
        reviews = Review.objects.filter(hotel_id=hotel_id)
        reviews_count = reviews.count()
        hotel = Hotel.objects.get(id=hotel_id)
        images = AdditionalImages.objects.filter(hotel_id=hotel_id)
        return render(request, 'hotel_homepage.html',
                      {'hotel': hotel, 'rooms': rooms, 'reviews': reviews, 'count': reviews_count,
                       'form': form, 'images': images})


class AddHotels(View):
    def post(self, request):
        ImageFormSet = modelformset_factory(AdditionalImages, fields=('image',), extra=5)
        if request.POST['name'] and request.FILES['icon'] and request.FILES['image'] and request.POST['description'] and \
                request.POST['rooms'] and request.POST['location_url']:
            formset = ImageFormSet(request.POST or None, request.FILES or None)

            new_hotel = Hotel()
            new_hotel.name = request.POST['name']
            new_hotel.icon = request.FILES['icon']
            new_hotel.image = request.FILES['image']

            if request.POST['location_url'].startswith('http://') or request.POST['location_url'].startswith(
                    'https://'):
                new_hotel.location_url = request.POST['location_url']
            else:
                new_hotel.location_url = 'http://' + request.POST['location_url']

            new_hotel.location_url = request.POST['location_url']
            new_hotel.description = request.POST['description']
            new_hotel.number_of_rooms = request.POST['rooms']
            new_hotel.location = request.POST['location']
            new_hotel.owner = request.user
            new_hotel.save()

            for i in range(int(new_hotel.number_of_rooms)):
                new_room = Room(
                    name='room' + str(i),
                    price=1000,
                    number_of_people=4,
                    assoc_hotel=new_hotel,
                )
                new_room.save()

            if formset.is_valid():
                for f in formset:
                    try:
                        photo = AdditionalImages(hotel=new_hotel, image=f.cleaned_data['image'])
                        photo.save()
                    except Exception as e:
                        break

            return redirect('hotels')

        else:
            return render(request, 'add_hotel.html', {'error': 'All fields are required'})

    def get(self, request):
        ImageFormSet = modelformset_factory(AdditionalImages, fields=('image',), extra=5)
        formset = ImageFormSet(queryset=AdditionalImages.objects.none())
        return render(request, 'add_hotel.html', {'formset': formset})


class HotelViewForCustomer(View):
    def get(self, request):
        unsorted_hotels = Hotel.objects.all()
        rooms = Room.objects.all()
        hotels = sorted(unsorted_hotels, key=lambda t: t.get_avg_rating(), reverse=True)
        return render(request, 'customer_hotel_view.html', {'hotels': hotels, 'rooms': rooms})

    def post(self, request):
        return redirect('reservations')


class ListReservations(View):
    def get(self, request):
        review_form = ReviewForm()
        upcoming_reservations = Reservation.objects.filter(check_out__gte=datetime.now().date()).order_by('check_in')
        previous_reservations = Reservation.objects.filter(check_out__lte=datetime.now().date()).order_by('check_in')
        return render(request, 'view_reservations.html',
                      {'previous_reservations': previous_reservations, 'upcoming_reservations': upcoming_reservations,
                       'form': review_form})


class AjaxListReservations(View):
    def post(self, request, id):
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = request.POST.get('review')
            rating = request.POST.get('rating')

        customer = request.user
        hotel = Hotel.objects.get(id=id)

        review = Review.objects.create(customer=customer, rating=rating, hotel=hotel, review=review,
                                       date=datetime.now())
        review.save()
        return redirect('reservations')


class AjaxMakeReservation(View):
    def post(self, request, hotel_id):
        reservation_form = ReservationForm(request.POST)

        if reservation_form.is_valid():
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            room = Room.objects.filter(assoc_hotel_id=hotel_id, name__contains=request.POST.get('room')).first()

        guest = request.user

        case_1 = Reservation.objects.filter(room=room, check_in__lte=check_in, check_out__gte=check_in).exists()
        case_2 = Reservation.objects.filter(room=room, check_in__lte=check_out, check_out__gte=check_out).exists()
        case_3 = Reservation.objects.filter(room=room, check_in__gte=check_in, check_out__lte=check_out).exists()

        if case_1 or case_2 or case_3:
            return render(request, "hotel_homepage.html",
                          {"errors": "This room is not available on your selected dates"})

        reservation = Reservation.objects.create(check_in=check_in, check_out=check_out, room=room, guest=guest)

        reservation.save()

        return redirect("reservations")


class DeleteReservation(View):
    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.delete()
        return redirect('reservations')
