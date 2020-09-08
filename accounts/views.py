from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import View

from accommodation.models import Review
from accounts.forms import CustomerSignUpForm, OwnerSignUpForm
from accounts.models import UserPP


class SignUpCustomer(View):
    def post(self, request):
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        return render(request, 'signup_customer.html', {'form': form})

    def get(self, request):
        form = CustomerSignUpForm()
        return render(request, 'signup_customer.html', {'form': form})


class SignUpOwner(View):
    def post(self, request):
        form = OwnerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            login(request, user)
            return redirect('home')
        return render(request, 'signup_owner.html', {'form': form})

    def get(self, request):
        form = OwnerSignUpForm()
        return render(request, 'signup_owner.html', {'form': form})


class LogIn(View):
    def post(self, request):
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect'})

    def get(self, request):
        return render(request, 'login.html')


class LogOut(View):
    def post(self, request):
        auth.logout(request)
        return redirect('home')


class Profile(View):
    def get(self, request):
        reviews = Review.objects.filter(customer_id=request.user.id)
        profile_picture = UserPP.objects.get(user__id=request.user.id)

        return render(request, 'profile.html', {'picture': profile_picture.profile_picture, 'reviews': reviews})

    def post(self, request):
        user = User.objects.get(id=request.user.id)

        if len(request.POST.get('username')) != 0:
            user.username = request.POST.get('username')

        if request.user.is_staff and len(request.POST.get('email')) != 0:
            user.email = request.POST.get('email')

        if user.check_password(request.POST.get('current_pass')):
            if request.POST.get('confirm_pass') == request.POST.get('new_pass') and len(
                    request.POST.get('confirm_pass')) != 0 and len(request.POST.get('new_pass')) != 0:
                user.set_password(request.POST.get('new_pass'))

        user.save()

        if request.FILES['file']:
            profile_picture = UserPP.objects.get(user__id=request.user.id)
            profile_picture.delete()
            new_pp = UserPP()
            new_pp.profile_picture = request.FILES['file']
            new_pp.user = request.user
            new_pp.save()

        return redirect('profile')
