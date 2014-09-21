import copy
from shapely.geometry import Polygon


def evidence_to_grid(evidences, grid_map):
    """
    Put polygon evidences in evidencegrid.
    :param evidences:
    :param grid_map:
    :return:
    """
    evid_var = {}
    for e in evidences:
        if not e.variable_name in evid_var:
            evid_var[e.variable_name] = []

        evid_var[e.variable_name].append(e)

    grid_vars = {}

    ## Evidences to Grid
    # For each variable
    for var_name, evids in evid_var.items():
        # Create evidencegrid
        grid = copy.deepcopy(grid_map)
        grid_vars[var_name] = grid

        # for each cell in evidencegrid
        for i, j in zip(grid.n_rows, grid.n_columns):
            cell = Polygon(grid.cell_points(i, j))

            # For each evidence
            for e in evids:
                boundary = Polygon(e.boundary)

                # If cell is in evidence boundary
                if not cell.intersects(boundary):
                    continue

                if grid.get(i, j) is None:
                    grid.set(i, j, [0, 0])

                false_evidences, true_evidences = grid.get(i, j)

                # For each true state
                for st in e.get_detections():
                    polygon_state = Polygon(st)

                    if polygon_state.intersects(cell):
                        true_evidences += 1

                false_evidences += 1 if true_evidences == 0 else 0

                # Se the update evidences.
                grid.set(i, j, [false_evidences, true_evidences])

    return grid_vars