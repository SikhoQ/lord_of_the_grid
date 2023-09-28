# import sys.argv to allow players to put their initial when launching the game
# e.g. python3 lord_of_the_grid.py player1=S player2=K
# also to allow players to choose grid size, min 4 (i.e. 4x4) - max 20

from sys import argv

grid = []  # game grid
alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # to be used in play prompt and input validation
# boolean to keep track of win status ???


def print_greeting():
    pass


def create_grid(grid_size):
    global grid

    # 'dots' to be connected in grid are represented by +
    # spaces between neighbouring 'dots' both horizontally and vertically (to be replaced by connecting lines during play)
    for i in range(grid_size):
        grid.append(["+", " "] * grid_size)
        grid[-1].pop()  # remove last spaces in each list (useless)
        if i != grid_size - 1:
            grid.append([" "] * grid_size * 2)  # add vertical spaces
            grid[-1].pop()  # remove last spaces in each list (useless)    


def display_grid(grid_size):
    print("  ")
    for each_list in grid:
        for item in each_list:
            print(item, end="  ")
        print()


def get_user_play(current_player, grid_size):
    print(f"\n\n\nPlayer {current_player}'s turn\n===============\n")

    player_prompt = f"Choose adjacent cells (format e.g. A1-A2) [min: A1  max: {alphas[grid_size - 1]}{grid_size}] to connect: "
    print(player_prompt)
    print(" " * 41, "==================")
    user_play = input().upper()

    while not valid_play(user_play, grid_size):
        print(player_prompt)
        print(" " * 41, "==================")
        user_play = input().upper()

    return user_play


def valid_play(user_play, grid_size):
    if len(user_play) != 5 or user_play[0] not in alphas[:grid_size] or user_play[3] not in alphas[:grid_size]\
        or not user_play[1].isdigit() or not int(user_play[1]) in range(1, grid_size + 1)\
            or not user_play[4].isdigit() or not int(user_play[4]) in range(1, grid_size + 1)\
            or user_play[2] != "-" or (user_play[0] == user_play[3] and abs(int(user_play[1]) - int(user_play[4])) != 1)\
            or (user_play[1] == user_play[4] and abs(alphas.index(user_play[0]) - alphas.index(user_play[3])) != 1):
        return False
    return True


def update_grid(current_play, player_1_block_count):
    global grid

    row_1 = 2 * alphas.index(current_play[0])  # multiply by 2 to compensate for seperating spaces
    col_1 = 2 * (int(current_play[1]) - 1)

    row_2 = 2 * alphas.index(current_play[3])  # multiply by 2 to compensate for seperating spaces
    col_2 = 2 * (int(current_play[4]) - 1)

    if row_1 == row_2:  # horizontal play
        grid[row_1][min([col_1, col_2]) + 1] = "-"  # find space to replace by adding 1 to the smaller column
    else:
        grid[min([row_1, row_2]) + 1][col_1] = "|"




def run_game(player_names, grid_size): 
    global grid

    game_not_over = True
    player_1_block_count = player_2_block_count = 0
    current_player = 1

    print_greeting()
    create_grid(grid_size)

    while game_not_over:
        display_grid(grid_size)  # display the current grid

        # Player 1's turn
        current_play = get_user_play(current_player, grid_size)  # prompt current user to play (current_play is a list of 2 tuples representing co-ord's)
        player_1_block_count = update_grid(current_play, player_1_block_count)  # update grid according to current player's play, and update block count if play completes block
        display_grid(grid_size)
 
        current_player = current_player % 2 + 1  # change current player, wrapping around 2 to alternate btw 1 & 2

        # Player 2's turn
        current_play = get_user_play(current_player, grid_size)
        player_2_block_count = update_grid(current_play, player_2_block_count)

        # if not still_space_in(grid):
        #     game_not_over = False
        #     print_game_result(player_1_block_count, player_2_block_count)


if __name__ == "__main__":
    if len(argv) == 4 and argv[3].isdigit():
        player_names = [argv[1][8], argv[2][8]]  # a list containing player initials
        grid_size = int(argv[3])  # the size of the grid, as a single number (e.g. 9 means 9x9)
        run_game(player_names, grid_size)
