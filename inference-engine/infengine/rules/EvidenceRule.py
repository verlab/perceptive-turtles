from infengine.rules.Rule import Rule


class EvidenceRule(Rule):
    """
    This rule triggers with a effect/evidence to infer about an cause when a new evidence appears.
    To apply Bayes rule. CAUSE => EFFECT
    """

    def __init__(self, cause_var, effect_var, cause_states, effect_states, cause_cprob, effect_cprob, cause_radio=0.0):
        """
        Construct.
        :param cause_var: cause variable or parent (str)
        :param effect_var: effect variable (str) ----> TRIGGER.
        :param cause_states: possible states of the cause variable (str[])
        :param effect_states:  possible states of the effect variable (str[])
        :param cause_cprob: Conditional Probability Table for the cause
        :param effect_cprob: Conditional Probability Table for the effect
        :param cause_radio: defines a radio to determine that a evidence infer about a near cause.
        """
        self.cause_var = cause_var
        self.effect_var = effect_var
        self.cause_states = cause_states
        self.effect_states = effect_states
        self.cause_cprob = cause_cprob
        self.effect_cprob = effect_cprob
        self.cause_radio = cause_radio

    def generate_inference(self, disc_bn, evidences, bn_evidences, vertex_locations):
        """
        Create the parent nodes in the Bayesian Network based on evidences.
        :param vertex_locations:
        :param evidences: Evidences dictionary
        :param disc_bn: Discrete Bayesian Network
        """
        # Generate inferred variables based on evidence rules
        for i, e in enumerate(evidences):
            # this evidence is not our interest.
            if e.var != self.effect_var:
                continue

            # vertex location in map.
            evidence_location = [e.x, e.y]

            ## Create a node for this evidence
            evidence_name = "'" + e.var + "'" + str(evidence_location) + "_" + str(i)

            ##### TRIGGER if evidence is equals to effect variable in rule.

            # Inferred location
            inferred_loc = evidence_location

            ## create a new parent variable
            parent_name = "'" + self.cause_var + "'" + str(inferred_loc)

            # If parent has not been created.
            if not parent_name in disc_bn.V:
                ## add to bn
                disc_bn.add_vertex(parent_name, self.cause_states)
                ## position
                vertex_locations[parent_name] = inferred_loc
                # CPT
                disc_bn.set_cprob(parent_name, self.cause_cprob)

            # If the new edge has not been created before
            if not [parent_name, evidence_name] in disc_bn.E:
                disc_bn.add_edge([parent_name, evidence_name])

                # CPT for child
                disc_bn.set_cprob(evidence_name, self.effect_cprob)
