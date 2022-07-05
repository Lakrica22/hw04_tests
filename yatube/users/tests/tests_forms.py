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
        
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
            group=cls.group,
            id='1',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_signup_page_create_user(self):
        """При заполнении валидной формы signup создается 
        новый пользователь."""
        user_count = User.objects.count()
        form_data = {
            'first_name':'Любовь',
            'last_name': 'Воронова',
            'username': 'lakrica',
            'email':'lakrica@yandex.ru',
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:index')
        )
        self.assertEqual(User.objects.count(), user_count+1)
