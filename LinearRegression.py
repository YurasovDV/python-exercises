# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk

FIELD_SIZE_X = 1000
FIELD_SIZE_Y = 700


class PointList:
    points = []


class Transformer:
    def __init__(self, point_list):
        def transform_x(x):
            return FIELD_SIZE_X * (x - point_list.x_min) / (point_list.x_max - point_list.x_min)

        def transform_y(y):
            return FIELD_SIZE_Y * (
                1 - ((y - point_list.y_min) / (point_list.y_max - point_list.y_min)))

        self.transform_x = transform_x
        self.transform_y = transform_y

    def transform(self, x, y):
        return self.transform_x(x), self.transform_y(y)


def prepare_data(path):
    file = open(path, 'r')
    data = file.read().split('\n')
    xs = []
    ys = []
    x_min = 10
    y_min = 10
    y_max = -10
    x_max = -10
    x_average = 0
    y_average = 0

    for pair in data:
        words = pair.split(',')
        try:
            y_cur = float(words[0])
            x_cur = float(words[1])
            x_average += x_cur
            y_average += y_cur
            if x_cur > x_max:
                x_max = x_cur
            if x_cur < x_min:
                x_min = x_cur

            if y_cur > y_max:
                y_max = y_cur
            if y_cur < y_min:
                y_min = y_cur

            ys.append(y_cur)
            xs.append(x_cur)
        except ValueError:
            continue
    file.close()
    n = len(xs)
    result = PointList()
    result.size = n
    y_average /= n
    ys_new = []
    for y_cur in ys:
        if abs(y_cur - y_average) > 0.4:
            ys_new.append(y_average)
        else:
            ys_new.append(y_cur)

    y_average = sum(ys_new)
    result.points = list(zip(xs, ys_new))
    result.x_max = x_max
    result.x_min = x_min
    result.y_max = y_max
    result.y_min = y_min
    if n != 0:
        x_average /= n
        y_average /= n

    result.x_average = x_average
    result.y_average = y_average
    # print(y_average)
    return result


def draw_points(canvas, point_list):
    tr = Transformer(point_list)
    for p in point_list.points:
        x, y = tr.transform(p[0], p[1])
        canvas.create_rectangle((x, y, x + 5, y + 5), fill="blue")


# y = ax + b
def get_equation(point_list):
    n = point_list.size
    if n == 0:
        return
    ch = sum(map(lambda pair_x_y: pair_x_y[0] * pair_x_y[1], point_list.points)) / float(n)
    ch -= point_list.x_average * point_list.y_average
    zn = sum(map(lambda pair_x_y: pair_x_y[0] * pair_x_y[0], point_list.points)) / float(n) - point_list.x_average ** 2
    b = ch / zn

    a = point_list.y_average - b * point_list.x_average
    # ch = sum(map(lambda pair_x_y: pair_x_y[0] * pair_x_y[1], point_list.points)) / n * -point_list.x_average
    # ch += point_list.y_average * sum(map(lambda pair_x_y: pair_x_y[0] * pair_x_y[0], point_list.points)) / n
    # a = ch / zn
    # print(a)

    def equation(x):
        return a + b * x

    # print("a = %s b = %s" % (a, b))
    # print("y_av = %s x_av = %s" % (point_list.y_average, point_list.x_average))
    return equation


def draw_regression(canvas, point_list):
    funfordraw = get_equation(point_list)
    y0 = funfordraw(point_list.x_min)
    y1 = funfordraw(point_list.x_max)
    tr = Transformer(point_list)
    x0, y0 = tr.transform(point_list.x_min, y0)
    x1, y1 = tr.transform(point_list.x_max, y1)

    canvas.create_line(x0, y0, x1, y1, fill="red")


def main():
    canvas, root = create_window()
    pairs = prepare_data('bread.txt')
    draw_points(canvas, pairs)
    draw_regression(canvas, pairs)
    root.mainloop()


def create_window():
    root = Tk("caption")
    root.geometry('{}x{}'.format(FIELD_SIZE_X, FIELD_SIZE_Y))
    mainframe = ttk.Frame(root, padding="3 3 3 3")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    canvas = Canvas(mainframe, width=FIELD_SIZE_X, height=FIELD_SIZE_Y)
    # start = time.time()

    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    return canvas, root


main()
