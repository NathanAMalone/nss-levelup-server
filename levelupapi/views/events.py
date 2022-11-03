"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer
from django.contrib.auth.models import User

class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()

        if "game" in request.query_params:
            for event in events:
                if int(request.query_params['game']) == event.game_id:
                    events = events.filter(game=event.game_id)
        else:
            pass

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(pk=request.data["organizer"])

        game = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=organizer
        )
        serializer = EventSerializer(game)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)


class OrganizerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', )

class GamersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', )
        
class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('title', )

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    organizer = OrganizerSerializer(many=False)
    gamers = GamersSerializer(many=True)
    game = GameSerializer(many=False)
    
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer', 'description', 'date', 'time', 'gamers', )
        