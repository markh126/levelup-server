from django.http import HttpResponseServerError
from django.db.models import Count
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer


class GameView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)
        try:
            games = Game.objects.annotate(
                event_count=Count('events'),
                user_event_count=Count('events', filter=Q(events__organizer=gamer))
            ).get(pk=pk)
            serializer = GameSerializer(
                games, context={'request': request})
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)
        games = Game.objects.annotate(
            event_count=Count('events'),
            user_event_count=Count('events', filter=Q(events__organizer=gamer))
            )
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests to get all games

        Returns:
            Response -- 204
        """
        game = Game.objects.get(pk=pk)
        game.title = request.data['title']
        game.maker = request.data['maker']
        game.number_of_players = request.data['numberOfPlayers']
        game.skill_level = request.data['skillLevel']

        game_type = GameType.objects.get(pk=request.data['gameType'])
        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        game.game_type = game_type
        game.gamer = gamer
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE
        Returns:
             Response -- 204
        """
        game = Game.objects.get(pk=pk)
        game.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']

class GameSerializer(serializers.ModelSerializer):
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)
    """JSON serializer"""
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker',
                  'gamer', 'number_of_players', 'skill_level',
                  'event_count', 'user_event_count', 'event_info')
        depth = 1
