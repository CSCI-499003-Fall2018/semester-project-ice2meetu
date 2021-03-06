from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from creation.models import EventUser, Event, Grouping, Group
from games.models import Game, GameType
from rest_framework.permissions import IsAuthenticated


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EventUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = EventUser
        fields = '__all__'



class EventSerializer(serializers.ModelSerializer):
    event_users = EventUserSerializer(required=True, many=True)
    class Meta:
        model = Event
        fields = '__all__'


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class =  EventSerializer

class GroupingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grouping
        fields = '__all__'

class GroupingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Grouping.objects.all()
    serializer_class = GroupingSerializer

class GroupSerializer(serializers.ModelSerializer):
    grouping = GroupingSerializer(required=True)
    class Meta:
        model = Group
        fields = '__all__'

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    game_type = GameTypeSerializer(required=True)
    class Meta:
        model = Game
        fields = '__all__'

class GameViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer
