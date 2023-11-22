# Generated by Django 4.2.7 on 2023-11-19 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chats', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyChatMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_containers', to='chats.chat', verbose_name='Чат')),
            ],
            options={
                'verbose_name': 'Контейнер сообщений чата',
                'verbose_name_plural': 'Контейнеры сообщений чатов',
            },
        ),
        migrations.CreateModel(
            name='UserChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1024, verbose_name='Текст')),
                ('time', models.TimeField(auto_now_add=True, null=True, verbose_name='Время отправки')),
                ('container', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_messages', to='users_messages.dailychatmessages', verbose_name='Контейнер')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_messages', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Сообщение чата',
                'verbose_name_plural': 'Сообщения чата',
            },
        ),
    ]
