# Generated by Django 4.0.1 on 2022-05-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_customuser_created_at_customuser_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=280, null=True),
        ),
    ]
