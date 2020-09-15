import operator
import re
from nltk.corpus import stopwords
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from accommodation.models import Hotel, Room, Reservation, Review, AdditionalImages
from accounts.models import CustomerLikes, UserPP
from blog.models import BlogPost
from .forms import ReviewForm, ReservationForm
from django.db.models import Q
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
import pandas as pd
from datetime import datetime

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))


class Home(View):
    def get(self, request):
        unsorted_blogs = BlogPost.objects.all()

        blog_all = sorted(unsorted_blogs, key=lambda t: t.get_likes_no(), reverse=True)
        blogs = []
        for i in range(len(blog_all)):
            if i < 3:
                blogs.append(blog_all[i])

        popularity = {}
        pop_hotels = []
        for hotel in Hotel.objects.all():
            popularity[hotel] = hotel.get_popularity()

        sorted_hotel = sorted(popularity.items(), key=operator.itemgetter(1), reverse=True)

        for i in range(len(sorted_hotel)):
            if i < 6:
                pop_hotels.append(sorted_hotel[i][0])

        return render(request, 'index.html', {'blogs': blogs, 'pop_hotels': pop_hotels})

    def post(self, request):
        search_term = request.POST.get('search')

        unsorted_hotels = Hotel.objects.filter(Q(location__icontains=search_term) | Q(name__icontains=search_term))
        hotels = sorted(unsorted_hotels, key=lambda t: t.get_avg_rating(), reverse=True)

        paginator = Paginator(hotels, 15, orphans=5)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page') or 1
        try:
            current_page = paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        context = {
            'current_page': current_page,
            'is_paginated': is_paginated
        }

        return render(request, 'customer_hotel_view.html', context)


class Hotels(LoginRequiredMixin, View):
    def get(self, request):
        hotels = Hotel.objects.filter(owner=request.user.id)

        hotel_up_reservations = {}
        for hotel in hotels:
            income = 0
            for reservation in Reservation.objects.filter(room__assoc_hotel=hotel,
                                                          check_out__lte=datetime.now().date()):
                income += reservation.days() * 1000

            hotel_up_reservations[hotel] = [Reservation.objects.filter(room__assoc_hotel=hotel,
                                                                       check_in__gte=datetime.now().date()), income]

        return render(request, 'hotels.html', {'dict': hotel_up_reservations})


class HotelHomePage(LoginRequiredMixin, View):
    def get(self, request, hotel_id):
        form = ReservationForm()
        reviews = Review.objects.select_related('customer', 'hotel').filter(hotel_id=hotel_id)
        reviews_count = reviews.count()
        hotel = Hotel.objects.get(id=hotel_id)
        images = AdditionalImages.objects.select_related('hotel').filter(hotel_id=hotel_id)
        is_liked = CustomerLikes.objects.filter(liked_hotel_id=hotel_id, user_id=request.user.id).exists()

        pps = {}
        for review in reviews:
            pps[review] = UserPP.objects.get(user_id=review.customer.id)

        ds = pd.DataFrame(list(Hotel.objects.all().values('description', 'name', 'location', 'number_of_stars')))

        def clean_text(text):
            text = text.lower()  # lowercase text
            text = REPLACE_BY_SPACE_RE.sub(' ', text)
            text = BAD_SYMBOLS_RE.sub('', text)
            text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # remove stopwors from text
            return text

        ds['desc_clean'] = ds['description'].apply(clean_text)

        ds.set_index('name', inplace=True)
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['desc_clean'])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        indices = pd.Series(ds.index)

        def recommendations(name, cosine_similarities=cosine_similarities):
            recommended_hotels = []
            idx = indices[indices == name].index[0]
            score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
            top_10_indexes = list(score_series.iloc[1:6].index)
            for i in top_10_indexes:
                recommended_hotels.append(Hotel.objects.get(name=list(ds.index)[i]))

            return recommended_hotels


        return render(request, 'hotel_homepage.html',
                      {'hotel': hotel, 'reviews': reviews, 'count': reviews_count,
                       'form': form, 'images': images, 'liked': is_liked, 'dict': pps,
                       'recommendations': recommendations(hotel.name)})


