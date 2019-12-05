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
        "form": form,
        "can_reject": False,
        "submit_button_text": "Add"
    })


def process_draft(request, video_id=None):
    q = QuestionTrack.objects.filter(state="DRAFT")

    if video_id:
        q = q.filter(videoId=video_id)

    qt = q.first()

    if not qt:
        raise Exception("No question tracks in DRAFT state")

    form = Form(instance=qt)

    if request.method == 'POST':
        if 'reject' in request.POST:
            qt.state = "REJECTED"
            qt.save()
            return redirect('process_draft')

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
        "form": form,
        "can_reject": True,
        "submit_button_text": "Mark as Done"
    })
