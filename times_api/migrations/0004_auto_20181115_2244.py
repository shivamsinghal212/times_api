# Generated by Django 2.1.3 on 2018-11-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('times_api', '0003_auto_20181115_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
