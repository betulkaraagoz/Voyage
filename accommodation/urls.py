from django.urls import path
from accommodation import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('hotels/', views.Hotels.as_view(), name='hotels'),
    path('hotels/add/', views.AddHotels.as_view(), name='add_hotel'),
    path('hotel/', views.HotelViewForCustomer.as_view(), name='customer_hotel'),
    path('reservations/', views.ListReservations.as_view(), name='reservations'),
    path('add_r/<int:id>', views.AjaxListReservations.as_view(), name='add_r'),
    path('add_reservation/<int:hotel_id>', views.AjaxMakeReservation.as_view(), name='add_reservation'),
    path('delete_reservation/<int:reservation_id>', views.DeleteReservation.as_view(), name='delete_reservation'),
    path('<int:hotel_id>/homepage', views.HotelHomePage.as_view(), name='hotel_homepage'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
