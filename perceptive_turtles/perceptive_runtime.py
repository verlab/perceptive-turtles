import site
# add the related projects based on the libs.pth file.
site.addsitedir('.')

import glob
import cv2
from people_detector import Detector

### Constants
# folder with tiff files
TIF_FOLDER = './tif_files/'
ROTATION_ANGLE_PEOPLE = 30

### Detectors
# People detector
people_detector = Detector()


## Read tiff files
tif_files = glob.glob(TIF_FOLDER + "*.tif")

# For each tif file
for tif in tif_files:
    print "processing ", tif

    # Read the file
    frame = cv2.imread(tif)
    cv2.imshow("test", frame)
    cv2.waitKey(0)
    ### Detect people
    # output = people_detector.test_image_rotate(frame, ROTATION_ANGLE_PEOPLE)
    # transform position
    # add evidence

    ### Detect fire
    # transform position
    # add evidence

    ### show results
    # show bayesian network
    # write shapes for results
    # view pie charts

    ## sleep





