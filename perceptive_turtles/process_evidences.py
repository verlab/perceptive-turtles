import pickle
from gi.repository import Gtk

from infengine.InferenceEngine import InferenceEngine
from infengine.gis import geojson
from lib_sallybn.disc_bayes_net.BoxDiscreteBN import BoxDiscreteBN, Mode
import rules


with open('evidences.pkl', 'rb') as evidence_input:
    evidences = pickle.load(evidence_input)

## Engine
engine = InferenceEngine(rules.get_rules())

# create bayesian network
bn, bn_evidences = engine.infer_bn(evidences)

# Output Layer
geojson.write(bn, engine.vertex_locations, bn_evidences)

##### Show the resultant Bayesian Network
# for i in range(1, 16, 5):
#     bn, bn_evidences = engine.infer_bn(evidences[:i])
#     window = Gtk.Window()
#     window.set_size_request(800, 600)
#
#     box = BoxDiscreteBN(window, disc_bn=bn)
#     box.evidences = bn_evidences
#     box.organize_graph(random=False)
#     box.set_mode(Mode.run)
#
#     window.add(box)
#     window.show_all()
#
#     window.connect("delete-event", Gtk.main_quit)
#     Gtk.main()



# bn, bn_evidences = engine.infer_bn(evidences[:20])
# window = Gtk.Window()
# window.set_size_request(800, 600)
#
# box = BoxDiscreteBN(window, disc_bn=bn)
# box.evidences = bn_evidences
# box.organize_graph(random=False)
# box.set_mode(Mode.run)
#
# window.add(box)
# window.show_all()
#
# window.connect("delete-event", Gtk.main_quit)
# Gtk.main()