import site
import glob

import cv2

from fire_evidence import FireEvidence
from lib_sallybn.util import ufile


site.addsitedir('.')
# from gi.repository import Gtk

# add the related projects based on the libs.pth file.
import geotransformer
from infengine.InferenceEngine import InferenceEngine
from infengine.gis import shape_writer
from people_evidence import PeopleEvidence
import rules

### Constants
# folder with tiff files
TIF_FOLDER = './tif_files/'
ROTATION_ANGLE_PEOPLE = 30
# Variables names

BOOLEAN_STATES = ["true", "false"]


### Detectors
people = PeopleEvidence()
fire = FireEvidence()

## Engine
engine = InferenceEngine(rules.get_rules())

## Read tiff files
tif_files = glob.glob(TIF_FOLDER + "*.tif")
tif_files.sort()

evidences = []

# For each tif file
for tif in tif_files:
    print "processing ", tif
    # Read the file
    frame = cv2.imread(tif)
    # cv2.imshow("test", frame)
    # cv2.waitKey(0)

    ### Detect people
    people_evidences = people.get_evidences(frame)
    # people_evidences=[]
    ### Detect fire
    fire_evidences = fire.get_evidences(frame)
    # fire_evidences=[]
    evidences += people_evidences + fire_evidences

    # for p in evidences:
    #     print p.x, p.y, p.var, p.evidence_state

    # transform to geoposition
    geotransformer.geo_transform(evidences, tif)

    ### show geo-results
    # show bayesian network
    bn, bn_evidences = engine.infer_bn(evidences)

    nbn = {
        "vertex_loc": engine.vertex_locations,
        "E": bn.get_edges(),
        "V": bn.get_vertices(),
        "Vdata": bn.get_vdata()}

    ufile.dic_to_file(nbn, 'output.bn')

# write shapes for results
shape_writer.write(bn, engine.vertex_locations, bn_evidences)

## sleep
# time.sleep(10)
##### Show the resultant Bayesian Network
# window = Gtk.Window()
# window.set_size_request(800, 600)
#
# box = BoxDiscreteBN(window, disc_bn=bn)
# box.evidences = bn_evidences
# box.organize_graph(random=False)
# box.set_mode(Mode.run)
#
# window.add(box)
# window.show_all()
#
# window.connect("delete-event", Gtk.main_quit)
# Gtk.main()


