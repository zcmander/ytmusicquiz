from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator

from ytmusicquiz.models import QuestionTrack


@staff_member_required
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
