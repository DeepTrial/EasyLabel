import math


def map_min_max(data_dict,coords):
    minx = 20000000000
    miny = 20000000000
    maxx = -1
    maxy = -1

    if coords[0] == 1:
        # x,y,w,h
        minx = max(coords[1] - coords[3] / 2.0, 0)
        miny = max(coords[2] - coords[4] / 2.0, 0)
        maxx = min(coords[1] + coords[3] / 2.0, data_dict["width"])
        maxy = min(coords[2] + coords[4] / 2.0, data_dict["height"])
        return minx, miny, maxx, maxy
    else:
        # (x1,y1),(x2,y2)...
        for i in range(1, len(coords) - 1):
            if minx > coords[i][0]:
                minx = coords[i][0]
            if miny > coords[i][1]:
                miny = coords[i][1]
            if maxx < coords[i][0]:
                maxx = coords[i][0]
            if maxy < coords[i][1]:
                maxy = coords[i][1]
        return minx, miny, maxx, maxy


def overlap_area(shape_rectangle, shape_polygon):
    area_polygon = (shape_polygon[2] - shape_polygon[0]) * (shape_polygon[3] - shape_polygon[1])
    minx = max(shape_rectangle[0], shape_polygon[0])
    miny = max(shape_rectangle[1], shape_polygon[1])
    maxx = min(shape_rectangle[2], shape_polygon[2])
    maxy = min(shape_rectangle[3], shape_polygon[3])

    overlap_area = (maxx - minx) * (maxy - miny)
    return overlap_area / area_polygon
    # if overlap_area / area_polygon >= 0.8:
    #     return True
    # else:
    #     return False


def calculate_shape(coord_list):
    area=0
    for i in range(len(coord_list)):
        area=area+(coord_list[i][0]*coord_list[(i+1)%len(coord_list)][1]-coord_list[(i+1)%len(coord_list)][0]*coord_list[i][1])
    return math.fabs(area*0.5)