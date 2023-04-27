# Generated by Django 4.1.1 on 2023-04-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0002_customuser_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.URLField()),
                ('ingredients', models.TextField()),
                ('recipe', models.TextField()),
                ('categories', models.CharField(max_length=200)),
            ],
        ),
    ]