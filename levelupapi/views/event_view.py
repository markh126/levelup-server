"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, Game, Gamer, EventGamer


class EventView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.annotate(attendees_count=Count('attendees')).get(pk=pk)
            serializer = EventSerializer(
                event, context={'request': request})
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)
        events = Event.objects.annotate(attendees_count=Count('attendees'))
        # game = request.query_params.get('game', None)

        # if game is not None:
        #     events = events.filter(game_id=game)
        for event in events:
            # Check to see if there is a row in the Event Games
            # table that has the passed in gamer and event
            event.joined = len(EventGamer.objects.filter(
                gamer=gamer, event=event)) > 0

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns 
        Response - JSON serialized event instance
        """

        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            game=game,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=gamer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests to get all game types

        Returns:
            Response -- 204
        """
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE
        Returns:
             Response -- 204
        """
        event = Event.objects.get(pk=pk)
        event.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        event = Event.objects.get(pk=pk)
        EventGamer.objects.create(
            gamer=gamer,
            event=event
    )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.get(
            gamer=gamer,
            event=event
        )
        attendee.delete()

        return Response({'message': 'Gamer left'}, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    attendees_count = serializers.IntegerField(default=None)
    """JSON serializer"""
    time = serializers.TimeField(format="%I:%M %p")
    date = serializers.DateField(format="%B %d, %Y")

    class Meta:
        model = Event
        fields = (
            'id',
            'game',
            'description',
            'date',
            'time',
            'organizer',
            'joined',
            'attendees_count')
        depth = 1
