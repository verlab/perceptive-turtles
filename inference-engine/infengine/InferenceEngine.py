import math

from lib_sallybn.disc_bayes_net.DiscreteBayesianNetworkExt import DiscreteBayesianNetworkExt


class InferenceEngine:
    """
    vertex_locations: locations in map. This is a dictionary with key as vertex name
        and values [x,y]
    """
    vertex_locations = None

    def __init__(self, rules):
        """

        :param rules:  set of rules to infer about a bayesian network.
        """
        self.rules = rules

    def infer_bn(self, evidences):
        """
        :param evidences: evidences to create a bayesian network.
            each evidence is an instance of Evidence.
        """
        # Create an empty BN.
        disc_bn = DiscreteBayesianNetworkExt()
        bn_evidences = {}
        #
        self.vertex_locations = {}

        new_nodes = True

        # Generate inferred variables based on evidence rules
        for i, e in enumerate(evidences):
            # vertex location in map.
            evidence_location = [e.x, e.y]

            ## Create a node for this evidence
            evidence_name = "'" + e.var + "'" + str(evidence_location) + "_" + str(i)
            # states
            disc_bn.add_vertex(evidence_name, e.var_states)

            # evidence
            bn_evidences[evidence_name] = e.evidence_state

            # Save location
            self.vertex_locations[evidence_name] = evidence_location

            # A new node was added to infer
            new_nodes = True

        # Run the rules until
        while new_nodes:
            n_ve = len(disc_bn.V) + len(disc_bn.E)
            # evaluate each evidence rule
            for r in self.rules:
                # number of vertices and edges
                r.generate_inference(disc_bn, evidences, bn_evidences, self.vertex_locations)

            # There is new edges or vertices after applying the rules
            new_n_ve = len(disc_bn.V) + len(disc_bn.E)
            new_nodes = new_n_ve > n_ve

        # return the created bn
        return disc_bn, bn_evidences