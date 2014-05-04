import unittest

from infengine.InferenceEngine import InferenceEngine
from infengine.rules.EvidenceRule import EvidenceRule
from infengine.rules.QueryRule import QueryRule
from infengine.Evidence import Evidence
from infengine import joint_functions

fire_sensor_cprob = {
    "['true']": [.7, .3],
    "['false']": [.1, 0.9],
}
human_sensor_cprob = {
    "['true']": [.7, .3],
    "['false']": [.4, 0.6],
}
fire_cprob = [0.05, 0.95]
human_cprob = [0.2, 0.8]


class TestEngine(unittest.TestCase):
    def setUp(self):
        pass

    def rrrtest_evidence_rule(self):
        # Evidence Rules
        erules = []
        er = EvidenceRule("Fire", "Fire_Sensor", ["true", "false"],
                          ["true", "false"], fire_cprob, fire_sensor_cprob)
        erules.append(er)

        # Query Rules

        # Create engine
        engine = InferenceEngine(erules, [])

        # Evidence
        e1 = Evidence(10, 30, "Fire_Sensor", ["true", "false"], "true")

        # run inference engine
        bn, bn_evidences = engine.infer_bn([e1])

        # Validate result
        self.assertEqual(len(bn.V), 2)

        # Another evidence
        e2 = Evidence(50, 30, "Fire_Sensor", ["true", "false"], "true")
        # run inference engine
        bn, bn_evidences = engine.infer_bn([e1, e2])

        # Validate result
        self.assertEqual(len(bn.V), 4)

        # Another evidence in the same location of e1
        e3 = Evidence(10, 30, "Fire_Sensor", ["true", "false"], "true")
        # run inference engine
        bn, bn_evidences = engine.infer_bn([e1, e2, e3])
        # Validate result
        self.assertEqual(len(bn.V), 5, "Error for evidence in the same location")
        self.assertEqual(len(bn.E), 3, "Error for evidence in the same location")


    def test_query_rule(self):
        # Evidence Rules
        fire_er = EvidenceRule("Fire", "Fire_Sensor", ["true", "false"],
                               ["true", "false"], fire_cprob, fire_sensor_cprob)
        human_er = EvidenceRule("Human", "Human_Sensor", ["true", "false"],
                                ["true", "false"], human_cprob, human_sensor_cprob)

        # Query Rules
        qr = QueryRule('Human', 'Human in Danger', ["true", "false"], human_cprob, "Fire", ["true", "false"], 10, joint_functions.mean)

        # Create engine
        engine = InferenceEngine([fire_er, human_er], [qr])


        ##### EVIDENCE
        e1 = Evidence(10, 30, "Fire_Sensor", ["true", "false"], "true")
        e2 = Evidence(10, 30, "Human_Sensor", ["true", "false"], "true")

        # bn, bn_evidences = engine.infer_bn([e1, e2])
        #
        # # Validate result
        # self.assertEqual(len(bn.V), 6, "number of vertices in query rule")
        # self.assertEqual(len(bn.E), 4, "number of edges for query rule")

        e3 = Evidence(12, 30, "Fire_Sensor", ["true", "false"], "true")
        bn, bn_evidences = engine.infer_bn([e1, e2, e3])

        # Validate result
        self.assertEqual(len(bn.V), 8, "number of vertices in query rule")
        self.assertEqual(len(bn.E), 5, "number of edges for query rule")

        print "V: ", bn.V
        print "E: ", bn.E
        print "Evidences: ", bn_evidences
        print "Vertex loc", engine.vertex_locations

        # e3 = Evidence(12, 30, "Fire_Sensor", ["true", "false"], "true")
        # bn, bn_evidences = engine.infer_bn([e1, e2, e3,e1])
        #
        # # Validate result
        # self.assertEqual(len(bn.V), 9, "number of vertices in query rule")
        # self.assertEqual(len(bn.E), 4, "number of edges for query rule")

if __name__ == '__main__':
    unittest.main()