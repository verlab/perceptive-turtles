import cv2

from people_detector import PeopleDetector


def run():
    detector = PeopleDetector()

    frame = cv2.imread("44.png")

    detected_points = detector.detect(frame, debug=True)

    # Extend to rectangle
    for p in detected_points:
        p.append(10)
        p.append(10)

    PeopleDetector.draw_detections(frame, detected_points, 3)
    cv2.imshow("test", frame)
    cv2.waitKey(0)


if __name__ == "__main__":
    run()

