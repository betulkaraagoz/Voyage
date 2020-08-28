from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import View
from .models import UserProfilePhoto

class SignUpCustomer(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        return render(request, 'signup_customer.html', {'form': form})

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup_customer.html', {'form': form})


class SignUpOwner(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        return render(request, 'signup_owner.html', {'form': form})

    def get(self, request):
        form = UserCreationForm()
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
        user = request.user
        return render(request, 'profile.html', {'user': user})


class AjaxAddPP(View):
    def post(self, request):
        print("HERE")
        user = request.user
        profile_photo = UserProfilePhoto.objects.create(user=user, photo=request.POST.get('profile_photo'))
        profile_photo.save()
        return redirect('profile')

