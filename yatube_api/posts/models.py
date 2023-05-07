from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес'
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True, verbose_name='Изображение')
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name='posts',
        blank=True, null=True, verbose_name='Группа'
    )

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        verbose_name='Публикация',
        related_name='comments')
    text = models.TextField('Текст')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Подписан',
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            ),)
