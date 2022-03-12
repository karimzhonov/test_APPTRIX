from django.urls import path
from .views import *

urlpatterns = [
    path('clients/create', CreateClientView.as_view()),
    path('client/auth', AuthClientView.as_view({'post': 'post'})),
    path('clents/<int:pk>/', ShowClientView.as_view(), name='show_client'),
]