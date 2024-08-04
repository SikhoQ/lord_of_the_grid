import curses


class Colours:
    curses.initscr()
    curses.start_color()

    BLACK_YELLOW = curses.color_pair(1)
    WHITE_BLUE = curses.color_pair(2)
    YELLOW_BLACK = curses.color_pair(3)
    WHITE_MAGENTA = curses.color_pair(4)
    WHITE_BLACK = curses.color_pair(5)
