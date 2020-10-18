from django.shortcuts import render


def intro(request):
    """
    Frontpage, where user must choose if current device should act as game
    master or dashboard.
    """
    return render(request, "ytmusicquiz/intro.html")
