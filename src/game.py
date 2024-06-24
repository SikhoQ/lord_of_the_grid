import os

from input_handler import InputHandler
from player import Player
import utils
from game_grid import Grid


def main():
    os.system("clear")
    utils.print_instructions()

    InputHandler.pause_and_prompt()

    grid_size = InputHandler.get_grid_size()
    player1_name, player2_name = Player.get_player_initials()
    player1 = Player(player1_name)
    player2 = Player(player2_name)

    grid = Grid(grid_size)
    player = player1

    while not utils.game_ended(grid):
        os.system("clear")
        grid.print_grid()
        print("Current player:", player.name)

        current_play = InputHandler.get_current_play()

        if InputHandler.valid_input_length(current_play) and\
           InputHandler.valid_input_format(current_play, grid_size):
            if grid.already_played(current_play):
                os.system("clear")
                print("Line has already been played")
                InputHandler.pause_and_prompt()
                continue
            else:
                os.system("clear")
                grid.update_grid(current_play)

            completed_block = grid.check_block_completed(current_play)  # to check if current play completed a block; if yes, call further functions from within
            if completed_block:
                grid.do_block_sign(str(player.name))
            else:
                player = player2 if player == player1 else player1
        else:
            os.system("clear")
            print("Invalid input format")
            InputHandler.pause_and_prompt()

    grid.print_grid()
    print("Game over\n")
    scores_dict = utils.scores(grid, player1, player2)
    print(f"Scores:\n{player1.name}: {scores_dict[player1.name]}\n{player2.name}: {scores_dict[player2.name]}")


if __name__ == "__main__":
    main()
