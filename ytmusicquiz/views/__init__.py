from .newgame import newgame
from .dashboard import dashboard

from . import game_master
from . import management

__all__ = [
    newgame,
    dashboard,
    game_master,
    management
]
