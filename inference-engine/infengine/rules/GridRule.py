from infengine.rules.Rule import Rule


class Grid(object):
    """
    Map grid representation
    """

    def __init__(self, tx, ty, dx, dy, width, height):
        """
        :param tx: translation in x.
        :param ty: translation in y
        :param dx: delta x - cell width.
        :param dy: delta y - cell height.
        """

        self.height = height
        self.width = width
        self.dy = dy
        self.dx = dx
        self.ty = ty
        self.tx = tx


class GridRule(Rule):
    """
    This type or rule creates a grid and group by the center of the cell.
    """

    def __init__(self, cause_var, effect_var, cause_states, effect_states, cause_cprob, effect_cprob, grid):
        """
        Construct.
        :param cause_var: cause variable or parent (str)
        :param effect_var: effect variable (str) ----> TRIGGER.
        :param cause_states: possible states of the cause variable (str[])
        :param effect_states:  possible states of the effect variable (str[])
        :param cause_cprob: Conditional Probability Table for the cause
        :param effect_cprob: Conditional Probability Table for the effect
        :param grid:  grid representation
        """

        self.cause_var = cause_var
        self.effect_var = effect_var
        self.cause_states = cause_states
        self.effect_states = effect_states
        self.cause_cprob = cause_cprob
        self.effect_cprob = effect_cprob
        self.grid = grid

    def generate_inference(self, disc_bn, evidences, bn_evidences, vertex_locations):
        """

        :param disc_bn:
        :param evidences:
        :param bn_evidences:
        :param vertex_locations:
        """
        g = self.grid

        # Nodes that are in query
        query_nodes = []
        # Interested query variables
        for vname in disc_bn.V:
            query_name = "'" + self.effect_var + "'"
            ## if vname fill in the query
            if vname[:len(query_name)] == query_name:
                query_nodes.append(vname)

        ### Create an empty grid
        nodes_in_grid = [[[] for x in range(g.tx, g.tx + g.width, g.dx)] for y in range(g.ty, g.ty + g.height, g.dy)]

        # Put query nodes in grid
        for qn in query_nodes:
            x, y = vertex_locations[qn]

            j = int((x - g.tx) / g.dx)
            i = int((y - g.ty) / g.dy)

            nodes_in_grid[i][j].append(qn)

        ## for each cell in grid, create an inference node
        for i, row in enumerate(nodes_in_grid):
            for j, cell in enumerate(row):
                parent_location = [g.tx + j * g.dx * 0.5, g.ty + i * g.dy * 0.5]
                # Parent name
                parent_name = "'" + self.cause_var + "' " + str(parent_location)

                if parent_name in disc_bn.V:
                    continue

                disc_bn.add_vertex(parent_name, self.cause_states)
                # CPT
                disc_bn.set_cprob(parent_name, self.cause_cprob)
                # Vertex location
                vertex_locations[parent_name] = parent_location

                # for each child
                for child_node in cell:
                    disc_bn.add_edge([parent_name, child_node])
                    disc_bn.set_cprob(child_node, self.effect_cprob)