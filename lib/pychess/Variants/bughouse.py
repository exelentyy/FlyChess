# Bughouse Chess

from flychess.Utils.const import VARIANTS_OTHER_NONSTANDARD, BUGHOUSECHESS
from flychess.Utils.Board import Board


class BughouseBoard(Board):
    variant = BUGHOUSECHESS
    __desc__ = _("FICS bughouse: http://www.freechess.org/Help/HelpFiles/bughouse.html")
    name = _("Bughouse")
    cecp_name = "bughouse"
    need_initial_board = False
    standard_rules = False
    variant_group = VARIANTS_OTHER_NONSTANDARD
