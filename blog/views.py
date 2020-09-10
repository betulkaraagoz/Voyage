from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views import View
from blog.forms import BlogForm
from blog.models import BlogPost


class ExploreHome(View):
    def get(self, request):
        blogs = BlogPost.objects.all()
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
            post = request.POST.get('post')
            cover_image = request.FILES.get('cover_image')

            author = request.user

            blog_post = BlogPost.objects.create(author=author,
                                                title=title,
                                                place=place,
                                                post=post,
                                                cover_image=cover_image,
                                                date=datetime.now())

            blog_post.save()
        else:
            print(form.errors)

        return redirect('explore')