
from gi.repository import Gtk, GObject
import random

from lib_sallybn.disc_bayes_net.DiscreteBayesianNetworkExt import DiscreteBayesianNetworkExt
from infengine.DetectionMap import DetectionMap

## Discrete an empty discrete bayesian network
disc_bn = DiscreteBayesianNetworkExt()
# # Vertex and its states
# disc_bn.add_vertex("A", states=["true1", "false1"])
# disc_bn.add_vertex("C", states=["true", "false"])
# disc_bn.add_vertex("B", states=["true", "false"])
#
# # Edges
# disc_bn.add_edge(["A", "B"])
# disc_bn.add_edge(["C", "B"])
#
# # Conditional Probability Table
# cprob_b = {
#     "['true1', 'true']": [.3, .7],
#     "['true1', 'false']": [.9, .1],
#     "['false1', 'true']": [.05, .95],
#     "['false1', 'false']": [.5, .5]
# }
# cprob_a = [.3, .7]
# cprob_c = [.2, .8]
#
# disc_bn.set_cprob("A", cprob_a)
# disc_bn.set_cprob("B", cprob_b)
# disc_bn.set_cprob("C", cprob_c)

###### SHOW
# Create window
window = Gtk.Window()
window.set_size_request(800, 600)

box = DetectionMap(window)
box.on_organize(None)
window.add(box)
window.show_all()

window.connect("delete-event", Gtk.main_quit)
Gtk.main()


