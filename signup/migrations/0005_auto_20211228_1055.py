# Generated by Django 3.2.9 on 2021-12-28 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
