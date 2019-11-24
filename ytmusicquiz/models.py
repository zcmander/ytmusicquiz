from django.db import models


STATES = (
    ("DRAFT", "DRAFT"),
    ("DONE", "DONE"),
)


class QuestionTrack(models.Model):
    """
    Single track that can be as question in a game.
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

    def __str__(obj):
        if obj.feat:
            return "%s - %s (%s)" % (obj.artist, obj.track, obj.feat)
        return "%s - %s" % (obj.artist, obj.track)


class Game(models.Model):
    """
    Contains all information that is needed for single run of the game.
    """

    # -- Statistics
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    """
    Question track that has been selected to the game.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    track = models.ForeignKey(QuestionTrack, on_delete=models.PROTECT)

    index = models.IntegerField(blank=False, null=False)

    answered = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        unique_together = (
            # Game cannot have duplicate tracks
            ("game", "track"),

            # Track indexes must be unique for the game
            ("game", "index")
        )


class Player(models.Model):
    """
    Player in the game.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)


class Answer(models.Model):
    """
    The player has an answer for the question.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    # How many points the game master has given for the answer?
    points = models.IntegerField(null=False, blank=False)
