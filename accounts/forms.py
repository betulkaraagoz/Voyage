from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import ModelForm

# class CustomerSignUpForm(ModelForm):
#     class Meta:
#         model = Customer

#
# class OwnerSignUpForm(ModelForm):
#     class Meta:
#         model = Owner
#         fields = ('email',)


class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()

        return user


class OwnerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_staff = True
        user.save()

        return user
