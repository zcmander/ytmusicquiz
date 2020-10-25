from django.shortcuts import render

from ytmusicquiz.models import Game


def setup(request, game_id):
    """
    Pair dahsboard.
    """
    game = Game.objects.get(pk=game_id)

    return render(request, "ytmusicquiz/setup.html", {
        "game": game,
    })
