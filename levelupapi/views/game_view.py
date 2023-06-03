from django.http import HttpResponseServerError
from django.db.models import Count
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
        try:
            game = Game.objects.annotate(event_count=Count('events')).get(pk=pk)
            serializer = GameSerializer(
                game, context={'request': request})
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.annotate(event_count=Count('events'))
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
        game_type = GameType.objects.get(pk=request.data["gameType"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["numberOfPlayers"],
            skill_level=request.data["skillLevel"],
            game_type=game_type,
            gamer=gamer,
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)

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


class GameSerializer(serializers.ModelSerializer):
    event_count = serializers.IntegerField(default=None)
    """JSON serializer"""
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker',
                  'gamer', 'number_of_players', 'skill_level', 'event_count', 'event_info')
        depth = 1
