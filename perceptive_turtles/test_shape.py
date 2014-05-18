from infengine.gis import shape_writer
from lib_sallybn.disc_bayes_net.DiscreteBayesianNetworkExt import DiscreteBayesianNetworkExt
from lib_sallybn.drawer.GPoint import GPoint
from lib_sallybn.util import ufile

file_name = 'output.bn'
disc_bn = DiscreteBayesianNetworkExt()
disc_bn.load(file_name)

vertex_locations = {}
### Load Vertex locations
json_data = ufile.dic_from_json_file(file_name)
# Vertex locations
if "vertex_loc" in json_data.keys():
    for vname, point in json_data["vertex_loc"].items():
        vertex_locations[vname] = GPoint(point[0], point[1])

shape_writer.write(disc_bn, vertex_locations, {})
