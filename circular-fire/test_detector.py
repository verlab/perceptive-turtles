import cv2

from fire_detector import CircleFireDetector

def run():
    detector = CircleFireDetector()

    img = cv2.imread("stuff.jpg")

    found_list = detector.test_image(img)

    for point in found_list:
        cv2.circle(img, (point[0], point[1]), 30, (0, 255, 0), 2)

    print found_list

    cv2.imshow("image", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    run()
