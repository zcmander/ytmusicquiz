from django.shortcuts import render, redirect
from django import forms

from ytmusicquiz.models import QuestionTrack


class Form(forms.ModelForm):
    class Meta:
        model = QuestionTrack
        fields = ('videoId', 'start', 'end', 'artist', 'track', 'feat')


def add(request):
    form = Form(initial={
        # "videoId": "yQkdMh4GW4M",
        # "start": 103,
        # "end": 103 + 15,
        # "artist": "costee",
        # "track": "Satuta mua kunnolla"
    })

    if request.method == 'POST':
        form = Form(request.POST)

        if form.is_valid():

            form.save()
            return redirect('add')

    return render(request, "ytmusicquiz/form.html", {"form": form})
