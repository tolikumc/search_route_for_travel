from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import *


def city_list_view(request):
    search_query = request.GET.get('search', '')

    if search_query:
        cities = City.objects.filter(name__icontains=search_query)
    else:
        cities = City.objects.all()

    paginator = Paginator(cities, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context ={
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }
    return render(request, 'cities/city_list.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'city_detail'
    template_name = 'cities/city_detail.html'


class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:city_list')
    success_message = 'Місто успішно створено!'


class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('city:city_list')
    success_message = 'Місто успішно відредаговано!'


class CityDeleteView(DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('city:city_list')

    # # для видалення без підтвердження!!!!
    # def get(self, request, *args, **kwargs):
    # messages.success(request, 'Місто успішно видалено!')
    #     return self.post(request, *args, **kwargs)