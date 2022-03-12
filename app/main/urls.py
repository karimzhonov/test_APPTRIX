from django.urls import path
from .views import *


urlpatterns = [
    path('client/list/', ListClientsView.as_view(), name='list_client'),
    path('client/create/', CreateClientView.as_view(), name='create_client'),
    path('client/auth/', AuthClientView.as_view({'post': 'login'}), name='auth_client'),
    path('client/coordinates/', CoordinateClientView.as_view({'post': 'post', 'get': 'get'}), name='coordinates_client'),
    path('client/<int:pk>/', ShowClientView.as_view(), name='show_client'),
    path('client/<int:pk>/match/', MatchClientView.as_view({'get': 'match'}), name='match_client'),
    path('client/<int:pk>/distance/', DistanceClientView.as_view({'get': 'get'}), name='distance_client'),
]
