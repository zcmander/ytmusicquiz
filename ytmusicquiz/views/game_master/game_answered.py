from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from django.shortcuts import render

from ytmusicquiz.models import Game, Question


def game_answered(request, game_id):
    """
    The page after answers are given. This step provides a pause between
    questions, so participants can get ready for the next question.
    """
    game = Game.objects.get(pk=game_id)

    channel_layer = get_channel_layer()

    question = Question.objects.filter(
        game=game,
        answered=True
    ).order_by("-index").first()

    question_count = Question.objects.filter(game=game).count()

    correct_answered_players = []

    for answer in question.answer_set.all():
        if answer.points <= 0:
            continue

        correct_answered_players.append({
            "player": {
                "id": answer.player.id,
                "display_name": answer.player.display_name,
            },
            "points": answer.points
        })

    async_to_sync(channel_layer.group_send)(
        'game-{}'.format(game.id), {
            "type": 'game.answer',
            "game_id": game.id,
            "question_id": question.id,
            "correct_answered_players": correct_answered_players
        }
    )

    return render(request, "ytmusicquiz/game_answered.html", {
        "game": game,
        "question_progress": question.index + 1,
        "question_count": question_count,
    })
