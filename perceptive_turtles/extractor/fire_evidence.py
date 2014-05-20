from fire_detector import CircleFireDetector
from infengine.Evidence import Evidence

FIRE_SENSOR = "Fire_Sensor"
BOOLEAN_STATES = ["true", "false"]

class FireEvidence:
    def __init__(self):
        self.detector = CircleFireDetector()

    def get_evidences(self, frame):
        fire_points = self.detector.test_image(frame)

        evidences = []

        # True evidences
        for pp in fire_points:
            # create evidence
            ev = Evidence(pp[0], pp[1], FIRE_SENSOR, BOOLEAN_STATES, BOOLEAN_STATES[0])

            # add evidence
            evidences.append(ev)

        # False evidence
        if not fire_points:
            rows, cols = frame.shape[0], frame.shape[1]
            ev = Evidence(cols / 2.0, rows / 2.0, FIRE_SENSOR, BOOLEAN_STATES, BOOLEAN_STATES[1])
            evidences.append(ev)

        return evidences