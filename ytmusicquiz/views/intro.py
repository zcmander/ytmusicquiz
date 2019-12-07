from django.shortcuts import render


def intro(request):
    return render(request, "ytmusicquiz/intro.html")
