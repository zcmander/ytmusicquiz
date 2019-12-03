import json

from channels.generic.websocket import AsyncWebsocketConsumer

from ytmusicquiz.models import Game, Question, Player


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_name = 'game-{}'.format(self.game_id)

        await self.channel_layer.group_add(
            "game",
            self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "game",
            self.channel_name)

    async def receive(self, text_data):
        print("REVEICE", text_data)

    async def game_status(self, event):

        game = Game.objects.get(pk=event["game_id"])

        question_count = Question.objects.filter(game=game).count()

        question = Question.objects.filter(
            game=game,
            answered=False
        ).order_by("index").first()

        question_history = Question.objects.filter(
            game=game,
            answered=True,
        ).order_by("index").all()

        history = []
        stats = []

        for player in game.player_set.all():
            new_player = {
                "id": player.id,
                "display_name": player.display_name,
                "points": 0,
            }
            stats.append(new_player)

        for question_history in question_history:
            answers = question_history.answer_set.all()

            right_answers = list(filter(
                lambda answer: answer.points > 0,
                answers))

            # Statistics
            for right_answer in right_answers:

                player = None
                for existing_player in stats:
                    if existing_player["id"] == right_answer.player.id:
                        player = existing_player
                        break

                player["points"] += right_answer.points

            # History
            if len(right_answers) == 0:
                history.append({
                    "type": "failed",
                })
            elif len(right_answers) == 1:
                history.append({
                    "text": right_answers[0].points,
                    "player": right_answers[0].player.display_name,
                    "type": "player",
                })
            else:
                history.append({
                    "text": "{} players".format(len(right_answers)),
                    "type": "players",
                })

        return_event = {
            "type": "game.status",
            "history": history,
            "stats": sorted(stats, key=lambda obj: obj["points"], reverse=True),
            "question": {
                "progress": question.index,
                "count": question_count,
                "youtube": {
                    "id": question.track.videoId,
                    "start": question.track.start,
                    "end": question.track.end,
                }
            }
        }

        await self.send(json.dumps(return_event))

    async def game_answer(self, event):
        question = Question.objects.filter(
            game_id=event["game_id"],
            id=event["question_id"]
        ).first()

        await self.send(json.dumps({
            "type": "game.answer",
            "answer": {
                "artist": question.track.artist,
                "track": question.track.track,
                "feat": question.track.feat,
            },
            "correct_answered_players": event["correct_answered_players"]
        }))
