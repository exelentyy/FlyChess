import os.path
import unittest

from flychess.System import uistuff
from flychess.widgets import gamewidget
from flychess.perspectives.games import Games
from flychess.perspectives.database import Database
from flychess.perspectives import perspective_manager


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        widgets = uistuff.GladeWidgets("flychess.glade")
        gamewidget.setWidgets(widgets)
        perspective_manager.set_widgets(widgets)

        self.games_persp = Games()
        perspective_manager.add_perspective(self.games_persp)

        self.database_persp = Database()
        self.database_persp.create_toolbuttons()
        perspective_manager.add_perspective(self.database_persp)

    def test1(self):
        """Open a .pgn database"""
        curdir = os.path.dirname(__file__)
        filename = "%s/gamefiles/world_matches.pgn" % curdir
        self.database_persp.open_chessfile(filename)


if __name__ == "__main__":
    unittest.main()
