from django.contrib.auth import login
from django.forms import ValidationError
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.fields import empty
from rest_framework.response import Response

from playgroups.models import Commander, Match, Player, Playgroup
from playgroups.permissions import PlaygroupChildPermission, PlaygroupPermission
from playgroups.serializers.commander import CommanderSerializer
from playgroups.serializers.match import (
    MatchCreateSerializer,
    MatchSerializer,
    MatchSimpleSerializer,
)
from playgroups.serializers.player import PlayerSerializer
from playgroups.serializers.playgroup import (
    PlaygroupCreateSerializer,
    PlaygroupSerializer,
    PlaygroupUpdateSerializer,
)


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data or isinstance(
            serializer.validated_data, empty
        ):
            return ValidationError("Invalid credentials")
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class PlaygroupViewSet(viewsets.ModelViewSet):
    queryset = Playgroup.objects.all()
    permission_classes = [PlaygroupPermission]

    def get_serializer_class(self):
        if self.action == "update":
            return PlaygroupUpdateSerializer
        elif self.action == "create":
            return PlaygroupCreateSerializer
        else:
            return PlaygroupSerializer


class PlaygroupChildViewSet(viewsets.ModelViewSet):
    permission_classes = [PlaygroupChildPermission]

    def get_playgroup_id(self) -> str:
        return self.kwargs["playgroup_pk"]

    def perform_create(self, serializer):
        serializer.save(playgroup_id=self.get_playgroup_id())

    def perform_update(self, serializer):
        serializer.save(playgroup_id=self.get_playgroup_id())


class PlayerViewSet(PlaygroupChildViewSet):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.filter(playgroup=self.get_playgroup_id())


class MatchViewSet(PlaygroupChildViewSet):
    def get_queryset(self):
        return Match.objects.filter(self.get_playgroup_id())

    def get_serializer_class(self):
        if self.action == "list":
            return MatchSimpleSerializer
        elif self.action == "create":
            return MatchCreateSerializer
        return MatchSerializer


class CommanderList(generics.ListAPIView):
    queryset = Commander.objects.all()
    serializer_class = CommanderSerializer


class CommanderDetail(generics.RetrieveAPIView):
    queryset = Commander.objects.all()
    serializer_class = CommanderSerializer
