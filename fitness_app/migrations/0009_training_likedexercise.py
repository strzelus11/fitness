# Generated by Django 4.1.1 on 2023-05-24 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0008_alter_exercise_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'exercise')},
            },
        ),
        migrations.CreateModel(
            name='LikedExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness_app.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'exercise')},
            },
        ),
    ]
