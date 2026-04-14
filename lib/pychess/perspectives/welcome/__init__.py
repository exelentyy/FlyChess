from flychess.widgets.TaskerManager import tasker
from flychess.perspectives import Perspective


class Welcome(Perspective):
    def __init__(self):
        Perspective.__init__(self, "welcome", _("Welcome"))

        self.default = True
        self.widget.add(tasker)
