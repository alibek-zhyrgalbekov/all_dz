# Generated by Django 3.2.5 on 2021-07-06 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kkkkk', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='created_data',
            new_name='created_date',
        ),
    ]
