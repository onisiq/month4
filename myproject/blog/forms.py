from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Post, Tag


# Форма для создания категории.
# ModelForm сам делает поля формы из модели Category.
class CategoryForm(forms.ModelForm):
    class Meta:
        # Говорим Django, с какой моделью связана форма.
        model = Category
        # Эти поля пользователь увидит на странице.
        fields = ['name', 'description']


# Форма для создания поста.
# Она связана с моделью Post, поэтому Django сам сохранит данные в базу.
class PostForm(forms.ModelForm):
    # Это дополнительное поле, его нет прямо в модели Post.
    # Тут можно написать тэги через запятую, например: python, django, blog.
    tag_names = forms.CharField(
        label='Тэги',
        required=False,
        help_text='Введите тэги через запятую.',
    )

    class Meta:
        model = Post
        # Поля, которые будут показаны в форме создания поста.
        fields = ['category', 'title', 'body', 'image', 'tags', 'tag_names', 'is_published', 'rate']
        widgets = {
            # Показываем тэги чекбоксами, чтобы можно было выбрать несколько.
            'tags': forms.CheckboxSelectMultiple()
        }

    def save(self, commit=True):
        # Забираем текст из поля tag_names.
        # pop убирает tag_names из cleaned_data, потому что такого поля нет в модели Post.
        tag_names = self.cleaned_data.pop('tag_names', '')

        # Сначала сохраняем сам пост обычным способом.
        post = super().save(commit=commit)

        # Если пост уже сохранен и пользователь написал тэги через запятую,
        # создаем эти тэги или берем уже существующие.
        if commit and tag_names:
            tags = [
                Tag.objects.get_or_create(name=name.strip())[0]
                for name in tag_names.split(',')
                if name.strip()
            ]
            # Привязываем найденные/созданные тэги к посту.
            post.tags.add(*tags)

        return post


# Форма регистрации пользователя.
# UserCreationForm уже умеет проверять password1 и password2.
class RegisterForm(UserCreationForm):
    # Добавляем email к стандартной форме регистрации.
    # required=False значит, что email можно не заполнять.
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        # Регистрируем обычного пользователя Django.
        model = User
        # Эти поля будут в форме регистрации.
        fields = ['username', 'email', 'password1', 'password2']
