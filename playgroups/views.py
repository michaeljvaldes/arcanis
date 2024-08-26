from django.contrib.auth import login
from django.forms import DateTimeField, ValidationError
from drf_spectacular.utils import extend_schema, inline_serializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.fields import CharField, DateTimeField, empty

from playgroups.models import Commander, Match, Player, Playgroup
from playgroups.permissions import PlaygroupChildPermission, PlaygroupPermission
from playgroups.serializers import (
    CommanderSerializer,
    MatchSerializer,
    PlayerSerializer,
    PlaygroupSerializer,
)


@extend_schema(
    request=AuthTokenSerializer,
    responses=inline_serializer(
        name="LoginResponseSerializer",
        fields={"expiry": DateTimeField(), "token": CharField()},
    ),
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
    serializer_class = PlaygroupSerializer
    permission_classes = [PlaygroupPermission]


class PlaygroupChildViewSet(viewsets.ModelViewSet):
    """
    A generic viewset to support common operations for child
    objects of playgroups. The playgroup id obtained from the
    url is used to inform permissions, filter the queryset,
    and overwrite the data in create/update operations.
    """

    permission_classes = [PlaygroupChildPermission]

    def get_playgroup_id(self) -> str:
        return self.kwargs["playgroup_pk"]

    def get_queryset(self):
        if self.queryset:
            return self.queryset.filter(playgroup=self.get_playgroup_id())


class PlayerViewSet(PlaygroupChildViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class MatchViewSet(PlaygroupChildViewSet):
    queryset = Match.objects.prefetch_related("match_players").all()
    serializer_class = MatchSerializer


class CommanderList(generics.ListAPIView):
    queryset = Commander.objects.all()
    serializer_class = CommanderSerializer


class CommanderDetail(generics.RetrieveAPIView):
    queryset = Commander.objects.all()
    serializer_class = CommanderSerializer
