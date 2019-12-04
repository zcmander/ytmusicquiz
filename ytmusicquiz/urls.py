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
    path('', views.newgame, name='newgame'),
    path('game/<int:game_id>', views.game, name='game'),
    path('game/<int:game_id>/answered', views.game_answered,
         name='game_answered'),
    path('game/<int:game_id>/finnish', views.gameover, name='gameover'),


    path('dashboard/<int:game_id>', views.dashboard, name='dashboard'),

    # Management
    path('process_draft', views.process_draft, name='process_draft'),
    path('add', views.add, name='add'),
    path('import_playlist', views.import_playlist, name='import_playlist'),
    path('admin/', admin.site.urls),
]
