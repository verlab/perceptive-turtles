import math
from infengine.rules.Rule import Rule


class QueryRule(Rule):
    """
    This rule make a query to infer about a hidden variable.
    """

    def __init__(self, cause_var, inferred_var, inferred_states, inferred_cprob, query_var, query_states, query_range, query_function):
        """
        Define the essential parameters for this rule.

        :param cause_var: cause variable to TRIGGER (str).
        :param inferred_var: variable to infer (str).
        :param inferred_cprob: conditional probability distribution for inferred_var (dict).
        :param query_var: variable to query before inference (str)
        :param query_range: range or radio that this rule can affect (float).
        :param query_function: Function to fusion multiple nodes (function). It can be:
            [Maximum, Minimum, Mean, or Proportional to distance].
        """
        self.cause_var = cause_var
        self.inferred_var = inferred_var
        self.inferred_states = inferred_states
        self.inferred_cprob = inferred_cprob
        self.query_var = query_var
        self.query_states = query_states
        self.query_range = query_range
        self.query_function = query_function

    def generate_inference(self, disc_bn, evidences, bn_evidences, vertex_locations):
        """

        :param disc_bn:
        :param evidences:
        :param vertex_locations:
        """

        ## TRIGGER if there is a cause variable in this point
        triggers = self._find_triggers(self.cause_var, vertex_locations)

        for cause_var in triggers:
            tx, ty = vertex_locations[cause_var]

            ### query for nodes with name ...
            query_nodes = []
            for vname, loc in vertex_locations.items():
                query_name = "'" + self.query_var + "'"
                ## if vname fill in the query
                if not vname[:len(query_name)] == query_name:
                    continue

                ## if rule the distance
                p1 = vertex_locations[vname]
                dist = math.hypot(p1[0] - tx, p1[1] - ty)

                if dist <= self.query_range:
                    query_nodes.append(vname)

            # TRIGGER If there is not nodes that rule the query.
            # Then rule does not trigger.
            if not query_nodes:
                continue

            ## Create a virtual/query var
            query_loc = [tx, ty]
            query_node_name = "'" + self.query_var + "'q" + str(query_loc)

            ## add to bn
            if not query_node_name in disc_bn.V:
                ## Marginals and joint function
                query_marginals = []
                for qn in query_nodes:
                    mar = disc_bn.compute_vertex_marginal(qn, bn_evidences)
                    query_marginals.append(mar)

                ## APPLY joint function to obtain states and cpt
                query_cprob = self.query_function(self.query_states, query_marginals)

                disc_bn.add_vertex(query_node_name, self.query_states)
                disc_bn.set_cprob(query_node_name, query_cprob)
                vertex_locations[query_node_name] = query_loc

            ## Create inferred var
            inf_var_name = "'" + self.inferred_var + "'" + str(query_loc)

            if not inf_var_name in disc_bn.V:
                disc_bn.add_vertex(inf_var_name, self.inferred_states)

            # Add edges
            if not [query_node_name, inf_var_name] in disc_bn.E:
                disc_bn.add_edge([query_node_name, inf_var_name])
                disc_bn.add_edge([cause_var, inf_var_name])
                #CPT
                disc_bn.set_cprob(inf_var_name, self.inferred_cprob)

    @staticmethod
    def _find_triggers(trig_name, vertex_locations):
        triggers = []
        for vertex_name, loc in vertex_locations.items():
            cause_name = "'" + trig_name + "'"
            ## if vertex_name fill in the trigger variable cause name
            tmp_name = vertex_name[:len(cause_name)]

            if tmp_name == cause_name:
                triggers.append(vertex_name)

        return triggers


