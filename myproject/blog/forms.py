from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Post, Tag


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class PostForm(forms.ModelForm):
    tag_names = forms.CharField(
        label='Тэги',
        required=False,
        help_text='Введите тэги через запятую.',
    )

    class Meta:
        model = Post
        fields = ['category', 'title', 'body', 'image', 'tags', 'tag_names', 'is_published', 'rate']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def save(self, commit=True):
        tag_names = self.cleaned_data.pop('tag_names', '')
        post = super().save(commit=commit)

        if commit and tag_names:
            tags = [
                Tag.objects.get_or_create(name=name.strip())[0]
                for name in tag_names.split(',')
                if name.strip()
            ]
            post.tags.add(*tags)

        return post


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
