import people_detector
import cv2
import numpy as np

def run():
	detector = people_detector.Detector()

	frame = cv2.imread("photo_1.png")

	output = detector.test_image_rotate( frame, 30 )

	for idx, image in enumerate(output):
		cv2.imshow("test", image)
		cv2.waitKey(0)

if __name__ == "__main__":
	run()