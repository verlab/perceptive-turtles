import cv2

from people_detector import PeopleDetector


def run():
    detector = PeopleDetector()

    frame = cv2.imread("photo_0.png")

    output = detector.test_image_rotate_list(frame)

    # print detector.has_person( frame )

    for idx, image in enumerate(output):
        cv2.imshow("test", image)
        cv2.waitKey(0)


if __name__ == "__main__":
    run()
