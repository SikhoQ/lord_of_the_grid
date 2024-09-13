import curses
import game_grid
import colours

options_coords = tuple()
bottom_space_coords = tuple()
top_space_coords = tuple()


def print_help(stdscr):
    stdscr.clear()

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
        stdscr.addstr(y, x, line, colours.Colours.YELLOW_BLACK | curses.A_BOLD)

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


def calculate_scores(stdscr, total_blocks, player_1, player_2):
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


def print_score_card(stdscr, total_blocks, current_player, player_1, player_2):
    height, width = stdscr.getmaxyx()

    grid_max_x = game_grid.Grid.corners[1][1]
    grid_min_y = game_grid.Grid.corners[0][0]

    output_colour = None
    player_1_score = f"{list(player_1.items())[0][0]}: {list(player_1.items())[0][1]}/{total_blocks}"
    player_2_score = f"{list(player_2.items())[0][0]}: {list(player_2.items())[0][1]}/{total_blocks}"
    max_score_length = max(len(player_1_score), len(player_2_score))

    line1 = f"NOW PLAYING: {current_player}"
    line2 = "SCORE:" + (' ' * (max_score_length - 6))
    line3 = player_1_score + (' ' * (max_score_length - len(player_1_score)))
    line4 = player_2_score + (' ' * (max_score_length - len(player_2_score)))
    line5 = "RESTART   QUIT"
    lines = [line2, line3, line4, line5]

    start_y = height // 2 - len(lines) // 2 - 2
    start_x = grid_max_x + len(line1) // 2 - 2

    print_current_player(stdscr, current_player, start_y, start_x)
    max_score_length = print_scores(stdscr, (start_y, start_x),
                                    (player_1, player_2), total_blocks)

    print_in_game_options(stdscr, start_y, start_x, max_score_length, colours.Colours.GREEN_BLACK)

    print_border(stdscr, start_y, start_x - 1, max_score_length)

    if total_blocks == list(player_1.items())[0][1] + list(player_2.items())[0][1]:
        if list(player_1.items())[0][1] == list(player_2.items())[0][1]:
            message = "IT'S A TIE!"
            stdscr.addstr(grid_min_y // 2, width // 2 - len(message) // 2 - 1, message, colours.Colours.YELLOW_BLACK)
        else:
            if list(player_1.items())[0][1] > list(player_2.items())[0][1]:
                message = f"PLAYER {list(player_1.items())[0][0]} WINS!"
                output_colour = colours.player_colours[list(player_1.items())[0][0]]
            else:
                message = f"PLAYER {list(player_2.items())[0][0]} WINS!"
                output_colour = colours.player_colours[list(player_2.items())[0][0]]
            stdscr.addstr(top_space_coords[0], top_space_coords[1], " " * 16)
            stdscr.addstr(top_space_coords[0], top_space_coords[1] + 1, message, output_colour)

        stdscr.nodelay(True)
        stdscr.addch(bottom_space_coords[0], bottom_space_coords[1] + 3, "|", colours.Colours.CYAN_BLACK)
        stdscr.addch(bottom_space_coords[0], bottom_space_coords[1] + 12, "|", colours.Colours.CYAN_BLACK)

        print_in_game_options(stdscr, start_y, start_x, max_score_length, colours.Colours.RED_BLACK)
        while True:
            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                _, col, row, _, _ = curses.getmouse()
                if row == bottom_space_coords[0] and\
                   col in range(bottom_space_coords[1] + 4, bottom_space_coords[1] + 12):
                    stdscr.nodelay(False)
                    break
            stdscr.addstr(bottom_space_coords[0], bottom_space_coords[1] + 4, "CLICK ME", colours.Colours.GREEN_BLACK)
            stdscr.refresh()
            curses.napms(300)
            stdscr.addstr(bottom_space_coords[0], bottom_space_coords[1] + 4, " " * 8)
            stdscr.refresh()
            curses.napms(300)

    stdscr.refresh()


def print_current_player(stdscr, current_player, start_y, start_x):
    stdscr.addstr(start_y, start_x + 1, "NOW PLAYING:",
                  colours.Colours.BLACK_CYAN)
    stdscr.addstr(start_y, start_x + 14, current_player, colours.player_colours[current_player])


def print_scores(stdscr, coords, players, total_blocks):
    player_1 = players[0]
    player_2 = players[1]
    start_y, start_x = coords

    player_1_score = f"{list(player_1.items())[0][0]}: {list(player_1.items())[0][1]}/{total_blocks}"
    player_2_score = f"{list(player_2.items())[0][0]}: {list(player_2.items())[0][1]}/{total_blocks}"
    max_score_length = max(len(player_1_score), len(player_2_score))

    score_heading = "SCORE:" + (' ' * (max_score_length - 6))
    player_1_score = player_1_score + (' ' * (max_score_length - len(player_1_score)))
    player_2_score = player_2_score + (' ' * (max_score_length - len(player_2_score)))

    stdscr.addstr(start_y + 2, start_x, score_heading,
                  colours.Colours.BLACK_CYAN | curses.A_UNDERLINE)
    stdscr.addstr(start_y + 3, start_x, player_1_score,
                  colours.player_colours[list(player_1.items())[0][0]] | curses.A_UNDERLINE)
    stdscr.addstr(start_y + 4, start_x, player_2_score,
                  colours.player_colours[list(player_2.items())[0][0]])

    return max_score_length


def print_in_game_options(stdscr, start_y, start_x, max_score_length, option_colours):
    global options_coords
    stdscr.addstr(start_y + 2, start_x + max_score_length + 1, "OPTIONS:", colours.Colours.BLACK_CYAN | curses.A_UNDERLINE)
    stdscr.addstr(start_y + 3, start_x + max_score_length + 1, "RESTART", option_colours)
    stdscr.addstr(start_y + 4, start_x + max_score_length + 1, "EXIT", option_colours)
    stdscr.refresh()

    options_coords = (start_y + 3, start_x + max_score_length + 1)


def print_border(stdscr, start_y, start_x, max_score_length):
    global bottom_space_coords, top_space_coords

    top_space_coords = (start_y, start_x + 1)

    border_colour = colours.Colours.CYAN_BLACK

    # horizontals
    stdscr.addstr(start_y - 1, start_x, '=' * 18, border_colour)
    stdscr.addstr(start_y + 1, start_x, '-' * 18, border_colour)
    stdscr.addstr(start_y + 5, start_x, '=' * 18, border_colour)
    stdscr.addstr(start_y + 7, start_x, '=' * 18, border_colour)

    # centre verticals
    for i in range(2, 5):
        stdscr.addch(start_y + i, start_x + max_score_length + 1, '|', border_colour)

    # outter verticals
    for i in range(7):
        if i in (1, 5):
            continue
        stdscr.addch(start_y + i, start_x, '|', border_colour)
        stdscr.addch(start_y + i, start_x + 17, '|', border_colour)
        bottom_space_coords = (start_y + i, start_x + 1)
    stdscr.refresh()


def check_valid_horizontal(stdscr, row, col):
    _, width = stdscr.getmaxyx()
    left_coord = tuple()
    right_coord = tuple()

    min_x = max(1, col - 3)
    # max x is col + 3
    max_x = min(col + 3, width - 6)
    # iterate from min to max
    for x in range(min_x, max_x + 1):
        first_dot = chr(stdscr.inch(row, x) & 0xFF)
        if first_dot == '+' and (x + 4) <= (min_x + 7):
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


def do_block_sign(stdscr, coords, current_player):
    for i, coord in enumerate(coords):
        y, x = coord
        if i == 1 or i == 4:
            stdscr.addch(y, x, current_player, colours.player_colours[current_player])
        else:
            stdscr.addch(y, x, ' ', colours.player_colours[current_player])
    stdscr.refresh()


def connect_horizontal(stdscr, left_coord, right_coord):
    y = left_coord[0]
    min_x, max_x = left_coord[1], right_coord[1]

    for x in range(min_x + 1, max_x):
        stdscr.addstr(y, x, "-")
    stdscr.refresh()


def connect_vertical(stdscr, row, col):
    stdscr.addch(row, col, "|")
    stdscr.refresh()
