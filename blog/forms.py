from django import forms
from blog.models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        widgets = {
            'post': forms.Textarea(attrs={'class': 'ckeditor'}),
        }

        fields = ['title', 'place', 'post', 'cover_image']
