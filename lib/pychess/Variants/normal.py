"""Standard Chess game"""

from flychess.Utils.Board import Board


class NormalBoard(Board):
    """:Description: A standard chess game board setup"""

    __desc__ = _("Classic chess rules\n" + "http://en.wikipedia.org/wiki/Chess")
    name = _("Normal")
    cecp_name = "normal"
    need_initial_board = False
    standard_rules = True
