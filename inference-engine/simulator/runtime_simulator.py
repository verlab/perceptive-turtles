import numpy as np

from infengine.rules.GridRule import Grid
from infengine.Evidence import Evidence
from infengine.InferenceEngine import InferenceEngine
from simulator import rules
from simulator.ambient import Ambient
from simulator.sensor import Sensor


FIRE_SENSOR = "Fire_Sensor"
BOOLEAN_STATES = ["true", "false"]
PEOPLE_SENSOR = "Human_Sensor"

human_tt = 0.7
human_tf = 0.8
fire_tt = 0.999
fire_tf = 0.999
map = Grid(0, 0, 100, 200, 10, 15)

ambient = Ambient(map_size=[100, 200], n_people=20, n_fire=5, distance_danger=2)
evidences = []


def add_evidences(true_points, false_points, sensor):
    """ Points to evidences
    """
    for tp in true_points:
        ev = Evidence(tp[0], tp[1], sensor, BOOLEAN_STATES, BOOLEAN_STATES[0])
        evidences.append(ev)

    for tp in false_points:
        ev = Evidence(tp[0], tp[1], sensor, BOOLEAN_STATES, BOOLEAN_STATES[1])
        evidences.append(ev)


##### People
print "Persons ", len(ambient.people_points), " points: ", ambient.people_points
human_sensor = Sensor(ambient, ambient.people_points, tt=1, ff=1, std_dev=2.00000001, true_samples_prop=0.2)

true_points, false_points = human_sensor.sense(800)
print "People detected:", true_points
print "No people in:", false_points
add_evidences(true_points, false_points, PEOPLE_SENSOR)


###### Fire
# fire_sensor = Sensor(ambient, ambient.fire_points, tt=1, ff=1, std_dev=10.00000001, true_samples_prop=0.5)
# true_points, false_points = human_sensor.sense(20)
# add_evidences(true_points, false_points, FIRE_SENSOR)

### PLOT

# noinspection PyNoneFunctionAssignment
# people = ambient.people_points.round().astype(np.int32)
# people_true = true_points.round().astype(np.int32)
# people_false = false_points.round().astype(np.int32)
#
# img = np.zeros((ambient.map_size[0], ambient.map_size[1], 3), dtype=np.int32)
#
# img[people[:, 0], people[:, 1]] = [100, 100, 100]
# img[people_true[:, 0], people_true[:, 1]] = [0, 100, 0]
# img[people_false[:, 0], people_false[:, 1]] = [100, 0, 0]
#
# plt.imshow(img)
# plt.show()

# Run engine
# Engine
engine = InferenceEngine(rules.get_rules(human_tt, human_tf, fire_tt, fire_tf, map))

# create bayesian network
bn, bn_evidences = engine.infer_bn(evidences)

# window = Gtk.Window()
# window.set_size_request(800, 600)
#
# box = BoxDiscreteBN(window, disc_bn=bn)
# box.evidences = bn_evidences
# box.organize_graph(random=False)
# box.set_mode(Mode.edit_vertex)
#
# window.add(box)
# window.show_all()
#
# window.connect("delete-event", Gtk.main_quit)
# Gtk.main()

### Resultant human grid.
rhg = [[[] for x in np.arange(map.tx, map.tx + map.width, map.dx)] for y in
       np.arange(map.ty, map.ty + map.height, map.dy)]

# query_points = []
for v in bn.V:
    print v
    var_name = v.split("'")[1]

    if var_name != 'Human':
        continue

    loc = engine.vertex_locations[v]
    j = int((loc[0] - map.tx) / map.dx)
    i = int((loc[1] - map.ty) / map.dy)

    if len(rhg) <= i or i < 0 or len(rhg[0]) <= j or j < 0:
        print "point out of range ", loc
        continue

    marginal = bn.compute_vertex_marginal(v, bn_evidences)
    rhg[i][j] = marginal['true']
    # query_points.append([loc[0], loc[1], marginal['true']])

print "grid=", rhg

# for
