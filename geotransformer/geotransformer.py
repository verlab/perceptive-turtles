import gdal
from osgeo.gdalconst import GA_ReadOnly


def geo_transform(polygon, tiff_path):
    """
    :param points vector of points (pixels) to convert, it should has p.x and p.y
    :param tiff_path path of the tiff file.
    """
    tiff_info = gdal.Open(tiff_path, GA_ReadOnly)
    #Transform
    transform = tiff_info.GetGeoTransform()
    origin_x = transform[0]
    origin_y = transform[3]
    pixel_width = transform[1]
    pixel_height = transform[5]

    # Convert polygons
    for p in polygon:
        # Convert from pixels to geoposition
        p[0] = origin_x + p[0] * pixel_width
        p[1] = origin_y + p[1] * pixel_height