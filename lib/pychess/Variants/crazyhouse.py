# Crazyhouse Chess

from flychess.Utils.const import CRAZYHOUSECHESS, VARIANTS_OTHER_NONSTANDARD
from flychess.Utils.Board import Board


class CrazyhouseBoard(Board):
    variant = CRAZYHOUSECHESS
    __desc__ = _(
        "FICS crazyhouse: http://www.freechess.org/Help/HelpFiles/crazyhouse.html"
    )
    name = _("Crazyhouse")
    cecp_name = "crazyhouse"
    need_initial_board = False
    standard_rules = False
    variant_group = VARIANTS_OTHER_NONSTANDARD
