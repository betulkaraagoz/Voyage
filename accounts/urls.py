from django.urls import path
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/customer', views.SignUpCustomer.as_view(), name='signupcustomer'),
    path('signup/owner', views.SignUpOwner.as_view(), name='signupowner'),
    path('login', views.LogIn.as_view(), name='login'),
    path('logout', views.LogOut.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('add_pp/', views.AjaxAddPP.as_view(), name='add_pp')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
