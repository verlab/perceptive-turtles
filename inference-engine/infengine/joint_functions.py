


def mean(states, query_marginals):
    probs = []

    for s in states:
        vals = [m[s] for m in query_marginals]

        # sum
        mean= sum(vals)/len(vals)

        probs.append(mean)

    return probs


##TODO max, min, proportional to the distance
#