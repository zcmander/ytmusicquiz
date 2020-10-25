from django.shortcuts import render, redirect
from django import forms

from ytmusicquiz.models import Game
from ytmusicquiz.utils import generate_questions


class Form(forms.Form):
    player1 = forms.CharField(label='Player 1', max_length=100, required=False)
    player2 = forms.CharField(label='Player 2', max_length=100, required=False)
    player3 = forms.CharField(label='Player 3', max_length=100, required=False)
    player4 = forms.CharField(label='Player 4', max_length=100, required=False)


def newgame(request):
    """
    Creates a new game using given player names.
    """
    form = Form()

    if request.method == 'POST':
        form = Form(request.POST)

        if form.is_valid():
            player1 = form.cleaned_data["player1"]
            player2 = form.cleaned_data["player2"]
            player3 = form.cleaned_data["player3"]
            player4 = form.cleaned_data["player4"]

            game = Game()
            game.save()

            if player1:
                game.player_set.create(display_name=player1)
            if player2:
                game.player_set.create(display_name=player2)
            if player3:
                game.player_set.create(display_name=player3)
            if player4:
                game.player_set.create(display_name=player4)

            generate_questions(game)
            return redirect("setup", game_id=game.id)

    return render(request, "ytmusicquiz/newgame.html", {"form": form})
