# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-21 22:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channels', '0003_auto_20161009_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='Site that chat will use', max_length=255, unique=True, verbose_name='URL')),
                ('domain', models.CharField(help_text='Domain of URL', max_length=255, unique=True, verbose_name='Domain')),
                ('status', models.CharField(choices=[('not_approved', 'Not approved'), ('approved', 'Approved')], default='not_approved', help_text='Confirmation of the website owner', max_length=50, verbose_name='Domain status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(help_text='Owner of the domain', on_delete=django.db.models.deletion.CASCADE, related_name='domain_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'site',
                'verbose_name_plural': 'Sites',
            },
        ),
        migrations.RenameField(
            model_name='channel',
            old_name='superuser',
            new_name='owner',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='site',
        ),
        migrations.AddField(
            model_name='channel',
            name='sites',
            field=models.ManyToManyField(related_name='links', to='channels.Site'),
        ),
    ]