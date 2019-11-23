from ytmusicquiz.models import QuestionTrack


def generate_questions(game):
    """
    Generates questions for the game.
    """
    count = 10
    tracks = QuestionTrack.objects.order_by("?")[:count]

    for index, track in enumerate(tracks):
        game.question_set.create(
            track=track,
            index=index
        )
