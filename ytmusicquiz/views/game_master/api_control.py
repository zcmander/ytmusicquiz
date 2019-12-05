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

    async_to_sync(channel_layer.group_send)(
        'game-{}'.format(game.id), {
            "type": "control.{}".format(json.loads(request.body)["action"]),
            "game_id": game.id,
        }
    )

    return JsonResponse({})
