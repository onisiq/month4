from django import forms

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
        fields = ['category', 'title', 'body', 'image', 'is_published', 'rate']

    def save(self, commit=True):
        post = super().save(commit=commit)
        tag_names = self.cleaned_data.get('tag_names', '')
        tags = [
            name.strip()
            for name in tag_names.split(',')
            if name.strip()
        ]

        if commit:
            post.tags.set(
                Tag.objects.get_or_create(name=name)[0]
                for name in tags
            )

        return post
