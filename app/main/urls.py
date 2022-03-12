from django.urls import path
from .views import *

urlpatterns = [
    path('clients/list/', ListClientsView.as_view(), name='list_client'),
    path('clients/create/', CreateClientView.as_view(), name='create_client'),
    path('clients/auth/', AuthClientView.as_view({'post': 'post'}), name='auth_client'),
    path('clients/<int:pk>/', ShowClientView.as_view(), name='show_client'),
    path('clients/<int:client_id>/match/', MatchClientView.as_view({'get': 'get'}), name='match_client'),
]