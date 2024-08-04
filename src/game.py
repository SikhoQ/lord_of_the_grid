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
    # prompt grid size
    grid_size = game_grid.Grid.get_grid_size(stdscr)

    alphas = string.ascii_lowercase
    # prompt player 1 initial
    player_1, alphas = player.Player.get_player_initial(stdscr, alphas)
    # prompt player 2 initial
    player_2, alphas = player.Player.get_player_initial(stdscr, alphas)

    block_colors = {player_1: colours.Colours.BLACK_YELLOW,
                    player_2: colours.Colours.WHITE_BLUE}

    current_player = player_1
    next_player = player_2

    stdscr.clear()

    # use grid size to initialise new grid
    grid = game_grid.Grid(grid_size)
    total_blocks = (grid_size - 1) ** 2

    grid.draw(stdscr)

    player_1_score = 0
    player_2_score = 0

    utils.print_gameplay_details(stdscr, total_blocks, current_player, {player_1: player_1_score}, {player_2: player_2_score})

    while not game_over:  # until player(s) enter(s) q or game is over
        completed_block = False

        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            do_exit_game(stdscr)
        if key == curses.KEY_MOUSE:
            mid_coord = tuple()

            _, mx, my, _, _ = curses.getmouse()
            row, col = my, mx

            ####################
            stdscr.addstr(1, 0, f"clicked at (  {mx},   {my})")
            ####################

            mid_char = chr(stdscr.inch(row, col) & 0xFF)

            if mid_char == ' ' and row in range(1, height - 1) and\
               col in range(1, width - 1):
                valid_horizontal, left_coord, right_coord = \
                    utils.check_valid_horizontal(stdscr, row, col)

                valid_vertical, top_coord, bootom_coord = \
                    utils.check_valid_vertical(stdscr, row, col)

                if valid_horizontal:
                    grid.connect_horizontal(stdscr, left_coord, right_coord)
                    mid_coord = (left_coord[0], left_coord[1] + 2)
                elif valid_vertical:
                    grid.connect_vertical(stdscr, row, col)
                    mid_coord = (row, col)

                if valid_horizontal or valid_vertical:
                    completed_block, sign_coords = grid.block_completed(
                        stdscr, mid_coord, valid_horizontal, valid_vertical)
                    if completed_block:
                        grid.do_block_sign(stdscr, sign_coords, current_player, block_colors)
                        game_over, player_1_score, player_2_score = utils.scores(stdscr, total_blocks, player_1, player_2)
                ###############################################
                stdscr.addstr(0, 0, str(completed_block) + " ")
                ###############################################
                if not completed_block and (valid_horizontal or valid_vertical):
                    current_player, next_player = next_player, current_player

        utils.print_gameplay_details(stdscr, total_blocks, current_player, {player_1: player_1_score}, {player_2: player_2_score})

        stdscr.refresh()
    # play_game(stdscr)


def do_exit_game(stdscr):
    stdscr.clear()
    stdscr.refresh()

    menu = ["Quit game?", "Yes", "No"]
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
                break


def exit_game(stdscr):
    stdscr.clear()
    stdscr.refresh()

    message = "Quitting..."

    height, width = stdscr.getmaxyx()
    x = width // 2 - len(message) // 2
    y = height // 2

    stdscr.addstr(y, x, message)
    stdscr.refresh()

    curses.napms(1100)
    sys.exit()
>>>>>>> 910f7a4 (fixed incorrect scoring and moved gameplay details to single score card)
