# Generated by Django 3.0.6 on 2020-07-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osp', '0007_auto_20200708_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='form_fields',
        ),
        migrations.AddField(
            model_name='form',
            name='questions',
            field=models.ManyToManyField(blank=True, default=None, related_name='forms', to='osp.Question'),
        ),
    ]
