class Evidence:
    def __init__(self, boundary, variable_name, var_states, default_state):
        """


        :param boundary: polygon of the boundary.
        :param default_state:
        :param variable_name: variable.
        :param var_states: states of the variable.
        """
        self.default_state = default_state
        self.var = variable_name
        self.var_states = var_states
        self.boundary = boundary
        # Dictionary {state: [polygons]}
        self.detections = {}


    def add_detection(self, state, polygon):
        """
        Add to detections dictionary: {state: [polygons]}
        :param state:
        :param polygon:
        """
        if not state in self.detections:
            self.detections[state] = []

        self.detections[state].append(polygon)



