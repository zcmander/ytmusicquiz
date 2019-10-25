from django.contrib import admin
from .models import QuestionTrack

@admin.register(QuestionTrack)
class QuestionTrackAdmin(admin.ModelAdmin):
    pass
