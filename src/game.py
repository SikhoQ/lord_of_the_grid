import curses
<<<<<<< HEAD
from curses import wrapper
import os
from input_handler import InputHandler
from player import Player
import utils as utils
from game_grid import Grid


def main(stdscr):
    # stdscr.nodelay(1)
    # stdscr.timeout(100)

    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.clear()

    # utils.print_instructions()

    # InputHandler.pause_and_prompt()
=======
import utils
import player
import game_grid
import sys
import string
import colours

game_over = False

>>>>>>> 910f7a4 (fixed incorrect scoring and moved gameplay details to single score card)

<<<<<<< HEAD
def play_game(stdscr):
    global game_over

<<<<<<< HEAD
    grid = Grid(grid_size, stdscr)
    player = player1

    stdscr.refresh()
    grid.draw()

    while not utils.game_ended(grid):
        key = stdscr.getch()

        if key == curses.KEY_MOUSE:
            click = grid.get_mouse_coordinates()
            grid.update_grid_with_click(click)
            grid.draw()
        elif key == ord('q'):
            break

        # current_play = InputHandler.get_current_play()

        # if InputHandler.valid_input_length(current_play) and\
        #    InputHandler.valid_input_format(current_play, grid_size):
        #     if grid.already_played(current_play):
        #         os.system("clear")
        #         print("Line has already been played")
        #         InputHandler.pause_and_prompt()
        #         continue
        #     else:
        #         os.system("clear")
        #         grid.update_grid(current_play)

        #     completed_block = grid.check_block_completed(current_play)  # to check if current play completed a block; if yes, call further functions from within
        #     if completed_block:
        #         grid.do_block_sign(player)
        #     else:
        #         player = player2 if player == player1 else player1
        # else:
        #     os.system("clear")
        #     print("Invalid input format")
        #     InputHandler.pause_and_prompt()

    grid.print_grid()
    print("Game over\n")
    scores_dict = utils.scores(grid, player1, player2)
    print(f"Scores:\n{player1.name}: {scores_dict[player1.name]}\n{player2.name}: {scores_dict[player2.name]}")


if __name__ == "__main__":
    wrapper(main)
=======
    stdscr.clear()

    height, width = stdscr.getmaxyx()
=======
def get_players_and_size(stdscr):
>>>>>>> b9fbcd5 (various fixes and improvements)
    # prompt grid size
    grid_size = game_grid.Grid.get_grid_size(stdscr)

    alphas = string.ascii_lowercase + string.ascii_uppercase
    # prompt player 1 initial
    player_1, alphas = player.Player.get_player_initial(stdscr, alphas)
    # prompt player 2 initial
    player_2, alphas = player.Player.get_player_initial(stdscr, alphas)
    play_game(stdscr, player_1, player_2, grid_size)


