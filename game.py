import pygame
import robot
import numpy as np

# nastavovacky
width_window = 800
height_window = 800
SIZE = (width_window, height_window)
fps = 30
x_offset = int(width_window/2)
y_offset = int(height_window/2)
start_point = (x_offset, y_offset)

white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
vr = 0
vl = 0

L = 0.2
r = 0.05
robot = robot.Robot(L, r)
robot.pos_x = x_offset
robot.pos_y = y_offset
robot.vel_r = 0.0
robot.vel_l = 0.0
robot.phi = -np.pi/2

mierka = 1000
vel_drive = 10.0
vel_stop = 0.0

while True:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        robot.vel_r = vel_drive
        robot.vel_l = -vel_drive
    elif keys[pygame.K_RIGHT]:
        robot.vel_r = -vel_drive
        robot.vel_l = vel_drive
    elif keys[pygame.K_UP]:
        robot.vel_r = vel_drive
        robot.vel_l = vel_drive
    elif keys[pygame.K_DOWN]:
        robot.vel_r = -vel_drive
        robot.vel_l = -vel_drive
    else:
        robot.vel_r = vel_stop
        robot.vel_l = vel_stop

    robot.calc_pos_to_game()
    robot.draw_to_game(screen, mierka)

    pygame.display.update()
    clock.tick(fps)



