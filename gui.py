from tkinter import *
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
import robot


def split_to_vector(string):
    list = string.split(",")
    vector = []
    for i in list:
        vector.append(float(i))
    return vector


class Root(Tk):
    def __init__(self, robot):
        super(Root, self).__init__()
        self.minsize(400, 600)
        self.robot = robot
        self.num_fig = 1

        self.app_frame = Frames(self)
        self.work_panel()

    def work_panel(self):
        # uloha1
        self.time_entry = Entry(self.app_frame)
        self.time_entry.grid(row=2, column=2, sticky=W+E)
        self.vel_l_entry = Entry(self.app_frame)
        self.vel_l_entry.grid(row=3, column=2, sticky=W + E)
        self.vel_r_entry = Entry(self.app_frame)
        self.vel_r_entry.grid(row=4, column=2, sticky=W + E)

        draw1 = Button(self.app_frame, text='Vykresli', command=self.task1)
        draw1.grid(row=5, column=1)
        anim1 = Button(self.app_frame, text='Animuj', command=self.anim1)
        anim1.grid(row=5, column=2)

        # uloha2
        self.a_entry = Entry(self.app_frame)
        self.a_entry.grid(row=7, column=2, sticky=W + E)

        draw2 = Button(self.app_frame, text='Vykresli', command=self.task2)
        draw2.grid(row=8, column=1)
        anim2 = Button(self.app_frame, text='Animuj', command=self.anim2)
        anim2.grid(row=8, column=2)

        # uloha3
        self.r1_entry = Entry(self.app_frame)
        self.r1_entry.grid(row=10, column=2, sticky=W + E)
        self.l_entry = Entry(self.app_frame)
        self.l_entry.grid(row=11, column=2, sticky=W + E)
        self.r2_entry = Entry(self.app_frame)
        self.r2_entry.grid(row=12, column=2, sticky=W + E)

        draw3 = Button(self.app_frame, text='Vykresli', command=self.task3)
        draw3.grid(row=13, column=1)
        anim3 = Button(self.app_frame, text='Animuj', command=self.anim3)
        anim3.grid(row=13, column=2)
        Button(self.app_frame, text='HRA', command=self.hra).grid(row=2, column=3, rowspan=2)
        Button(self.app_frame, text='QUIT', command=self.quit).grid(row=14, column=1, columnspan=2)

    def hra(self):
        exec(open('game.py').read())

    def graf(self, t, x, y, fi, right_wheel, left_wheel):
        plt.figure(self.num_fig)
        self.num_fig += 1
        plt.plot(x, y)
        right_wheel_x = [item[0] for item in right_wheel]
        right_wheel_y = [item[1] for item in right_wheel]
        plt.plot(right_wheel_x, right_wheel_y, 'g')
        left_wheel_x = [item[0] for item in left_wheel]
        left_wheel_y = [item[1] for item in left_wheel]
        plt.plot(left_wheel_x, left_wheel_y, 'r')

        plt.grid()
        plt.show()

    def task1(self):
        time_vector = split_to_vector(self.time_entry.get())
        vl_vector = split_to_vector(self.time_entry.get())
        vr_vector = split_to_vector(self.time_entry.get())
        t, x, y, fi, right_wheel, left_wheel = self.robot.move(time_vector, vl_vector, vr_vector)
        self.graf(t, x, y, fi, right_wheel, left_wheel)

    def anim1(self):
        time_vector = split_to_vector(self.time_entry.get())
        vl_vector = split_to_vector(self.time_entry.get())
        vr_vector = split_to_vector(self.time_entry.get())
        t, x, y, fi, right_wheel, left_wheel = self.robot.move(time_vector, vl_vector, vr_vector)
        right_wheel_x = [item[0] for item in right_wheel]
        right_wheel_y = [item[1] for item in right_wheel]
        left_wheel_x = [item[0] for item in left_wheel]
        left_wheel_y = [item[1] for item in left_wheel]
        self.robot.animate_movement(t, x, y, right_wheel_x, right_wheel_y, left_wheel_x, left_wheel_y, saving=self.app_frame.checkbox_anim.get() == 1)

    def task2(self):
        a = float(self.a_entry.get())
        t, x, y, fi, right_wheel, left_wheel = self.robot.make_square(a)
        self.graf(t, x, y, fi, right_wheel, left_wheel)

    def anim2(self):
        a = float(self.a_entry.get())
        t, x, y, fi, right_wheel, left_wheel = self.robot.make_square(a)
        right_wheel_x = [item[0] for item in right_wheel]
        right_wheel_y = [item[1] for item in right_wheel]
        left_wheel_x = [item[0] for item in left_wheel]
        left_wheel_y = [item[1] for item in left_wheel]
        self.robot.animate_movement(t, x, y, right_wheel_x, right_wheel_y, left_wheel_x, left_wheel_y, saving=self.app_frame.checkbox_anim.get() == 1)

    def task3(self):
        r1 = float(self.r1_entry.get())
        l1 = float(self.l_entry.get())
        r2 = float(self.r2_entry.get())
        t, x, y, fi, right_wheel, left_wheel = self.robot.make_line(r1, l1, r2)
        self.graf(t, x, y, fi, right_wheel, left_wheel)

    def anim3(self):
        r1 = float(self.r1_entry.get())
        l1 = float(self.l_entry.get())
        r2 = float(self.r2_entry.get())
        t, x, y, fi, right_wheel, left_wheel = self.robot.make_line(r1, l1, r2)
        right_wheel_x = [item[0] for item in right_wheel]
        right_wheel_y = [item[1] for item in right_wheel]
        left_wheel_x = [item[0] for item in left_wheel]
        left_wheel_y = [item[1] for item in left_wheel]
        # if self.app_frame.checkbox_anim.get() == 1:

        self.robot.animate_movement(t, x, y, right_wheel_x, right_wheel_y, left_wheel_x, left_wheel_y, saving=self.app_frame.checkbox_anim.get() == 1)


