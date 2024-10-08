# Generated by Django 5.0.7 on 2024-08-28 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Оценка', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.AlterField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='helpful',
            field=models.BooleanField(default=False),
        ),
    ]
