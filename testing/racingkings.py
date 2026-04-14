import unittest

from flychess.Utils.const import DRAW, DRAW_KINGSINEIGHTROW, RUNNING, UNKNOWN_REASON
from flychess.Utils.logic import validate, getStatus
from flychess.Utils.Move import parseSAN
from flychess.Variants.racingkings import RacingKingsBoard

# . . ♜ . . . ♖ .
# . . ♚ . . . . ♔
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
FEN = "2r3R1/2k4K/8/8/8/8/8/8 w - - 0 1"


class RacingKingsTestCase(unittest.TestCase):
    def test1(self):
        """Testing both king goes to 8.row draw in racingkings variant"""

        board = RacingKingsBoard(setup=FEN)
        board = board.move(parseSAN(board, "Kh8"))
        print(board)
        # White king reached 8th row, but this is not a win
        # because black can reach 8th row also with hes next move
        self.assertEqual(getStatus(board), (RUNNING, UNKNOWN_REASON))

        self.assertTrue(validate(board, parseSAN(board, "Kb8")))
        self.assertTrue(not validate(board, parseSAN(board, "Kd8")))

        board = board.move(parseSAN(board, "Kb8"))
        print(board)
        self.assertEqual(getStatus(board), (DRAW, DRAW_KINGSINEIGHTROW))


if __name__ == "__main__":
    unittest.main()
