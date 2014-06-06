import numpy as np
import math

import cv2


background = None
size = 50
opacity = 0.3
manager = None


class ClusterManager(object):
    def __init__(self, min_distance=50):
        self.types = {}
        self.min_distance = min_distance
        self.clusters = []

    def add_point(self, point, point_type):
        if point_type not in self.types:
            self.types[point_type] = []

        self.types[point_type].append(np.array(point))
        self.group_points()

    def group_points(self):
        self.clusters = {}

        for key in self.types:
            self.clusters[key] = []

            # Create cluster based on each point and its neighborhood
            for id_src, point_src in enumerate(self.types[key]):
                point_list = []
                point_list.append(id_src)

                for id_tgt, point_target in enumerate(self.types[key]):
                    if np.array_equal(point_src, point_target):
                        continue

                    if np.linalg.norm(point_src - point_target) <= self.min_distance:
                        point_list.append(id_tgt)

                if len(point_list) > 1:
                    if ( sorted(point_list) not in self.clusters[key] ):
                        # print "point_list: ", point_list
                        self.clusters[key].append(point_list)

            # For each create cluster, merge then if have >=50% equal to another
            def merge_clusters(c0, c1):
                c_out = []
                c_out_aux = []
                for i in c0:
                    for j in c1:
                        if i == j:
                            c_out.append(i)
                        else:
                            if i not in c_out_aux:
                                c_out_aux.append(i)
                            if j not in c_out_aux:
                                c_out_aux.append(j)

                size = min(len(c0), len(c1))
                if len(c_out) >= size / 2:
                    return c_out_aux
                return False

            while True:
                merge = False

                for id_src, cluster_src in enumerate(self.clusters[key]):
                    for id_tgt, cluster_target in enumerate(self.clusters[key]):
                        if id_src == id_tgt:
                            continue

                        result = merge_clusters(cluster_src, cluster_target)

                        if result:
                            self.clusters[key].pop(id_src)
                            self.clusters[key].pop(id_tgt - 1)
                            self.clusters[key].append(result)
                            merge = True
                            break

                    if merge:
                        break

                if not merge:
                    break

        for key in self.clusters:
            print key, ":", len(self.clusters[key])
        print "--------------------------------------"


def mouseCallback(event, x, y, flags, param):
    global background
    global manager

    overlay = background.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(overlay, (x, y), size, (0, 0, 255), -1)
        cv2.addWeighted(overlay, opacity, background, 1 - opacity, 0, background)

        manager.add_point(np.array((x, y)), 1)
        draw_line()

    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(overlay, (x, y), size, (255, 0, 0), -1)
        cv2.addWeighted(overlay, opacity, background, 1 - opacity, 0, background)

        manager.add_point(np.array((x, y)), 2)
        draw_line()


def draw_line():
    global background
    global manager

    for key in manager.clusters:
        for cluster in manager.clusters[key]:

            last_point = cluster.pop()
            while len(cluster):
                point = cluster.pop()
                cv2.line(background, tuple(manager.types[key][last_point]), tuple(manager.types[key][point]),
                         (255, 255, 255), 1)
                last_point = point


def run():
    global background
    global manager

    manager = ClusterManager()
    background = np.zeros(shape=(600, 600, 3), dtype=np.uint8)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouseCallback)

    while True:

        cv2.imshow("image", background)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
