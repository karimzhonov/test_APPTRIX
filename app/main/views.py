from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .serializer import *
from .models import *
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
            login(self.request, client)
            return redirect('show_client', pk=client.pk)
        else:
            return Response({})

class ShowClientView(generics.RetrieveAPIView):
    serializer_class = ShowClientSerializer
    queryset = Client.objects.all()


class MatchClientView(viewsets.ModelViewSet):
    queryset = Client.objects.all()

    def get(self, request, client_id):
        # Getting Data
        from_client_id = self.request.user.pk
        to_client_id = client_id
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
            return Response(data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
