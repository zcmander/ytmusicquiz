from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.send)(
                'background-tasks',
                {
                    "type": "import.playlist",
                    "url": form.cleaned_data["url"]
                }
            )

            return redirect('process_draft')

    return render(request, "ytmusicquiz/import_playlist.html", {"form": form})
