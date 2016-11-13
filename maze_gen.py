# -*- coding: utf-8 -*-
import random
import uuid

from tkinter import *
from tkinter import ttk

CELL_SIZE = 15
FIELD_SIZE = 1000
CELLS_IN_ROW = round(FIELD_SIZE / CELL_SIZE)


def first_or_default(list_for_filtering, predicate):
    return next((f for f in list_for_filtering if predicate(f)), None)


def get_random_value(adjancy, visited_cells_ids, key):
    non_visited = [cellId for cellId in adjancy.get(key, []) if cellId not in visited_cells_ids]
    if len(non_visited) == 0:
        return None
    return random.choice(non_visited)


def get_cell(index, cells):
    return first_or_default(cells, lambda x: x.index == index)


class Line(object):
    def __init__(self, x0, y0, x1, y1, name):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.name = name


#
#      N
# E         W
#      S
class Cell(object):
    def __init__(self, x, y, width, height, name, index):
        line_n = Line(x, y, x + width, y, 'N')
        line_w = Line(x + width, y, x + width, y + height, 'W')
        line_e = Line(x, y, x, y + height, 'E')
        line_s = Line(x, y + height, x + width, y + height, 'S')
        lines = [line_n, line_w, line_e, line_s]
        self.name = name
        self.index = index
        self.lines = lines
        self.x = x
        self.y = y
        self.borders = {'N', 'W', 'E', 'S'}

    def __repr__(self):
        return str(self.index)

    def draw(self, canvas):
        # canvas.create_text(self.x + 10, self.y + 10, text=self.index, width=20, font=("Arial", "6"))
        fill = "blue"
        for line in [l for l in self.lines if l.name in self.borders]:
            # if len(self.borders) == 3:
            #     fill = "blue"
            # elif len(self.borders) == 2:
            #     fill = "green"
            # elif len(self.borders) == 1:
            #     fill = "red"
            # elif len(self.borders) == 0:
            #     fill = "yellow"
            # else:
            #     fill = "purple"
            canvas.create_line(line.x0, line.y0, line.x1, line.y1, fill=fill)

    def __hash__(self):
        return self.index


def generate_cells(width, height):
    index = 0
    cells = []
    adjency_dict = {}
    for i in [x for x in range(0, width, CELL_SIZE)]:
        for j in [x for x in range(0, height, CELL_SIZE)]:
            c = Cell(j, i, CELL_SIZE, CELL_SIZE, str.format("%s %s" % (j, i)), index)
            already_added = adjency_dict.get(index, [])

            if i > 0:
                next_cell_id = index - CELLS_IN_ROW
                already_added.append(next_cell_id)
                already_added2 = adjency_dict.get(next_cell_id, [])
                already_added2.append(index)
                adjency_dict[next_cell_id] = already_added2
            if j > 0:
                next_cell_id = index - 1
                already_added.append(next_cell_id)
                already_added2 = adjency_dict.get(next_cell_id, [])
                already_added2.append(index)
                adjency_dict[next_cell_id] = already_added2

            adjency_dict[index] = already_added
            cells.append(c)
            index += 1

    return cells, adjency_dict


def draw_edge(canvas, from_cell, to_cell):
    canvas.create_line(from_cell.x + CELL_SIZE * 0.5, from_cell.y + CELL_SIZE * 0.5, to_cell.x + 5, to_cell.y + 5)


def draw_cells(canvas, cells):
    for cell in cells:
        cell.draw(canvas)
        # for (from_index, to_index) in edge_list:
        #     from_cell = get_cell(from_index, cells)
        #     to_cell = get_cell(to_index, cells)
        #     if to_cell is not None and from_cell is not None:
        #         draw_edge(canvas, from_cell, to_cell)


def get_direction(start, to):
    if abs(start.index - to.index) == CELLS_IN_ROW:
        if start.index > to.index:
            symbol = 'N'
            symbol_to = 'S'
        else:
            symbol = 'S'
            symbol_to = 'N'
    else:
        if start.index > to.index:
            symbol = 'E'
            symbol_to = 'W'
        else:
            symbol = 'W'
            symbol_to = 'E'
    return symbol, symbol_to


def generate_maze(cells, adjency_dict):
    fst = random.choice(cells)
    candidates = [fst]
    visited = {fst.index}

    while len(candidates) > 0:
        start = random.choice(candidates)
        next_cell_id = get_random_value(adjency_dict, visited_cells_ids=visited, key=start.index)
        if next_cell_id is not None:
            cell_to = cells[next_cell_id]
            candidates.append(cell_to)
            visited.add(cell_to.index)
            used_direction, dir_to = get_direction(start, cell_to)
            start.borders.remove(used_direction)
            cell_to.borders.remove(dir_to)
        else:
            candidates.remove(start)


def serialize(cells):
    guid = uuid.uuid1()

    f = open(str(guid) + '.xml', mode='w', encoding='utf-8')
    f.write('<cells>\n')
    for c in cells:
        f.write("<cell>\n")
        f.write("<lines>\n")

        for line in [l for l in c.lines if l.name in c.borders]:
            f.write("<line>"+ "\n")
            f.write("<name>\n")
            f.write(line.name+ "\n")
            f.write("</name>\n")
            if line.name in c.borders:
                f.write("<x0>\n")
                f.write(str(line.x0) + "\n")
                f.write("</x0>\n")

                f.write("<x1>\n")
                f.write(str(line.x1) + "\n")
                f.write("</x1>\n")

                f.write("<y0>\n")
                f.write(str(line.y0) + "\n")
                f.write("</y0>\n")

                f.write("<y1>\n")
                f.write(str(line.y1) + "\n")
                f.write("</y1>\n")
            f.write("</line>"+ "\n")
        f.write("</lines>\n")
        f.write("</cell>\n")
    f.write('</cells>\n')


def main():
    random.seed()
    root = Tk("caption")
    root.geometry('{}x{}'.format(FIELD_SIZE, FIELD_SIZE))
    mainframe = ttk.Frame(root, padding="3 3 3 3")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    canvas = Canvas(mainframe, width=FIELD_SIZE, height=FIELD_SIZE)
    # start = time.time()

    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    (cells, adjancy_dict) = generate_cells(FIELD_SIZE, FIELD_SIZE)
    generate_maze(cells, adjancy_dict)
    draw_cells(canvas, cells)
    serialize(cells)
    # end = time.time()
    # print(end - start)

    root.mainloop()


main()
