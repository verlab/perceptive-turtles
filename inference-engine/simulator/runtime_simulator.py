import numpy as np

import matplotlib.pyplot as plt

from infengine.rules.GridRule import Grid
from infengine.observation import Observation
from infengine.InferenceEngine import InferenceEngine
from simulator import rules
from simulator.ambient import Ambient
from simulator.sensor import Sensor


FIRE_SENSOR = "Fire_Sensor"
BOOLEAN_STATES = ["true", "false"]
PEOPLE_SENSOR = "Human_Sensor"


def add_evidences(true_points, false_points, sensor, evidences):
    """ Points to evidences
    """
    for tp in true_points:
        ev = Observation(tp[0], tp[1], sensor, BOOLEAN_STATES, BOOLEAN_STATES[0])
        evidences.append(ev)

    for tp in false_points:
        ev = Observation(tp[0], tp[1], sensor, BOOLEAN_STATES, BOOLEAN_STATES[1])
        evidences.append(ev)


results = []

for param in np.arange(0.0, 0.5, 0.1):

    for aaa in range(10):
        #print "iteration",param, "a=", aaa

        sensor_human_tt = 0.99999999999999-param
        sensor_human_tf = 0.99999999999999
        apriori_human_tt = sensor_human_tt
        apriori_human_tf = sensor_human_tf
        fire_tt = 0.999
        fire_tf = 0.999
        map = Grid(0, 0, 200, 200, 10, 10)

        ambient = Ambient(map_size=[map.width, map.height], n_people=20, n_fire=5, distance_danger=2)
        evidences = []


        ##### People
        # print "Persons ", len(ambient.people_points), " points: ", ambient.people_points
        human_sensor = Sensor(ambient, ambient.people_points, tt=sensor_human_tt, ff=sensor_human_tt,
                              std_dev=(0.00000001),
                              true_samples_prop=0.7)

        true_points, false_points = human_sensor.sense(150)
        # print "People detected:", true_points
        # print "No people in:", false_points
        add_evidences(true_points, false_points, PEOPLE_SENSOR, evidences)


        ###### Fire
        # fire_sensor = Sensor(ambient, ambient.fire_points, tt=1, ff=1, std_dev=10.00000001, true_samples_prop=0.5)
        # true_points, false_points = human_sensor.sense(20)
        # add_evidences(true_points, false_points, FIRE_SENSOR, evidences)

        ### PLOT

        #### End plot

        # Run engine
        # Engine
        engine = InferenceEngine(rules.get_rules(apriori_human_tt, apriori_human_tf, fire_tt, fire_tf, map))

        # create bayesian network
        bn, bn_evidences = engine.infer_bn(evidences)

        ### Resultant human grid.
        rhg = [[[] for x in np.arange(map.tx, map.tx + map.width, map.dx)] for y in
               np.arange(map.ty, map.ty + map.height, map.dy)]

        # query_points = []
        for v in bn.V:
            # print v
            var_name = v.split("'")[1]

            if var_name != 'Human':
                continue

            loc = engine.vertex_locations[v]
            j = int((loc[0] - map.tx) / map.dx)
            i = int((loc[1] - map.ty) / map.dy)

            if len(rhg) <= i or i < 0 or len(rhg[0]) <= j or j < 0:
                #print "point out of range ", loc
                continue

            marginal = bn.compute_vertex_marginal(v, bn_evidences)
            rhg[i][j] = marginal['true']
            # query_points.append([loc[0], loc[1], marginal['true']])

        #print "grid=", rhg

        detection_tt = 0
        no_detected = 0
        for pp in ambient.people_points:
            j = int((pp[0] - map.tx) / map.dx)
            i = int((pp[1] - map.ty) / map.dy)

            if len(rhg) <= i or i < 0 or len(rhg[0]) <= j or j < 0:
                #print "point out of range ", loc
                continue

            if rhg[i][j] > 0.95:
                detection_tt += 1
            else:
                no_detected += 1

        human_detection = 0

        for row in rhg:
            for c in row:
                if c > 0.95:
                    human_detection += 1

        print param, "detected=", detection_tt, " no detected=", no_detected, " false positives:", human_detection - detection_tt

        results.append(
            [param, float(detection_tt) / len(ambient.people_points), float(no_detected) / len(ambient.people_points),
             (human_detection - detection_tt)])

# detected, no detected, false positives
# tt, tf, ft
print results

import csv

with open('../data_analysis/results.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(results)