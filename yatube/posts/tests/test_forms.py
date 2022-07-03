from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user_author = User.objects.create_user(username='UserAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовая пост',
            group=cls.group,
            id='1',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.author_client = Client()
        self.author_client.force_login(self.user_author)

    def test_create_page_create_new_post(self):
        """При создании поста создается новая запись в БД."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовая пост',

        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': 'auth'}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Тестовая пост',).exists())

    def test_post_edit_page_change_post(self):
        """При редактировании поста на post_edit происходит
        изменение поста в БД."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовая пост2',
        }
        response = self.author_client.post(
            reverse('posts:post_edit', args=('1')),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:post_detail', kwargs={'post_id': '1'})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        response2 = self.author_client.get(
            reverse('posts:post_detail', kwargs={'post_id': '1'})
        )
        self.assertContains(response2, 'Тестовая пост2')
