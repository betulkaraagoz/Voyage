from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accommodation import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accomodation/', include('accommodation.urls')),
    path('explore/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
