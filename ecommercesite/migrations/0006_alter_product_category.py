# Generated by Django 3.2.5 on 2021-07-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommercesite', '0005_auto_20210726_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M', 'Mobile'), ('TW', 'Top Wear'), ('BW', 'Bottom Wear')], max_length=2),
        ),
    ]
