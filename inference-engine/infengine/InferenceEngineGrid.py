from infengine.observation import VAR_STATES
from lib_sallybn.disc_bayes_net.DiscreteBayesianNetworkExt import DiscreteBayesianNetworkExt
from evidencegrid.evidencetogrid import evidence_to_grid


class InferenceEngine:
    """
    vertex_locations: locations in map. This is a dictionary with key as vertex name
        and values [x,y]
    """
    vertex_locations = None

    def __init__(self, rules, map_grid):
        """

        :param rules:  set of rules to infer about a bayesian network.
        """
        self.map_grid = map_grid
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
        # for i, e in enumerate(evidences):
        # # vertex location in map.
        # evidence_location = [e.x, e.y]
        #
        # ## Create a node for this evidence
        # evidence_name = "'" + e.var + "'" + str(evidence_location) + "_" + str(i)
        # # states
        # disc_bn.add_vertex(evidence_name, e.var_states)
        #
        # # evidence
        # bn_evidences[evidence_name] = e.evidence_state
        #
        # # Save location
        # self.vertex_locations[evidence_name] = evidence_location
        #
        # # A new node was added to infer
        # new_nodes = True

        # Organize evidences for variables:
        evid_grid = evidence_to_grid(evidences, self.map_grid)

        # For each variable
        for var_name, grid in evid_grid.items():
            # For each cell
            for i, j in zip(grid.n_rows, grid.n_columns):
                true_evidences, false_evidences = grid.get(i, j)
                cell_location = grid.cell_center(i, j)

                #True values
                for te in range(true_evidences):
                    evidence_name = "'" + var_name + "' " + str([i, j]) + "_true_" + str(te)
                    #Add to bn
                    disc_bn.add_vertex(evidence_name, VAR_STATES)

                    # Evidences
                    bn_evidences[evidence_name] = VAR_STATES[1]
                    # Save location
                    self.vertex_locations[evidence_name] = cell_location

                #False values
                for fe in range(false_evidences):
                    evidence_name = "'" + var_name + "' " + str([i, j]) + "_false_" + str(fe)
                    # Add to bn
                    disc_bn.add_vertex(evidence_name, VAR_STATES)

                    #Evidences
                    bn_evidences[evidence_name] = VAR_STATES[0]

                    self.vertex_locations[evidence_name] = cell_location

                # if not evidences
                if true_evidences == 0 and false_evidences == 0:
                    evidence_name = "'" + var_name + "' " + str([i, j]) + "_no_evid"
                    disc_bn.add_vertex(evidence_name, VAR_STATES)


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