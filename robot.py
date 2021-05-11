import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame


def truncate(n, decimals=0):  # zaokruhlenie cisel
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


class Robot:
    def __init__(self, L, radius):
        self.L = L
        self.r = radius
        self.wheel_width = 0.025  # 2.5cm
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.phi = np.pi/2
        self.mid_right_wheel = self.calc_right_mid()
        self.mid_left_wheel = self.calc_left_mid()
        self.vel_r = 0.0
        self.vel_l = 0.0
        self.vel_t = 0.0
        self.omega = 0.0
        self.anim_num = 1

    #  Uloha 1
    def move(self, time_vector, vel_l, vel_r, step=0.01):
        out_x = [self.pos_x]
        out_y = [self.pos_y]
        out_phi = [self.phi]
        out_right = [self.mid_right_wheel]
        out_left = [self.mid_left_wheel]

        idx = 0
        temp_t = time_vector[0]
        out_t = [temp_t]
        for t in range(1, len(time_vector)):
            while temp_t <= time_vector[t]:

                self.vel_l = vel_l[t - 1]
                self.vel_r = vel_r[t - 1]
                self.vel_t = self.calc_vt()
                self.omega = self.calc_omega()

                v_x = self.vel_t * np.cos(self.phi)
                v_y = self.vel_t * np.sin(self.phi)

                delta_x_t = v_x * step
                delta_y_t = v_y * step

                self.pos_x = self.pos_x + delta_x_t
                self.pos_y = self.pos_y + delta_y_t

                delta_phi = self.omega * step
                self.phi = self.phi + delta_phi

                if self.phi > 2 * np.pi:
                    self.phi = self.phi % (2 * np.pi)
                elif self.phi < -2 * np.pi:
                    self.phi = self.phi % (2 * np.pi)

                out_x.append(self.pos_x)
                out_y.append(self.pos_y)
                out_phi.append(self.phi)
                out_right.append(self.calc_right_mid())
                out_left.append(self.calc_left_mid())

                out_t.append(temp_t)
                temp_t += step
                idx += 1
        self.mid_right_wheel = out_right[-1]
        self.mid_left_wheel = out_left[-1]
        return out_t, out_x, out_y, out_phi, out_right, out_left

    #  Uloha 2
    def make_square(self, a):
        vl = [1, 1, 1, 1, 1, 1, 1, 1]
        vr = [1, -1, 1, -1, 1, -1, 1, -1]
        t = [0]
        angle = np.pi/2
        t_omega = 0.0
        t_v = 0.0
        for i in range(7):
            akt_vl = vl[i]
            akt_vr = vr[i]
            v_t = (akt_vr + akt_vl)/2
            omega_t = (akt_vr - akt_vl)/self.L
            if omega_t == 0:
                t_v = a/v_t
                t.append(t[-1] + t_v)
            else:
                t_omega = angle/omega_t
                t.append(t[-1] + abs(truncate(t_omega, 4)))

        t.append(t[-1] + abs(truncate(t_omega, 4)))
        time, x, y, fi, right_wheel, left_wheel = self.move(t, vl, vr, 0.0001)
        return time, x, y, fi, right_wheel, left_wheel

    #  Uloha 3
    def make_line(self, r1, l1, r2):
        vl = [1, 1, 1]
        vr1 = self.calc_vr_via_vl(-r1, vl[0])
        vr2 = 1
        vr3 = self.calc_vr_via_vl(r2, vl[2])
        vr = [vr1, vr2, vr3]
        t = [0]
        angle = np.pi/2
        for i in [0, 1, 2]:
            akt_vr = vr[i]
            akt_vl = vl[i]
            omega_t = (akt_vr - akt_vl)/self.L
            v_t = (akt_vr + akt_vl)/2
            if omega_t == 0:
                t_v = l1 / v_t
                t.append(t[-1] + t_v)
            else:
                t_omega = angle / omega_t
                t.append(t[-1] + abs(truncate(t_omega, 4)))

        time, x, y, fi, right_wheel, left_wheel = self.move(t, vl, vr, 0.0001)
        return time, x, y, fi, right_wheel, left_wheel

    def animate_movement(self, t, x, y, rx, ry, lx, ly, saving=False):
        every = 100
        temp_x = x[0::every]
        temp_y = y[0::every]
        temp_rx = rx[0::every]
        temp_ry = ry[0::every]
        temp_lx = lx[0::every]
        temp_ly = ly[0::every]

        fig = plt.figure()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(min(temp_x)-0.2, max(temp_x)+0.2), ylim=(min(temp_y)-0.2, max(temp_y)+0.2))
        ax.grid()
        line, = ax.plot([], [], 'b-', lw=2, label='Tazisko')
        line_l, = ax.plot([], [], 'r-', lw=2, label='Lave koleso')
        line_r, = ax.plot([], [], 'g-', lw=2, label='Prave koleso')
        ax.legend()
        thisx = []
        thisy = []
        l_x = []
        l_y = []
        r_x = []
        r_y = []

        def init():
            line.set_data([], [])
            line_l.set_data([], [])
            line_r.set_data([], [])
            return line, line_l, line_r,

        def animate(i):
            thisx.append(temp_x[i])
            thisy.append(temp_y[i])
            l_x.append(temp_lx[i])
            l_y.append(temp_ly[i])
            r_x.append(temp_rx[i])
            r_y.append(temp_ry[i])

            line.set_data(thisx, thisy)
            line_l.set_data(l_x, l_y)
            line_r.set_data(r_x, r_y)
            return line, line_l, line_r,

        ani = animation.FuncAnimation(fig, animate, np.arange(1, len(temp_x)), interval=0.1, blit=True, init_func=init)

        if saving:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=30, metadata=dict(artist='Lukas'), bitrate=1800)

            ani.save('Animations/' + 'animacia' + '_{}'.format(self.anim_num) + '.mp4', writer=writer)
            self.anim_num += 1

        plt.show()

    def calc_vr_via_vl(self, R, vl):  # vypocet rychlosti praveho kolesa ked pozname rychlost laveho a polomer otacania
        vr = vl*((2*R + self.L)/(2*R - self.L))
        return vr

    def calc_vl_via_vr(self, R, vr):  # vypocet rychlosti laveho kolesa ked pozname rychlost praveho a polomer otacania
        vl = vr*((2*R - self.L)/(2*R + self.L))
        return vl

    def calc_vr(self, R):  # vypocet rychlosti praveho kolesa ked pozname rychlost laveho a polomer otacania
        self.vel_r = self.vel_l*((2*R + self.L)/(2*R - self.L))
        return self.vel_r

    def calc_R_icr(self):
        return (self.L/2) * (self.vel_r + self.vel_l)/(self.vel_r - self.vel_l)

    def calc_vt(self):
        return (self.vel_r + self.vel_l)/2

    def calc_omega(self):
        return (self.vel_r - self.vel_l)/self.L

    def calc_right_mid(self):
        x = (self.L / 2 + self.wheel_width / 2) * np.sin(self.phi)
        y = (self.L / 2 + self.wheel_width / 2) * np.cos(self.phi)
        xy = [self.pos_x + x, self.pos_y - y]
        return xy

    def calc_left_mid(self):
        x = (self.L/2 + self.wheel_width/2) * np.sin(self.phi)
        y = (self.L/2 + self.wheel_width/2) * np.cos(self.phi)
        xy = [self.pos_x - x, self.pos_y + y]
        return xy

    def draw_robot(self, figure, new_fi=None):
        if new_fi is not None:
            self.phi = new_fi

        poloos = self.L/2

        inner_x = poloos * np.sin(self.phi)
        inner_y = poloos * np.cos(self.phi)
        inner_l_coords = [self.pos_x-inner_x, self.pos_y + inner_y]
        inner_r_coords = [self.pos_x + inner_x, self.pos_y - inner_y]

        outer_x = (poloos + self.wheel_width) * np.sin(self.phi)
        outer_y = (poloos + self.wheel_width) * np.cos(self.phi)
        outer_l_coords = [self.pos_x - outer_x, self.pos_y + outer_y]
        outer_r_coords = [self.pos_x + outer_x, self.pos_y - outer_y]

        #  Zvyraznenie taziska
        # figure.plot([self.pos_x], [self.pos_y], 'ko', markersize=8)

        # Hlavna os
        figure.plot([inner_r_coords[0], inner_l_coords[0]], [inner_r_coords[1], inner_l_coords[1]], 'k-')

        # Lave koleso
        temp_x1 = self.r * np.cos(self.phi)
        temp_y1 = self.r * np.sin(self.phi)

        left_urx = inner_l_coords[0] + temp_x1
        left_ury = inner_l_coords[1] + temp_y1
        left_ur = [left_urx, left_ury]

        left_lrx = inner_l_coords[0] - temp_x1
        left_lry = inner_l_coords[1] - temp_y1
        left_lr = [left_lrx, left_lry]

        left_ulx = outer_l_coords[0] + temp_x1
        left_uly = outer_l_coords[1] + temp_y1
        left_ul = [left_ulx, left_uly]

        left_llx = outer_l_coords[0] - temp_x1
        left_lly = outer_l_coords[1] - temp_y1
        left_ll = [left_llx, left_lly]
        self.draw_wheel(figure, left_ul, left_ll, left_lr, left_ur)

        # Prave koleso

        right_urx = outer_r_coords[0] + temp_x1
        right_ury = outer_r_coords[1] + temp_y1
        right_ur = [right_urx, right_ury]

        right_lrx = outer_r_coords[0] - temp_x1
        right_lry = outer_r_coords[1] - temp_y1
        right_lr = [right_lrx, right_lry]

        right_ulx = inner_r_coords[0] + temp_x1
        right_uly = inner_r_coords[1] + temp_y1
        right_ul = [right_ulx, right_uly]

        right_llx = inner_r_coords[0] - temp_x1
        right_lly = inner_r_coords[1] - temp_y1
        right_ll = [right_llx, right_lly]
        self.draw_wheel(figure, right_ul, right_ll, right_lr, right_ur)

    @staticmethod
    def draw_wheel(figure, upper_left, lower_left, lower_right, upper_right):
        figure.plot([upper_left[0], lower_left[0], lower_right[0], upper_right[0], upper_left[0]], [upper_left[1], lower_left[1], lower_right[1], upper_right[1], upper_left[1]], 'k-')  # linewidth=3

    def calc_pos_to_game(self):
        step = 0.5
        self.vel_t = self.calc_vt()
        self.omega = self.calc_omega()

        v_x = self.vel_t * np.cos(self.phi)
        v_y = self.vel_t * np.sin(self.phi)

        delta_x_t = v_x * step
        delta_y_t = v_y * step

        self.pos_x = self.pos_x + delta_x_t
        self.pos_y = self.pos_y + delta_y_t

        delta_phi = self.omega * step
        self.phi = self.phi + delta_phi

        if self.phi > 2*np.pi:
            self.phi = self.phi % (2*np.pi)
        elif self.phi < -2*np.pi:
            self.phi = self.phi % (2*np.pi)

    def draw_to_game(self, surface, mierka):
        black = (0, 0, 0)
        poloos = self.L * mierka / 2

        inner_x = poloos * np.sin(self.phi)
        inner_y = poloos * np.cos(self.phi)
        inner_l_coords = [self.pos_x + inner_x, self.pos_y - inner_y]
        inner_r_coords = [self.pos_x - inner_x, self.pos_y + inner_y]

        outer_x = (poloos + self.wheel_width * mierka) * np.sin(self.phi)
        outer_y = (poloos + self.wheel_width * mierka) * np.cos(self.phi)
        outer_l_coords = [self.pos_x + outer_x, self.pos_y - outer_y]
        outer_r_coords = [self.pos_x - outer_x, self.pos_y + outer_y]

        pygame.draw.line(surface, black, inner_l_coords, inner_r_coords, 4)

        pygame.draw.circle(surface, black, [self.pos_x, self.pos_y], 6)

        # kolesa
        # Lave koleso
        temp_x1 = self.r * mierka * np.cos(self.phi)
        temp_y1 = self.r * mierka * np.sin(self.phi)

        left_urx = inner_l_coords[0] + temp_x1
        left_ury = inner_l_coords[1] + temp_y1

        left_lrx = inner_l_coords[0] - temp_x1
        left_lry = inner_l_coords[1] - temp_y1

        left_ulx = outer_l_coords[0] + temp_x1
        left_uly = outer_l_coords[1] + temp_y1

        left_llx = outer_l_coords[0] - temp_x1
        left_lly = outer_l_coords[1] - temp_y1

        # Prave koleso
        right_urx = outer_r_coords[0] + temp_x1
        right_ury = outer_r_coords[1] + temp_y1

        right_lrx = outer_r_coords[0] - temp_x1
        right_lry = outer_r_coords[1] - temp_y1

        right_ulx = inner_r_coords[0] + temp_x1
        right_uly = inner_r_coords[1] + temp_y1

        right_llx = inner_r_coords[0] - temp_x1
        right_lly = inner_r_coords[1] - temp_y1

        scatter_l = []
        scatter_l.append((left_urx, left_ury))
        scatter_l.append((left_lrx, left_lry))
        scatter_l.append((left_llx, left_lly))
        scatter_l.append((left_ulx, left_uly))

        scatter_r = []
        scatter_r.append((right_urx, right_ury))
        scatter_r.append((right_lrx, right_lry))
        scatter_r.append((right_llx, right_lly))
        scatter_r.append((right_ulx, right_uly))

        pygame.draw.lines(surface, black, True, scatter_l, 4)
        pygame.draw.lines(surface, black, True, scatter_r, 4)

        # smer otocenia v hre
        # green = (0, 255, 0)
        # l_sipka = 50
        # x_sipka = self.pos_x + (l_sipka * np.cos(self.phi))
        # y_sipka = self.pos_y + (l_sipka * np.sin(self.phi))
        # pygame.draw.line(surface, (0, 255, 0), [self.pos_x, self.pos_y], [x_sipka, y_sipka], 4)

