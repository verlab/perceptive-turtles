from infengine.rules.Rule import Rule


class CommunityRule(Rule):


    def __init__(self, individual_var, max_distance, joint_function):
        self.individual_var = individual_var
        self.max_distance = max_distance
        self.joint_function = joint_function

