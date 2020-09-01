from django import forms

from accommodation.models import Review, Reservation, Room


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        widgets = {
            'review': forms.Textarea(attrs={'class': 'ckeditor'}),
        }

        fields = ['review', 'rating']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation

        widgets = {
            'check_in': forms.DateInput(attrs={'class': 'datepicker_1'}),
            'check_out': forms.DateInput(attrs={'class': 'datepicker_2'}),
            'room': forms.Select(attrs={'class': 'js-example-basic-single'})
        }

        fields = ['check_in', 'check_out', 'room']



