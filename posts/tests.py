from django.core import mail
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import Post, User, Group

# Данные для регистрации
signup_data = {
    'first_name': 'Петр',
    'last_name': 'Петров',
    'username': 'petr',
    'email': 'petr@example.com',
    'password1': 'password-of-petr',
    'password2': 'password-of-petr',
}


class TestEmail(TestCase):
    def test_send_email(self):
        # Регистрируемся
        self.client.post(reverse('signup'), signup_data)
        # Проверяем, что письмо лежит в исходящих
        self.assertEqual(len(mail.outbox), 1)
        # Проверяем, что тема первого письма правильная.
        self.assertEqual(mail.outbox[0].subject, 'Регистрация')


class TestProfile(TestCase):
    def setUp(self):
        # Очищаем кэш
        cache.clear()
        # Создаем пользователя
        self.user = User.objects.create_user(
            username="nikita", email="nikita@example.com",
            password="12345"
        )
        # Создаем пост
        self.post = Post.objects.create(text="Тестовый пост", author=self.user)

    def test_add_profile_page(self):
        """Проверяет, появилась ли страница пользователя после регистрации"""
        # Регистрируемся
        self.client.post(reverse('signup'), signup_data)
        # Логинемся
        self.client.login(username='petr', password='password-of-petr')
        # Проверяем, появился ли новый пользователь
        response = self.client.get(
            reverse('profile', kwargs={'username': 'petr'}))
        self.assertEqual(response.status_code, 200)

    def test_authorized_user_new_post(self):
        """Проверяет, что авторизованный пользователь
        может опубликовать пост
        """
        # Логинемся
        self.client.login(username='nikita', password='12345')
        # Создаем новый пост
        self.client.post(reverse('new_post'), {'text': 'Новый пост'})
        # Проверяем, появился ли пост после отправки формы
        response = self.client.get(reverse('index'))
        self.assertContains(
            response, 'Новый пост', count=1, status_code=200,
            msg_prefix='Пост не найден', html=False
        )

    def test_unauthorized_user_new_post(self):
        """Проверяет, что неавторизованный пользователь не
        может опубликовать пост, и его редиректит
        на страницу авторизации
        """
        # Попытка создать пост неавторизованным пользователем
        response = self.client.post(
            reverse('new_post'), {'text': 'Новый пост'})
        self.assertRedirects(
            response, '/auth/login/?next=/new/', status_code=302)

    def test_post_add_everywhere(self):
        """Проверяет, что опубликовынный пост появляется на всех связанных страницах"""
        # Пост на главной странице
        response = self.client.get(reverse('index'))
        self.assertContains(
            response, 'Тестовый пост', count=1,
            status_code=200, msg_prefix='Пост не найден на главной странице', html=False
        )
        # Пост на странице автора
        self.client.login(username='nikita', password='12345')
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(
            response, 'Тестовый пост', count=1,
            status_code=200, msg_prefix='Пост не найден на странице пользователя', html=False
        )
        # Пост на стронице поста
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(
            response, 'Тестовый пост', count=1,
            status_code=200, msg_prefix='Пост не найден на странице поста', html=False
        )

    def test_authorized_user_post_edit(self):
        """Проверяет, что авторизованный пользователь может
        отредактировать свой пост, и его содержимое изменится
        на всех связанных страницах
        """
        # Логинемся
        self.client.login(username='nikita', password='12345')
        # Редактируем пост
        self.client.post(
            reverse('post_edit', kwargs={'username': 'nikita',
                                         'post_id': self.post.id}),
            {'text': 'Изменили тестовый пост'}
        )
        # Проверка изменения поста на главной странице
        response = self.client.get(reverse('index'))
        self.assertContains(
            response, 'Изменили тестовый пост', count=1,
            status_code=200, msg_prefix='Пост не изменен на главной странице', html=False
        )
        # Проверка изменения на странице пользователя
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(
            response, 'Изменили тестовый пост', count=1,
            status_code=200, msg_prefix='Пост не изменен на странице пользователя', html=False
        )
        # Проверка изменения на странице поста
        response = self.client.get(
            reverse('post', kwargs={
                'username': self.user.username, 'post_id': self.post.id})
        )
        self.assertContains(
            response, 'Изменили тестовый пост', count=1,
            status_code=200, msg_prefix='Пост не изменен на странице поста', html=False
        )


