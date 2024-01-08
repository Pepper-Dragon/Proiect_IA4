import math
import pygame
import pygame.rect

import objutils as ut
from globals import *

class Ball:
    def __init__(self, origin_x, origin_y, ballradius, num_p, mass, color):

        self.points = []
        self.springs = []
        self.radius = ballradius
        self.mass = mass
        self.color = color
        self.p = 3000
        self.kd = 80
        self.ks = 400

        self.collider = pygame.Rect(0,0,0,0)

        for i in range(0, num_p + 1):
            x = ballradius * math.sin(i * (2.0 * math.pi) / num_p) + origin_x
            y = ballradius * math.cos(i * (2.0 * math.pi) / num_p) + origin_y
            self.add_point(x, y, 0, 0, 0, 0)

        for i in range(0, num_p):
            length = ut.distance(self.points[i].x, self.points[i].y, self.points[i + 1].x, self.points[i + 1].y)
            self.add_spring(i, i + 1, length, 0, 0)

        length = ut.distance(self.points[0].x, self.points[0].y, self.points[num_p].x, self.points[num_p].y)
        self.add_spring(num_p, 0, length, 0, 0)

    def add_point(self, x, y, vx, vy, fx, fy):
        point = ut.CPoint(x, y, vx, vy, fx, fy)
        self.points.append(point)

    def add_spring(self, a, b, length, nx, ny):
        spring = ut.CSpring(a, b, length, nx, ny)
        self.springs.append(spring)

    def draw(self, screen, offset):
        verteces = []

        for point in self.points:
            x = point.x + offset.x
            y = point.y + offset.y
            vertex = (x, y)
            verteces.append(vertex)

        red = (225, 100, 100)
        pygame.draw.polygon(screen, self.color, verteces, 0)
        # pygame.draw.circle(screen, (0, 0, 225), (verteces[0][0], verteces[0][1]), 5)

    def gravity(self):
        for point in self.points:
            point.fx = 0
            point.fy = GRAVITY * self.mass

    def forces(self):
        self.gravity()
        for spring in self.springs:
            x1 = self.points[spring.a].x
            x2 = self.points[spring.b].x
            y1 = self.points[spring.a].y
            y2 = self.points[spring.b].y

            # curent spring length
            d = ut.distance(x1, y1, x2, y2)

            if d != 0:
                # relative velocity
                vx = self.points[spring.a].vx - self.points[spring.b].vx
                vy = self.points[spring.a].vy - self.points[spring.b].vy

                # calculate spring force
                # KS-spring constant KD-dampaning factor

                f = (d - spring.length) * self.ks + (vx * (x1 - x2) + vy * (y1 - y2)) * self.kd / d
                fx = ((x1 - x2) / d) * f
                fy = ((y1 - y2) / d) * f

                # adding forces to points
                self.points[spring.a].fx -= fx
                self.points[spring.a].fy -= fy

                self.points[spring.b].fx += fx
                self.points[spring.b].fy += fy

                # calculating normal forces
                spring.nx = (y1 - y2) / d
                spring.ny = -(x1 - x2) / d

        # volume calculation for pressure model
        volume = 0
        for spring in self.springs:
            x1 = self.points[spring.a].x
            x2 = self.points[spring.b].x
            y1 = self.points[spring.a].y
            y2 = self.points[spring.b].y

            # curent spring length
            d = ut.distance(x1, y1, x2, y2)

            volume += 0.5 * math.fabs(x1 - x2) * math.fabs(spring.nx) * d

        for spring in self.springs:
            x1 = self.points[spring.a].x
            x2 = self.points[spring.b].x
            y1 = self.points[spring.a].y
            y2 = self.points[spring.b].y

            # curent spring length
            d = ut.distance(x1, y1, x2, y2)

            pressure = d * self.p * (1.0 / volume)

            # adding pressure force to total force
            self.points[spring.a].fx += pressure * spring.nx
            self.points[spring.a].fy += pressure * spring.ny

            self.points[spring.b].fx += pressure * spring.nx
            self.points[spring.b].fy += pressure * spring.ny
