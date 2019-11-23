from django.shortcuts import render

from ytmusicquiz.models import Game, Question


def game(request, game_id):
    """
    Main game page, where answers are given.
    """

    game = Game.objects.get(pk=game_id)

    question_count = Question.objects.filter(game=game).count()

    question = Question.objects.filter(
        game=game,
        answered=False
    ).order_by("index").first()

    return render(request, "ytmusicquiz/game.html", {
        "game": game,
        "question": question,
        "question_progress": question.index,
        "question_count": question_count,
    })
