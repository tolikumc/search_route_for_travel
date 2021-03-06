# Generated by Django 2.1.7 on 2019-02-27 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0002_auto_20190227_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Назва потягу')),
                ('travel_time', models.IntegerField(verbose_name='Час в дорозі')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_city', to='cities.City', verbose_name='Початкову місто місто')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_city', to='cities.City', verbose_name='Кінцеве місто')),
            ],
            options={
                'verbose_name': 'Поїзд',
                'verbose_name_plural': 'Поїзда',
                'ordering': ['name'],
            },
        ),
    ]
