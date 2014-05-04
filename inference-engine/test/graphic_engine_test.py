from gi.repository import Gtk

from infengine import joint_functions

from infengine.Evidence import Evidence
from infengine.InferenceEngine import InferenceEngine
from infengine.rules.EvidenceRule import EvidenceRule
from infengine.rules.QueryRule import QueryRule
from lib_sallybn.disc_bayes_net.BoxDiscreteBN import BoxDiscreteBN, Mode


fire_sensor_cprob = {
    "['true']": [.7, .3],
    "['false']": [.1, 0.9],
}
human_sensor_cprob = {
    "['true']": [.7, .3],
    "['false']": [.4, 0.6],
}
fire_cprob = [0.4, 0.6]
human_cprob = [0.3, 0.7]

human_danger_cprob = {
    "['true', 'true']": [.9, .1],
    "['true', 'false']": [.2, .8],
    "['false', 'true']": [.1, .9],
    "['false', 'false']": [.05, .95]
}


# Evidence Rules
fire_er = EvidenceRule("Fire", "Fire_Sensor", ["true", "false"],
                       ["true", "false"], fire_cprob, fire_sensor_cprob)
human_er = EvidenceRule("Human", "Human_Sensor", ["true", "false"],
                        ["true", "false"], human_cprob, human_sensor_cprob)

# Query Rules
qr = QueryRule('Human', 'Human in Danger', ["true", "false"], human_danger_cprob, "Fire", ["true", "false"], 10,
               joint_functions.mean)

# Create engine
engine = InferenceEngine([fire_er, human_er], [qr])


##### EVIDENCE
e1 = Evidence(10, 30, "Fire_Sensor", ["true", "false"], "true")
e2 = Evidence(10, 30, "Human_Sensor", ["true", "false"], "true")

e3 = Evidence(12, 30, "Fire_Sensor", ["true", "false"], "true")
bn, bn_evidences = engine.infer_bn([e1, e2, e2, e3, e1])

###### SHOW
# Create window
window = Gtk.Window()
window.set_size_request(800, 600)

box = BoxDiscreteBN(window, disc_bn=bn)
box.evidences = bn_evidences
box.organize_graph(random=False)
box.set_mode(Mode.run)

window.add(box)
window.show_all()

window.connect("delete-event", Gtk.main_quit)
Gtk.main()



