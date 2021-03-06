"""ytmusicquiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [

    # Intro
    path('', views.intro, name='intro'),

    # New game (step 1/1)
    path('new', views.newgame, name='newgame'),

    # TV (DEPRECATED, use ytmusicquiz-dashboard project)
    path('dashboard', views.dashboard, name='dashboard'),

    # Game master

    # New game (Step 2/2)
    path('game/<int:game_id>/setup', views.game_master.setup, name='setup'),

    # Question
    path('game/<int:game_id>', views.game_master.game, name='game'),

    # Answer
    path('game/<int:game_id>/answered', views.game_master.game_answered,
         name='game_answered'),

    # Game over (Statistics)
    path('game/<int:game_id>/gameover', views.game_master.gameover,
         name='gameover'),

    # End game (Return to new game -page)
    path('game/<int:game_id>/finish', views.game_master.finish,
         name='finish'),

    # Game Master API
    path('api/game/<int:game_id>/control', views.game_master.api_control,
         name='api_control'),


    # Management
    path('list_unprocessed', views.management.list_unprocessed,
         name='list_unprocessed'),
    path('process_draft', views.management.process_draft,
         name='process_draft'),
    path('process_draft/<video_id>', views.management.process_draft,
         name='process_draft'),
    path('add', views.management.add, name='add'),
    path('import_playlist', views.management.import_playlist,
         name='import_playlist'),

    path('admin/', admin.site.urls),
]
