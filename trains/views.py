from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Train
from .forms import TrainForm


def train_list_view(request):
    search_query = request.GET.get('search', '')

    if search_query:
        cities = Train.objects.filter(name__icontains=search_query)
    else:
        cities = Train.objects.all()

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
    return render(request, 'trains/train_list.html', context)


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    context_object_name = 'train_detail'
    template_name = 'trains/train_detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:train_list')
    success_message = 'Потяг успішно створено!'


class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    context_object_name = 'object'
    success_url = reverse_lazy('train:train_list')
    success_message = 'Потяг успішно відредаговано!'


class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('train:train_list')

    # # для видалення без підтвердження!!!!
    # def get(self, request, *args, **kwargs):
    # messages.success(request, 'Місто успішно видалено!')
    #     return self.post(request, *args, **kwargs)