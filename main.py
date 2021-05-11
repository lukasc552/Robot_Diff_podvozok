import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from robot import Robot
from gui import Root

# parametre Diferencialneho podvozku
L = 0.2  # Rozchod [m] = 200mm
r = 0.05  # Polomer kolesa [m] = 50mm

dt = 0.01

# time = [0, 5, 10, 15, 20]
# vel_L = [2, -1, 0, 2, 1]
# vel_R = [2, 1, 0, -2, 1]
#
# r1 = 2.0
# l1 = 1.0
# r2 = 2.0


if __name__ == '__main__':
    robot = Robot(L, r)
    root = Root(robot)

    root.mainloop()

