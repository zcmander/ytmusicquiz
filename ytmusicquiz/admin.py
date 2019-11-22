from django.contrib import admin
from .models import QuestionTrack, Question, Game, Player, Answer


@admin.register(QuestionTrack)
class QuestionTrackAdmin(admin.ModelAdmin):
    pass


class PlayerInline(admin.TabularInline):
    model = Player


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [
        PlayerInline,
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
