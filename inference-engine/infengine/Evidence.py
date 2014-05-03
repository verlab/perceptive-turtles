

class Evidence:
    def __init__(self, x, y, var, var_states, evidence_state):
        """

        :param x: x position.
        :param y: y position.
        :param var: variable.
        :param var_states: states of the variable.
        :param evidence_state: state of the variable.
        """
        self.x = x
        self.y = y
        self.var = var
        self.var_states = var_states
        self.evidence_state = evidence_state


