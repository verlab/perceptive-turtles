import site
import pickle

site.addsitedir('.')
import glob

import cv2

# add the related projects based on the libs.pth file.
import geotransformer
from infengine.InferenceEngine import InferenceEngine
from extractor.people_evidence import PeopleEvidence
from extractor.fire_evidence import FireEvidence
import rules

# #
import logging

logging.basicConfig(level=logging.DEBUG)

### Constants
# folder with tiff files
TIF_FOLDER = './tif_files/'
ROTATION_ANGLE_PEOPLE = 30
# Variables names

BOOLEAN_STATES = ["true", "false"]

debug = False

## Engine
engine = InferenceEngine(rules.get_rules())

## Read tiff files
tif_files = glob.glob(TIF_FOLDER + "*.tif")
tif_files.sort()

evidences = []

# For each tif file
for tif in tif_files[:]:
    ### Detectors
    people = PeopleEvidence()
    fire = FireEvidence()

    print "processing ", tif
    # Read the file
    frame = cv2.imread(tif)

    ### Detect people
    people_evidence = people.get_evidence(frame)
    # people_evidences=[]
    ### Detect fire
    # fire_evidences = fire.get_evidences(frame)
    fire_evidences = None
    new_evidences = [people_evidence, fire_evidences]

    if debug:
        # for e in new_evidences:
        #     print [e.x, e.y], "var=", e.var, " ste=", e.evidence_state
        # for e in fire_evidences:
        #     color = (0, 0, 255)
        #     if e.evidence_state == 'false':
        #         color = (100, 100, 100)
        #     cv2.circle(frame, (int(e.x), int(e.y)), 30, color, 2)
        # for e in people_evidences:
        #     color = (0, 255, 0)
        #     if e.evidence_state == 'false':
        #         color = (0, 10, 0)
        #     cv2.circle(frame, (int(e.x), int(e.y)), 10, color, 4)
        #TODO draw squares
        cv2.imshow(tif, frame)
        cv2.waitKey(0)

    # transform to geo-transform
    for e in new_evidences:
        # None val
        if not e:
            continue
        # Transform detections.
        for p in e.detections.values():
            for p1 in p:
                geotransformer.geo_transform(p1, tif)

        # Transform boundaries
        geotransformer.geo_transform(e.boundary, tif)

    evidences += new_evidences

with open('evidences.pkl', 'wb') as output:
    pickle.dump(evidences, output, pickle.HIGHEST_PROTOCOL)





