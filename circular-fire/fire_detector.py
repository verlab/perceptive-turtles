import numpy as np

import cv2

class CircleFireDetector(object):
    """
    Detect circular paper simulating fire.
    """
    LOWER_BOUND = np.array([142, 52, 147])
    UPPER_BOUND = np.array([185, 255, 255])

    def __init__(self):
        pass

    def test_image(self, img):
        """

        :param img:
        :return:
        """
        source = img
        source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
        source_blur = cv2.medianBlur(source_gray, 7)
        source_hsv = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)

        hg = 3  #cv2.HOUGH_GRADIENT || cv2.cv.CV_HOUGH_GRADIENT
        circles = cv2.HoughCircles(source_blur, hg, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=50)



        found_list = []

        if circles is not None:
            circles = np.uint16(np.around(circles))
            circles = circles[0]
            roi_list = []

            for mark in circles:
                x1 = mark[1] - (mark[2] * np.sqrt(2) / 2)
                y1 = mark[0] - (mark[2] * np.sqrt(2) / 2)
                size = (mark[2] * np.sqrt(2) / 2 * 2)

                roi = np.array(source_hsv[x1:x1 + size, y1:y1 + size])
                roi_list.append((roi, (mark[0], mark[1])))

            for roi, position in roi_list:
                if not (roi.shape[0] and roi.shape[1]):
                    continue

                mask = cv2.inRange(roi, self.LOWER_BOUND, self.UPPER_BOUND)
                avg = np.average(mask)

                if avg > (255 * 0.8):
                    found_list.append(position)

        return found_list
