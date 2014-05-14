import ogr
import os


def write(disc_bn, vertex_locs):
    layers = {}
    vertices = disc_bn.V

    for v in vertices:
        try:
            var_name = v.split("'")[1]
        except Exception:
            print v, " could not be parsed",

        # get or create a layer
        layer = None
        if not var_name in layers:
            # Create the output shapefile
            # layer = _create_layer(var_name)
            outSHPfn = '../shapes/' + var_name + '.shp'

            # Create the output shapefile
            shpDriver = ogr.GetDriverByName("ESRI Shapefile")
            if os.path.exists(outSHPfn):
                shpDriver.DeleteDataSource(outSHPfn)
            outDataSource = shpDriver.CreateDataSource(outSHPfn)
            layer = outDataSource.CreateLayer(outSHPfn, geom_type=ogr.wkbPoint)

            # Create field in layer
            new_field = ogr.FieldDefn('name', ogr.OFTString)
            layer.CreateField(new_field)

            # save layer
            layers[var_name] = layer
        else:
            layer = layers[var_name]

        ## Features
        # create a field
        # Input data
        # fieldName = 'prob'
        # fieldType = ogr.OFTInteger
        # fieldValue = 15

        # Create the feature and set values
        feature_schema = layer.GetLayerDefn()

        # Location
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(*vertex_locs[v])

        feature = ogr.Feature(feature_schema)
        feature.SetGeometry(point)
        # variable name
        feature.SetField('name', v)
        # add the new feature to the layer
        layer.CreateFeature(feature)


def _create_layer(var_name):
    outSHPfn = var_name + '.shp'

    # Create the output shapefile
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outSHPfn):
        shpDriver.DeleteDataSource(outSHPfn)
    outDataSource = shpDriver.CreateDataSource(outSHPfn)
    layer = outDataSource.CreateLayer(outSHPfn, geom_type=ogr.wkbPoint)

    return layer











