import cv2
import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .serializer import *
from .image_refactor import impose_ico_to_image


class CreateClientView(generics.CreateAPIView):
    serializer_class = CreateClientSerializer
    queryset = Client.objects.all()

    def create(self, request, *args, **kwargs):
        # Refactor avatar
        avatar = request.data['avatar']
        image = cv2.imdecode(np.frombuffer(avatar.read(), np.uint8), -1)
        image = impose_ico_to_image(image)
        # Serialzing data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.data)
        data['avatar'] = request.data['avatar'].name.__str__()
        # create Client
        client = Client.create(**data)
        client.save_avatar(image)
        # Response
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class AuthClientView(viewsets.ModelViewSet):
    serializer_class = AuthClientSerializer
    queryset = Client.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        client = authenticate(username=username, password=password)
        if client is not None:
            return redirect('show_client', pk=client.pk)
        else:
            return Response({})

class ShowClientView(generics.RetrieveAPIView):
    serializer_class = ShowClientSerializer
    queryset = Client.objects.all()

def test(request):
    return HttpResponse('Test')
