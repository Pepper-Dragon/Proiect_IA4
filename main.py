import cProfile
import math
import pstats

import pygame
import time
import ball
import rectangle as rect
import objutils as ut


# constants

# screen
SCRSIZE = 600
GY = 9.8

def main():
    with cProfile.Profile() as pr:

        # misc
        '''
        b1 = ball.Ball(SCRSIZE / 3, SCRSIZE / 2, 10, 10, 1, (100, 0, 0))
        b2 = ball.Ball(SCRSIZE, SCRSIZE / 3, 10, 10, 1, (100, 30, 80))
        b3 = ball.Ball(SCRSIZE / 5, SCRSIZE / 5, 10, 10, 1, (100, 100, 80))
        '''
        player = ball.Ball(SCRSIZE / 3, SCRSIZE / 2, 10, 30, 1, (100, 0, 80))
        rect1 = rect.Rect(SCRSIZE/2,SCRSIZE/2,50,50,0.1,(10,80,80), 0)
        floor = rect.Rect(SCRSIZE/2,SCRSIZE, 50, SCRSIZE, 100, (25,35,100), 1)
        floor1 = rect.Rect(SCRSIZE,SCRSIZE, 50, SCRSIZE, 100, (25,35,100), 1)
        floor2 = rect.Rect(SCRSIZE,SCRSIZE/2, SCRSIZE, 50, 100, (25,35,100), 1)
        floor3 = rect.Rect(0,SCRSIZE/2, SCRSIZE, 50, 100, (25,35,100), 1)

        # screen
        pygame.init()
        background_color = (0, 0, 0)
        screen = pygame.display.set_mode((SCRSIZE,SCRSIZE ), pygame.RESIZABLE)
        pygame.display.set_caption("BLOB")

        # update
        running = True

        # time
        clock = pygame.time.Clock()
        prev_time = time.time()
        dt = 0

        while running:
            # close window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # delta time calculation

            crt_time = time.time()
            dt = crt_time - prev_time
            prev_time = crt_time

            if dt > 0.006:
                dt = 0.006

            clock.tick()
            print(clock.get_fps())

            # rendering
            screen.fill(background_color)
            player.draw(screen)
            rect1.draw(screen)
            floor.draw(screen)
            floor1.draw(screen)
            floor2.draw(screen)
            floor3.draw(screen)

            '''
            b1.draw(screen)
            b2.draw(screen)
            b3.draw(screen)
            '''
            # simulation
            while dt > 0.0:
                player.forces()
                rect1.forces()

                '''
                b1.spring_forces()
                b2.spring_forces()
                b3.spring_forces()
                '''

                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    for points in player.points:
                        points.fx -= 5
                if keys[pygame.K_d]:
                    for points in player.points:
                        points.fx += 5
                if keys[pygame.K_s]:
                    for points in player.points:
                        points.vx -= 0.003*points.vx

                deltatime = min(dt, 0.0006)

                ut.euler_integ(player, deltatime * 10)
                ut.euler_integ(rect1, deltatime * 10)



                ut.colider(player)
                ut.colider(rect1)
                ut.colider(floor)
                ut.colider(floor1)
                ut.colider(floor2)
                ut.colider(floor3)


                ut.collision(player, floor)
                ut.collision(rect1, floor)


                ut.collision(player, floor1)
                ut.collision(rect1, floor1)


                ut.collision(player, floor2)
                ut.collision(rect1, floor2)

                ut.collision(player, floor3)
                ut.collision(rect1, floor3)

                ut.collision(player, rect1)
                ut.collision(rect1, player)

                ut.collision(player, rect1)
                ut.collision(rect1, player)
                ut.collision(player, rect1)
                ut.collision(rect1, player)
                ut.collision(player, rect1)
                ut.collision(rect1, player)

                '''
                ut.euler_integ(b1, deltatime * 10)
                ut.euler_integ(b2, deltatime * 10)
                ut.euler_integ(b3, deltatime * 10)
                '''

                dt -= deltatime
            pygame.display.update()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()


if __name__ == "__main__":
    main()
