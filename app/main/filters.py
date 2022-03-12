import django_filters.rest_framework as filters
from .models import Client


class ClientFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.CharFilter(field_name='gender__name', lookup_expr='icontains')
    distanse = filters.NumberFilter(field_name='distance', method='distance_filter', label='Distance')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'gender']

    def distance_filter(self, queryset, name, value):
        """Фильтр расстояние"""
        D = self.request.user.get_distance_str()
        queryset = queryset.extra(where=[
            f"{D} < {value}"])
        return queryset
        # pifagure = SQRT(({user_latitude} - latitude)*({user_latitude} - latitude) + ({user_longitude} - longitude)*({user_longitude} - longitude))
        # value < self.request.user.get_distance((F('longitude'), F('latitude')))
        # return queryset.filter(flag)
