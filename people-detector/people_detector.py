import numpy as np

import cv2


class PeopleDetector(object):
    """
    Detector for people.
    """
    IMAGE_OUTPUT = 1
    BOOLEAN_OUTPUT = 2
    DEFAULT_DEGREE = 30

    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def inside(self, r, q):
        rx, ry, rw, rh = r
        qx, qy, qw, qh = q
        return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

    def draw_detections(self, img, rects, thickness=1):
        for x, y, w, h in rects:
            pad_w, pad_h = int(0.15 * w), int(0.05 * h)
            cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)

    def quadfy_image(self, img):
        rows, cols = img.shape[0], img.shape[1]

        if rows % 2 != 0:
            img = np.delete(img, img.shape[0] - 1, 0)
        if cols % 2 != 0:
            img = np.delete(img, img.shape[1] - 1, 1)

        rows, cols = img.shape[0], img.shape[1]
        quad_dim = max(rows, cols)

        quad = np.zeros(shape=( quad_dim, quad_dim, 3 ), dtype=img.dtype)

        quad[((quad_dim / 2) - rows / 2):((quad_dim / 2) + rows / 2),
        ((quad_dim / 2) - cols / 2):((quad_dim / 2) + cols / 2)] = img

        return quad

    def rotate_image(self, img, degree=DEFAULT_DEGREE):
        source_image = self.quadfy_image(img)

        image_list = [source_image]
        rows, cols = source_image.shape[0], source_image.shape[1]

        for rotate_degree in xrange(degree, 359, degree):
            rotate_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotate_degree, 1)
            dst = cv2.warpAffine(source_image, rotate_matrix, (cols, rows))

            image_list.append(dst)

        return image_list

    def test_image_rotate_list(self, img, degree=DEFAULT_DEGREE):

        image_list = self.rotate_image(img, degree)

        image_list_out = []
        for idx, image in enumerate(image_list):
            image_list_out.append(self.test_image(image))

        return image_list_out

    def test_image(self, img, output=IMAGE_OUTPUT):

        found, w = self.hog.detectMultiScale(img, winStride=(8, 8), padding=(32, 32), scale=1.05)
        self.draw_detections(img, found, 2)

        if output == self.IMAGE_OUTPUT:
            return img
        elif output == self.BOOLEAN_OUTPUT:
            return np.array(found).any()

    def has_person(self, img, degree=DEFAULT_DEGREE):
        image_list = self.rotate_image(img, degree)

        for idx, image in enumerate(image_list):
            if self.test_image(image, self.BOOLEAN_OUTPUT):
                return True

        return False
