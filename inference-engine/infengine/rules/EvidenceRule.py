

class EvidenceRule:
    """
    This rule triggers with a effect/evidence to infer about an cause when a new evidence appears.
    To apply Bayes rule. CAUSE => EFFECT
    """
    def __init__(self, cause_var, effect_var, cause_states, effect_states,cause_cprob, effect_cprob):
        """
        Construct.
        :param cause_var: cause variable or parent (str)
        :param effect_var: effect variable (str) ----> TRIGGER.
        :param cause_states: possible states of the cause variable (str[])
        :param effect_states:  possible states of the effect variable (str[])
        :param cause_cprob: Conditional Probability Table for the cause
        :param effect_cprob: Conditional Probability Table for the effect
        """
        self.cause_var = cause_var
        self.effect_var = effect_var
        self.cause_states = cause_states
        self.effect_states = effect_states
        self.cause_cprob = cause_cprob
        self.effect_cprob = effect_cprob