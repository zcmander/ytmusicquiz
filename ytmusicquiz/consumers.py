import json

import youtube_dl
from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer

from ytmusicquiz.models import Game, Question, QuestionTrack


class GameConsumer(WebsocketConsumer):
    """
    Dashboard consumer. Every dashboard connects using websocket using game
    url.
    """

    def connect(self):
        """
        Handle websocket connection.
        """
        self.accept()

        return_event = {
            "type": "dashboard.id",
            "dashboard_id": self.channel_name
        }

        # Send channel name back to game, because client is
        # not aware of it otherwise. It's used to show QR-code
        # for game master.
        self.send(json.dumps(return_event))

        # Just connected, but not connected to any game
        self.game_name = None

    def disconnect(self, close_code):
        """
        Handles websocket disconnection.
        """

        # If connected to game, leave game group.
        if self.game_name:
            self.channel_layer.group_discard(
                self.game_name,
                self.channel_name)

    def receive(self, text_data):
        """
        Handle data sent from client.
        """

        # Dashboard does not send anything. It just displays game state and
        # acts as audio sink.
        print("REVEICE", text_data)

    def _get_statistics(self, game):
        """
        Returns current statistics of the game: Who is winning and how many
        points totally.
        """
        stats = []

        question_history = Question.objects.filter(
            game=game,
            answered=True,
        ).order_by("index").all()

        for player in game.player_set.all():
            new_player = {
                "id": player.id,
                "display_name": player.display_name,
                "points": 0,
            }
            stats.append(new_player)

        for question_history in question_history:
            for answer in question_history.answer_set.all():
                player = None
                for existing_player in stats:
                    if existing_player["id"] == answer.player.id:
                        player = existing_player
                        break

                player["points"] += answer.points

        return sorted(stats, key=lambda obj: obj["points"], reverse=True)

    def _get_history(self, game):
        """
        During game, top bar shows who player has answered right on previous
        questions and by how many points. This collectes that information.
        """
        question_history = Question.objects.filter(
            game=game,
            answered=True,
        ).order_by("index").all()

        history = []

        for question_history in question_history:
            answers = question_history.answer_set.all()

            right_answers = list(filter(
                lambda answer: answer.points > 0,
                answers))

            # No-one answered right
            if len(right_answers) == 0:
                history.append({
                    "type": "failed",
                })

            # Single player has answered right
            elif len(right_answers) == 1:
                history.append({
                    "text": right_answers[0].points,
                    "player": right_answers[0].player.display_name,
                    "type": "player",
                })

            # Multiple players have answered right
            else:
                history.append({
                    "text": "{} players".format(len(right_answers)),
                    "type": "players",
                })
        return history

    def game_status(self, event):
        """
        Game status -message is Question-state, where music starts to play and
        players should listen carefully.
        """
        game = Game.objects.get(pk=event["game_id"])

        question_count = Question.objects.filter(game=game).count()

        question = Question.objects.filter(
            game=game,
            answered=False
        ).order_by("index").first()

        return_event = {
            "type": "game.status",
            "history": self._get_history(game),
            "stats": self._get_statistics(game),
            "question": {
                "progress": question.index + 1,
                "count": question_count,
                "youtube": {
                    "id": question.track.videoId,
                    "start": question.track.start,
                    "end": question.track.end,
                }
            }
        }

        self.send(json.dumps(return_event))

    def game_answer(self, event):
        """
        After players have answered, dashboard shows right answered players on
        the screen.
        """
        question = Question.objects.filter(
            game_id=event["game_id"],
            id=event["question_id"]
        ).first()

        self.send(json.dumps({
            "type": "game.answer",
            "answer": {
                "artist": question.track.artist,
                "track": question.track.track,
                "feat": question.track.feat,
            },
            "correct_answered_players": event["correct_answered_players"]
        }))

    def game_over(self, event):
        """
        The game is over and it's time to show graphs.
        """
        game = Game.objects.get(pk=event["game_id"])

        question_history = Question.objects.filter(
            game=game,
            answered=True,
        ).order_by("index").all()

        # Calculate cumulative history of the right answers.
        cumhist = []

        event = {}
        for player in game.player_set.all():
            event["index"] = "0"
            event[player.display_name] = 0
        cumhist.append(event)

        for i, question_history in enumerate(question_history):
            answers = question_history.answer_set.all()

            latest_event = cumhist[-1].copy()
            latest_event["index"] = str(i + 1)

            for answer in answers:
                latest_event[answer.player.display_name] += answer.points

            cumhist.append(latest_event)

        return_event = {
            "type": "game.over",
            "stats": self._get_statistics(game),
            "cumhist": cumhist,
        }

        self.send(json.dumps(return_event))

    def game_finish(self, event):
        """
        After game over -screen. The game really ends and dashboard returns to
        pairing mode.
        """
        self.game_name = "game-{}".format(event["game_id"])
        self.send(json.dumps({
            "type": "game.finish",
        }))

    def control_playpause(self, event):
        """
        Game master controls during question stage: Play/Pause player.
        """
        self.send(json.dumps({
            "type": "control.playpause",
        }))

    def control_replay(self, event):
        """
        Game master controls during question stage: Replay question.
        """
        self.send(json.dumps({
            "type": "control.replay",
        }))

    def control_connect(self, event):
        """
        After pairing has been done, inform dashboard (client) so it can hide
        QR code and start wait for game to begin.
        """
        self.game_name = "game-{}".format(event["game_id"])
        self.send(json.dumps({
            "type": "control.connect",
        }))


class BackgroundConsumer(SyncConsumer):
    """
    Consumer for background tasks. All tasks that cannot be compelted during
    single HTTP request/response.
    """

    def import_playlist(self, message):
        """
        Handles importing playlist.
        """
        ydl_opts = {
            "dump_single_json": True,
            "ignoreerrors": True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                message["url"],
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
