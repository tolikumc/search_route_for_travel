from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import *
from trains.models import Train
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
       из одного города в другой. Вариант посещения
       одного и того же города более одного раза,
        не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():
    qs = Train.objects.values('from_city')
    from_city_set = set(i['from_city'] for i in qs)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp

    return graph


@login_required(login_url='/login/')
def search_route(request):
    form = RouteForm()
    return render(request, 'routes/search_route.html', context={'forms': form})


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            # отримуєво дані з форми пошуку маршруту
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            travelling_time = data['travelling_time']
            # створюємо граф
            graph = get_graph()
            # шукаемо маршрути в графі/ передаєм сам граф, айді обєкту міста який приходить з форми/ аналогічно доінцевої точки
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            # здійснюємо провірку якщо в нас нема ніяких маршрутів тобто рівна 0
            if len(all_ways) == 0:
                messages.error(request, 'Маршруту, згідно умов пошуку не існує.')
                return render(request, 'routes/search_route.html', {'forms': form})
            # перевіряєм чи є міста через які необхідно проїхати
            if across_cities_form:
                #якщо є список необхідних міст через які треба проїхати ми робим генератор через які взнаєм айді цих міст
                across_cities = [city.id for city in across_cities_form]
                #створюємо пустий список
                right_ways = []
                # створюємо перевірки чи існують маршрути які проходять через вказані міста
                for way in all_ways:
                    # якщо є такі маршрути піхаєм їх в список вище
                    # вей це список міст через який проходить маршрут
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                # якщо нема ніодного маршрута який проходить через міста
                if not right_ways:
                    messages.error(request, 'Маршрут, через ці міста немоєливий')
                    return render(request, 'routes/search_route.html', {'forms': form})
                # якщо нема міст через які треба проїжати запихаєм всі маршрути яку найшла функція dfs_paths
            else:
                right_ways = all_ways

            # створюємо список потягів
            trains = []
            # необхідно вибрати всі позда в списку right_away
            for route in right_ways:
                # словник
                print(route)
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(route) - 1):
                    # отримуємо всі поїзда в яких є наш маршрут right_way
                    qs = Train.objects.filter(from_city=route[index], to_city=route[index + 1])
                    #  якщо ми отримуємо декілька поїздів то сортуєм по часу який найкоротший
                    qs = qs.order_by('travel_time').first()
                    # записуємо час на дорогу в перемінну тотал тайм
                    total_time += qs.travel_time
                    #  добавляємо потяг в словник за ключом потягу
                    tmp['trains'].append(qs)
                # добавляємо тотал тайм в наш словник
                tmp['total_time'] = total_time
                # якщо час менший ніж ми отримали з форми від користувача тоді ми наший словник добаляєм в словник тмп
                if total_time <= travelling_time:
                    trains.append(tmp)
            # якщо список пустий ми видаєм помилку і повертаємо на головну
            print(trains)
            if not trains:
                messages.error(request, "Час в дорозі, більше вибраного.", )
                return render(request, 'routes/search_route.html', {'forms': form})
            routes = []
            # параметри які будем виводити на сорінку
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            # добавляєм словник з траінс з даними
            for tr in trains:
                routes.append({'route': tr['trains'],
                               'total_time': tr['total_time'],
                               'from_city': from_city.name,
                               'to_city': to_city.name})
            # сортуємо список роутес
            print(routes)
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                #  отримуємо всі часи які є в тотал тайм (список унікального значення часу по маршрутах)
                times = list(set(x['total_time'] for x in routes))
                # сортуєм від меншого до більшого
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)

            form = RouteForm()
            print(sorted_routes)
            context = {
                'forms': form,
                'routes': sorted_routes,
                'cities': cities
            }
            return render(request, 'routes/search_route.html', context)
        return render(request, 'routes/search_route.html', {'forms': form})
    else:
        messages.error(request, 'Створіть маршрут')
        form = RouteForm()
        return render(request, 'routes/search_route.html', {'forms': form})


def add_route(request):
    if request.method == 'POST':
        form = SaveRouteModel(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            travel_time = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities'].split(' ')
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            print(qs)
            route = Route(name=name, from_city=from_city, to_city=to_city, travel_times=travel_time)
            route.save()
            for tr in qs:
                route.across_cities.add(tr.id)
                print(tr.id)
            messages.success(request, 'Маршрут збережено')
            return redirect('/')
    else:
        data = request.GET
        if data:
            travel_time = data['travel_time']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities']
            print('across_cities', across_cities)
            trains = [int(x) for x in across_cities if x.isalnum()]
            print('trains', trains)
            qs = Train.objects.filter(id__in=trains)
            print('qs:', qs)
            train_list = ' '.join(str(i) for i in trains)
            print('tarin_list:', train_list)
            form = SaveRouteModel(initial={'travel_times': travel_time,
                                           'from_city': from_city,
                                           'to_city': to_city,
                                           'across_cities': train_list})

            route_desc = []
            for tr in qs:
                description = 'Потяг №{} прямує з міста {} в місто {}. Час в дорозі {}'.format(tr.name, tr.from_city, tr.to_city, tr.travel_time)
                route_desc.append(description)

            context = {
                'form': form,
                'description': route_desc,
                'from_city': from_city,
                'to_city': to_city,
                'travel_time': travel_time
            }
            return render(request, 'routes/save_route.html', context)
        else:
            messages.error(request, 'Неможливо зберегти маршрут зверніться в адміністрацію')
            return redirect('/')


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'routes_detail'
    template_name = 'routes/routes_detail.html'


class RouteListView(ListView):
    queryset = Route.objects.all()
    context_object_name = 'routes_list'
    template_name = 'routes/routes_list.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    template_name = 'routes/delete_routes.html'
    success_url = reverse_lazy('routes/routes_list.html')
    login_url = '/login/'

