# Generated by Django 2.1.7 on 2019-02-27 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['name'], 'verbose_name': 'Місто', 'verbose_name_plural': 'Міста'},
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Місто:'),
        ),
    ]
