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
    path('', views.newgame, name='newgame'),

    # TV (DEPRECATED, use ytmusicquiz-dashboard project)
    path('dashboard/<int:game_id>', views.dashboard, name='dashboard'),

    # Game master
    path('game/<int:game_id>', views.game_master.game, name='game'),
    path('game/<int:game_id>/answered', views.game_master.game_answered,
         name='game_answered'),
    path('game/<int:game_id>/finnish', views.game_master.gameover,
         name='gameover'),


    # Management
    path('process_draft', views.management.process_draft,
         name='process_draft'),
    path('add', views.management.add, name='add'),
    path('import_playlist', views.management.import_playlist,
         name='import_playlist'),

    path('admin/', admin.site.urls),
]
