from django.contrib import admin
from .models import QuestionTrack, Question, Game, Player, Answer


@admin.register(QuestionTrack)
class QuestionTrackAdmin(admin.ModelAdmin):
    list_display = ('display_name', "length")

    def length(self, obj):
        if obj.start and obj.end:
            return obj.end - obj.start
        return None

    def display_name(self, obj):
        if obj.feat:
            return "%s - %s (%s)" % (obj.artist, obj.track, obj.feat)
        return "%s - %s" % (obj.artist, obj.track)


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
