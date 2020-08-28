from accommodation.models import Review, Reservation
from django.forms import ModelForm


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation

        fields = ['check_in', 'check_out', 'room']

