import math
import pygame

#constants
#screen
BALLRADIUS = 50
SCRSIZE = 600

#time
DT = 0.006

#ball
NUMP = 30
BALLRADIUS = 50
MASS = 1
GY = 9.8
KD=80
KS=40
P=1330

class CPoint:
     def __init__(self, x, y, vx, vy, fx, fy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.fx = fx
        self.fy = fy
        
class CSpring:
    def __init__(self, a, b, lenght, nx, ny):
        self.a = a
        self.b = b
        self.lenght = lenght
        self.nx = nx
        self.ny = ny

class Ball:
    def __init__(self):
        self.points = []
        self.springs = [] 

    def add_point(self, x, y, vx, vy, fx, fy):
        point = CPoint(x, y, vx, vy, fx, fy)
        self.points.append(point)

    def add_spring(self, a, b, lenght, nx, ny):
        spring = CSpring(a, b, lenght, nx, ny)
        self.springs.append(spring)

    def gravity(self):
        for point in self.points:
            point.fx = 0
            point.fy = GY * MASS

    def spring_forces(self):
        self.gravity()
        for spring in self.springs:
            x1 = self.points[spring.a].x
            x2 = self.points[spring.b].x
            y1 = self.points[spring.a].y
            y2 = self.points[spring.b].y

            #curent spring lenght
            d = distance(x1, y1, x2, y2)

            if d != 0:
                #relative velocity
                vx = self.points[spring.a].vx - self.points[spring.b].vx
                vy = self.points[spring.a].vy - self.points[spring.b].vy

                #calculate spring force
                #KS-spring constant KD-dampaning factor
                f = (d - spring.lenght) * KS + (vx * (x1 - x2) + vy * (y1 - y2)) * KD / d
                fx = ((x1 - x2) / d) * f
                fy = ((y1 - y2) / d) * f

                #adding forces to points
                self.points[spring.a].fx -= fx
                self.points[spring.a].fy -= fy

                self.points[spring.b].fx += fx
                self.points[spring.b].fy += fy

                #calculating normal forces
                spring.nx = (y1 - y2) / d
                spring.ny = -(x1 - x2) / d

        #volume calculation for pressure model
        volume = 0
        for spring in self.springs:
            x1 = self.points[spring.a].x
            x2 = self.points[spring.b].x
            y1 = self.points[spring.a].y
            y2 = self.points[spring.b].y

            #curent spring lenght
            d = distance(x1, y1, x2, y2)

            volume += 0.5 * math.fabs(x1 - x2) * math.fabs(spring.nx) * d

        for spring in self.springs:
            x1 = self.points[spring.a].x
            x2 = self.points[spring.b].x
            y1 = self.points[spring.a].y
            y2 = self.points[spring.b].y

            #curent spring lenght
            d = distance(x1, y1, x2, y2)     
            
            pressure = d * P * (1.0 / volume);

            #adding pressure force to total force
            self.points[spring.a].fx += pressure * spring.nx
            self.points[spring.a].fy += pressure * spring.ny

            self.points[spring.b].fx += pressure * spring.nx
            self.points[spring.b].fy += pressure * spring.ny


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def init_ball():
    ball = Ball()

    for i in range(0, NUMP+1):
        x =  BALLRADIUS * math.sin(i * (2.0 * math.pi) / NUMP) + (SCRSIZE / 2)
        y = BALLRADIUS * math.cos(i * (2.0 * math.pi) / NUMP) + (SCRSIZE / 2)
        ball.add_point(x, y, 0 ,0 ,0 ,0)

    for i in range(0, NUMP):
        lenght = distance(ball.points[i].x, ball.points[i].y, ball.points[i+1].x, ball.points[i+1].y)
        ball.add_spring(i, i+1, lenght, 0, 0)

    lenght = distance(ball.points[0].x, ball.points[0].y, ball.points[NUMP].x, ball.points[NUMP].y)
    ball.add_spring(NUMP, 0, lenght, 0, 0)

    return ball


def draw_ball(screen, ball):
    verteces = []

    for i in range(0, NUMP):
        x = ball.points[i].x
        y = ball.points[i].y
        vertex = (x, y)
        verteces.append(vertex)

    red = (225, 100, 100)
    pygame.draw.polygon(screen, red, verteces, 0)

def euler_integ(ball):
    for point in ball.points:
        point.vx = point.vx + ( point.fx / MASS  ) * DT
        point.x = point.x + point.vx*DT

        point.vy = point.vy + ( point.fy / MASS  ) * DT
       
        dry = point.vy * DT

		#y boundary 
        if point.y + dry > SCRSIZE:
            dry = SCRSIZE - point.y
            point.vy = -0.1 * point.vy
		
        point.y = point.y + dry;

def main():
    #misc
    player = init_ball()

    #screen
    pygame.init()
    backround_color = (0, 0, 0)
    screen = pygame.display.set_mode((SCRSIZE,SCRSIZE))
    pygame.display.set_caption("BLOB")

    #update
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;

        screen.fill(backround_color)
        draw_ball(screen, player)
        euler_integ(player)
        player.spring_forces()
        pygame.display.update()

if __name__ == "__main__":
    main()