# Generated by Django 3.2.5 on 2021-07-22 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommercesite', '0002_auto_20210722_1202'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Member',
        ),
    ]
