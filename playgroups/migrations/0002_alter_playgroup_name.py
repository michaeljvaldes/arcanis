# Generated by Django 4.2.15 on 2024-08-20 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playgroups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playgroup',
            name='name',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
