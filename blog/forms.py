from django import forms
from blog.models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        widgets = {
            'post_part_1': forms.Textarea(attrs={'class': 'ckeditor'}),
            'post_part_2': forms.Textarea(attrs={'class': 'ckeditor'}),
        }

        fields = ['title', 'place', 'continent', 'post_part_1', 'subtitle', 'post_part_2', 'cover_image']
