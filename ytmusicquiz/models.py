from django.db import models


STATES = (
    ("DRAFT", "DRAFT"),
    ("DONE", "DONE"),
)


class QuestionTrack(models.Model):
    """
    Track question-model
    """

    videoId = models.CharField(
        verbose_name="Youtube Video ID",
        max_length=100,
        primary_key=True)

    state = models.CharField(max_length=10, choices=STATES)

    # -- Part of the video that should be regonized
    start = models.IntegerField()
    end = models.IntegerField(blank=True, null=True)

    # -- Categories
    released = models.IntegerField(blank=True, null=True)
    cover = models.BooleanField(blank=True, default=False)
    is_finnish = models.BooleanField(blank=True, null=True)

    # -- Playback categories

    # Can be used for 10s rule
    rule10s = models.BooleanField(blank=True, default=False)

    # If track is disliked, it won't show up
    disliked = models.BooleanField(blank=True, default=False)

    # -- Statistics
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -- Answer
    artist = models.CharField(max_length=255)
    track = models.CharField(max_length=255)
    feat = models.CharField(max_length=255, blank=True, null=True)
