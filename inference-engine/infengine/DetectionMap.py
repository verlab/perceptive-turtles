from lib_sallybn.disc_bayes_net.BoxDiscreteBN import BoxDiscreteBN
from lib_sallybn.drawer.GPoint import GPoint
from lib_sallybn.drawer.GRectangle import GRectangle


class DetectionMap(BoxDiscreteBN):
    def __init__(self, window):
        super(DetectionMap, self).__init__(window)
        # self.window = window

        self.toolbar_edit.set_visible(False)
        print "oh oh"

        self.background_gobjs = [GRectangle(GPoint(10, 10), 20, 20, None)]
        self.drawer.repaint()

    def add_evidence(self, x, y, variable, state):
        pass

    def add_infered(self, x, y, variable, state):
        pass

