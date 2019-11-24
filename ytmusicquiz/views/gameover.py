from django.shortcuts import render


def gameover(request, game_id):
    """
    The end of the game: Shows statistics and the winner of the game.
    """

    return render(request, "ytmusicquiz/gameover.html")
