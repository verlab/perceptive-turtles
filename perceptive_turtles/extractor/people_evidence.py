from infengine.Evidence import Evidence
from people_detector import PeopleDetector


PEOPLE_SENSOR = "Human_Sensor"
BOOLEAN_STATES = ["true", "false"]


class PeopleEvidence:
    def __init__(self):
        # People detector
        self.people_detector = PeopleDetector()


    def get_evidences(self, frame):
        people_points = self.people_detector.detect(frame, degree=30)

        evidences = []
        # True evidences
        for pp in people_points:
            # create evidence
            ev = Evidence(pp[0], pp[1], PEOPLE_SENSOR, BOOLEAN_STATES, BOOLEAN_STATES[0])

            # add evidence
            evidences.append(ev)

        # False evidence
        if not people_points:
            rows, cols = frame.shape[0], frame.shape[1]
            ev = Evidence(cols / 2.0, rows / 2.0, PEOPLE_SENSOR, BOOLEAN_STATES, BOOLEAN_STATES[1])
            evidences.append(ev)

        return evidences