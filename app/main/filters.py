import django_filters.rest_framework as filters
from .models import Client


class ClientFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.CharFilter(field_name='gender__name', lookup_expr='iexact', label='Пол (female, male)')
    distanse = filters.NumberFilter(field_name='distance', method='distance_filter', label='Расстояние')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name']

    def distance_filter(self, queryset, name, value):
        """Фильтр расстояние"""
        D = self.request.user.get_distance_str()
        queryset = queryset.extra(where=[
            f"{D} < {value}"])
        return queryset
