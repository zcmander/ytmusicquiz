from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from django.shortcuts import render

from ytmusicquiz.models import Game


def gameover(request, game_id):
    """
    The end of the game: Shows statistics and the winner of the game.
    """

    channel_layer = get_channel_layer()

    game = Game.objects.get(pk=game_id)

    async_to_sync(channel_layer.group_send)(
        'game', {
            "type": 'game.over',
            "game_id": game.id,
        }
    )

    return render(request, "ytmusicquiz/gameover.html")
