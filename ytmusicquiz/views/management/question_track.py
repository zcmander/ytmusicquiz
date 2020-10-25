from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django import forms

from ytmusicquiz.models import QuestionTrack


class Form(forms.ModelForm):
    class Meta:
        model = QuestionTrack
        fields = ('videoId', 'start', 'end', 'artist', 'track', 'feat')


@staff_member_required
def add(request):
    form = Form()

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


@staff_member_required
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
