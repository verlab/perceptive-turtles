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

community_cprob = {
    "['true', 'true']": [.99, .01],
    "['true', 'false']": [.01, .99],
    "['false', 'true']": [.01, .99],
    "['false', 'false']": [.01, .99]
}


# Evidence Rules
fire_er = EvidenceRule("Fire", "Fire_Sensor", ["true", "false"],
                       ["true", "false"], fire_cprob, fire_sensor_cprob)
human_er = EvidenceRule("Human", "Human_Sensor", ["true", "false"],
                        ["true", "false"], human_cprob, human_sensor_cprob)

# Query Rules
qr = QueryRule('Human', 'Human in Danger', ["true", "false"], human_danger_cprob, "Fire", ["true", "false"], 10,
               joint_functions.mean)

cr = QueryRule('Human', 'Person in Community', ["true", "false"], community_cprob, 'Human', ["true", "false"], 10,
               joint_functions.mean)

##TODO community in fire

# Create engine
engine = InferenceEngine([fire_er, human_er, qr])


##### EVIDENCE
ef1 = Evidence(10, 30, "Fire_Sensor", ["true", "false"], "true")
ef2 = Evidence(19, 30, "Fire_Sensor", ["true", "false"], "false")

eh1 = Evidence(10, 30, "Human_Sensor", ["true", "false"], "true")
eh2 = Evidence(13, 31, "Human_Sensor", ["true", "false"], "true")

bn, bn_evidences = engine.infer_bn([eh1, ef1])

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



