from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django import forms

from bootstrap4.widgets import RadioSelectButtonGroup

from ytmusicquiz.models import Game, Question, Player


class AnswerForm(forms.Form):
    player_id = forms.CharField(required=True, widget=forms.HiddenInput())
    points = forms.ChoiceField(
        choices=(
            (0, '0'),
            (1, '+1'),
            (2, '+2'),
            (3, '+3'),
            (4, '+4'),
        ),
        initial=0,
        label="",
        required=True,
        widget=RadioSelectButtonGroup
    )


def game(request, game_id):
    """
    Main game page, where answers are given.

    In this stage, the dashboard will play the question track and
    game master can input answers during or after the track has been played.
    """

    game = Game.objects.get(pk=game_id)

    channel_layer = get_channel_layer()

    question_count = Question.objects.filter(game=game).count()

    question = Question.objects.filter(
        game=game,
        answered=False
    ).order_by("index").first()

    if not question:
        return redirect('gameover', game_id=game.id)

    players = Player.objects.filter(
        game=game,
    )

    AnswerFormset = forms.formset_factory(
        AnswerForm,
        min_num=len(players),
        max_num=len(players),
        can_delete=False,
        extra=0)

    initial = []

    for player in players:
        initial.append({
            "player_id": player.id,
            "player_name": player.display_name,
        })

    form = None
    if request.method == 'POST':
        form = AnswerFormset(request.POST)

        if form.is_valid():
            for player_form in form.cleaned_data:
                player = Player.objects.filter(
                    game=game,
                    id=player_form["player_id"]
                ).first()

                points = int(player_form["points"])

                game.answer_set.create(
                    player=player,
                    question=question,
                    points=points
                )

            question.answered = True

            question.save()

            questions_left = Question.objects.filter(
                game=game,
                answered=False
            ).count()

            if questions_left > 0:
                return redirect("game_answered", game_id=game.id)
            else:
                return redirect("gameover", game_id=game.id)
    else:
        form = AnswerFormset(initial=initial)

    async_to_sync(channel_layer.group_send)(
        'game-{}'.format(game.id), {
            "type": 'game.status',
            "game_id": game.id
        }
    )

    return render(request, "ytmusicquiz/game.html", {
        "game": game,
        "question": question,
        "question_progress": question.index + 1,
        "question_count": question_count,
        "formset": form,
        "player_names": [player.display_name for player in players]
    })
