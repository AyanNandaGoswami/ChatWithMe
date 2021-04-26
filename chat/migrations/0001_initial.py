# Generated by Django 3.2 on 2021-04-26 11:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_room_id', models.CharField(blank=True, max_length=10, null=True)),
                ('room_name', models.CharField(blank=True, max_length=50, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_one', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_two', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Thread',
                'verbose_name_plural': 'Threads',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messag_body', models.TextField()),
                ('created_date', models.DateField(default=datetime.datetime(2021, 4, 26, 17, 28, 9, 671434))),
                ('created_time', models.TimeField(default=datetime.time(17, 28, 9, 671434))),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.thread')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]