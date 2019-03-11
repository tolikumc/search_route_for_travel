from django import forms
from .models import Train
from cities.models import City


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Потяг', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть назву потяга'}))
    from_city= forms.ModelChoiceField(label='Звідки', queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    to_city = forms.ModelChoiceField(label='Куди', queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    travel_time = forms.IntegerField(label='Місто', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Час в дорозі'}))

    class Meta:
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time')