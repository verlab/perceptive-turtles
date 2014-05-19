import json
import logging
import os

logger = logging.getLogger(__name__)


def write(disc_bn, vertex_locs, evidences, output_folder='output_shapes'):
    layers = {}
    vertices = disc_bn.V
    # Compute maginal probabilities
    marginals = disc_bn.compute_marginals(evidences)

    for v in vertices:
        logger.debug("writing shape for vertex %s", v)

        try:
            var_name = v.split("'")[1]
        except Exception:
            logger.error("%s, name could not be parsed", v)

        # get or create a layer
        layer = None
        if not var_name in layers:
            # Create layer
            layer = {
                "type": "FeatureCollection",
                "features": []
            }

            layers[var_name] = layer

        else:
            layer = layers[var_name]

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": vertex_locs[v]},
            "properties": {"name": v}
        }

        ## Set probs
        states = disc_bn.get_states(v)

        for s in states:
            feature["properties"][s] = marginals[v][s]

        layer["features"].append(feature)

    # write
    for var_name, dic in layers.items():
        outSHPfn = output_folder + '/' + var_name + '.json'
        if os.path.exists(outSHPfn):
                os.remove(outSHPfn)

        with open(outSHPfn, 'w') as outfile:
            json.dump(dic, outfile)





