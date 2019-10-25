from django.shortcuts import render, redirect
from django import forms

from .models import QuestionTrack


class Form(forms.ModelForm):
    class Meta:
        model = QuestionTrack
        fields = ('videoId', 'start', 'end', 'artist', 'track', 'feat')


def add(request):
    if request.method == 'POST':
        form = Form(request.POST)

        if form.is_valid():

            form.save()
            return redirect('add')
    else:
        form = Form(initial={
            "videoId": "yQkdMh4GW4M",
            "start": 103,
            "stop": 103 + 15,
            "artist": "costee",
            "track": "Satuta mua kunnolla"
        })

    return render(request, "ytmusicquiz/form.html", {"form": form})
