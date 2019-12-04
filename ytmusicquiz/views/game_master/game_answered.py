from django.shortcuts import render

from ytmusicquiz.models import Game


def game_answered(request, game_id):
    """
    The page after answers are given. This step provides a pause between
    questions, so participants can get ready for the next question.
    """
    game = Game.objects.get(pk=game_id)
    return render(request, "ytmusicquiz/game_answered.html", {
        "game": game,
    })
