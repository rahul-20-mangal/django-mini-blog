# Generated by Django 3.2 on 2021-04-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
