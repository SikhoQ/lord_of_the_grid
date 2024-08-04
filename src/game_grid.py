import string
import curses
import colours


class Grid:
<<<<<<< HEAD
    def __init__(self, size, stdscr):
=======
    corners = tuple()

    def __init__(self, size):
>>>>>>> 910f7a4 (fixed incorrect scoring and moved gameplay details to single score card)
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

    def block_completed(self, stdscr, coord, horizontal=False, vertical=False):
        height, width = stdscr.getmaxyx()
        y, x = coord
        self.sign_block = list()

        # VERITCAL
        # ========
        if vertical:
            # if the played vertical line is not along left or right edges
            if x >= 5 and x <= width - 6:
                # if on the left of vertical line
                if chr(stdscr.inch(y, x - 4) & 0xFF) == '|' and\
                 "---" == ''.join([chr(stdscr.inch(y - 1, col) & 0xFF) for col in range(x - 3, x)]) and\
                 "---" == ''.join([chr(stdscr.inch(y + 1, col) & 0xFF) for col in range(x - 3, x)]):
                    self.sign_block.extend([(y, col) for col in range(x - 3, x)])

                # if on the right of vertical line
                if chr(stdscr.inch(y, x + 4) & 0xFF) == '|' and\
                   "---" == ''.join([chr(stdscr.inch(y - 1, col) & 0xFF) for col in range(x + 1, x + 4)]) and\
                   "---" == ''.join([chr(stdscr.inch(y + 1, col) & 0xFF) for col in range(x + 1, x + 4)]):
                    self.sign_block.extend([(y, col) for col in range(x + 1, x + 4)])

            # else if played vertical line is along left edge
            elif x == 1:
                if chr(stdscr.inch(y, 5) & 0xFF) == '|' and\
                 "---" == ''.join([chr(stdscr.inch(y - 1, col) & 0xFF) for col in range(2, 5)]) and\
                 "---" == ''.join([chr(stdscr.inch(y + 1, col) & 0xFF) for col in range(2, 5)]):
                    self.sign_block.extend([(y, col) for col in range(2, 5)])

            # else played vertical line is along right edge
            elif x == width - 2:
                if chr(stdscr.inch(y, width - 6) & 0xFF) == '|' and\
                 "---" == ''.join([chr(stdscr.inch(y - 1, col) & 0xFF) for col in range(width - 5, width - 2)]) and\
                 "---" == ''.join([chr(stdscr.inch(y + 1, col) & 0xFF) for col in range(width - 5, width - 2)]):
                    self.sign_block.extend([(y, col) for col in range(width - 5, width - 2)])

        # HORIZONTAL
        # ==========
        elif horizontal:

            # if played horizontal line is not along top or bottom edge
            if y >= 3 and y <= height - 4:
                # if above horizontal line
                if chr(stdscr.inch(y - 1, x - 2) & 0xFF) == '|' and\
                 chr(stdscr.inch(y - 1, x + 2) & 0xFF) == '|' and\
                 "---" == ''.join([chr(stdscr.inch(y - 2, col) & 0xFF) for col in range(x - 1, x + 2)]):
                    self.sign_block.extend([(y - 1, col) for col in range(x - 1, x + 2)])
                # if below horizontal line
                if chr(stdscr.inch(y + 1, x - 2) & 0xFF) == '|' and\
                    chr(stdscr.inch(y + 1, x + 2) & 0xFF) == '|' and\
                        "---" == ''.join([chr(stdscr.inch(y + 2, col) & 0xFF) for col in range(x - 1, x + 2)]):
                    self.sign_block.extend([(y + 1, col) for col in range(x - 1, x + 2)])

            # else if played horizontal line is on top edge
            elif y == 1:
                if chr(stdscr.inch(y + 1, x - 2) & 0xFF) == '|' and\
                 chr(stdscr.inch(y + 1, x + 2) & 0xFF) == '|' and\
                 "---" == ''.join([chr(stdscr.inch(y + 2, col) & 0xFF) for col in range(x - 1, x + 2)]):
                    self.sign_block.extend([(y + 1, col) for col in range(x - 1, x + 2)])
            # else played horizontal line is on bottom edge
            elif y == height - 2:
                if chr(stdscr.inch(y - 1, x - 2) & 0xFF) == '|' and\
                 chr(stdscr.inch(y - 1, x + 2) & 0xFF) == '|' and\
                 "---" == ''.join([chr(stdscr.inch(y - 2, col) & 0xFF) for col in range(x - 1,  x + 2)]):
                    self.sign_block.extend([(y - 1, col) for col in range(x - 1, x + 2)])

        return len(self.sign_block) != 0, self.sign_block  # True if our list of co-ords is no longer empty (i.e. a completed block was found)

<<<<<<< HEAD
    def draw(self):
        # Draw the grid
=======
    def draw(self, stdscr):
        height, width = stdscr.getmaxyx()

        min_x = (width // 2) - len(self.grid[0])
        min_y = height // 2 - len(self.grid) // 2
        max_x = min_x + len(self.grid[0]) * 2
        max_y = min_y + len(self.grid)

        stdscr.clear()

<<<<<<< HEAD
        # game_title = "L O R D  O F  T H E  G R I D"
        # title_y = max(0, height // 2 - len(self.grid) // 2 - 5)
        # title_x = width // 2 - len(game_title) // 2
        # stdscr.addstr(title_y, title_x, "L O R D  O F  T H E  G R I D")

>>>>>>> 910f7a4 (fixed incorrect scoring and moved gameplay details to single score card)
=======
>>>>>>> c3a8d74 (updated layout)
        for i, row in enumerate(self.grid):
            y = height // 2 - len(self.grid) // 2 + (i - 1)
            for j, cell in enumerate(row):
<<<<<<< HEAD
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
=======
                x = (width // 2) - len(row) + j
                stdscr.addch(y, j + x, cell)
        stdscr.refresh()

        Grid.corners = (min_y, min_x), (max_y, max_x)

    @staticmethod
    def get_grid_size(stdscr):
        curses.curs_set(1)
        prompt = "Enter grid size (2 - 9): "

        stdscr.clear()

        height, width = stdscr.getmaxyx()
        x = width // 2 - len(prompt) // 2
        y = height // 2

        stdscr.addstr(y, x, prompt)
        stdscr.refresh()

        grid_size = stdscr.getch()

        if grid_size not in range(50, 58):
            message = "Invalid grid size"
            x = width // 2 - len(message) // 2
            stdscr.clear()
            stdscr.addstr(y, x, message)
            stdscr.refresh()
            curses.napms(1600)

            return Grid.get_grid_size(stdscr)
        curses.napms(650)

        unicode_to_ascii = {key: key - 48 for key in range(50, 58)}

        curses.curs_set(0)
        return unicode_to_ascii[grid_size]
<<<<<<< HEAD

    def connect_horizontal(self, stdscr, left_coord, right_coord):
        y = left_coord[0]
        min_x, max_x = left_coord[1], right_coord[1]

        for x in range(min_x + 1, max_x):
            stdscr.addstr(y, x, "-")
        stdscr.refresh()

    def connect_vertical(self, stdscr, row, col):
        stdscr.addch(row, col, "|")
        stdscr.refresh()
>>>>>>> 910f7a4 (fixed incorrect scoring and moved gameplay details to single score card)
=======
>>>>>>> c3a8d74 (updated layout)
