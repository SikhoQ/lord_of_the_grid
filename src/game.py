import curses
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

    grid_size = InputHandler.get_grid_size()
    player1_name, player2_name = Player.get_player_initials()
    player1 = Player(player1_name)
    player2 = Player(player2_name)

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