class Frames(Frame):
    def __init__(self, master=None):
        super(Frames, self).__init__(master)
        self.master = master

        self.checkbox_anim = IntVar()

        self.unitUI()

    def unitUI(self):
        self.master.title("ROB: Zadanie 3")
        self.pack(side=LEFT, fill=BOTH, expand=True)

        self.columnconfigure(1, pad=2)
        self.columnconfigure(2, pad=2)
        self.columnconfigure(3, pad=2)
        self.columnconfigure(4, pad=2)

        self.rowconfigure(1, pad=5)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)
        self.rowconfigure(5, pad=5)
        self.rowconfigure(6, pad=5)
        self.rowconfigure(7, pad=5)
        self.rowconfigure(8, pad=5)
        self.rowconfigure(9, pad=5)
        self.rowconfigure(10, pad=5)
        self.rowconfigure(11, pad=5)
        self.rowconfigure(12, pad=5)
        self.rowconfigure(13, pad=5)
        self.rowconfigure(14, pad=5)

        Label(self, text="Vykreslenie trajektorie podla preddefinovanych rychlosti").grid(row=1, column=1, columnspan=2, sticky=W + E)
        Label(self, text="Time vec.").grid(row=2, column=1, sticky=W + E)
        Label(self, text="Lavy vec.").grid(row=3, column=1, sticky=W + E)
        Label(self, text="Pravy vec.").grid(row=4, column=1, sticky=W + E)

        Label(self, text="Vykreslenie kocky taziskom podvozku").grid(row=6, column=1, columnspan=2,
                                                                     sticky=W + E)
        Label(self, text="Strana kocky").grid(row=7, column=1, sticky=W + E)

        Label(self, text="Vykreslenie trajektorie krivky").grid(row=9, column=1, columnspan=2,
                                                                sticky=W + E)
        Label(self, text="R1").grid(row=10, column=1, sticky=W + E)
        Label(self, text="L").grid(row=11, column=1, sticky=W + E)
        Label(self, text="R2").grid(row=12, column=1, sticky=W + E)
        Checkbutton(self, text='Save to .mp4', variable=self.checkbox_anim, onvalue=1, offvalue=0).grid(row=14, column=3, padx=0,
                                                                                          pady=0, sticky=W + E)




