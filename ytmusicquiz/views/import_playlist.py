from django.shortcuts import render, redirect
from django import forms

import youtube_dl

from ytmusicquiz.models import QuestionTrack


class Form(forms.Form):
    url = forms.CharField(max_length=500)


def import_playlist(request):

    form = Form()

    if request.method == 'POST':
        form = Form(request.POST)

        if form.is_valid():

            ydl_opts = {
                "dump_single_json": True,
                "ignoreerrors": True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(
                    form.cleaned_data["url"],
                    download=False)

            for entry in result["entries"]:
                if not entry:
                    continue

                existing_qt = QuestionTrack.objects \
                    .filter(videoId=entry["id"]) \
                    .first()

                if (existing_qt):
                    continue

                question_track = QuestionTrack(
                    videoId=entry["id"],
                    track=entry["title"],
                    state="DRAFT",
                    start=0,
                )
                question_track.save()

            return redirect('process_draft')

    return render(request, "ytmusicquiz/import_playlist.html", {"form": form})
