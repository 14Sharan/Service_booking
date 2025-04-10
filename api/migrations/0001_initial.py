# Generated by Django 4.2 on 2025-04-10 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('otp', models.CharField(max_length=6)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
