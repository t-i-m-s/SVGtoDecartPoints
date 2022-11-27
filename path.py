import pygame as pg
from pygame import Surface
from data_parse import work_tags, Tag, get_ellipse_arc
import sys
import math


def to_pos(_data: list[list[tuple]], x: float = 0.0, y: float = 0.0):
    min_x, min_y = _data[0][0]
    for dt in _data:
        for _x, _y in dt:
            min_x = _x if _x < min_x else min_x
            min_y = _y if _y < min_y else min_y
    for dt in _data:
        for i, _xy in enumerate(dt[:]):
            dt[i] = (float(format(_xy[0] - min_x + x, '.3f')),
                     float(format(_xy[1] - min_y + y, '.3f')))


def scaling(_data: list[list[tuple]], scale: float = 2.0):
    for dt in _data:
        for i, xy in enumerate(dt):
            dt[i] = (float(format(xy[0] * scale, '.3f')),
                     float(format(xy[1] * scale, '.3f')))


def get_xy_speed(sp: tuple, ep: tuple):
    delta_x = ep[0] - sp[0]
    delta_y = ep[1] - sp[1]
    x_sign = delta_x/abs(delta_x) if delta_x else 1
    y_sign = delta_y/abs(delta_y) if delta_y else 1
    if delta_x == 0 and delta_y == 0:
        return 0, 0
    elif not delta_x:
        return 0, SPEED*y_sign
    elif not delta_y:
        return SPEED*x_sign, 0
    k = abs(delta_y / delta_x)
    v_x = math.sqrt(SPEED ** 2/(k ** 2 + 1))
    return float(format(v_x*x_sign, '.3f')), float(format(k*v_x*y_sign, '.3f'))


def main(scr: Surface, dt: list[list[tuple]]):
    printed_tags = 0
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        while dt:
            circuit = dt[0]
            if len(circuit) < 2:
                dt.remove(circuit)
                printed_tags += 1
            else:
                start_p = circuit[0]
                end_p = circuit[1]
                v_x, v_y = get_xy_speed(start_p, end_p)
                if v_x != 0 or v_y != 0:
                    _x, _y = start_p
                    while abs(_x - end_p[0]) >= abs(v_x) and abs(
                            _y - end_p[1]) >= abs(v_y):
                        pg.time.Clock().tick(30)
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                sys.exit()
                        _x += v_x
                        _y += v_y
                        pg.draw.line(scr, (0, 255, 255), start_p, (_x, _y))
                        pg.display.flip()
                    pg.draw.line(scr, (0, 255, 255), start_p, end_p)
                    pg.display.flip()
                circuit.remove(start_p)
        else:
            print("Done!")
            # break


SPEED = 5
CURR_POS = 0.0, 0.0


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode(size=(640, 480))

    with open('house-2374925.svg', 'r') as svg:
        row_data = svg.read()

    for tag in work_tags:
        tag.find(row_data)

    RES_DATA = []

    for tag_set in Tag.founded_tags.values():
        for tag in tag_set:
            RES_DATA.extend(tag.data)
    scaling(RES_DATA, scale=10)
    to_pos(RES_DATA, x=0.0, y=0.0)
    print(RES_DATA)
    main(screen, RES_DATA)
    # grads = 30
    # step = 1
    # x1 = 124.721
    # y1 = 124.721
    # x2 = 85.279
    # y2 = 85.279
    # a = 80
    # b = 50
    # while 1:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             sys.exit()
    #     grads %= 360
    #     screen.fill((0, 0, 0))
    #     main(screen,
    #          get_ellipse_arc(x1 + 50, y1 + 50, a, b, grads, x2 + 50, y2 + 50))
    #     pg.draw.circle(screen, (255, 255, 0), (x1 + 50, y1 + 50), 4)
    #     pg.draw.circle(screen, (255, 255, 0), (x2 + 50, y2 + 50), 4)
    #     main(screen,
    #          get_ellipse_arc(x1 + 200, y1 + 50, a, b, grads, x2 + 200, y2 + 50, large_arc=0, clockwise=0))
    #     pg.draw.circle(screen, (255, 255, 0), (x1 + 200, y1 + 50), 4)
    #     pg.draw.circle(screen, (255, 255, 0), (x2 + 200, y2 + 50), 4)
    #     main(screen,
    #          get_ellipse_arc(x1 + 50, y1 + 200, a, b, grads, x2 + 50, y2 + 200, clockwise=0))
    #     pg.draw.circle(screen, (255, 255, 0), (x1 + 50, y1 + 200), 4)
    #     pg.draw.circle(screen, (255, 255, 0), (x2 + 50, y2 + 200), 4)
    #     main(screen,
    #          get_ellipse_arc(x1 + 200, y1 + 200, a, b, grads, x2 + 200, y2 + 200, large_arc=0))
    #     pg.draw.circle(screen, (255, 255, 0), (x1 + 200, y1 + 200), 4)
    #     pg.draw.circle(screen, (255, 255, 0), (x2 + 200, y2 + 200), 4)
    #
    #     pg.display.flip()
    #     # if grads in (45, 135, 225, 315):
    #     #     pg.image.save(screen, f'{grads}_grads.jpeg')
    #     #     break
    #     pg.time.Clock().tick(30)
    #     grads += 1
