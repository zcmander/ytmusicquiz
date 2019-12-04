from django.shortcuts import render

from django.core.paginator import Paginator

from ytmusicquiz.models import QuestionTrack


def list_unprocessed(request):
    tracks = QuestionTrack.objects.filter(
        state="DRAFT"
    ).order_by("artist", "track")

    paginator = Paginator(tracks, 25)

    page = request.GET.get('page')

    return render(request, "ytmusicquiz/list.html", {
        "title": "List of unprocessed tracks",
        "tracks": paginator.get_page(page)
    })
