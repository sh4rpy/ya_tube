from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    text = models.TextField(verbose_name='Текст:')
    pub_date = models.DateTimeField("date published", auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_posts")
    group = models.ForeignKey(
        'Group', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категория:'
    )
    image = models.ImageField(upload_to='posts/', blank=True, verbose_name='Изображение:')

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments')
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('user', 'following')

