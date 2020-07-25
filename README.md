# Yatube

### Что ты такое?

Это один из моих проектов, который я писал во время учебы в Яндекс.Практикуме.

Социальная сеть, дающая пользователям возможность завести учетную запись, публиковать записи, подписываться на любимых авторов и создавать сообщества по интересам. Так же реализовано REST API с помощью инструментов Django Rest Framework.

### Как запустить?

Склонируйте репозиторий:

```bash
git clone https://github.com/sh4rpy/ya_tube.git
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Выполните миграции:

```bash
python manage.py migrate
```

### Подробнее про Yatube API:

Публикации:

```
Обязательное поле: text

/api/v1/posts/ - получить список всех пубоикаций (GET)
/api/v1/posts/ - создать новую публикацию (POST)
/api/v1/posts/{post_id}/ - получить публикацию по id (GET)
/api/v1/posts/{post_id}/ - обновить публикацию по id (PUT)
/api/v1/posts/{post_id}/ - частично обновить публикацию по id (PATCH)
/api/v1/posts/{post_id}/ - удалить публикацию по id (DELETE)
```

Комментарии:

```
Обязательные поля: post_id, text

/api/v1/posts/{post_id}/comments/ - получить список всех комментариев публикации (GET)
/api/v1/posts/{post_id}/comments/ - создать новый комменатрий для публикации (POST)
/api/v1/posts/{post_id}/comments/{comment_id}/ - получить комментарий для публикации по id (GET)
/api/v1/posts/{post_id}/comments/{comment_id}/ - получить комментарий для публикации по id (GET)
/api/v1/posts/{post_id}/comments/{comment_id}/ - обновить комментарий для публикации по id (PUT)
/api/v1/posts/{post_id}/comments/{comment_id}/ - частично обновить комментарий для публикации по id (PATCH)
/api/v1/posts/{post_id}/comments/{comment_id}/ - удалить комментарий для публикации по id (DELETE)
```

Подписки:

```
Обязательное поле: following (username того, на кого подписываемся)

/api/v1/follow/ - получить список всех подписчиков (GET)
/api/v1/follow/ - создать подписку (POST)
/api/v1/follow/{follow_id}/ - получить подписку по id (GET)
/api/v1/follow/{follow_id}/ - удалить подписку по id (DELETE)
```

Группы:

```
Обязательные поля: title, description, slug

/api/v1/group/ - получить список всех групп (GET)
/api/v1/group/ - создать новую группу (POST)
/api/v1/group/{group_id}/ - получить группу по id (GET)
/api/v1/posts/{post_id}/ - обновить группу по id (PUT)
/api/v1/posts/{post_id}/ - частично обновить группу по id (PATCH)
/api/v1/group/{group_id}/ - удалить группу по id (DELETE)
```

Токен:

```
/api/v1/token/ - получить JWT-токен (POST)
/api/v1/token/refresh/ - обновить JWT-токен (POST)
```

### Потыкать можно тут:

[Последние обновления | Yatube](https://www.mysocialnetwork.tk)