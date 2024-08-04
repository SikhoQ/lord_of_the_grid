import curses
import game_grid
import colours


def print_help(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    YELLOW = curses.color_pair(1)

    line_1 = "Own as many blocks as possible by connecting neighbour"
    line_2 = "dots on the 'grid' either vertically or horizontally."
    line_3 = "Dots are connected by clicking the space between them."
    line_4 = "The game ends when no more connections can be made."
    line_5 = "The player with the most blocks wins."
    line_6 = ""
    line_7 = "PRESS ANY KEY TO RETURN TO MAIN MENU"

    all_lines = [line_1, line_2, line_3, line_4, line_5, line_6, line_7]
    height, width = stdscr.getmaxyx()

    for line in all_lines:
        x = width // 2 - len(line) // 2
        y = height // 2 - len(all_lines) + all_lines.index(line)
        stdscr.addstr(y, x, line, YELLOW | curses.A_BOLD)

    stdscr.refresh()
    stdscr.getch()


def print_menu(stdscr, menu, selected):
    height, width = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = width // 2 - len(row) // 2
        y = height // 2 - len(menu) // 2 + idx
        if idx == selected:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, row)
        stdscr.refresh()


def scores(stdscr, total_blocks, player_1, player_2):
    top_left, bottom_right = game_grid.Grid.corners
    y1, x1 = top_left
    y2, x2 = bottom_right

    player_1_score = 0
    player_2_score = 0

    player_1_blocks = 0
    player_2_blocks = 0

    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if chr(stdscr.inch(y, x) & 0xFF) == player_1:
                player_1_blocks += 1
                player_1_score += 1
            elif chr(stdscr.inch(y, x) & 0xFF) == player_2:
                player_2_blocks += 1
                player_2_score += 1

    return total_blocks == player_1_score + player_2_score, player_1_score, player_2_score


def print_gameplay_details(stdscr, total_blocks, current_player, player_1, player_2):
    height, width = stdscr.getmaxyx()

    grid_max_x = game_grid.Grid.corners[1][1]
    grid_min_y = game_grid.Grid.corners[0][0]

    line1 = f"NOW PLAYING: {current_player}"
    line2 = "SCORE"
    line3 = f"{list(player_1.items())[0][0]}: {list(player_1.items())[0][1]}/{total_blocks}"
    line4 = f"{list(player_2.items())[0][0]}: {list(player_2.items())[0][1]}/{total_blocks}"
    lines = [line1, line2, line3, line4]

    start_y = height // 2 - len(lines) // 2
    start_x = grid_max_x + 1 + len(line1) // 2

    stdscr.attron(curses.A_BOLD)

    print_border(stdscr, start_y, start_x - 1)

    # stdscr.addstr(height // 2, game_grid.Grid.corners[0][1] - 17, "NOW PLAYING:", WHITE_MAGENTA)
    # stdscr.addstr(height // 2 + 1, game_grid.Grid.corners[0][1] - 11, current_player, WHITE_MAGENTA)

    for i, line in enumerate(lines):
        color = colours.Colours.WHITE_BLUE
        if i > 0:
            i += 1
        else:
            color = colours.Colours.WHITE_MAGENTA
        stdscr.addstr(start_y + i, start_x, line, color)

    if total_blocks == list(player_1.items())[0][1] + list(player_2.items())[0][1]:
        if list(player_1.items())[0][1] == list(player_2.items())[0][1]:
            message = "IT'S A TIE!"
        elif list(player_1.items())[0][1] > list(player_2.items())[0][1]:
            message = f"{list(player_1.items())[0][0]} WINS!"
        else:
            message = f"{list(player_2.items())[0][0]} WINS!"

        stdscr.addstr(grid_min_y // 2, width // 2 - len(message) // 2, message)
        stdscr.addstr(grid_min_y // 2 + 2, width // 2 - 12, "PRESS ANY KEY TO CONTINUE")
        key = stdscr.getch()

        # do nothing if mouse is clicked
        if key == curses.KEY_MOUSE:
            print_gameplay_details(stdscr, total_blocks, current_player, player_1, player_2)

    stdscr.refresh()


def print_border(stdscr, start_y, start_x):
    stdscr.addstr(start_y - 1, start_x, "-" * 16)
    stdscr.addstr(start_y + 1, start_x, "-" * 16)
    stdscr.addstr(start_y + 5, start_x, "-" * 16)
    for i in range(5):
        if i == 1:
            continue
        stdscr.addch(start_y + i, start_x, "|")
        stdscr.addch(start_y + i, start_x + 15, "|")
    stdscr.refresh()


def check_valid_horizontal(stdscr, row, col):
    _, width = stdscr.getmaxyx()
    left_coord = tuple()
    right_coord = tuple()

    min_x = max(1, col - 3)
    # max x is row + 3
    max_x = min(col + 3, width - 2)
    # iterate from min to max
    for x in range(min_x, max_x + 1):
        first_dot = chr(stdscr.inch(row, x) & 0xFF)
        if first_dot == '+':
            left_coord = (row, x)
            second_dot = chr(stdscr.inch(row, x + 4) & 0xFF)
            if second_dot == '+' and "   " == \
               ''.join([chr(stdscr.inch(row, x) & 0xFF) for x in
                        range(x + 1, x + 4)]):
                right_coord = (row, x + 4)
                return True, left_coord, right_coord
    return False, None, None


def check_valid_vertical(stdscr, row, col):
    height, _ = stdscr.getmaxyx()

    min_y = max(1, row - 1)
    max_y = min(row + 1, height - 2)

    top_char = chr(stdscr.inch(min_y, col) & 0xFF)
    bottom_char = chr(stdscr.inch(max_y, col) & 0xFF)
    mid_char = chr(stdscr.inch(min_y + 1, col) & 0xFF)

    if top_char == bottom_char == '+' and mid_char == " ":
        return True, (min_y, col), (max_y, col)
    return False, None, None
