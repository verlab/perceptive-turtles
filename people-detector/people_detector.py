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

    @staticmethod
    def draw_detections(img, rects, thickness=1):
        for x, y, w, h in rects:
            pad_w, pad_h = int(0.15 * w), int(0.05 * h)
            x = int(x)
            y = int(y)
            cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)

    @staticmethod
    def quadfy_image(img):
        """
        Put  a rotated image in a bigger frame.
        :param img:
        :return:
        """
        rows, cols = img.shape[0], img.shape[1]

        # It it can be divided by 2, eliminate the last column or row
        if rows % 2 != 0:
            img = np.delete(img, img.shape[0] - 1, 0)
        if cols % 2 != 0:
            img = np.delete(img, img.shape[1] - 1, 1)

        # New size
        rows, cols = img.shape[0], img.shape[1]

        # Create the new big frame
        quad_dim = max(rows, cols)
        quad = np.zeros(shape=(quad_dim, quad_dim, 3), dtype=img.dtype)

        quad[((quad_dim / 2) - rows / 2):((quad_dim / 2) + rows / 2),
        ((quad_dim / 2) - cols / 2):((quad_dim / 2) + cols / 2)] = img

        return quad

    def rotate_image(self, img, degree=DEFAULT_DEGREE):
        """
        Put the image in a bigger frame and rotate it
        :param img: image to rotate
        :param degree: delta angle for rotations
        :return: rotated list of tuples of images in a bigger box along with the angle.
        """
        # Put the image in a new bigger frame
        source_image = self.quadfy_image(img)

        image_list = []
        rows, cols = source_image.shape[0], source_image.shape[1]

        for rotate_degree in xrange(0, 359, degree):
            # Rotation matrix
            rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotate_degree, 1)
            # Rotate the image
            dst = cv2.warpAffine(source_image, rotation_matrix, (cols, rows))

            image_list.append((dst, rotation_matrix))

        return image_list


    def detect(self, img, degree=DEFAULT_DEGREE, debug=False, min_size=150):
        """
        Detect people in the image.
        :param debug: show each rotated image and press to continue
        :param img: source image
        :param degree: delta angle for rotations.
        :param min_size: minimum height in pixels for a person
        """
        # Rotate image
        image_list = self.rotate_image(img, degree)

        detected_pols = []
        # For each rotated image
        for image, rotation_matrix in image_list:
            # Run HOG
            detected_rectangles, w = self.hog.detectMultiScale(image,
                                                               winStride=(8, 8), padding=(32, 32), scale=1.05)

            if debug:
                self.draw_detections(image, detected_rectangles)
                cv2.imshow("test", image)
                cv2.waitKey(0)

            # Inverted matrix
            inv_mat = cv2.invertAffineTransform(rotation_matrix)

            # For each detected person
            for x, y, w, h in detected_rectangles:

                # WARNING: size of the person is known a priori
                if w < min_size:
                    continue

                # transform
                # transformed_point
                p1 = inv_mat.dot(np.array([x, y, 1])).tolist()
                p2 = inv_mat.dot(np.array([x + w, y, 1])).tolist()
                p3 = inv_mat.dot(np.array([x + w, y + h, 1])).tolist()
                p4 = inv_mat.dot(np.array([x, y + h, 1])).tolist()

                polygon = [p1, p2, p3, p4]

                # Add to the list
                detected_pols.append(polygon)

        return detected_pols