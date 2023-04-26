# Generated by Django 3.2.8 on 2022-03-05 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_phone', models.CharField(max_length=50)),
                ('customer_email', models.CharField(max_length=100)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dataforchat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_phone', models.CharField(max_length=50)),
                ('customer_email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Deleted', models.BooleanField(default=False)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='chat.customerdetail')),
                ('user2', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user1', 'user2')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MessageText', models.CharField(max_length=10000)),
                ('Seen', models.BooleanField(default=False)),
                ('Deleted', models.BooleanField(default=False)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
                ('Room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.rooms')),
                ('Sender', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]