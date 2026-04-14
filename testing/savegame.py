import os
import os.path
import asyncio
import logging
import unittest

from flychess.Utils.Move import Move
from flychess.Utils.lutils.lmovegen import newMove
from flychess.Utils.GameModel import GameModel
from flychess.Utils.TimeModel import TimeModel
from flychess.Utils.const import WHITE, BLACK, LOCAL, F2, F3, E7, E5, G2, G4, D8, H4
from flychess.Players.Human import Human
from flychess.System import conf, uistuff, cancel_all_tasks
from flychess.widgets import gamewidget
from flychess.perspectives import perspective_manager
from flychess.perspectives.games import Games
from flychess.perspectives.database import Database
from flychess.perspectives.welcome import Welcome
from flychess.perspectives.database.FilterPanel import formatted, TAG_FILTER, RULE
from flychess.System.Log import log

log.logger.setLevel(logging.INFO)

base_name = "flychess_test"
conf.set("saveOwnGames", True)
conf.set("autoSaveFormat", base_name)
default_path = os.path.expanduser("~")
test_pgn = os.path.join(default_path, "%s.pgn" % base_name)
test_bin = os.path.join(default_path, "%s.bin" % base_name)
test_scout = os.path.join(default_path, "%s.scout" % base_name)
test_sqlite = os.path.join(default_path, "%s.sqlite" % base_name)

for f in (test_pgn, test_bin, test_scout, test_sqlite):
    if os.path.isfile(f):
        os.remove(f)


class DatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        loop = asyncio.get_event_loop()
        loop.set_debug(enabled=True)

        widgets = uistuff.GladeWidgets("flychess.glade")
        gamewidget.setWidgets(widgets)
        perspective_manager.set_widgets(widgets)

        self.welcome_persp = Welcome()
        perspective_manager.add_perspective(self.welcome_persp)

        self.games_persp = Games()
        perspective_manager.add_perspective(self.games_persp)

        self.database_persp = Database()
        perspective_manager.add_perspective(self.database_persp)
        self.database_persp.create_toolbuttons()

    async def asyncTearDown(self):
        await cancel_all_tasks()

    async def test1(self):
        """Play and save Human-Human 1 min game"""

        gamemodel = GameModel(TimeModel(1, 0))

        player0tup = (LOCAL, Human, (WHITE, "w"), "w")
        player1tup = (LOCAL, Human, (BLACK, "b"), "b")

        def on_game_end(game, state, event):
            event.set()

        event = asyncio.Event()
        gamemodel.connect("game_ended", on_game_end, event)

        def on_players_changed(game):
            # fill fools mate moves to players move queue
            p0 = game.players[0]
            p0.move_queue.put_nowait(Move(newMove(F2, F3)))
            p0.move_queue.put_nowait(Move(newMove(G2, G4)))

            p1 = gamemodel.players[1]
            p1.move_queue.put_nowait(Move(newMove(E7, E5)))
            p1.move_queue.put_nowait(Move(newMove(D8, H4)))

        gamemodel.connect("players_changed", on_players_changed)
        await self.games_persp.generalStart(gamemodel, player0tup, player1tup)

        # waiting for game end ...
        await event.wait()

        fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        self.assertEqual(gamemodel.boards[-1].board.asFen(), fen)

        # Now save our game to flychess.pgn
        self.games_persp.saveGamePGN(gamemodel)

    def test2(self):
        """Import world_matches.pgn into flychess_test.pgn"""

        def on_chessfile_opened(persp, cf):
            self.assertEqual(self.database_persp.chessfile.count, 1)

            curdir = os.path.dirname(__file__)
            filename = "%s/gamefiles/world_matches.pgn" % curdir
            self.database_persp.importing(
                [
                    filename,
                ]
            )

        def on_chessfile_imported(persp, cf):
            # We saved 1 game in test1 and world_matches.pgn has 580 games
            self.assertEqual(self.database_persp.chessfile.count, 581)

        self.database_persp.connect("chessfile_opened", on_chessfile_opened)
        self.database_persp.connect("chessfile_imported", on_chessfile_imported)
        self.database_persp.open_chessfile(test_pgn)

    async def test3(self):
        """Filter flychess.pgn by Kasparov as white"""

        def on_chessfile_opened(persp, cf):
            self.assertEqual(self.database_persp.chessfile.count, 581)

            fp = self.database_persp.filter_panel
            name_filter = {"white": "Kasparov"}
            fp.ini_widgets_from_query(name_filter)
            tag_query, material_query, pattern_query = fp.get_queries_from_widgets()
            self.assertEqual(tag_query, name_filter)

            selection = fp.get_selection()
            model, treeiter = selection.get_selected()
            fp.treestore.append(
                treeiter, [formatted(tag_query), tag_query, TAG_FILTER, RULE]
            )
            fp.filtered = True
            fp.update_filters()
            # world_matches.pgn has 49 games where Kasparov was white
            self.assertEqual(len(self.database_persp.gamelist.records), 49)

        self.database_persp.connect("chessfile_opened", on_chessfile_opened)
        self.database_persp.open_chessfile(test_pgn)


if __name__ == "__main__":
    unittest.main()
