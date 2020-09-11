from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views import View

from accounts.models import UserPP, BlogLikes
from blog.forms import BlogForm
from blog.models import BlogPost, BlogPostImages


class ExploreHome(View):
    def get(self, request):
        blog_objects = BlogPost.objects.all()
        blogs = {}
        for blog in blog_objects:
            blogs[blog] = UserPP.objects.get(user_id=blog.author.id)

        return render(request, 'index3.html', {'blogs': blogs})


class AddBlog(View):
    def get(self, request):
        blog_form = BlogForm()
        return render(request, 'add_blog.html', {'form': blog_form})

    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            place = request.POST.get('place')
            post_part_1 = request.POST.get('post_part_1')
            post_part_2 = request.POST.get('post_part_2')
            subtitle = request.POST.get('subtitle')
            cover_image = request.FILES.get('cover_image')

            author = request.user

            blog_post = BlogPost.objects.create(author=author,
                                                title=title,
                                                place=place,
                                                post_part_1=post_part_1,
                                                post_part_2=post_part_2,
                                                subtitle=subtitle,
                                                cover_image=cover_image,
                                                date=datetime.now())

            blog_post.save()

            for picture in request.FILES.getlist('files'):
                photo = BlogPostImages(blog=blog_post, image=picture)
                photo.save()

        else:
            print(form.errors)

        return redirect('explore')


class BlogDetails(View):
    def get(self, request, blog_id):
        blog = BlogPost.objects.get(id=blog_id)
        blog_photos = BlogPostImages.objects.filter(blog_id=blog_id)
        is_liked = BlogLikes.objects.filter(user_id=request.user.id, liked_blog_id=blog_id).exists()

        return render(request, 'blog-detailpage.html', {'blog': blog, 'photos': blog_photos, 'liked': is_liked})


class DeleteBlog(View):
    def post(self, request, blog_id):
        blog = BlogPost.objects.get(id=blog_id)
        blog.delete()
        return redirect('profile')


class AjaxLike(View):
    def post(self, request, blog_id):
        blog = BlogPost.objects.get(id=blog_id)
        like = BlogLikes.objects.create(user_id=request.user.id, liked_blog=blog)
        like.save()
        return redirect('reservations')


class AjaxUnlike(View):
    def post(self, request, blog_id):
        blog = BlogPost.objects.get(id=blog_id)
        like = BlogLikes.objects.filter(user_id=request.user.id, liked_blog=blog)
        like.delete()
        return redirect('reservations')