class AddHotels(LoginRequiredMixin, View):
    def post(self, request):
        if request.POST['name'] and request.FILES['icon'] and request.FILES.get('image') and request.POST['description'] \
                and request.POST['rooms'] and request.POST['location_url'] and request.FILES['files']:

            new_hotel = Hotel()
            new_hotel.name = request.POST['name']
            new_hotel.icon = request.FILES['icon']
            new_hotel.image = request.FILES['image']
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

            for picture in request.FILES.getlist('files'):
                photo = AdditionalImages(hotel=new_hotel, image=picture)
                photo.save()

            return redirect('hotels')

        else:
            return render(request, 'add_hotel.html', {'error': 'All fields are required'})

    def get(self, request):
        return render(request, 'add_hotel.html')


class HotelViewForCustomer(LoginRequiredMixin, View):
    def get(self, request):
        unsorted_hotels = Hotel.objects.all().order_by('image').reverse()
        hotels = sorted(unsorted_hotels, key=lambda t: t.get_avg_rating(), reverse=True)

        paginator = Paginator(hotels, 15, orphans=5)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page') or 1
        try:
            current_page = paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        context = {
            'current_page': current_page,
            'is_paginated': is_paginated
        }

        return render(request, 'customer_hotel_view.html', context)

    def post(self, request):
        return redirect('reservations')


class ListReservations(LoginRequiredMixin, View):
    def get(self, request):
        review_form = ReviewForm()
        upcoming_reservations = Reservation.objects.filter(check_out__gte=datetime.now().date(),
                                                           guest=request.user).order_by('check_in')
        previous_reservations = Reservation.objects.filter(check_out__lte=datetime.now().date(),
                                                           guest=request.user).order_by('check_in')

        suggestions = []

        for reservation in upcoming_reservations:
            blogs = BlogPost.objects.filter(Q(title__contains=reservation.room.assoc_hotel.location.lower().split(", ")[0]) | Q(
                title__icontains=reservation.room.assoc_hotel.name.lower()) | Q(
                place__icontains=reservation.room.assoc_hotel.name.lower()) | Q(
                place__icontains=reservation.room.assoc_hotel.location.lower().split(", ")[0]) | Q(
                place__icontains=reservation.room.assoc_hotel.location.lower().split(", ")[1]) | Q(
                title__contains=reservation.room.assoc_hotel.location.lower().split(", ")[1]))

            for blog in blogs:
                if blog not in suggestions:
                    suggestions.append(blog)

        return render(request, 'view_reservations.html',
                      {'previous_reservations': previous_reservations, 'upcoming_reservations': upcoming_reservations,
                       'form': review_form, 'suggestions': suggestions})


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
        else:
            print(reservation_form.errors)

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


class DeleteReservation(LoginRequiredMixin, View):
    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.delete()
        return redirect('reservations')


class DeleteReview(View):
    def post(self, request, review_id):
        review = Review.objects.get(id=review_id)
        review.delete()
        return redirect('profile')


class AjaxLike(View):
    def post(self, request, hotel_id):
        hotel = Hotel.objects.get(id=hotel_id)
        like = CustomerLikes.objects.create(user=request.user, liked_hotel=hotel)
        like.save()
        return redirect('reservations')


class AjaxUnlike(View):
    def post(self, request, hotel_id):
        hotel = Hotel.objects.get(id=hotel_id)
        like = CustomerLikes.objects.filter(user=request.user, liked_hotel=hotel)
        like.delete()
        return redirect('reservations')


class DestinationsView(View):
    def get(self, request, place):
        unsorted_hotels = Hotel.objects.filter(location__icontains=place).order_by('image').reverse()
        hotels = sorted(unsorted_hotels, key=lambda t: t.get_avg_rating(), reverse=True)

        paginator = Paginator(hotels, 15, orphans=5)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page') or 1
        try:
            current_page = paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        context = {
            'current_page': current_page,
            'is_paginated': is_paginated
        }

        return render(request, 'customer_hotel_view.html', context)
