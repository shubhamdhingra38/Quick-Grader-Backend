# Generated by Django 3.1.3 on 2021-05-26 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='taken_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
