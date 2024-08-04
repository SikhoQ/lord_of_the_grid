import curses

block_colors = dict()


class Colours:
    curses.initscr()
    curses.start_color()

    BLACK_YELLOW = curses.color_pair(1)
    WHITE_BLUE = curses.color_pair(2)
    YELLOW_BLACK = curses.color_pair(3)
    WHITE_MAGENTA = curses.color_pair(4)
    WHITE_BLACK = curses.color_pair(5)
    CYAN_BLACK = curses.color_pair(6)
    CYAN_MAGENTA = curses.color_pair(7)
    BLACK_CYAN = curses.color_pair(8)

    def __init__(self, player_1, player_2):
        global block_colors

        block_colors = {player_1: Colours.BLACK_YELLOW,
                        player_2: Colours.WHITE_BLUE}
