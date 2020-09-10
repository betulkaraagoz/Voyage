from django.urls import path
from blog import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('explore', views.ExploreHome.as_view(), name='explore'),
    path('add/blog', views.AddBlog.as_view(), name='add_blog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