class TestErrorsPages(TestCase):
    def test_404(self):
        """Проверяет, что в ответ на запрос несуществующей страницы возвращается 404
        """
        # Запрос к несуществующей странице
        response = self.client.get(
            'exactly-a-non-existent-page-with-gibberish/')
        self.assertEqual(response.status_code, 404)


class TestImage(TestCase):
    def setUp(self):
        # Очищаем кэш
        cache.clear()
        # Создаем пользователя
        self.user = User.objects.create_user(
            username="nikita", email="nikita@example.com", password="12345")
        # Создаем группу
        self.group = Group.objects.create(
            title='Qwerty', slug='qwrt', description='desc')
        # Логинемся
        self.client.login(username='nikita', password='12345')
        # Создаем пост с картинкой
        with open('media/posts/bb6fbe32.jpg', 'rb') as f_obj:
            self.client.post(
                reverse('new_post'),
                {'text': 'Text', 'image': f_obj,
                 'group': self.group.id}
            )

    def test_image_everywhere(self):
        """Проверяет, что картинка есть на всех
        связанных страницах
        """
        # Ищем картинку на главной странице
        response = self.client.get(reverse('index'))
        self.assertContains(
            response, '<img', status_code=200, count=1,
            msg_prefix='Тэг не найден на главной странице',
            html=False
        )
        # На странице поста
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(
            response, '<img', status_code=200, count=1,
            msg_prefix='Тэг не найден на странице профиля',
            html=False
        )
        # На странице группы
        response = self.client.get(
            reverse('group', kwargs={'slug': 'qwrt'}))
        self.assertContains(
            response, '<img', status_code=200, count=1,
            msg_prefix='Тэг не найден на странице группы',
            html=False
        )

    def test_wrong_format_file(self):
        """Проверяет защиту от загрузки файлов
        неправильных форматов
        """
        with open('requirements.txt', 'rb') as f_obj:
            self.client.post(
                reverse('new_post'), {'text': 'Тест картинки с неправильным форматом',
                                      'image': f_obj}
            )
        response = self.client.get(reverse('index'))
        self.assertNotContains(
            response, 'Тест картинки с неправильным форматом',
            status_code=200, msg_prefix='Тэг найден, а не должен', html=False
        )


class TestCache(TestCase):
    def setUp(self):
        self.client.get(reverse('index'))
        user = User.objects.create_user(
            username="nikita", email="nikita@example.com", password="12345")
        self.client.login(username='nikita', password='12345')
        self.client.post(reverse('new_post'), {'text': 'Тест кэша'})

    def test_cache(self):
        response = self.client.get(reverse('index'))
        self.assertNotContains(
            response, 'Тест кэша',
            status_code=200, msg_prefix='Пост найден, а не должен', html=False
        )
        cache.clear()
        response = self.client.get(reverse('index'))
        self.assertContains(
            response, 'Тест кэша',
            status_code=200, count=1, msg_prefix='Пост не найден', html=False
        )


