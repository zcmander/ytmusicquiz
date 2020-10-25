from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from django.shortcuts import redirect

from ytmusicquiz.models import Game


def finish(request, game_id):
    """
    Dashboard returns to initialize view (QR view)
    """

    channel_layer = get_channel_layer()

    game = Game.objects.get(pk=game_id)

    async_to_sync(channel_layer.group_send)(
        'game-{}'.format(game.id), {
            "type": 'game.finish',
            "game_id": game.id,
        }
    )

    return redirect("newgame")
