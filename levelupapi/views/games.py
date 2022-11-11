"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType, Event, EventGamer
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.core.exceptions import ValidationError



class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        event_gamers = EventGamer.objects.all()
        # gamer = Gamer.objects.get(user=request.auth.user)
        for event_gamer in event_gamers:
            games = Game.objects.annotate(event_count=Count('events'),
                user_event_count=Count('events', filter=Q(gamer=event_gamer.gamer)))

        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # game_type = GameType.objects.get(pk=request.data["game_type"])

        # game = Game.objects.create(
        #     title=request.data["title"],
        #     maker=request.data["maker"],
        #     number_of_players=request.data["number_of_players"],
        #     skill_level=request.data["skill_level"],
        #     gamer=gamer,
        #     game_type=game_type
        # )
        # serializer = GameSerializer(game)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)

class GamersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', )

class CreateGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    gamer = GamersSerializer(many=False)
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)

    class Meta:
        model = Game
        fields = ('id', 'game_type', 'gamer', 'title', 'maker', 'number_of_players', 
            'skill_level', 'event_count', 'user_event_count')
        depth = 1