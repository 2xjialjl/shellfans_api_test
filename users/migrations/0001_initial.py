# Generated by Django 4.2.4 on 2023-09-02 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=10)),
                ('birthday', models.DateField()),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pics/')),
                ('level', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
