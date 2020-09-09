from django.urls import path
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/customer', views.SignUpCustomer.as_view(), name='signupcustomer'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