def play_game(stdscr, player_1, player_2, grid_size):
    global game_over

    stdscr.clear()
    height, width = stdscr.getmaxyx()

    curses.noecho()

    # initialize block colours
    colours.Colours(player_1, player_2)

    current_player = player_1
    next_player = player_2

    stdscr.clear()

    # use grid size to initialise new grid
    grid = game_grid.Grid(grid_size)
    total_blocks = (grid_size - 1) ** 2

    grid.draw(stdscr)

    player_1_score = 0
    player_2_score = 0

    utils.print_score_card(stdscr, total_blocks, current_player, {player_1: player_1_score}, {player_2: player_2_score})

    while not game_over:  # until player(s) enter(s) q or game is over
        completed_block = False

        key = stdscr.getch()

        if key == curses.KEY_MOUSE:
            mid_coord = tuple()

            _, col, row, _, _ = curses.getmouse()

            if col in range(utils.options_coords[1], utils.options_coords[1] + 7):
                if row == utils.options_coords[0]:
                    if restart_game(stdscr):
                        play_game(stdscr, player_1, player_2, grid_size)
                elif row == utils.options_coords[0] + 1:
                    if exit_current_game(stdscr):
                        return

            mid_char = chr(stdscr.inch(row, col) & 0xFF)

            if mid_char == ' ' and row in range(1, height - 1) and\
               col in range(1, width - 1):
                valid_horizontal, left_coord, right_coord = \
                    utils.check_valid_horizontal(stdscr, row, col)

                valid_vertical, top_coord, bootom_coord = \
                    utils.check_valid_vertical(stdscr, row, col)

                if valid_horizontal:
                    utils.connect_horizontal(stdscr, left_coord, right_coord)
                    mid_coord = (left_coord[0], left_coord[1] + 2)
                elif valid_vertical:
                    utils.connect_vertical(stdscr, row, col)
                    mid_coord = (row, col)

                if valid_horizontal or valid_vertical:
                    completed_block, sign_coords = grid.block_completed(
                        stdscr, mid_coord, valid_horizontal, valid_vertical)
                    if completed_block:
                        utils.do_block_sign(stdscr, sign_coords, current_player)
                        game_over, player_1_score, player_2_score = utils.calculate_scores(stdscr, total_blocks, player_1, player_2)

                if not completed_block and (valid_horizontal or valid_vertical):
                    current_player, next_player = next_player, current_player

        utils.print_score_card(stdscr, total_blocks, current_player, {player_1: player_1_score}, {player_2: player_2_score})

        stdscr.refresh()


def restart_game(stdscr):
    y, x = utils.bottom_space_coords
    stdscr.addstr(y, x + 9, "YES", colours.Colours.BLACK_GREEN)
    stdscr.addstr(y, x + 13, "NO", colours.Colours.BLACK_RED)

    stdscr.nodelay(True)

    while True:
        stdscr.addstr(y, x, "RESTART?", colours.Colours.BLACK_CYAN)
        stdscr.refresh()
        curses.napms(500)
        stdscr.addstr(y, x, "RESTART?", colours.Colours.CYAN_BLACK)
        stdscr.refresh()
        curses.napms(500)

        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, col, row, _, _ = curses.getmouse()
            if row == y:
                if col in range(x + 9, x + 12):
                    stdscr.nodelay(False)
                    return True
                if col in range(x + 13, x + 15):
                    stdscr.addstr(y, x, " " * 15)
                    stdscr.refresh()
                    stdscr.nodelay(False)
                    return False


def exit_current_game(stdscr):
    y, x = utils.bottom_space_coords
    stdscr.addstr(y, x + 8, "YES", colours.Colours.BLACK_GREEN)
    stdscr.addstr(y, x + 13, "NO", colours.Colours.BLACK_RED)

    stdscr.nodelay(True)

    while True:
        stdscr.addstr(y, x + 1, "EXIT?", colours.Colours.BLACK_CYAN)
        stdscr.refresh()
        curses.napms(500)
        stdscr.addstr(y, x + 1, "EXIT?", colours.Colours.CYAN_BLACK)
        stdscr.refresh()
        curses.napms(500)

        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, col, row, _, _ = curses.getmouse()
            if row == y:
                if col in range(x + 8, x + 11):
                    stdscr.nodelay(False)
                    return True
                if col in range(x + 13, x + 15):
                    stdscr.addstr(y, x, " " * 15)
                    stdscr.refresh()
                    stdscr.nodelay(False)
                    return False


def do_exit_game(stdscr):
    stdscr.clear()
    stdscr.refresh()

    menu = ["Exit game?", "Yes", "No"]
    current_row = 1

    while True:
        utils.print_menu(stdscr, menu, current_row)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 1:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_row == 1:
                exit_game(stdscr)
            else:
                stdscr.clear()
                break


def exit_game(stdscr):
    stdscr.clear()
    stdscr.refresh()

    message = "Please wait..."

    height, width = stdscr.getmaxyx()
    x = width // 2 - len(message) // 2
    y = height // 2

    stdscr.addstr(y, x, message)
    stdscr.refresh()

    curses.napms(1100)
    sys.exit()
>>>>>>> 910f7a4 (fixed incorrect scoring and moved gameplay details to single score card)
