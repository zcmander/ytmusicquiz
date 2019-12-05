import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse, HttpResponseBadRequest

from ytmusicquiz.models import Game


def api_control(request, game_id):
    if not request.is_ajax():
        return HttpResponseBadRequest()

    channel_layer = get_channel_layer()

    game = Game.objects.get(pk=game_id)

    data = json.loads(request.body)
    action = data["action"]

    # Connect to dashboard
    if action == 'connect':
        game_name = 'game-{}'.format(game.id)

        async_to_sync(channel_layer.group_add)(
            game_name,
            data['dashboard_id'])

    # Other control events
    else:
        async_to_sync(channel_layer.group_send)(
            'game-{}'.format(game.id), {
                "type": "control.{}".format(action),
                "game_id": game.id,
            }
        )

    return JsonResponse({})
