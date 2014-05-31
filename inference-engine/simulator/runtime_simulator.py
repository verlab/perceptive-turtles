
from simulator.ambient import Ambient
from simulator.sensor import Sensor

ambient = Ambient(map_size=[100, 200])

print ambient.people_points
human_sensor = Sensor(ambient, ambient.people_points, samples=2, variance=1)

print human_sensor.sense()


