import django_filters.rest_framework as filters
from .models import Client

class ClientFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.CharFilter(field_name='gender__name', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'gender']

