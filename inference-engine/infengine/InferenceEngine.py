from lib_sallybn.disc_bayes_net.DiscreteBayesianNetworkExt import DiscreteBayesianNetworkExt


class InferenceEngine:
    """
    evidences: evidences to create a bayesian network.
        each evidence is an instance of Evidence.
    """
    evidences = []

    """
    vertex_locations: locations in map. This is a dictionary with key as vertex name
        and values [x,y]
    """
    vertex_locations = {}

    def __init__(self, evidence_rules, query_rules):
        """

        :param evidence_rules:  set of rules to infer about a bayesian network.
        :param query_rules: set of rules to query before infer.
        """
        self.evidence_rules = evidence_rules
        self.query_rules = query_rules


    def create_bn(self):
        # Create an empty BN.
        disc_bn = DiscreteBayesianNetworkExt()
        bn_evidences = {}


        # Generate inferred variables based on evidence rules
        for i, e in enumerate(self.evidences):
            ## Create a node for this evidence
            evidence_name = e.var + str(i)
            # states
            disc_bn.add_vertex(evidence_name, e.var_states)

            # evidence
            bn_evidences[evidence_name] = e.evidence_state

            # vertex location in map.
            self.vertex_locations[evidence_name] = [e.x, e.y]

            # evaluate each evidence rule
            for j, erule in enumerate(self.evidence_rules):
                ##### TRIGGER if evidence is equals to effect variable in rule.
                if e.var == erule.effect_var:
                    #TODO if parent exist in this location, use it, else create a new one.
                    #TODO radio to find

                    ## create a new parent variable
                    parent_name = erule.cause_var + str(i) + "-" + str(j)

                    ## add to bn
                    disc_bn.add_vertex(parent_name, erule.cause_var)
                    ## position
                    self.vertex_locations[parent_name] = [e.x, e.y]

                    # edge
                    disc_bn.add_edge(parent_name, evidence_name)

                    # cpts
                    disc_bn.set_cprob(evidence_name, erule.effect_cprob)
                    disc_bn.set_cprob(parent_name, erule.cause_cprob)



        # TODO Apply query rules


        # TODO validate bn

        # return the created bn
        return disc_bn, bn_evidences


