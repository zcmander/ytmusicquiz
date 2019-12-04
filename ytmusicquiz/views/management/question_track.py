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
            obj = form.save()
            obj.state = "DONE"
            obj.save()
            return redirect('add')

    return render(request, "ytmusicquiz/form.html", {
        "title": "Add new entry",
        "form": form
    })


def process_draft(request):
    qt = QuestionTrack.objects.filter(state="DRAFT").first()

    if not qt:
        raise Exception("No question tracks in DRAFT state")

    form = Form(instance=qt)

    if request.method == 'POST':
        form = Form(request.POST, instance=qt)

        if form.is_valid():
            obj = form.save()
            obj.state = "DONE"
            obj.save()
            return redirect('process_draft')

    left = QuestionTrack.objects.filter(state="DRAFT").count() - 1

    title = "Process Question tracks in DRAFT-state ({} left)".format(left)

    return render(request, "ytmusicquiz/form.html", {
        "title": title,
        "form": form
    })