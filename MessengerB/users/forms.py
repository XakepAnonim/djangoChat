from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from core.widgets import CustomClearableFileInput

from .models import Profile
from .utils import send_email_for_verify

User = get_user_model()


class EditProfileForm(forms.Form):
    """
    Форма редактирования профиля пользователя


    Fields:
        login (CharField): имя пользователя
        email (EmailField): электронная почта
        image (ImageField): изображение
        biography (CharField): краткая информация о пользователе

    """

    login = forms.CharField(max_length=150,
                            label='Имя пользователя',
                            help_text='Максимум 150 символов',
                            required=True)

    email = forms.EmailField(label='Почта',
                             required=False)

    image = forms.ImageField(label='Аватар',
                             required=False,
                             allow_empty_file=False,
                             widget=CustomClearableFileInput)

    biography = forms.CharField(label='Расскажите немного о себе',
                                widget=forms.Textarea(),
                                max_length=500,
                                required=False)

    def validate_edit_login(self, current_user):
        login = self.cleaned_data['login']

        if len(login.strip()) < 2:
            self.add_error('login', 'Длина имени не менее 2 символов!')
            return

        if login != current_user.username and User.objects.filter(username=login):
            self.add_error('login',
                           'Пользователь с таким именем уже существует!')
            return

        return True

    def validate_edit_email(self, current_user):
        email = self.cleaned_data['email']

        if email != current_user.email and User.objects.filter(email=email):
            self.add_error('email',
                           'Пользователь с такой почтой уже существует!')
            return

        return True

    def validate_all(self, current_user):
        return self.validate_edit_email(current_user) and self.validate_edit_login(current_user)


class AuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is not None:
                if not self.user_cache.email_verify:
                    send_email_for_verify(self.request, self.user_cache)
                    raise ValidationError(
                        'Ты еще не подтвердил свою электронную почту?'
                        'Посмотри ее!',
                        code="invalid_login",
                    )
                else:
                    self.confirm_login_allowed(self.user_cache)
            else:
                raise self.get_invalid_login_error()

        return self.cleaned_data


class UserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150,
                            label='Имя пользователя',
                            help_text='Максимум 150 символов',
                            required=True)

    email = forms.EmailField(label='Почта',
                             required=True)

    phone = forms.CharField(label='Телефон',
                                   required=True)


    #
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", 'phone')
