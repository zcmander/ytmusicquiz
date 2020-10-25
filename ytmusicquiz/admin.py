from django.contrib import admin
from .models import QuestionTrack, Question, Game, Player, Answer


def track_display_name(obj):
    if obj.feat:
        return "%s - %s (%s)" % (obj.artist, obj.track, obj.feat)
    return "%s - %s" % (obj.artist, obj.track)


@admin.register(QuestionTrack)
class QuestionTrackAdmin(admin.ModelAdmin):
    list_display = ('display_name', "length", "state")
    list_filter = ('state',)

    def length(self, obj):
        if obj.start and obj.end:
            return obj.end - obj.start
        return None

    def display_name(self, obj):
        return track_display_name(obj)


class PlayerInline(admin.TabularInline):
    model = Player


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [
        PlayerInline,
        QuestionInline,
    ]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
