from gi.repository import Gtk

from infengine import joint_functions
from infengine.Evidence import Evidence
from infengine.InferenceEngine import InferenceEngine
from infengine.rules.GridRule import GridRule, Grid
from infengine.rules.CommunityRule import CommunityRule
from infengine.rules.EvidenceRule import EvidenceRule
from infengine.rules.QueryRule import QueryRule
from lib_sallybn.disc_bayes_net.BoxDiscreteBN import BoxDiscreteBN, Mode

COMMUNITY_RADIO = 0.000018006862307153121620199864860722982484730891883373260498046875

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

cr = CommunityRule('Human', 'Community', ["true", "false"], COMMUNITY_RADIO,
                   joint_functions.mean)

cdr = QueryRule('Community', 'Community in Danger', ["true", "false"], human_danger_cprob, "Fire", ["true", "false"],
                10,
                joint_functions.mean)
# Grid rule
human_gridr = GridRule("Human", "Human_Sensor", ["true", "false"],
                       ["true", "false"], human_cprob, human_sensor_cprob, Grid(0, 0, 10, 20, 30, 60))


# Create engine
#engine = InferenceEngine([fire_er, human_er, qr, cr, cdr])
engine = InferenceEngine([human_gridr])


##### EVIDENCE
ef1 = Evidence(10, 30, "Fire_Sensor", ["true", "false"], "true")
ef2 = Evidence(19, 30, "Fire_Sensor", ["true", "false"], "false")

eh1 = Evidence(10.0, 20.0, "Human_Sensor", ["true", "false"], "true")
eh2 = Evidence(5, 19, "Human_Sensor", ["true", "false"], "false")
eh3 = Evidence(15, 18, "Human_Sensor", ["true", "false"], "true")
eh4 = Evidence(16, 17, "Human_Sensor", ["true", "false"], "true")
eh5 = Evidence(-124.4577, 108.0135, "Human_Sensor", ["true", "false"], "true")

# bn, bn_evidences = engine.infer_bn([eh2, eh3, eh4, eh1, eh5, ])
bn, bn_evidences = engine.infer_bn([eh1, eh2, eh3, eh4])

# shape_writer.write(bn, engine.vertex_locations, bn_evidences)
# geojson.write(bn, engine.vertex_locations, bn_evidences, output_folder='../output_shapes')

###### SHOW
# # Create window
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



