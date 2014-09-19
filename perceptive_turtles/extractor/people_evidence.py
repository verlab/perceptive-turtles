from infengine.Evidence import Evidence
from people_detector import PeopleDetector


PEOPLE_SENSOR = "Human_Sensor"
BOOLEAN_STATES = ["false", "true"]


class PeopleEvidence:
    def __init__(self):
        # People detector
        self.people_detector = PeopleDetector()


    def get_evidence(self, frame):
        people_squares = self.people_detector.detect(frame, degree=30)

        rows, cols = frame.shape[0], frame.shape[1]
        boundary = [[0, 0], [rows, 0], [rows, cols], [0, rows]]

        evidence = Evidence(boundary, PEOPLE_SENSOR, BOOLEAN_STATES, BOOLEAN_STATES[0])


        # Square to evidence
        for square in people_squares:
            evidence.add_detection(BOOLEAN_STATES[1], square)

        return evidence