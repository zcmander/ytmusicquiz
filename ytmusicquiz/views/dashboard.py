import json

from django.shortcuts import render
from django.utils.safestring import mark_safe


def dashboard(request, game_id):
    return render(
        request,
        "ytmusicquiz/dashboard.html",
        {"game_id_json":  mark_safe(json.dumps(game_id))})
