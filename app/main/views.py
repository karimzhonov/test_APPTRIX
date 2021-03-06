from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializer import *
from .models import *
from .image_refactor import impose_ico_to_image
from .filters import ClientFilter


class CreateClientView(generics.CreateAPIView):
    """Создается клиент, рефакторинг изображения и сохраняет изображение"""
    serializer_class = CreateClientSerializer
    queryset = Client.objects.all()

    def create(self, request, *args, **kwargs):
        # Refactor avatar
        avatar = request.data['avatar']
        image = impose_ico_to_image(avatar)
        # Serialzing data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.data)
        # Refactor fields
        data['avatar'] = request.data['avatar'].name.__str__()
        # create Client
        client = Client.objects.create_user(**data)
        client.save_avatar(image)
        client.save()
        # Response
        headers = self.get_success_headers(serializer.data)
        data['id'] = client.pk
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class AuthClientView(viewsets.ModelViewSet):
    """Аутентификация клиента"""
    serializer_class = AuthClientSerializer
    queryset = Client.objects.all()

    def login(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        data = {
            'auth_status': False,
            'client': None,
        }
        client = authenticate(username=username, password=password)
        if client is not None:
            login(self.request, client)
            data['auth_status'] = True
            serializer = ShowClientSerializer(client)
            data['client'] = serializer.data
            return Response(data, status.HTTP_202_ACCEPTED)
        else:
            return Response(data, status.HTTP_306_RESERVED)


class ShowClientView(generics.RetrieveAPIView):
    """Покажит одного из клиентов(Пол: female=1, male=2)"""
    serializer_class = ShowClientSerializer
    queryset = Client.objects.all()


class MatchClientView(viewsets.ViewSet):
    """Подходящие клиенты, если они оба совпадают, отправляется электронное письмо"""
    def match(self, request, pk):
        # Getting Data
        if not self.request.user.is_authenticated:
            return redirect('auth_client')
        else:
            from_client_id = self.request.user.pk
            to_client_id = pk
            # Create Match
            data = {
                'match_created_status': False,
                'email_sent_status': False,
            }
            try:
                Match.objects.create(from_client_id=from_client_id, to_client_id=to_client_id)
                data['match_created_status'] = True
                # Searching Match
                old_matchs = Match.objects.filter(from_client_id=to_client_id, to_client_id=from_client_id)
                if old_matchs:
                    from_client = Client.objects.get(pk=from_client_id)
                    to_client = Client.objects.get(pk=to_client_id)
                    data['from_client_id'] = from_client.pk
                    data['from_client_response'] = from_client.send_email_about_matching(to_client)
                    data['from_client_email'] = from_client.email
                    data['to_client_id'] = to_client.pk
                    data['to_client_response'] = to_client.send_email_about_matching(from_client)
                    data['to_client_eamil'] = to_client.email
                    data['email_sent_status'] = True
                return Response(data, status=status.HTTP_202_ACCEPTED)
            except IntegrityError:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ListClientsView(generics.ListAPIView):
    """Список клиентов с фильтрами (Пол: female=1, male=2)"""
    serializer_class = ShowClientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClientFilter
    queryset = Client.objects.all()


class CoordinateClientView(viewsets.ViewSet):
    """
    Координат Клиента
    get запрос для получения
    post запрос для корректировки
    """
    serializer_class = CoordinateClientSerializer

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('auth_client')
        else:
            user = self.request.user
            data = {
                'longitude': user.longitude,
                'latitude': user.latitude,
            }
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Getting Data
        if not self.request.user.is_authenticated:
            return redirect('auth_client')
        else:
            user = self.request.user
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid()
            data = serializer.data
            # Update Model
            user.longitude = data['longitude']
            user.latitude = data['latitude']
            user.save()
            return self.get(request)


class DistanceClientView(viewsets.ViewSet):
    """View для получение расстояние"""
    def get(self, request, pk):
        if not self.request.user.is_authenticated:
            return redirect('auth_client')
        else:
            user = self.request.user
            client = get_object_or_404(Client, pk=pk)
            data = {
                'user_id': user.id,
                'client_id': client.id,
                'user_longitude': user.longitude,
                'user_latitude': user.latitude,
                'client_longitude': client.longitude,
                'client_latitude': client.latitude,
                'distance': user.get_distance(
                    (client.latitude, client.longitude)
                ),
            }
            return Response(data, status=status.HTTP_200_OK)
