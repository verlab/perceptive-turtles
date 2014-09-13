from infengine.Evidence import Evidence
from people_detector import PeopleDetector


PEOPLE_SENSOR = "Human_Sensor"
BOOLEAN_STATES = ["true", "false"]


class PeopleEvidence:
    def __init__(self):
        # People detector
        self.people_detector = PeopleDetector()


    def get_evidences(self, frame):
        people_squares = self.people_detector.detect(frame, degree=30)

        evidences = []
        # Square to evidence
        true_evidences = [Evidence(square, PEOPLE_SENSOR, BOOLEAN_STATES, BOOLEAN_STATES[0])
                          for square in people_squares]


        # TODO false evidence for area of the image without true_evidence polygon.
        # False evidence when no detections
        if not people_squares:
            rows, cols = frame.shape[0], frame.shape[1]

            pol = [[0, 0], [rows, 0], [rows, cols], [0, rows]]
            ev = Evidence(pol, PEOPLE_SENSOR, BOOLEAN_STATES, BOOLEAN_STATES[1])
            evidences.append(ev)

        return true_evidences + evidences