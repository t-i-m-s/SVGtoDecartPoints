import math


def get_angle_rel_zero_pos(x, y):
    ang_rel_y_axis = math.asin(x/(math.sqrt(x**2 + y**2)))
    if y >= 0:
        return (math.pi/2 - ang_rel_y_axis)*180/math.pi
    else:
        return ((3*math.pi)/2 + ang_rel_y_axis)*180/math.pi


def get_new_coord_from_rot_axis(x, y, rot_ang):
    c = math.sqrt(x**2 + y**2)
    pnt_ang = get_angle_rel_zero_pos(x, y)
    res_ang = (pnt_ang - rot_ang)*math.pi/180
    return c * math.cos(res_ang), c * math.sin(res_ang)


def find_ellipse_center(x1, y1, x2, y2, a, b):
    if abs(y1 - y2) >= 0.001:
        p = (b ** 2 / a ** 2) * ((x2 - x1) / (y1 - y2))
        t = (y1 + y2) / 2 - ((b ** 2) / (2 * a ** 2)) * (
                (x2 ** 2 - x1 ** 2) / (y1 - y2))
        _a = 1 / a ** 2 + p ** 2 / b ** 2
        _b = (2 * p * t) / b ** 2 - (2 * x1) / a ** 2 - (2 * y1 * p) / b ** 2
        _c = x1 ** 2 / a ** 2 + y1 ** 2 / b ** 2 + t ** 2 / b ** 2 - ((2 * y1 * t) / b ** 2) - 1
        _d = _b ** 2 - 4 * _a * _c
        if _d < 0:
            raise Exception('Negative variable: _d')
        _x1 = (-_b + math.sqrt(_d)) / (2 * _a)
        _y1 = float(format(p * _x1 + t, '.3f'))
        _x1 = float(format(_x1, '.3f'))
        _x2 = (-_b - math.sqrt(_d)) / (2 * _a)
        _y2 = float(format(p * _x2 + t, '.3f'))
        _x2 = float(format(_x2, '.3f'))
    elif abs(x1 - x2) >= 0.001:
        p = (a ** 2 / b ** 2) * ((y2 - y1) / (x1 - x2))
        t = (x1 + x2) / 2 - ((a ** 2) / (2 * b ** 2)) * (
                (y2 ** 2 - y1 ** 2) / (x1 - x2))
        _a = 1 / b ** 2 + p ** 2 / a ** 2
        _b = (2 * p * t) / a ** 2 - (2 * y1) / b ** 2 - (2 * x1 * p) / a ** 2
        _c = x1 ** 2 / a ** 2 + y1 ** 2 / b ** 2 + t ** 2 / a ** 2 - ((2 * x1 * t) / a ** 2) - 1
        _d = _b ** 2 - 4 * _a * _c
        if _d < 0:
            raise Exception('Negative variable: _d')
        _y1 = (-_b + math.sqrt(_d)) / (2 * _a)
        _x1 = float(format(p * _y1 + t, '.3f'))
        _y1 = float(format(_y1, '.3f'))
        _y2 = (-_b - math.sqrt(_d)) / (2 * _a)
        _x2 = float(format(p * _y2 + t, '.3f'))
        _y2 = float(format(_y2, '.3f'))
    else:
        raise Exception(f'Identical coordinates: ({x1}, {y1}), ({x2}, {y2})')
    return (_x1, _y1), (_x2, _y2)


def get_angle_range(centers: tuple, x1, y1, x2, y2, clockwise, large_arc, step):
    arcs = []
    for cent in centers:
        arc_angles = []
        cx, cy = cent
        ang1 = get_angle_rel_zero_pos(x1 - cx, y1 - cy)
        ang2 = get_angle_rel_zero_pos(x2 - cx, y2 - cy)
        arc_angles.append(ang1)
        if clockwise:
            ang1 = math.floor(ang1)
            _ang2 = math.ceil(ang2)
            for ang in range(ang1 + (360 if ang1 < _ang2 else 0), _ang2 - step, -step):
                ang %= 360
                arc_angles.append(ang)
        else:
            _ang2 = math.floor(ang2)
            ang1 = math.ceil(ang1)
            for ang in range(ang1, _ang2 + (360 if ang1 > _ang2 else 0) + step, step):
                ang %= 360
                arc_angles.append(ang)
        arc_angles.append(ang2)
        arcs.append(arc_angles)
    if large_arc:
        return (centers[0], arcs[0]) if len(arcs[0]) >= len(arcs[1]) else (centers[1], arcs[1])
    else:
        return (centers[0], arcs[0]) if len(arcs[0]) <= len(arcs[1]) else (centers[1], arcs[1])


def get_ellipse_arc(x1, y1, a, b, ang, x2, y2, clockwise=1, large_arc=1, step=1):
    _x1, _y1 = get_new_coord_from_rot_axis(x1, y1, ang)
    _x2, _y2 = get_new_coord_from_rot_axis(x2, y2, ang)
    centers = find_ellipse_center(_x1, _y1, _x2, _y2, a, b)
    center, angles = get_angle_range(centers, _x1, _y1, _x2, _y2, clockwise, large_arc, step)
    ell_points = list()
    for phi in angles:
        phi = phi * math.pi / 180
        r = math.sqrt(((a ** 2) * (b ** 2)) / ((b ** 2) * (math.cos(phi) ** 2) + (a ** 2) * (math.sin(phi) ** 2)))
        _x = center[0] + r*math.cos(phi)
        _y = center[1] + r*math.sin(phi)
        real_ang = (get_angle_rel_zero_pos(_x, _y) + ang)*math.pi/180
        r = math.sqrt(_x**2 + _y**2)
        ell_points.append((float(format(r*math.cos(real_ang), '.3f')),
                           float(format(r*math.sin(real_ang), '.3f'))))
    return [ell_points]