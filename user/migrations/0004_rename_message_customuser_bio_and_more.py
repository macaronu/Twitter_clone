# Generated by Django 4.0.1 on 2022-05-19 13:22

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_message_customuser_profile_img_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='message',
            new_name='bio',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_img',
            field=models.ImageField(blank=True, upload_to=user.models.directory_path),
        ),
    ]
