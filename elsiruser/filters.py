import django_filters
from .models import Sale, Customer
from django_filters import DateFilter
from django import forms
from django.utils import timezone

class salesRepofilter(django_filters.FilterSet):
    fromdate = DateFilter(field_name="date_paid", lookup_expr='gte', widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control', 
            'placeholder': 'End Date'
              }))
    todate = DateFilter(field_name="date_paid", lookup_expr='lte',widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control', 
            'placeholder': 'End Date'
              }))
    class Meta:
        model = Sale
        fields = ['date_paid']
        exclude = ['date_paid']
        

    


        