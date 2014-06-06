from infengine.Evidence import Evidence
from simulator.ambient import Ambient
from simulator.sensor import Sensor

FIRE_SENSOR = "Fire_Sensor"
BOOLEAN_STATES = ["true", "false"]
PEOPLE_SENSOR = "Human_Sensor"

ambient = Ambient(map_size=[100, 200], n_people=10, n_fire=5, distance_danger=2)
evidences = []

def add_evidences(true_points,false_points, sensor):
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
human_sensor = Sensor(ambient, ambient.people_points, tt=1, ff=1, std_dev=1.00000001, true_samples_prop=0.5)

true_points, false_points = human_sensor.sense(20)
print "People detected:", true_points
print "No people in:", false_points
add_evidences(true_points, false_points, PEOPLE_SENSOR)


###### Fire
# fire_sensor = Sensor(ambient, ambient.fire_points, tt=1, ff=1, std_dev=10.00000001, true_samples_prop=0.5)
# true_points, false_points = human_sensor.sense(20)
# add_evidences(true_points, false_points, FIRE_SENSOR)

### PLOT

## Run engine



