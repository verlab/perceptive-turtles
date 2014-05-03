from lib_sallybn.disc_bayes_net.BoxDiscreteBN import BoxDiscreteBN
from lib_sallybn.drawer.GPoint import GPoint
from lib_sallybn.drawer.GImage import GImage
from lib_sallybn.drawer.GRectangle import GRectangle


class DetectionMap(BoxDiscreteBN):
    def __init__(self, window):
        super(DetectionMap, self).__init__(window)


        self.toolbar_edit.set_visible(False)

        #self.background_gobjs = [GRectangle(GPoint(0, 0), 800, 600, None)]
        self.background_gobjs = [GImage(GPoint(0, 0), None, "../resources/map.png")]
        self.drawer.repaint()

    def add_evidence(self, x, y, variable, state):
        pass

    def add_infered(self, x, y, variable, state):
        pass

