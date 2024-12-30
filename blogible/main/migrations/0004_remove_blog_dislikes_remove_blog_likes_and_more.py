# Generated by Django 5.1.2 on 2024-12-25 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_blog_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='likes',
        ),
        migrations.AlterField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.profile'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='main.profile'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='main.profile'),
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='main.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('blog', 'user'), name='unique_dislike_per_user_blog')],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='main.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('blog', 'user'), name='unique_like_per_user_blog')],
            },
        ),
    ]
