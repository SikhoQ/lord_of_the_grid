import string
import curses


class Grid:
    def __init__(self, size, stdscr):
        self.size = size
        self.grid = self.create_grid()
        self.direction = ""
        self.alphas = string.ascii_uppercase
        self.sign_block = list()
        self.stdscr = stdscr
        self.screen_height, self.screen_width, \
            self.grid_height, self.grid_width, \
            self.start_row, self.start_col = self.get_dimensions()

    def get_dimensions(self):
        # Get screen size
        screen_height, screen_width = self.stdscr.getmaxyx()

        # Calculate grid dimensions
        grid_height = len(self.grid)
        grid_width = len(self.grid[0]) * 2  # Assuming each cell takes 2 columns (one for the cell and one for space)

        # Calculate starting positions to center the grid
        start_row = (screen_height - grid_height) // 2
        start_col = (screen_width - grid_width) // 2

        return screen_height, screen_width, grid_height, \
            grid_width, start_row, start_col

    def create_grid(self):
        # 'dots' to be connected in grid are represented by +
        # spaces between neighbouring 'dots' both horizontally and vertically (to be replaced by connecting lines during play)
        grid = list()

        for i in range(self.size):
            grid.append(["+", " "] * self.size)
            grid[-1].pop()  # remove last spaces in each list (useless)
            if i != self.size - 1:
                grid.append([" "] * self.size * 2)  # add vertical spaces
                grid[-1].pop()  # remove last spaces in each list (useless)

        return grid

    def already_played(self, play):
        row_1, col_1, row_2, col_2 = self.get_coordinates(play)

        if (row_1 == row_2):
            return self.grid[row_1][min([col_1, col_2]) + 1] == "-"
        return self.grid[min(row_1, row_2) + 1][col_1] == "|"

    def update_grid(self, play):
        row_1, col_1, row_2, col_2 = self.get_coordinates(play)
        if row_1 == row_2:  # horizontal play
            self.grid[row_1][min([col_1, col_2]) + 1] = "-"  # find space to replace by adding 1 to the smaller column
            if col_1 > col_2:  # play direction : RIGHT
                self.direction = "LEFT"
            else:
                self.direction = "RIGHT"
        else:
            self.grid[min([row_1, row_2]) + 1][col_1] = "|"

            if row_1 > row_2:  # play direction: UP
                self.direction = "UP"
            else:
                self.direction = "DOWN"

    def do_block_sign(self, player):
        self.grid[self.sign_block[0]][self.sign_block[1]] = player.name  # just put the player's initial in the completed block

        if len(self.sign_block) == 4:
            self.grid[self.sign_block[2]][self.sign_block[3]] = player.name  # sign_block has length 4 when single play completes 2 blocks, in which case sign both blocks

    def check_block_completed(self, play):
        row_1, col_1, row_2, col_2 = self.get_coordinates(play)

        self.sign_block = list()

        if self.direction == "UP":
            if play[1] != "1" and play[1] != str(self.size):  # if the played vertical line is not along the edges
                if self.grid[row_2][col_2 - 1] == "-" and self.grid[row_2 + 1][col_2 - 2] == "|" and self.grid[row_1][col_1 - 1] == "-"\
                   and self.grid[row_2][col_2 + 1] == "-" and self.grid[row_2 + 1][col_2 + 2] == "|" and self.grid[row_1][col_1 + 1] == "-":  # if play completes 2 blocks, either side of line
                    self.sign_block.extend([row_1 - 1, col_1 + 1, row_1 - 1, col_1 - 1])

                elif self.grid[row_2][col_2 - 1] == "-" and self.grid[row_2 + 1][col_2 - 2] == "|" and self.grid[row_1][col_1 - 1] == "-":  # on the left of vertical line
                    self.sign_block.extend([row_1 - 1, col_1 - 1])

                elif self.grid[row_2][col_2 + 1] == "-" and self.grid[row_2 + 1][col_2 + 2] == "|" and self.grid[row_1][col_1 + 1] == "-":  # on the right of vertical line
                    self.sign_block.extend([row_1 - 1, col_1 + 1])

            elif play[1] == "1":  # played vertical line is along left edge
                if self.grid[row_2][col_2 + 1] == "-" and self.grid[row_2 + 1][col_2 + 2] == "|" and self.grid[row_1][col_1 + 1] == "-":
                    self.sign_block.extend([row_1 - 1, col_1 + 1])

            else:  # played vertical line is along right edge
                if self.grid[row_2][col_2 - 1] == "-" and self.grid[row_2 + 1][col_2 - 2] == "|" and self.grid[row_1][col_1 - 1] == "-":  # on the left of vertical line
                    self.sign_block.extend([row_1 - 1, col_1 - 1])

        elif self.direction == "DOWN":
            if play[1] != "1" and play[1] != str(self.size):  # if the played vertical line is not along the edges
                if self.grid[row_2][col_2 - 1] == "-" and self.grid[row_2 - 1][col_2 - 2] == "|" and self.grid[row_1][col_1 - 1] == "-"\
                   and self.grid[row_2][col_2 + 1] == "-" and self.grid[row_2 - 1][col_2 + 2] == "|" and self.grid[row_1][col_1 + 1] == "-":  # if play completes 2 blocks, either side of line
                    self.sign_block.extend([row_2 - 1, col_2 - 1, row_2 - 1, col_2 + 1])

                elif self.grid[row_2][col_2 - 1] == "-" and self.grid[row_2 - 1][col_2 - 2] == "|" and self.grid[row_1][col_1 - 1] == "-":  # on left of line
                    self.sign_block.extend([row_2 - 1, col_2 - 1])

                elif self.grid[row_2][col_2 + 1] == "-" and self.grid[row_2 - 1][col_2 + 2] == "|" and self.grid[row_1][col_1 + 1] == "-":  # on right of line
                    self.sign_block.extend([row_2 - 1, col_2 + 1])

            elif play[1] == "1":  # played vertical line is along left edge
                if self.grid[row_2][col_2 + 1] == "-" and self.grid[row_2 - 1][col_2 + 2] == "|" and self.grid[row_1][col_1 + 1] == "-":
                    self.sign_block.extend([row_2 - 1, col_2 + 1])

            else:  # line is along right edge
                if self.grid[row_2][col_2 - 1] == "-" and self.grid[row_2 - 1][col_2 - 2] == "|" and self.grid[row_1][col_1 - 1] == "-":  # on left of line
                    self.sign_block.extend([row_2 - 1, col_2 - 1])

        elif self.direction == "RIGHT":
            if play[0] != "A" and play[0] != self.alphas[self.size - 1]:  # if played horizontal line is not along top or bottom edge
                if self.grid[row_2 - 1][col_2] == "|" and self.grid[row_2 - 2][col_2 - 1] == "-" and self.grid[row_1 - 1][col_1] == "|"\
                   and self.grid[row_2 + 1][col_2] == "|" and self.grid[row_2 + 2][col_2 - 1] == "-" and self.grid[row_2 + 1][col_2 - 2] == "|":  # if play completes 2 blocks, on either side
                    self.sign_block.extend([row_2 - 1, col_2 - 1, row_2 + 1, col_2 - 1])

                elif self.grid[row_2 - 1][col_2] == "|" and self.grid[row_2 - 2][col_2 - 1] == "-" and self.grid[row_1 - 1][col_1] == "|":  # above line
                    self.sign_block.extend([row_2 - 1, col_2 - 1])

                elif self.grid[row_2 + 1][col_2] == "|" and self.grid[row_2 + 2][col_2 - 1] == "-" and self.grid[row_2 + 1][col_2 - 2] == "|":  # below line
                    self.sign_block.extend([row_2 + 1, col_2 - 1])

            elif play[0] == "A":  # along top edge
                if self.grid[row_2 + 1][col_2] == "|" and self.grid[row_2 + 2][col_2 - 1] == "-" and self.grid[row_2 + 1][col_2 - 2] == "|":  # below line
                    self.sign_block.extend([row_2 + 1, col_2 - 1])

            else:  # along bottom edge
                if self.grid[row_2 - 1][col_2] == "|" and self.grid[row_2 - 2][col_2 - 1] == "-" and self.grid[row_1 - 1][col_1] == "|":  # above line
                    self.sign_block.extend([row_2 - 1, col_2 - 1])

        elif self.direction == "LEFT":  # obviously, direction: left
            if play[0] != "A" and play[0] != self.alphas[self.size - 1]:  # if played horizontal line is not along top or bottom edge
                if self.grid[row_2 + 1][col_2] == "|" and self.grid[row_2 + 2][col_2 + 1] == "-" and self.grid[row_2 + 1][col_2 + 2] == "|"\
                   and self.grid[row_2 - 1][col_2] == "|" and self.grid[row_2 - 2][col_2 + 1] == "-" and self.grid[row_2 - 1][col_2 + 2] == "|":  # if current play completes 2 blocks
                    self.sign_block.extend([row_2 + 1, col_2 + 1, row_2 - 1, col_2 + 1])

                elif self.grid[row_2 + 1][col_2] == "|" and self.grid[row_2 + 2][col_2 + 1] == "-" and self.grid[row_2 + 1][col_2 + 2] == "|":  # below line
                    self.sign_block.extend([row_2 + 1, col_2 + 1])

                elif self.grid[row_2 - 1][col_2] == "|" and self.grid[row_2 - 2][col_2 + 1] == "-" and self.grid[row_2 - 1][col_2 + 2] == "|":  # above line
                    self.sign_block.extend([row_2 - 1, col_2 + 1])

            elif play[0] == "A":  # along top edge
                if self.grid[row_2 + 1][col_2] == "|" and self.grid[row_2 + 2][col_2 + 1] == "-" and self.grid[row_2 + 1][col_2 + 2] == "|":  # below line
                    self.sign_block.extend([row_2 + 1, col_2 + 1])

            else:  # along bottom edge
                if self.grid[row_2 - 1][col_2] == "|" and self.grid[row_2 - 2][col_2 + 1] == "-" and self.grid[row_2 - 1][col_2 + 2] == "|":  # above line
                    self.sign_block.extend([row_2 - 1, col_2 + 1])

        return len(self.sign_block) != 0  # True if our list of co-ords is no longer empty (i.e. a completed block was found)

    def get_coordinates(self, play):
        row_1 = 2 * self.alphas.index(play[0])
        col_1 = 2 * (int(play[1]) - 1)
        row_2 = 2 * self.alphas.index(play[3])
        col_2 = 2 * (int(play[4]) - 1)
        return row_1, col_1, row_2, col_2

    def print_grid(self):
        print("\n\n" + " "*7, end="")  # print spaces before the 1
        for i in range(1, self.size + 1):  # printing column labels
            print(i, end=" "*5)

        print("\n\n")

        i = 0
        for this_line in self.grid:
            if "+" in this_line:
                print(f"{self.alphas[i]}", end=" "*6)
                i += 1
            else:
                print(" "*7, end="")
            for item in this_line:
                print(item, end=" "*2)
            print()

    def draw(self):
        # Draw the grid
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                self.stdscr.addch(self.start_row + i,
                                  self.start_col + j * 2, cell)

        # Calculate the position below the grid
        cursor_row = self.start_row + self.grid_height + 1
        cursor_col = self.start_col

        self.stdscr.addstr(cursor_row, cursor_col, "Press 'q' to quit")

        self.stdscr.refresh()

    def get_mouse_coordinates(self):
        id, x, y, z, bstate = curses.getmouse()
        return y, x

    def update_grid_with_click(self, click):
        row, col = click

        if col > 0 and col < (self.screen_width - 1) and\
           row > 0 and row < (self.screen_height - 1):
            left_char = self.stdscr.inch(row, col - 1) & 0xFF
            right_char = self.stdscr.inch(row, col + 1) & 0xFF
            mid_char1 = self.stdscr.inch(row, col) & 0xFF

            if left_char == right_char == "+" and mid_char1 == " ":
                self.stdscr.addstr(row, col, "-")

            top_char = self.stdscr.inch(row - 1, col) & 0xFF
            bottom_char = self.stdscr.inch(row + 1, col) & 0xFF
            mid_char2 = self.stdscr.inch(row, col) & 0xFF

            if top_char == bottom_char == "+" and mid_char2 == " ":
                self.stdscr.addstr(row, col, "|")

            self.stdscr.refresh()
