from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import mark_safe

User = get_user_model()


class BaseUserMessage(models.Model):
    """
    Абстрактная модель сообщения пользователя

    Attributes:
        text (TextField): текст сообщения
        time (TimeField): время отправки сообщения

    """

    text = models.TextField(max_length=1024,
                            verbose_name='Текст')
    time = models.TimeField(verbose_name='Время отправки',
                            auto_now_add=True,
                            null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Message<{self.id}>"


class BaseWebsocketGroup(models.Model):
    """
    Абстрактная модель websocket группы, которая создает свой channel layer

    Attributes:
        slug (SlugField): уникальный идентификатор
        name (CharField): имя
        image (ImageField): изображение
        owner (User): владелец
        group_members (User[]): участники

    """

    slug = models.SlugField(verbose_name='Идентификатор',
                            help_text='Используйте буквы, цифры или @/./+/-/_ ',
                            max_length=100,
                            unique=True,
                            primary_key=True)

    name = models.CharField(verbose_name='Название',
                            max_length=100,
                            help_text='Введите название, длина до 100 символов',
                            default='Default group name')

    image = models.ImageField(verbose_name='Изображение группы',
                              upload_to='uploads/groups_images',
                              null=True,
                              blank=True,
                              help_text='Выберите изображение группы')

    owner = models.ForeignKey(User,
                              verbose_name='Владелец',
                              related_name='owner_groups',
                              on_delete=models.SET_NULL,
                              null=True)

    group_members = models.ManyToManyField(User,
                                           verbose_name='Участники',
                                           related_name='users_groups')

    def image_tmb(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50"')
        return 'Нет изображения'

    image_tmb.short_description = 'Изображение'
    image_tmb.allow_tags = True

    class Meta:
        abstract = True

    def __str__(self):
        return f"WebsocketGroup<{self.slug}>"


class BaseDailyMessages(models.Model):
    """
    Абстрактная модель контейнера сообщений

    Attributes:
        date (DateField): дата создания контейнера

    """
    # TODO task с созданием нового контейнера раз в сутки с помощью django-rq

    date = models.DateField(verbose_name='Дата создания',
                            auto_now_add=True,
                            null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"DailyMessages<{self.date.strftime('%Y-%m-%d %H:%M')}>"
