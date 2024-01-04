import math
import numpy as np
import pygame

import ball
import rectangle
from main import SCRSIZE


class CPoint:
    def __init__(self, x, y, vx, vy, fx, fy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.fx = fx
        self.fy = fy


class CSpring:
    def __init__(self, a, b, length, nx, ny):
        self.a = a
        self.b = b
        self.length = length
        self.nx = nx
        self.ny = ny


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def euler_integ(obj: object, dt: object) -> object:

    if isinstance(obj, rectangle.Rect):
        if obj.static == 1:
            return

    for point in obj.points:
        point.vx = point.vx + (point.fx / obj.mass) * dt
        point.x = point.x + point.vx * dt

        point.vy = point.vy + (point.fy / obj.mass) * dt

        dry = point.vy * dt

        # y boundary

        '''
        if point.y + dry > SCRSIZE:
            point.vx -= 0.1 * point.vx
            point.fx = 0
            dry = SCRSIZE - point.y
            point.vy = -0.1 * point.vy

        point.y = point.y + dry
        '''
        point.y = point.y + point.vy * dt

    if isinstance(obj, ball.Ball):
        if obj.points[0].vx > 5 or obj.points[0].vx < -5:
            if obj.p > 0:
                obj.p -= 0.1

def colider(obj):

    low_x = high_x = obj.points[0].x
    low_y = high_y = obj.points[0].y

    for point in obj.points:
        low_x = min(point.x,low_x)
        low_y = min(point.y,low_y)
        high_x = max(point.x,high_x)
        high_y = max(point.y,high_y)

    obj.collider.update(low_x,low_y,high_x-low_x,high_y-low_y)
    obj.collider.inflate_ip(10,10)

def collision(obj1, obj2):

    if not pygame.Rect.colliderect(obj1.collider,obj2.collider):
        return

    for point in obj1.points:
        # point = obj1.points[0]
        # check if point is in obj2
        count = 0
        for point1 in obj2.points:
            idx = obj2.points.index(point1)
            if idx + 1 != len(obj2.points):
                point2 = obj2.points[idx + 1]
            else:
                point2 = obj2.points[0]

            if (point1.y >= point.y >= point2.y) or (point2.y >= point.y >= point1.y):
                a = point2.y - point1.y
                b = point1.x - point2.x
                c = a * point1.x + b * point1.y
                if a != 0:
                    is_left = (c - b * point.y) / a
                    if is_left > point.x:
                        count += 1

        # print(count)
        if count % 2 == 1:
            # print("is inside")
            # find closest line
            min_dis = 9999
            p1 = obj2.points[0]
            p2 = obj2.points[1]

            for point1 in obj2.points:
                idx = obj2.points.index(point1)
                if idx + 1 != len(obj2.points):
                    point2 = obj2.points[idx + 1]
                else:
                    point2 = obj2.points[0]

                dis = (abs((point2.x - point1.x) * (point1.y - point.y) - (point1.x - point.x) * (
                            point2.y - point1.y)) /
                       np.sqrt(np.square(point2.x - point1.x) + np.square(point2.y - point1.y)))

                if min_dis > dis:
                    min_dis = dis
                    p1 = point1
                    p2 = point2

            # print(obj2.points.index(p1),obj2.points.index(p2))
            # move point and line

            p = np.array((point.x, point.y))
            a = np.array((p1.x, p1.y))
            b = np.array((p2.x, p2.y))

            ab = b - a
            ap = p - a

            proj = a + np.dot(ap, ab) / np.dot(ab, ab) * ab
            # pygame.draw.circle(screen, (0, 0, 225), proj, 5)

            point.x = proj[0]
            point.y = proj[1]

            inf = distance(point.x, point.y, p1.x, p1.y)
            inf /= distance(p1.x, p1.y, p2.x, p2.y)

            # velocity update
            pointvirt = CPoint(p1.x,p1.y,p1.vx,p1.vy,p1.fx,p1.fy)

            pointvirt.vx = (p1.vx + p2.vx) / 2
            pointvirt.vy = (p1.vy + p2.vy) / 2

            m1 = obj1.mass
            m2 = obj2.mass * 2

            pointtemp = CPoint(point.x,point.y,point.vx,point.vy,point.fx,point.fy)

            unit_v = ((p2.x-p1.x)/ distance(p1.x,p1.y,p2.x,p2.y), (p2.y-p1.y)/ distance(p1.x,p1.y,p2.x,p2.y))

            vt1 = pointtemp.vx * unit_v[0] + pointtemp.vy * unit_v[1]
            vt2 = pointvirt.vx * unit_v[0] + pointvirt.vy * unit_v[1]

            vn1 = math.sqrt(pointtemp.vx**2 + pointtemp.vy**2 - vt1**2)
            vn2 = math.sqrt(pointvirt.vx**2 + pointvirt.vy**2 - vt2**2)

            vn1c = vn1

            vn1 = ((m1 - m2) * vn1c + 2 * m2 * vn2) / (m1 + m2)
            vn2 = -(2 * m1 * vn1c + (m2 - m1) * vn2) / (m1 + m2)

            vt1 *= 0.9
            vt2 *= 0.9

            vn1 *= 0.9
            vn2 *= 0.9

            pointtemp.vx = vt1 * unit_v[0] + vn1 * unit_v[1]
            pointtemp.vy = vt1 * unit_v[1] - vn1 * unit_v[0]

            pointvirt.vx = vt2 * unit_v[0] + vn2 * unit_v[1]
            pointtemp.vy = vt2 * unit_v[1] - vn2 * unit_v[0]

            point.vx = pointtemp.vx
            point.vy = pointtemp.vy

            p1.vx = pointvirt.vx * (1 - inf)
            p2.vx = pointvirt.vx * inf

            p1.vy = pointvirt.vy * (1 - inf)
            p2.vy = pointvirt.vy * inf

