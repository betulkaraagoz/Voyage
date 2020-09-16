from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import View

from accommodation.models import Review
from accounts.forms import CustomerSignUpForm, OwnerSignUpForm
from accounts.models import UserPP, CustomerLikes, BlogLikes
from blog.models import BlogPost


class SignUpCustomer(View):
    def post(self, request):
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
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
            print("here")
            return render(request, 'login.html', {'error': 'username or password is incorrect'})

    def get(self, request):
        return render(request, 'login.html')


class LogOut(View):
    def post(self, request):
        auth.logout(request)
        return redirect('home')


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        blog_objects = BlogPost.objects.filter(author_id=request.user.id)
        reviews = Review.objects.filter(customer_id=request.user.id)
        profile_picture = UserPP.objects.get(user__id=request.user.id)

        blogs = {}
        for blog in blog_objects:
            blogs[blog] = BlogLikes.objects.filter(liked_blog_id=blog.id)

        return render(request, 'profile.html', {'picture': profile_picture.profile_picture, 'reviews': reviews, 'blogs': blogs})

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


class Wishlist(LoginRequiredMixin, View):
    def get(self, request):
        liked_hotels = CustomerLikes.objects.filter(user=request.user)
        liked_blogs = BlogLikes.objects.filter(user=request.user)

        return render(request, 'wishlist.html', {'liked_hotels': liked_hotels, 'liked_blogs': liked_blogs})

