from django.urls import path
from blog import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('explore', views.ExploreHome.as_view(), name='explore'),
    path('add/blog', views.AddBlog.as_view(), name='add_blog'),
    path('<int:blog_id>/details', views.BlogDetails.as_view(), name='blog_details'),
    path('delete_blog/<int:blog_id>', views.DeleteBlog.as_view(), name='delete_blog'),
    path('like/<int:blog_id>', views.AjaxLike.as_view(), name='ajax_like'),
    path('unlike/<int:blog_id>', views.AjaxUnlike.as_view(), name='ajax_unlike'),
    path('explore/<filter>', views.FilterExplore.as_view(), name='explore_filtered'),
    path('search', views.SearchExplore.as_view(), name='explore_search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

