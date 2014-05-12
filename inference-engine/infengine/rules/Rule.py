from abc import abstractmethod


class Rule(object):
    """
    An abstract rule.
    """

    def __init__(self):
        pass

    @abstractmethod
    def generate_inference(self, disc_bn, evidences, bn_evidences, vertex_locations):
        """

        :param disc_bn: Discrete Bayesian Network to be extended based on this rule.
        :param evidences: evidences to extend the BN.
        :param vertex_locations: location for each node.
        :return new_nodes True if a new node or edge was created after applying the rule.
        """
        pass