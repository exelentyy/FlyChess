import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from flychess.Players.flychessCECP import flychessCECP


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = flychessCECP()

    @patch("sys.stdout", new_callable=StringIO)
    @patch(
        "flychess.Players.flychessCECP.get_input",
        new=MagicMock(side_effect=["protover 2", "stop_unittest"]),
    )
    def test1(self, mock_stdout):
        """Send 'protover 2' to flychess engine"""

        self.engine.run()
        output = mock_stdout.getvalue()

        self.assertTrue(output.endswith("feature done=1\n"))

    @patch("sys.stdout", new_callable=StringIO)
    @patch(
        "flychess.Players.flychessCECP.get_input",
        new=MagicMock(side_effect=["perft", "stop_unittest"]),
    )
    def test2(self, mock_stdout):
        """Send 'perft' to flychess engine"""

        self.engine.run()
        output = mock_stdout.getvalue()

        self.assertTrue(output.endswith("nps\n"))

    @patch("sys.stdout", new_callable=StringIO)
    @patch(
        "flychess.Players.flychessCECP.get_input",
        new=MagicMock(side_effect=["benchmark 2", "stop_unittest"]),
    )
    def test3(self, mock_stdout):
        """Send 'benchmark 2' to flychess engine"""

        self.engine.run()
        output = mock_stdout.getvalue()

        self.assertTrue(output.endswith("n/s\n"))


if __name__ == "__main__":
    unittest.main()
