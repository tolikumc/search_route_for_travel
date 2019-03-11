from django.db import models
from trains.models import Train


class Route(models.Model):
    name = models.CharField(verbose_name='Назва маршруту', max_length=100, unique=True)
    from_city = models.CharField(max_length=100, verbose_name='Звідки')
    to_city = models.CharField(max_length=100, verbose_name='Куди')
    across_cities = models.ManyToManyField(Train, blank=True, verbose_name='Через міста')
    travel_times = models.IntegerField(verbose_name='Время в пути')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршрути'
        ordering = ['name']
