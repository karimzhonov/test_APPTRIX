from django.urls import path
from .views import *

urlpatterns = [
    path('clients/create', CreateClientView.as_view()),
]