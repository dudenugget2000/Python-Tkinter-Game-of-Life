# Conway's Game of Life by Eli Levine
# Rules for each next generation:
# 1. Any live cell with fewer than two live neighbors dies, as if by
# underpopulation.
# 2. Any live cell with two or three live neighbors lives on to the next
# generation.
# 3. Any live cell with more than three live neighbors dies, as if by
# overpopulation.
# 4. Any dead cell with exactly three live neighbors becomes a live cell, as if
# by reproduction.
from tkinter import (Frame, Tk, Label, Button, TOP, BOTTOM, SUNKEN, W, E,
                     DISABLED, NORMAL)
from tkinter import font
import random


# GameOfLife --> Subclass of Tkinter Frame
class GameOfLife(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.grid(row=0, column=0)

        # max coord lengths of grid
        self.max_x = 40
        self.max_y = 28

        # creates list of cell_buttons (cell_buttons are the cells)
        self.cell_buttons = []

        # boolean telling whether the program should or should not continue
        # to advancing generations
        self.generate_next = True

        # for inheritance purposes
        self.parent = parent

        self.initUI()

    def initUI(self):

        self.parent.title("Game of Life")

        # frame for title and line of instruction
        self.title_frame = Frame(self.parent)
        self.title_frame.grid(row=0, column=0, columnspan=20)

        self.titleFont = font.Font(family="Helvetica", size=14)
        title = Label(self.title_frame,
                      text="Conway's Game of Life", font=self.titleFont)
        title.pack(side=TOP)

        prompt = Label(
            self.title_frame, text="Click the cells to create your starting config, then press Start Game:")
        prompt.pack(side=BOTTOM)

        # creates grid of buttons for starting configuration
        self.create_grid()

        # creates a button to start the simulation
        self.start_button = Button(
            self.parent, text="Start Game", command=self.simulate_game)
        self.start_button.grid(row=1, column=1, sticky=W)

        # resets the game
        self.reset_button = Button(
            self.parent, text="Reset", state=DISABLED, command=self.reset_game)
        self.reset_button.grid(row=1, column=2, sticky=W)

        # creates a glider
        self.glider_button = Button(
            self.parent, text="Glider", command= lambda: self.glider())
        self.glider_button.grid(row=1, column=3, sticky=W)

        # randomizes board
        self.random_button = Button(
            self.parent, text="Randomize", command = lambda: self.randomize())
        self.random_button.grid(row=1, column=0, sticky=W)

        # creates a blinker
        self.blinker_button = Button(
            self.parent, text="Blinker", command = lambda: self.blinker())
        self.blinker_button.grid(row=0, column=3, sticky=W)

        # creates a toad
        self.toad_button = Button(
            self.parent, text="Toad", command = lambda: self.toad())
        self.toad_button.grid(row=0, column=0, sticky=W)

    # initializes the grid of cells
    def create_grid(self):

        # creates frame for the cell grid
        self.game_frame = Frame(
            self.parent, width=self.max_x + 2, height=self.max_y + 2, borderwidth=1, relief=SUNKEN)
        self.game_frame.grid(row=2, column=0, columnspan=4)

        # instantiates buttons for choosing initial configuration
        self.cell_buttons = [[Button(self.game_frame, bg="white", width=2, height=1) for i in range(
            self.max_x + 2)] for j in range(self.max_y + 2)]
        # creates 2d array of buttons for grid
        for i in range(1, self.max_y + 1):
            for j in range(1, self.max_x + 1):
                self.cell_buttons[i][j].grid(row=i, column=j, sticky=W + E)
                # simple lambda function that set's the command of each cell
                # button to toggle the current state of said cell
                # Alive --> Dead
                # Dead --> Alive
                self.cell_buttons[i][j]['command'] = lambda i=i, j=j: self.cell_toggle(
                    self.cell_buttons[i][j])

    def simulate_game(self):
        # buttons are disabled once the simulation starts playing
        self.disable_buttons()
        # creates list of buttons in grid to toggle
        buttons_to_toggle = []
        for i in range(1, self.max_y + 1):
            for j in range(1, self.max_x + 1):
                coord = (i, j)
                # if cell = dead and has 3 neighbors, add coordinates to list of
                # coords to toggle (turn from dead --> alive)
                if self.cell_buttons[i][j]['bg'] == "white" and self.neighbor_count(i, j) == 3:
                    buttons_to_toggle.append(coord)
                # if cell = alive and does not have 2/3 neighbor cells, add
                # coordinates to list of coords to toggle
                # (turn from alive --> dead)
                elif self.cell_buttons[i][j]['bg'] == "black" and self.neighbor_count(i, j) != 3 and self.neighbor_count(i, j) != 2:
                    buttons_to_toggle.append(coord)

        # updates (toggles) the cells on the grid
        for coord in buttons_to_toggle:
            self.cell_toggle(self.cell_buttons[coord[0]][coord[1]])

        # if generate_next is True, then the simulation will start to play
        # if generate_next is False, cell buttons are enabled for the user to
        # pick which cells they want dead or alive to start the game
        if self.generate_next:
            self.after(100, self.simulate_game)
        else:
            self.enable_buttons()

    # makes cell buttons unusable
    # buttons are disabled while the simulation starts playing
    def disable_buttons(self):

        if self.cell_buttons[1][1] != DISABLED:
            for i in range(0, self.max_y + 2):
                for j in range(0, self.max_x + 2):
                    self.cell_buttons[i][j].configure(state=DISABLED)

            self.reset_button.configure(state=NORMAL)
            self.start_button.configure(state=DISABLED)

    # makes cell buttons usable
    # buttons are enabled before the simulation starts playing so the user can
    # choose which cells they want to be dead or alive before the simulation
    # starts playing
    def enable_buttons(self):
        # resets game
        for i in range(0, self.max_y + 2):
            for j in range(0, self.max_x + 2):
                self.cell_buttons[i][j]['bg'] = "white"
                self.cell_buttons[i][j].configure(state=NORMAL)

        self.reset_button.configure(state=DISABLED)
        self.start_button.configure(state=NORMAL)
        self.generate_next = True

# returns the number of "alive" neighbors surrounding the specified cell
    def neighbor_count(self, x_coord, y_coord):
        count = 0
        for i in range(x_coord - 1, x_coord + 2):
            for j in range(y_coord - 1, y_coord + 2):
                if (i != x_coord or j != y_coord) and self.cell_buttons[i][j]['bg'] == "black":
                    count += 1

        return count

# toggles whether a cell is "dead" or "alive"
    def cell_toggle(self, cell):
        if cell['bg'] == "white":
            cell['bg'] = "black"
        else:
            cell['bg'] = "white"

# restarts Game Of Life
    def reset_game(self):
        self.generate_next = False

# preset for a glider
    def glider(self):
        originX = 5
        originY = 5
        self.cell_toggle(self.cell_buttons[originX][originY - 1])
        self.cell_toggle(self.cell_buttons[originX - 1][originY + 1])
        self.cell_toggle(self.cell_buttons[originX][originY + 1])
        self.cell_toggle(self.cell_buttons[originX + 1][originY + 1])
        self.cell_toggle(self.cell_buttons[originX + 1][originY])

    # randomizes dead and alive cells on board
    def randomize(self):
        for i in range(28):
            for j in range(40):
                x = random.randint(0, 1)
                if x == 1:
                    self.cell_toggle(self.cell_buttons[i][j])

    # creates a blinker
    def blinker(self):
        originX = 14
        originY = 20
        self.cell_toggle(self.cell_buttons[originX][originY])
        self.cell_toggle(self.cell_buttons[originX][originY + 1])
        self.cell_toggle(self.cell_buttons[originX][originY - 1])

    # creates a toad
    def toad(self):
        originX = 14
        originY = 20
        self.cell_toggle(self.cell_buttons[originX][originY])
        self.cell_toggle(self.cell_buttons[originX][originY + 1])
        self.cell_toggle(self.cell_buttons[originX][originY + 2])
        self.cell_toggle(self.cell_buttons[originX + 1][originY])
        self.cell_toggle(self.cell_buttons[originX + 1][originY + 1])
        self.cell_toggle(self.cell_buttons[originX + 1][originY - 1])


def main():
    root = Tk()
    game = GameOfLife(root)
    root.mainloop()


main()
