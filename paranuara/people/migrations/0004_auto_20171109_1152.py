# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-09 11:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_food_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Food')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='favouritefood',
            unique_together=set([('person', 'food')]),
        ),
    ]