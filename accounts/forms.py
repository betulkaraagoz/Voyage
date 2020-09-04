from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django import forms

# class CustomerSignUpForm(ModelForm):
#     class Meta:
#         model = Customer

#
# class OwnerSignUpForm(ModelForm):
#     class Meta:
#         model = Owner
#         fields = ('email',)


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.save()
        return user


class OwnerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = user.username
        user.is_staff = True
        user.save()
        return user

