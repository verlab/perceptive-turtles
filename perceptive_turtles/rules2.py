from infengine import joint_functions
from infengine.rules.CommunityRule import CommunityRule
from infengine.rules.EvidenceRule import EvidenceRule
from infengine.rules.GridRule import GridRule, Grid
from infengine.rules.QueryRule import QueryRule

COMMUNITY_RADIO = 0.000018006862307153121620199864860722982484730891883373260498046875
HUMAN_RADIO = 0.0000270102934607296824302997972910844737270963378250598907470703125000


def get_rules():
    fire_sensor_cprob = {
        "['true']": [.86, .14],
        "['false']": [.001, 0.999],
    }
    human_sensor_cprob = {
        "['true']": [.36, .64],
        "['false']": [.07, 0.93],
    }
    fire_cprob = [0.4, 0.6]
    human_cprob = [0.3, 0.7]

    human_danger_cprob = {
        "['true', 'true']": [.9, .1],
        "['true', 'false']": [.01, .99],
        "['false', 'true']": [.01, .99],
        "['false', 'false']": [.001, .999]
    }

    community_cprob = {
        "['true', 'true']": [.99, .01],
        "['true', 'false']": [.01, .99],
        "['false', 'true']": [.01, .99],
        "['false', 'false']": [.01, .99]
    }


    # Evidence Rules
    fire_er = EvidenceRule("Fire", "Fire_Sensor", ["true", "false"],
                           ["true", "false"], fire_cprob, fire_sensor_cprob)
    human_er = GridRule("Human", "Human_Sensor", ["true", "false"],
                        ["true", "false"], human_cprob, human_sensor_cprob,
                        Grid(-43.9593, -19.8699, 0.0002, 0.0001, 20, 10))

    # Query Rules
    qr = QueryRule('Human', 'Human in Danger', ["true", "false"], human_danger_cprob, "Fire", ["true", "false"],
                   HUMAN_RADIO,
                   joint_functions.mean)

    cr = CommunityRule('Human', 'Community', ["true", "false"], COMMUNITY_RADIO,
                       joint_functions.mean)

    cdr = QueryRule('Community', 'Community in Danger', ["true", "false"], community_cprob, "Fire", ["true", "false"],
                    10,
                    joint_functions.mean)

    #return [fire_er, human_er, qr, cr, cdr]
    return [human_er]