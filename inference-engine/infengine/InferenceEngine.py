from lib_sallybn.disc_bayes_net.DiscreteBayesianNetworkExt import DiscreteBayesianNetworkExt


class InferenceEngine:
    """
    vertex_locations: locations in map. This is a dictionary with key as vertex name
        and values [x,y]
    """
    vertex_locations = None

    def __init__(self, evidence_rules, query_rules):
        """

        :param evidence_rules:  set of rules to infer about a bayesian network.
        :param query_rules: set of rules to query before infer.
        """
        self.evidence_rules = evidence_rules
        self.query_rules = query_rules

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

        # Generate inferred variables based on evidence rules
        for i, e in enumerate(evidences):
            # vertex location in map.
            evidence_location = [e.x, e.y]

            ## Create a node for this evidence
            evidence_name = e.var + str(evidence_location) + "_" + str(i)
            # states
            disc_bn.add_vertex(evidence_name, e.var_states)

            # evidence
            bn_evidences[evidence_name] = e.evidence_state

            # Save location
            self.vertex_locations[evidence_name] = evidence_location

            # evaluate each evidence rule
            for j, erule in enumerate(self.evidence_rules):
                ##### TRIGGER if evidence is equals to effect variable in rule.
                if e.var == erule.effect_var:
                    # Inferred location
                    inferred_loc = [e.x, e.y]

                    ## create a new parent variable
                    parent_name = erule.cause_var + str(inferred_loc)  #+ "_" + str(i) + "-" + str(j)

                    # If parent has not been created.
                    if not parent_name in self.vertex_locations:
                        ## add to bn
                        disc_bn.add_vertex(parent_name, erule.cause_var)
                        ## position
                        self.vertex_locations[parent_name] = inferred_loc
                        # CPT
                        disc_bn.set_cprob(parent_name, erule.cause_cprob)

                    # edge
                    disc_bn.add_edge([parent_name, evidence_name])

                    # CPT for child
                    disc_bn.set_cprob(evidence_name, erule.effect_cprob)


        # TODO Apply query rules

        # TODO validate bn

        # return the created bn
        return disc_bn, bn_evidences


