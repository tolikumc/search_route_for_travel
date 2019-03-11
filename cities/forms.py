from django import forms
from .models import *


class CityForm(forms.ModelForm):
    name = forms.CharField(label='Місто', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Введіть назву міста'}))

    class Meta:
        model = City
        fields = ('name', )