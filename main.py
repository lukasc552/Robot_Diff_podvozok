import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from robot import Robot

# parametre Diferencialneho podvozku
L = 0.2  # Rozchod [m] = 200mm
r = 0.05  # Polomer kolesa [m] = 50mm

time = [0, 5, 10, 15, 20]
# time_vector = [0, 5, 10, 17.5, 20]
# vel_L = [2, -1, 0, 2, 1]
# vel_R = [2, 1, 0, -2, 1]
dt = 0.01

# vel_L = [1.5, 2, 2, -2, 1]
# vel_R = [2, 2, 3, 2, 1]

vel_L = [2, -3, 3, 3, 1]
vel_R = [2, 1, 3, -1, 1]

r1 = 2.0
l1 = 2.0
r2 = 2.0


if __name__ == '__main__':
    robot = Robot(L, r)

    fig = plt.figure(1)
    subplot1 = fig.add_subplot(111)

    t, x, y, fi, right_wheel, left_wheel = robot.make_line(r1, l1, r2)
    # t, x, y, fi, right_wheel, left_wheel = robot.make_square(4)
    # t, x, y, fi, right_wheel, left_wheel = robot.move(time, vel_L, vel_R)
    # robot.draw_robot(subplot1)
    subplot1.plot(x, y)
    right_wheel_x = [item[0] for item in right_wheel]
    right_wheel_y = [item[1] for item in right_wheel]
    subplot1.plot(right_wheel_x, right_wheel_y, 'g')
    left_wheel_x = [item[0] for item in left_wheel]
    left_wheel_y = [item[1] for item in left_wheel]
    subplot1.plot(left_wheel_x, left_wheel_y, 'r')

    subplot1.grid()

    fig = plt.figure()
    robot.animate_movement(fig, t, x, y, right_wheel_x, right_wheel_y, left_wheel_x, left_wheel_y)

    plt.show()

