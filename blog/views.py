from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render, redirect
from datetime import datetime
from django.views import View
from accounts.models import UserPP, BlogLikes
from blog.forms import BlogForm
from blog.models import BlogPost, BlogPostImages
from django.db.models import Q


class ExploreHome(LoginRequiredMixin, View):
    def get(self, request):
        blog_objects = BlogPost.objects.all()

        blogs = {}
        for blog in blog_objects:
            blogs[blog] = UserPP.objects.get(user_id=blog.author.id)

        paginator = Paginator(blog_objects, 3, orphans=1)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page') or 1
        try:
            current_page = paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))


        continents = {"Africa": BlogPost.objects.filter(continent__contains="Africa").count(),
                      "Asia": BlogPost.objects.filter(continent__contains="Asia").count(),
                      "Australia": BlogPost.objects.filter(continent__contains="Australia").count(),
                      "Europe": BlogPost.objects.filter(continent__contains="Europe").count(),
                      "North America": BlogPost.objects.filter(continent__contains="North America").count(),
                      "South America": BlogPost.objects.filter(continent__contains="South America").count()}

        return render(request, 'index3.html', {'blogs': blogs, 'continents': continents, 'current_page': current_page,
                                               'is_paginated': is_paginated})


class AddBlog(LoginRequiredMixin, View):
    def get(self, request):
        blog_form = BlogForm()
        return render(request, 'add_blog.html', {'form': blog_form})

    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            place = request.POST.get('place')
            continent = request.POST.get('continent')
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
                                                continent=continent,
                                                cover_image=cover_image,
                                                date=datetime.now())

            blog_post.save()

            for picture in request.FILES.getlist('files'):
                photo = BlogPostImages(blog=blog_post, image=picture)
                photo.save()

        else:
            print("AAAAA")
            print(form.errors)

        return redirect('blog_details', blog_post.id)


class BlogDetails(LoginRequiredMixin, View):
    def get(self, request, blog_id):
        blog = BlogPost.objects.get(id=blog_id)
        blog_photos = BlogPostImages.objects.filter(blog_id=blog_id)
        is_liked = BlogLikes.objects.filter(user_id=request.user.id, liked_blog_id=blog_id).exists()
        like_count = BlogLikes.objects.all().count()

        return render(request, 'blog-detailpage.html',
                      {'blog': blog, 'photos': blog_photos, 'liked': is_liked, 'count': like_count})


class DeleteBlog(LoginRequiredMixin, View):
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


class FilterExplore(View):
    def get(self, request, filter):
        blog_objects = BlogPost.objects.filter(continent__contains=filter)

        blogs = {}
        for blog in blog_objects:
            blogs[blog] = UserPP.objects.get(user_id=blog.author.id)

        paginator = Paginator(blog_objects, 3, orphans=1)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page') or 1
        try:
            current_page = paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        continents = {"Africa": BlogPost.objects.filter(continent__contains="Africa").count(),
                      "Asia": BlogPost.objects.filter(continent__contains="Asia").count(),
                      "Australia": BlogPost.objects.filter(continent__contains="Australia").count(),
                      "Europe": BlogPost.objects.filter(continent__contains="Europe").count(),
                      "North America": BlogPost.objects.filter(continent__contains="North America").count(),
                      "South America": BlogPost.objects.filter(continent__contains="South America").count()}

        return render(request, 'index3.html', {'blogs': blogs, 'continents': continents, 'current_page': current_page,
                                               'is_paginated': is_paginated})


class SearchExplore(View):
    def post(self, request):
        blog_objects = BlogPost.objects.filter(Q(title__icontains=request.POST.get('search')) | Q(continent__icontains=request.POST.get('search'))| Q(place__icontains=request.POST.get('search'))| Q(author__first_name__icontains=request.POST.get('search')))

        blogs = {}
        for blog in blog_objects:
            blogs[blog] = UserPP.objects.get(user_id=blog.author.id)

        paginator = Paginator(blog_objects, 3, orphans=1)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page') or 1
        try:
            current_page = paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        continents = {"Africa": BlogPost.objects.filter(continent__contains="Africa").count(),
                      "Asia": BlogPost.objects.filter(continent__contains="Asia").count(),
                      "Australia": BlogPost.objects.filter(continent__contains="Australia").count(),
                      "Europe": BlogPost.objects.filter(continent__contains="Europe").count(),
                      "North America": BlogPost.objects.filter(continent__contains="North America").count(),
                      "South America": BlogPost.objects.filter(continent__contains="South America").count()}

        return render(request, 'index3.html', {'blogs': blogs, 'continents': continents, 'current_page': current_page,
                                               'is_paginated': is_paginated})