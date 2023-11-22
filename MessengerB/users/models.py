from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, phone, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, phone, password, **extra_fields)

    def create_superuser(self, username, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, phone, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14)

    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = ["username", ]


class Profile(models.Model):
    """
    Модель профиля пользователя. Расширяет модель User.

    Attributes:
        user (User): пользователь
        image (ImageField): изображение
        biography (TextField): краткая информация о пользователе

    """

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    biography = models.TextField(verbose_name='О себе',
                                 max_length=500,
                                 unique=False,
                                 null=True,
                                 help_text='Немного расскажите о себе')

    image = models.ImageField(verbose_name='Изображение пользователя',
                              upload_to='uploads/users_images',
                              null=True,
                              help_text='Выберите изображение')

    def get_image_x256(self):
        return get_thumbnail(self.image,
                             '256',
                             quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50"')
        return 'Нет изображения'

    image_tmb.short_description = 'Изображение'
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = 'Дополнительное поле'
        verbose_name_plural = 'Дополнительные поля'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()