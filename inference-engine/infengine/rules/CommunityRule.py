import math

from infengine.rules.Rule import Rule


class CommunityRule(Rule):
    """
    Rule to create nodes that represents communities or a set of nodes, based on a query variable.
    It eliminates subsets (communities inside other communities) and duplicated communities.
    """

    def __init__(self, query_var, effect_var, query_states, max_distance, joint_function):
        self.query_states = query_states
        self.effect_var = effect_var
        self.query_var = query_var
        self.max_distance = max_distance
        self.joint_function = joint_function

    def generate_inference(self, disc_bn, evidences, bn_evidences, vertex_locations):
        """

        :param disc_bn:
        :param evidences:
        :param bn_evidences:
        :param vertex_locations:
        """
        # Nodes that are in query
        query_nodes = []
        # Interested query variables
        for vname in disc_bn.V:
            query_name = "'" + self.query_var + "'"
            ## if vname fill in the query
            if vname[:len(query_name)] == query_name:
                query_nodes.append(vname)

        # For each query node, find the nearest neighbours to create a community
        communities = []
        for qn in query_nodes:
            neighbours = []
            for other_node in query_nodes:
                p1 = vertex_locations[other_node]
                p2 = vertex_locations[qn]
                dist = math.hypot(p1[0] - p2[0], p1[1] - p2[1])

                if dist <= self.max_distance:
                    neighbours.append(other_node)

            communities.append(sorted(neighbours))

        #### Eliminate subsets O(n**2)
        for c1 in communities:
            for c2 in communities:
                if c1 == c2:
                    continue

                if set(c1).issubset(set(c2)):
                    communities.remove(c1)

        ##### Eliminate duplicated elements
        communities_dict = {str(c): c for c in communities}
        communities = communities_dict.values()

        ##### create a node for each community
        for neighbours in communities:
            # compute position
            com_loc = [0, 0]
            for n in neighbours:
                nloc = vertex_locations[n]
                com_loc[0] += nloc[0]
                com_loc[1] += nloc[1]

            # mean
            com_loc[0] /= len(neighbours) * 1.0
            com_loc[1] /= len(neighbours) * 1.0

            # create a node
            query_loc = com_loc
            query_node_name = "'" + self.effect_var + "'" + str(com_loc)

            ## add to bn
            if not query_node_name in disc_bn.V:
                ## Marginals and joint function
                query_marginals = []
                for qn in neighbours:
                    mar = disc_bn.compute_vertex_marginal(qn, bn_evidences)
                    query_marginals.append(mar)

                ## APPLY joint function to obtain states and cpt
                query_cprob = self.joint_function(self.query_states, query_marginals)

                disc_bn.add_vertex(query_node_name, self.query_states)
                disc_bn.set_cprob(query_node_name, query_cprob)
                vertex_locations[query_node_name] = query_loc
