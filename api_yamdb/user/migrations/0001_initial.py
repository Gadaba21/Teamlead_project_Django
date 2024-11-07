# Generated by Django 3.2.16 on 2024-11-07 06:29

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone
import user.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует!'}, help_text="Допустимы только латинские буквы, цифры и символы @/./+/-/_. Имя пользователя 'me' использовать нельзя!", max_length=150, unique=True, validators=[user.validators.UsernameValidator(), user.validators.validate_username], verbose_name='Имя пользователя')),
                ('first_name', models.CharField(blank=True, help_text='Заполните Имя', max_length=150, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, help_text='Заполните Фамилию', max_length=150, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(error_messages={'unique': 'Пользователь с таким email уже существует!'}, help_text='Введите свой email', max_length=254, unique=True, verbose_name='Электронная почта')),
                ('bio', models.TextField(blank=True, help_text='Заполните информацию о себе', null=True, verbose_name='Биография')),
                ('role', models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', help_text='Уровень доступа пользователя', max_length=9, verbose_name='Роль пользователя')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('id', 'username'),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
