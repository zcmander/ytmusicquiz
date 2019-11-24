from django.shortcuts import render, redirect
from django import forms

from bootstrap4.widgets import RadioSelectButtonGroup

from ytmusicquiz.models import Game, Question, Player


class AnswerForm(forms.Form):
    player_id = forms.CharField(required=True, widget=forms.HiddenInput())
    player_name = forms.CharField(required=False)
    points = forms.ChoiceField(
        choices=(
            (0, '-2'),
            (1, '-1'),
            (2, '0'),
            (3, '+1'),
            (4, '+2'),
        ),
        initial=2,
        label="Points",
        required=True,
        widget=RadioSelectButtonGroup
    )


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
            print(form.cleaned_data)

            for player_form in form.cleaned_data:
                player = Player.objects.filter(
                    game=game,
                    id=player_form["player_id"]
                ).first()

                game.answer_set.create(
                    player=player,
                    question=question,
                    points=(int(player_form["points"]) - 2)
                )

            question.answered = True

            question.save()

            return redirect("game", game_id=game.id)
    else:
        form = AnswerFormset(initial=initial)

    return render(request, "ytmusicquiz/game.html", {
        "game": game,
        "question": question,
        "question_progress": question.index,
        "question_count": question_count,
        "form": form,
    })
