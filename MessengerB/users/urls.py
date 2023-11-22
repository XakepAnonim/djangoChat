from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import Register, MyLoginView, ProfileView, UsersListView, UserDetailView, EmailVerify

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('register', Register.as_view(), name='register'),
    path('login', MyLoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('users', UsersListView.as_view(), name='users_list'),
    path('users/<int:id>', UserDetailView.as_view(), name='user_detail'),

    path('confirm_email', TemplateView.as_view(template_name='registration/email/confirm_email.html'),
         name='confirm_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='registration/email/invalid_verify.html'),
         name='invalid_verify'),
    path('verify_email/<uidb64>/<token>', EmailVerify.as_view(), name='verify_email'),

]