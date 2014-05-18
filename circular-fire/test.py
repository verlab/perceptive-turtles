import cv2

from fire_detector import CircleFireDetector
from os import walk
import json

def run():
    detector = CircleFireDetector()

    results = {}

    output = json.dumps(results)
    output_file = open("output.json", "w")
    output_file.write(output)

    for (dirpath, dirnames, filenames) in walk("./imgs"):
        for img_name in filenames:

            img = cv2.imread("./imgs/%s" % img_name, 1)

            rows, cols = img.shape[0], img.shape[1]

            rows = rows / 2
            cols = cols / 3

            img[ rows:rows+1, 0:img.shape[1] ] = 0
            img[ 0:img.shape[0], cols:cols+1 ] = 0
            img[ 0:img.shape[0], cols*2:cols*2+1 ] = 0

            found_list = detector.test_image(img)

            for point in found_list:
                cv2.circle(img, (point[0], point[1]), 30, (0, 255, 0), 2)

            print found_list

            cv2.imshow("image", img)
            cv2.waitKey(10)

            true_true = raw_input("true_true ? ")
            true_false = raw_input("true_false ? ")
            false_true = raw_input("false_true ? ")
            false_false = raw_input("false_false ? ")

            results[img_name] = {
                "true_true" : true_true,
                "true_false" : true_false,
                "false_true" : false_true,
                "false_false" : false_false
            }

            output_file = open("output.json", "w")
            output = json.dumps(results)
            output_file.write(output)
            output_file.close()

if __name__ == "__main__":
    run()
