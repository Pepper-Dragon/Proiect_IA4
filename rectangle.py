import pygame
import objutils as ut

GY = 9.8


class Rect:
    def __init__(self, origin_x, origin_y, height, width, mass, color, static):

        self.points = []
        self.springs = []
        self.height = height
        self.width = width
        self.mass = mass
        self.color = color
        self.static = static

        self.collider = pygame.Rect(0,0,0,0)

        self.add_point(origin_x-width/2, origin_y-height/2, 0, 0, 0, 0)
        self.add_point(origin_x+width/2, origin_y-height/2, 0, 0, 0, 0)
        self.add_point(origin_x+width/2, origin_y+height/2, 0, 0, 0, 0)
        self.add_point(origin_x-width/2, origin_y+height/2, 0, 0, 0, 0)


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

    def draw(self, screen):
        verteces = []

        for point in self.points:
            x = point.x
            y = point.y
            vertex = (x, y)
            verteces.append(vertex)

        pygame.draw.polygon(screen, self.color, verteces, 0)
        #pygame.draw.circle(screen, (0, 0, 225), (self.center.x, self.center.y), 5)

    def gravity(self):
        for point in self.points:
            point.fx = 0
            point.fy = GY * self.mass

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







