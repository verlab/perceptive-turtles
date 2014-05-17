import gdal
from osgeo.gdalconst import GA_ReadOnly


def geo_transform(points, tiff_path):
    """
    :param points vector of points (pixels) to convert, it should has p.x and p.y
    :param tiff_path path of the tiff file.
    """
    tiff_info = gdal.Open(tiff_path, GA_ReadOnly)

    for p in points:
        transform = tiff_info.GetGeoTransform()

        origin_x = transform[0]
        origin_y = transform[3]
        pixel_width = transform[1]
        pixel_height = transform[5]

        # Convert from pixels to geoposition
        p.x = origin_x + p.x * pixel_width
        p.y = origin_y + p.y * pixel_height