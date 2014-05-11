import math

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
            evidence_name = "'" + e.var + "'" + str(evidence_location) + "_" + str(i)
            # states
            disc_bn.add_vertex(evidence_name, e.var_states)

            # evidence
            bn_evidences[evidence_name] = e.evidence_state

            # Save location
            self.vertex_locations[evidence_name] = evidence_location

            # evaluate each evidence rule
            self._apply_evidence_rules(disc_bn, e, evidence_name)

        # Generate inferred variables based on QUERY rules
        # Apply query rules
        self._apply_query_rules(disc_bn, bn_evidences)

        # return the created bn
        return disc_bn, bn_evidences

    def _apply_evidence_rules(self, disc_bn, evidence, evidence_name):
        for j, erule in enumerate(self.evidence_rules):
            ##### TRIGGER if evidence is equals to effect variable in rule.
            if evidence.var == erule.effect_var:
                # Inferred location
                inferred_loc = [evidence.x, evidence.y]

                ## create a new parent variable
                parent_name = "'" + erule.cause_var + "'" + str(inferred_loc)  #+ "_" + str(i) + "-" + str(j)

                # If parent has not been created.
                if not parent_name in self.vertex_locations:
                    ## add to bn
                    disc_bn.add_vertex(parent_name, erule.cause_states)
                    ## position
                    self.vertex_locations[parent_name] = inferred_loc
                    # CPT
                    disc_bn.set_cprob(parent_name, erule.cause_cprob)

                # edge
                disc_bn.add_edge([parent_name, evidence_name])

                # CPT for child
                disc_bn.set_cprob(evidence_name, erule.effect_cprob)

    def _find_triggers(self, trig_name):
        triggers = []
        for vertex_name, loc in self.vertex_locations.items():
            cause_name = "'" + trig_name + "'"
            ## if vertex_name fill in the trigger variable cause name
            tmp_name = vertex_name[:len(cause_name)]

            if tmp_name == cause_name:
                triggers.append(vertex_name)

        return triggers

    def _apply_query_rules(self, disc_bn, bn_evidences):
        # For each query rule
        for k, qr in enumerate(self.query_rules):
            ## TRIGGER if there is a cause variable in this point
            triggers = self._find_triggers(qr.cause_var)

            for cause_var in triggers:
                tx, ty = self.vertex_locations[cause_var]

                ### query for nodes with name ...
                query_nodes = []
                for vname, loc in self.vertex_locations.items():
                    query_name = "'" + qr.query_var + "'"
                    ## if vname fill in the query
                    if not vname[:len(query_name)] == query_name:
                        continue

                    ## if rule the distance
                    p1 = self.vertex_locations[vname]
                    dist = math.hypot(p1[0] - tx, p1[1] - ty)

                    if dist <= qr.query_range:
                        query_nodes.append(vname)

                # TRIGGER If there is not nodes that rule the query.
                # Then rule does not trigger.
                if not query_nodes:
                    continue

                ## Create a virtual/query var
                query_loc = [tx, ty]
                query_node_name = "'" + qr.query_var + "'q" + str(query_loc)
                self.vertex_locations[query_node_name] = query_loc

                ## Marginals and joint function
                query_marginals = []
                for qn in query_nodes:
                    mar = disc_bn.compute_vertex_marginal(qn, bn_evidences)
                    query_marginals.append(mar)

                ## APPLY joint function to obtain states and cpt
                query_cprob = qr.query_function(qr.query_states, query_marginals)

                ## add to bn
                disc_bn.add_vertex(query_node_name, qr.query_states)
                disc_bn.set_cprob(query_node_name, query_cprob)

                ## Create inferred var
                inf_var_name = "'" + qr.inferred_var + "'" + str(query_loc)
                disc_bn.add_vertex(inf_var_name, qr.inferred_states)

                # Add edges
                disc_bn.add_edge([query_node_name, inf_var_name])
                disc_bn.add_edge([cause_var, inf_var_name])
                #CPT
                disc_bn.set_cprob(inf_var_name, qr.inferred_cprob)