from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer

from playgroups.models import Commander, Match, Player, Playgroup
from playgroups.permissions import IsOwnerOrReadOnly
from playgroups.serializers import (CommanderSerializer, MatchCreateSerializer,
                                    MatchSerializer, PlayerSerializer,
                                    PlaygroupSerializer, SimpleMatchSerializer)


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class PlaygroupList(generics.ListAPIView):
    queryset = Playgroup.objects.all()
    serializer_class = PlaygroupSerializer


class PlaygroupDetail(generics.RetrieveAPIView):
    queryset = Playgroup.objects.all()
    serializer_class = PlaygroupSerializer


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommanderList(generics.ListAPIView):
    queryset = Commander.objects.all()
    serializer_class = CommanderSerializer


class CommanderDetail(generics.RetrieveAPIView):
    queryset = Commander.objects.all()
    serializer_class = CommanderSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleMatchSerializer
        elif self.action == 'create':
            return MatchCreateSerializer
        return MatchSerializer
