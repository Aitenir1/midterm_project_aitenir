import cv2
import tkinter as tk
import random
from copy import deepcopy


class Life:
    def __init__(self, n, m, width, height, c, image=None, color='BLack'):
        self.width = width
        self.height = height
        self.n = n
        self.m = m
        self.c = c
        self.c.bind('<Button-1>', self.click)
        self.is_clicked = False
        self.matrix = None
        self.image = image
        self.upload_image()

        self.color = color

    def upload_image(self):
        if self.image is None:
            for i in range(self.n):
                row = []
                for j in range(self.m):
                    row.append(random.choice([0, 1]))
                self.matrix.append(row)
        else:
            try:
                uploaded_image = cv2.imread(self.image)
                image_black_white = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

                matrix = cv2.resize(image_black_white, (self.n, self.m), interpolation=cv2.INTER_LINEAR)
                matrix[matrix < 128] = 1
                matrix[matrix >= 128] = 0
                self.matrix = matrix

            except cv2.error:
                raise Exception('No such file')

    def display(self):
        for i in self.matrix:
            print(' '.join(map(str, i)))
        print()

    def count_adj(self, i, j, matrix_clone):
        nn = 0
        i_up, i_do, j_le, j_ra = i - 1, i + 1, j - 1, j + 1
        if i == 0:
            i_up = self.n - 1
        if i == self.n - 1:
            i_do = 0
        if j == 0:
            j_le = self.m - 1
        if j == self.m - 1:
            j_ra = 0

        nn += matrix_clone[i_up][j]
        nn += matrix_clone[i_up][j_ra]
        nn += matrix_clone[i][j_ra]
        nn += matrix_clone[i_do][j_ra]
        nn += matrix_clone[i_do][j]
        nn += matrix_clone[i_do][j_le]
        nn += matrix_clone[i][j_le]
        nn += matrix_clone[i_up][j_le]

        return nn

    def __step(self):
        matrix_clone = deepcopy(self.matrix)

        for i in range(self.n):
            for j in range(self.m):
                nn = self.count_adj(i, j, matrix_clone)

                if nn not in (2, 3):
                    self.matrix[i][j] = 0
                elif nn == 3:
                    self.matrix[i][j] = 1

    def draw(self):
        self.c.delete('all')
        size_width = self.width / self.m
        size_height = self.height / self.n
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i][j]:
                    color = self.color
                else:
                    color = "white"
                self.c.create_rectangle(j * size_width, i * size_height, (j+1) * size_width, (i+1) * size_height, fill=color, outline='')

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, n):
        if n not in range(5, 301):
            raise Exception('The number of rows should be in the range of 5-100')
        self.__n = n  # Private variable

    @property
    def m(self):
        return self.__m

    @m.setter
    def m(self, m):
        if m not in range(5, 301):
            raise Exception('The number of columns should be in the range of 5-100')
        self.__m = m  # Private variable

    def click(self, event):
        self.is_clicked = True

    def run(self):
        if not self.is_clicked:
            self.draw()
        else:
            self.__step()
            self.draw()
        self.c.after(300, self.run)


master = tk.Tk()
master.geometry('1080x1080')

canvas = tk.Canvas(master, width=900, height=900)
canvas.pack()

# number_of_rows = int(input('Enter number of rows: '))
# # number_of_cols = int(input('Enter number of columns: '))
#

game = Life(100, 100, 900, 900, canvas, 'media/image4.jpeg', 'black')

game.display()
game.run()

master.mainloop()