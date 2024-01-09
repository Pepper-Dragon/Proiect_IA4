import pygame
import objutils as ut


from sprite import GameSprite
from globals import *

class Rect:
    def __init__(self, groups, image, position, size, mass, color, static):

        actual_position = (position[0] * TILE_SIZE, position[1] * TILE_SIZE)
        actual_size = (size[0] * TILE_SIZE, size[1] * TILE_SIZE)

        self.points = []
        self.springs = []
        self.height = actual_size[1]
        self.width = actual_size[0]
        self.mass = mass
        self.color = color
        self.static = static

        self.collider = pygame.Rect(0,0,0,0)

        if static:
            self.sprite = GameSprite(groups, image, position, size)

        self.add_point(actual_position[0]-self.width/2, actual_position[1]-self.height/2, 0, 0, 0, 0)
        self.add_point(actual_position[0]+self.width/2, actual_position[1]-self.height/2, 0, 0, 0, 0)
        self.add_point(actual_position[0]+self.width/2, actual_position[1]+self.height/2, 0, 0, 0, 0)
        self.add_point(actual_position[0]-self.width/2, actual_position[1]+self.height/2, 0, 0, 0, 0)

        self.add_spring(0,1,ut.distance(self.points[0].x,self.points[0].y,self.points[1].x,self.points[1].y),0,0)
        self.add_spring(1,2,ut.distance(self.points[1].x,self.points[1].y,self.points[2].x,self.points[2].y),0,0)
        self.add_spring(2,3,ut.distance(self.points[2].x,self.points[2].y,self.points[3].x,self.points[3].y),0,0)
        self.add_spring(3,0,ut.distance(self.points[3].x,self.points[3].y,self.points[0].x,self.points[0].y),0,0)
        self.add_spring(0,2,ut.distance(self.points[0].x,self.points[0].y,self.points[2].x,self.points[2].y),0,0)
        self.add_spring(3,1,ut.distance(self.points[3].x,self.points[3].y,self.points[1].x,self.points[1].y),0,0)

    def add_point(self, x, y, vx, vy, fx, fy):
        point = ut.CPoint(x, y, vx, vy, fx, fy)
        self.points.append(point)

    def add_spring(self, a, b, length, nx, ny):
        spring = ut.CSpring(a, b, length, nx, ny)
        self.springs.append(spring)

    def draw(self, screen, offset):
        if not self.static:
            verteces = []

            for point in self.points:
                x = point.x
                y = point.y
                vertex = (x, y) + offset
                verteces.append(vertex)

            pygame.draw.polygon(screen, self.color, verteces, 0)
            # pygame.draw.circle(screen, (0, 0, 225), (self.center.x, self.center.y), 5)

    def gravity(self):
        for point in self.points:
            point.fx = 0
            point.fy = GRAVITY * self.mass

    def forces(self):
        if self.static == 1:
            return

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

                f = (d - spring.length) * 200
                fx = ((x1 - x2) / d) * f
                fy = ((y1 - y2) / d) * f

                # adding forces to points
                self.points[spring.a].fx -= fx
                self.points[spring.a].fy -= fy

                self.points[spring.b].fx += fx
                self.points[spring.b].fy += fy







