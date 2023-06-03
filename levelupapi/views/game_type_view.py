"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = GameType.objects.all()
        serializer = GameTypeSerializer(
            game_types, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST request
        
        Returns
            Response - JSON serialzed instance of game type
        """
        game_type = GameType.objects.create(
            label=request.data["label"]
        )
        serializer = GameTypeSerializer(game_type)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests to get all game types

        Returns:
            Response -- 204
        """
        game_type = GameType.objects.get(pk=pk)
        game_type.label = request.data['label']
        game_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE
        Returns:
             Response -- 204
        """
        game_type = GameType.objects.get(pk=pk)
        game_type.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    class Meta:
        model = GameType
        fields = ('id', 'label')
