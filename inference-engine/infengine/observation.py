VAR_STATES = ['false', 'true']


class Observation:
    def __init__(self, boundary, variable_name, var_states=VAR_STATES, default_state=VAR_STATES[0]):
        """


        :param boundary: polygon of the boundary.
        :param default_state: where there is not state in the boundary is default_state.
        :param variable_name: variable.
        :param var_states: states of the variable.
        """
        self.default_state = default_state
        self.variable_name = variable_name
        self.var_states = var_states
        self.boundary = boundary
        # Dictionary {state: [polygons]}
        self.evidences = {}


    def add_detection(self, polygon, state=VAR_STATES[1]):
        """
        Add to detections dictionary: {state: [polygons]}
        :param state:
        :param polygon:
        """
        if not state in self.evidences:
            self.evidences[state] = []

        self.evidences[state].append(polygon)

    def get_detections(self, state=VAR_STATES[1]):
        return self.evidences[state]


