# Generated by Django 4.1.1 on 2023-04-17 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='sex',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]