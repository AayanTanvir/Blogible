# Generated by Django 5.1.2 on 2024-12-26 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_blog_dislikes_remove_blog_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
