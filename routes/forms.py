from django import forms
from cities.models import City
from .models import Route


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Звідки', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    to_city = forms.ModelChoiceField(label='Куди', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    across_cities = forms.ModelMultipleChoiceField(label='Через міста', queryset=City.objects.all(),
                                                   widget=forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple'}), required=False)
    travelling_time = forms.IntegerField(label='Час у дорозі', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Час в дорозі'}))


class SaveRouteModel(forms.Form):
    name = forms.CharField(label='Назва маршруту', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    from_city = forms.CharField(widget=forms.HiddenInput)
    to_city = forms.CharField(widget=forms.HiddenInput)
    across_cities = forms.CharField(widget=forms.HiddenInput)
    travel_times = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Route
        fields = ['name', 'from_city', 'to_city', 'across_cities', 'travel_times']

