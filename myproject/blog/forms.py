from django import forms

from .models import Category, Post


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'body', 'is_published', 'rate']



class PostForm(forms.ModelForm):

    class Meta:

        model = Post

        fields = ['title', 'content', 'tags']

        widgets = {

            'tags': forms.CheckboxSelectMultiple()

        }