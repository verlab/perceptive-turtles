

class QueryRule:
    """
    This rule make a query to infer about a hidden variable.
    """
    def __init__(self, cause_var, inferred_var, inferred_cprob, query_var, query_range, query_function):
        """
        Define the essential parameters for this rule.

        :param cause_var: cause variable to TRIGGER (str).
        :param inferred_var: variable to infer (str).
        :param inferred_cprob: conditional probability distribution for inferred_var (dict).
        :param query_var: variable to query before inference (str)
        :param query_range: range that this rule can affect (float).
        :param query_function: Function to fusion multiple nodes (function). It can be:
            [Maximum, Minimum, Mean, or Proportional to distance].
        """
        self.cause_var = cause_var
        self.inferred_var = inferred_var
        self.inferred_cprob = inferred_cprob
        self.query_var = query_var
        self.query_range = query_range
        self.query_function = query_function
