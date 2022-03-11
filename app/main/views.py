import os
import io
import cv2
from PIL import Image
import numpy as np
from django.core.files.base import File
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets, generics
from .serializer import *


class CreateClientView(generics.CreateAPIView):
    serializer_class = CreateClientSerializer
    queryset = Client.objects.all()

    def create(self, request, *args, **kwargs):
        # csrfmiddlewaretoken
        csrfmiddlewaretoken = request.data['csrfmiddlewaretoken'][0]
        request.data.pop('csrfmiddlewaretoken')
        # avatar
        avatar = request.data['avatar']
        request.data.pop('avatar')
        # refactor gender field
        request.data['gender_id'] = request.data['gender']
        request.data.pop('gender')
        # refactor data dict farmat: data[key] = [value]
        data = dict(request.data)
        for key, value in data.items():
            data[key] = value[0]
        client = Client(**data)
        # Resactor avatar
        # image = cv2.imdecode(np.frombuffer(avatar.read(), np.uint8), -1)
        # image_height, image_wight, _ = image.shape
        # path_to_ico = os.path.join(settings.STATIC_ROOT, 'favicon.jpeg')
        # ico = cv2.imread(path_to_ico)
        # ico_height, ico_width, _ = ico.shape
        # # refactoring ico
        # new_ico_width = image_wight // 10
        # new_ico_height = int(ico_height * (ico_width / new_ico_width))
        # new_ico = cv2.resize(ico, (new_ico_width, new_ico_height))
        # #


        client.avatar.save(
            avatar.name,
            File(avatar)
        )
        #
        # print(client.avatar)



def test(request):
    return HttpResponse('Test')