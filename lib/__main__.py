import logging
import sys

from pychess.System.Log import log
from pychess.Players.pychessCECP import pychessCECP

if len(sys.argv) == 1 or sys.argv[1:] == ["debug"]:
    if "debug" in sys.argv[1:]:
        log.logger.setLevel(logging.DEBUG)
    else:
        log.logger.setLevel(logging.WARNING)

    pychess = pychessCECP()
else:
    print("Unknown argument(s):", repr(sys.argv))
    sys.exit(0)

pychess.makeReady()
pychess.run()
