from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Game, Gamer
from levelupapi.views.game_view import GameSerializer

class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['tokens', 'gamers', 'game_types', 'games', 'events']
    
    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        game = {
            "title": "Clue",
            "maker": "Milton Bradley",
            "skill_level": 5,
            "number_of_players": 6,
            "game_type": 1,
        }

        response = self.client.post(url, game, format='json')

        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        # Get the last game added to the database, it should be the one just created
        new_game = Game.objects.last()

        # Since the create method should return the serialized version of the newly created game,
        # Use the serializer you're using in the create method to serialize the "new_game"
        # Depending on your code this might be different
        expected = GameSerializer(new_game)

        # Now we can test that the expected ouput matches what was actually returned
        self.assertEqual(expected.data, response.data)