# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce', '0008_product_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]
