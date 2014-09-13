

class Evidence:
    def __init__(self, polygon, var, var_states, evidence_state):
        """

        :param polygon: area where the evince occurred.
        :param var: variable.
        :param var_states: states of the variable.
        :param evidence_state: state of the variable.
        """
        self.polygon = polygon
        self.var = var
        self.var_states = var_states
        self.evidence_state = evidence_state


