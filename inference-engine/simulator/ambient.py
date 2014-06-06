import numpy as np


class Ambient(object):
    def __init__(self, n_people=10, n_fire=5, distance_danger=2, map_size=[100, 200]):
        self.map_size = map_size
        self.distance_danger = distance_danger
        self.n_fire = n_fire
        self.n_people = n_people

        self.people_points = np.random.rand(n_people, 2)
        self.points_in_map(self.people_points)


        self.fire_points = np.random.rand(n_fire, 2)
        self.points_in_map(self.fire_points)



    def points_in_map(self, people_points):
        """
        Distribute points in map.
        """
        for i, size in enumerate(self.map_size):
            for col in [people_points.T[i]]:
                col *= size

