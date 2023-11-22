from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.views import View
from django.views.generic import TemplateView

from .forms import UserCreationForm, AuthenticationForm, EditProfileForm
from .utils import send_email_for_verify

User = get_user_model()


# Authentication
class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('users:confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class MyLoginView(LoginView):
    form_class = AuthenticationForm


# Email
class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user


# Profile
class ProfileView(TemplateView):
    """
    Отображает страницу редактирования профиля пользователя.

    Context:
        user (User): экземпляр класса User
        form (EditProfileForm): форма редактирования профиля

    Template:
        template_name: 'users/profile.html'

    Form:
        form_class (EditProfileForm): форма редактирования профиля

    """

    template_name = 'users/profile.html'
    form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        user: User = get_object_or_404(User.objects.only('email', 'username'),
                                       pk=request.user.id)

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid() and form.validate_all(request.user):
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['login']
            user.profile.biography = form.cleaned_data['biography'] or user.profile.biography

            # если нажат чекбокс очистки изображения
            if form.cleaned_data['image'] is False:
                user.profile.image = None
            else:
                user.profile.image = form.cleaned_data['image'] or user.profile.image

            user.save()

            return redirect('users:profile')

        return render(request,
                      self.template_name,
                      self.get_context_data(request))

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)

        user: User = get_object_or_404(User.objects.only('email', 'username'),
                                       pk=request.user.id)

        initial_form_data = {
            'email': user.email,
            'login': user.username,
            'biography': user.profile.biography,
            'image': user.profile.image
        }
        form = self.form_class(request.POST or None,
                               request.FILES or None,
                               initial=initial_form_data)
        # небоходимо, чтобы показать ошибки валидации формы
        if form.is_valid():
            form.validate_all(user)

        context['user'] = user
        context['form'] = form

        return context


# Users
class UsersListView(TemplateView):
    """
    Отображает список пользователей

    Context:
        users (User[]): QuerySet, содержащий экземпляры класса User

    Template:
        template_name: 'users/users_list.html'

    """

    template_name = 'users/users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.only('id', 'username')
        context['users'] = users
        return context


class UserDetailView(TemplateView):
    """
    Отображает страницу пользователя (User)

    Context:
        user (User): экземпляр класса User

    Template:
        template_name: 'users/users_list.html'

    """
    template_name = 'users/user_detail.html'

    def get(self, request, id: int, *args, **kwargs):
        if request.user.id == id:
            return redirect('users:profile')
        else:
            return render(request,
                          self.template_name,
                          self.get_context_data(id))

    def get_context_data(self, id: int, **kwargs):
        context = super().get_context_data(**kwargs)
        user: User = get_object_or_404(User.objects.only('email', 'username'), pk=id)
        context['user'] = user
        return context