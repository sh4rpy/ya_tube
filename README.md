# Yatube

### Что ты такое?

Это один из моих проектов, который я писал во время учебы в Яндекс.Практикуме.

Социальная сеть, дающая пользователям возможность завести учетную запись, публиковать записи, подписываться на любимых авторов и создавать сообщества по интересам. Так же реализовано REST API с помощью инструментов Django Rest Framework.

### Как запустить?

Склонируйте репозиторий:

```bash
git clone https://github.com/sh4rpy/yatube.git
```

Создайте файл .env в одной директории с файлом settings.py. Создайте в нем переменную окружения  SECRET_KEY, которой присвойте скопированный ключ с [сайта генерации ключей](https://djecrety.ir). Далее добавьте переменные для работы с базой данных. Выглядеть файл должен так:

```python
SECRET_KEY=скопированный_ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=имя_базы
DB_USER=юзернейм
DB_PASSWORD=пароль
DB_HOST=db # имя контейнера базы данных
DB_PORT=порт
```

Запустите **docker-compose** командной:

```bash
docker-compose up
```

Сервис станет доступен по адресу [http://0.0.0.0:8000](http://0.0.0.0:8000).

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