class TestFollow(TestCase):
    def setUp(self):
        # Очищаем кэш
        cache.clear()
        # Создаем пользователей
        self.user1 = User.objects.create_user(
            username="nikita", email="nikita@example.com",
            password="12345"
        )
        self.user2 = User.objects.create_user(
            username="ivan", email="ivan@example.com",
            password="12345")
        self.user3 = User.objects.create_user(
            username="petr", email="petr@example.com",
            password="12345")
        # Логинемся
        self.client.login(username="nikita", password="12345")
        # Создаем пост
        self.post = Post.objects.create(
            text="Тест подписок", author=self.user3)

    def test_authorized_follow_unfollow(self):
        """Проверяет, что авторизованный пользователь может
        подписываться на других пользователей и
        удалять их из подписок
        """
        # Подписываемся
        self.client.get(
            reverse('profile_follow', kwargs={'username': self.user2}))
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user1}))
        self.assertEqual(response.context["follow"], 1)
        # Отписываемся
        self.client.get(reverse('profile_unfollow',
                                kwargs={'username': self.user2}))
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user1}))
        self.assertEqual(response.context["follow"], 0)

    def test_follow_posts_feed(self):
        """Проверяет, что новая запись пользователя появляется
        в ленте тех, кто на него подписан и не появляется
        в ленте тех, кто не подписан на него
        """
        # Подписываемся и проверяем наличие поста в ленте
        self.client.get(
            reverse('profile_follow', kwargs={'username': self.user3}))
        response = self.client.get(reverse('follow_index'))
        self.assertContains(
            response, 'Тест подписок', status_code=200,
            count=1, msg_prefix='Пост не найден',
            html=False
        )
        # Выходим из аккаунта и првоеряем ленту
        self.client.logout()
        # Очищаем кэш
        cache.clear()
        self.client.login(username='ivan', password='12345')
        response = self.client.get(reverse('follow_index'))
        self.assertNotContains(
            response, 'Тест подписок', status_code=200,
            msg_prefix='Пост найден, а не должен',
            html=False
        )

    def test_comment(self):
        """Проверяет, что только авторизированный пользователь
        может комментировать посты
        """
        # Оставляем комментарий залогиненным пользователем
        self.client.post(
            reverse('add_comment', kwargs={
                'username': self.user3, 'post_id': self.post.id}),
            {'text': 'Проверяем комментарий залогиненного'}
        )
        # Проверяем наличие комментария
        response = self.client.get(
            reverse('post', kwargs={'username': self.user3,
                                    'post_id': self.post.id})
        )
        self.assertContains(
            response, 'Проверяем комментарий залогиненного', status_code=200,
            count=1, msg_prefix='Комментарий не найден',
            html=False
        )
        # Выходим из аккаунта
        self.client.logout()
        # Пытаемся добавить комментарий незалогиненным пользователем
        self.client.post(
            reverse('add_comment', kwargs={
                'username': self.user3, 'post_id': self.post.id}),
            {'text': 'Проверяем комментарии незалогиненного'}
        )
        self.assertNotContains(
            response, 'Проверяем комментарии незалогиненного',
            status_code=200,
            msg_prefix='Комментарий найден, а не должен',
            html=False
        )


class TestGroup(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            username="nikita", email="nikita@example.com",
            password="12345"
        )
        # Логинемся
        self.user = self.client.login(username='nikita', password='12345')
        # Создаем группу
        self.client.post(reverse('create_group'),
                         {
                             'title': 'Тестовая группа',
                             'description': 'Проверяем создание новой группы',
                             'slug': 'test'
                         })

    def test_create_group(self):
        """Проверяет, что авторизованный пользователь
        может создать/удалить группу, и она появится/исчезнет
        на странице всех сообществ сайта
        """
        # Проверяем, появилась ли группа на старнице групп
        response = self.client.get(reverse('groups'))
        self.assertContains(
            response, 'Тестовая группа', status_code=200,
            count=1, msg_prefix='Группа не найдена',
            html=False
        )

    def test_delete_group(self):
        """Проверяет, что авторизованный пользователь
        может удалить группу, и она удалится
        на странице всех сообществ сайта
        """
        # Удаляем группу
        self.client.post(reverse('delete_group', kwargs={'slug': 'test'}))
        # Проверяем, удалилась ли группа на старнице групп
        response = self.client.get(reverse('groups'))
        self.assertNotContains(
            response, 'Тестовая группа',
            status_code=200,
            msg_prefix='Группа найдена, а не должна',
            html=False
        )

    def test_edit_group(self):
        """Проверяет, что авторизованный пользователь
        может изменить группу, и она изменится
        на странице всех сообществ сайта
        """
        # Редактируем группу
        self.client.post(reverse('group_edit', kwargs={'slug': 'test'}),
                         {
                             'title': 'Изменили название группы',
                             'description': 'Изменили описание группы',
                             'slug': 'test'
                         }
                         )
        # Проверяем, изменилась ли группа на старнице групп
        response = self.client.get(reverse('groups'))
        self.assertContains(
            response, 'Изменили название группы', status_code=200,
            count=1, msg_prefix='Группа не изменилась',
            html=False
        )
        # Проверяем, что группа до изменений не остается на странице групп
        response = self.client.get(reverse('groups'))
        self.assertNotContains(
            response, 'Тестовая группа',
            status_code=200,
            msg_prefix='Группа найдена, а не должна',
            html=False
        )
