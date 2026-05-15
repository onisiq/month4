from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post, Tag


class RegisterViewTests(TestCase):
    def test_register_creates_and_logs_in_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })

        self.assertRedirects(response, reverse('post_list'))
        self.assertTrue(User.objects.filter(username='new_user').exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username='new_user').pk)


class PostCreateViewTests(TestCase):
    def test_create_post_with_tags(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'Пост с тэгами',
            'body': 'Текст поста',
            'is_published': 'on',
            'rate': 7,
            'tag_names': 'django, python',
        })

        post = Post.objects.get()

        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(Tag.objects.count(), 2)
        self.assertQuerySetEqual(
            post.tags.order_by('name'),
            ['django', 'python'],
            transform=lambda tag: tag.name,
        )


class PostDeleteViewTests(TestCase):
    def test_delete_post(self):
        post = Post.objects.create(
            title='Пост для удаления',
            body='Текст поста',
            is_published=True,
            rate=7,
        )

        response = self.client.post(reverse('post_delete', kwargs={'pk': post.pk}))

        self.assertRedirects(response, reverse('post_list'))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())


class PostListViewTests(TestCase):
    def test_post_list_alias_opens_post_list(self):
        response = self.client.get('/blog/post/')

        self.assertEqual(response.status_code, 200)
