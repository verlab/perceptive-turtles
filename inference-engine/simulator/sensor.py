import numpy as np


class Sensor(object):
    def __init__(self, ambient, real_points, tt=1, ff=1, std_dev=0.00000001, true_samples_prop=0.5):
        self.ambient = ambient
        self.true_samples_prop = true_samples_prop
        self.std_dev = std_dev
        self.ff = ff
        self.tt = tt
        self.real_points = real_points


    # noinspection PyNoneFunctionAssignment
    def sense(self, samples=10):
        true_samples = int(samples * self.true_samples_prop)
        false_samples = samples - true_samples

        # True positives
        n_tt = int(self.tt * true_samples)
        # False positives
        n_ft = true_samples - n_tt
        # True negatives
        n_tn = int(self.ff * false_samples)
        # False negatives
        n_fn = false_samples - n_tn


        ## generate all the true positives
        true_positive_points = self.real_points[np.random.randint(0, self.real_points.shape[0], n_tt)]
        # move proportional
        true_positive_points = np.random.normal(true_positive_points, self.std_dev, true_positive_points.shape)


        ## generate the false positives. points in the map
        false_positive_points = np.random.rand(n_ft, 2)
        # distribute random points in map
        self.ambient.points_in_map(false_positive_points)


        ## generate all the false negatives
        false_negative_points = self.real_points[np.random.randint(0, self.real_points.shape[0], n_fn)]
        # move proportional
        false_negative_points = np.random.normal(false_negative_points, self.std_dev, false_negative_points.shape)
        # true negatives
        true_negative_points = np.random.rand(n_tn, 2)
        # distribute random points in map
        self.ambient.points_in_map(true_negative_points)


        ## mix the points
        true_points = np.vstack((true_positive_points, false_positive_points))
        false_points = np.vstack((true_negative_points, false_negative_points))

        return true_points, false_points