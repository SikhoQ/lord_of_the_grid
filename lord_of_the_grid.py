# import sys.argv to allow players to put their initial when launching the game
# e.g. python3 lord_of_the_grid.py player1=S player2=K
# also to allow players to choose grid size, min 4 (i.e. 4x4) - max 20

from sys import argv

completed_block = False  # boolean to check if current move completed a block; if so, player goes again
grid = []  # game grid
alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # to be used in play prompt and input validation


def print_instructions():
    print("\n")
    print(" " + "*" * 30)
    print("  Welcome to Lord of the Grid!")
    print(" " + "*" * 30, end="\n\n\n")
    print("""    > The objective of the game is to own as many blocks as possible by \n       connecting\
 dots on the 'grid' either vertically or horizontally.
    > Connections can only be made between 'neighbouring' dots.\n\n""")
    print("=" * 53)
    print("|" + " " * 51 + "|")
    print("""| NOTE: Input Format  >> row1column1-row2column2 << |
|            e.g:  >> d1-d2 <<                      |""")
    print("|" + " " * 51 + "|")
    print("=" * 53, end="\n\n")


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
    print("\n\n" + " "*7, end="")  # print spaces before the 1

    for i in range(1, grid_size + 1):  # printing column labels (1 to grid_size)
        print(i, end=" "*5)

    print("\n\n")

    i = 0
    for this_line in grid:
        if "+" in this_line:
            print(f"{alphas[i]}", end=" "*6)
            i += 1
        else:
            print(" "*7, end="")
        for item in this_line:
            print(item, end=" "*2)
        print()


def get_user_play(current_player, grid_size):
    print(f"\n\n\nPlayer {current_player}'s turn\n===============\n")

    player_prompt = f"Choose adjacent cells (format e.g. A1-A2) [min: A1  max: {alphas[grid_size - 1]}{grid_size}] to connect: "
    print(player_prompt)
    print(" " * 41, "==================")
    user_play = input().upper()
    if user_play == "Q":
        return "q"

    while not valid_play(user_play, grid_size):
        print(player_prompt)
        print(" " * 41, "==================")
        user_play = input().upper()
        if user_play == "Q":
            return "q"

    return user_play.upper()


def check_block_completed(current_play, player_name, direction, grid_size):
    global grid, completed_block

    row_1 = 2 * alphas.index(current_play[0])  # multiply by 2 to compensate for seperating spaces
    col_1 = 2 * (int(current_play[1]) - 1)

    row_2 = 2 * alphas.index(current_play[3])  # multiply by 2 to compensate for seperating spaces
    col_2 = 2 * (int(current_play[4]) - 1)

    sign_block = []

    if direction == "up":
        if current_play[1] != "1" and current_play[1] != str(grid_size):  # if the played vertical line is not along the edges
            if grid[row_2][col_2 - 1] == "-" and grid[row_2 + 1][col_2 - 2] == "|" and grid[row_1][col_1 - 1] == "-"\
             and grid[row_2][col_2 + 1] == "-" and grid[row_2 + 1][col_2 + 2] == "|" and grid[row_1][col_1 + 1] == "-":  # if play completes 2 blocks, either side of line
                sign_block.extend([row_1 - 1, col_1 + 1, row_1 - 1, col_1 - 1])

            elif grid[row_2][col_2 - 1] == "-" and grid[row_2 + 1][col_2 - 2] == "|" and grid[row_1][col_1 - 1] == "-":  # on the left of vertical line
                sign_block.extend([row_1 - 1, col_1 - 1])

            elif grid[row_2][col_2 + 1] == "-" and grid[row_2 + 1][col_2 + 2] == "|" and grid[row_1][col_1 + 1] == "-":  # on the right of vertical line
                sign_block.extend([row_1 - 1, col_1 + 1])

        elif current_play[1] == "1":  # played vertical line is along left edge
            if grid[row_2][col_2 + 1] == "-" and grid[row_2 + 1][col_2 + 2] == "|" and grid[row_1][col_1 + 1] == "-":
                sign_block.extend([row_1 - 1, col_1 + 1])

        else:  # played vertical line is along right edge
            if grid[row_2][col_2 - 1] == "-" and grid[row_2 + 1][col_2 - 2] == "|" and grid[row_1][col_1 - 1] == "-":  # on the left of vertical line
                sign_block.extend([row_1 - 1, col_1 - 1])

    elif direction == "down":
        if current_play[1] != "1" and current_play[1] != str(grid_size):  # if the played vertical line is not along the edges
            if grid[row_2][col_2 - 1] == "-" and grid[row_2 - 1][col_2 - 2] == "|" and grid[row_1][col_1 - 1] == "-"\
             and grid[row_2][col_2 + 1] == "-" and grid[row_2 - 1][col_2 + 2] == "|" and grid[row_1][col_1 + 1] == "-":  # if play completes 2 blocks, either side of line
                sign_block.extend([row_2 - 1, col_2 - 1, row_2 - 1, col_2 + 1])

            elif grid[row_2][col_2 - 1] == "-" and grid[row_2 - 1][col_2 - 2] == "|" and grid[row_1][col_1 - 1] == "-":  # on left of line
                sign_block.extend([row_2 - 1, col_2 - 1])

            elif grid[row_2][col_2 + 1] == "-" and grid[row_2 - 1][col_2 + 2] == "|" and grid[row_1][col_1 + 1] == "-":  # on right of line
                sign_block.extend([row_2 - 1, col_2 + 1])

        elif current_play[1] == "1":  # played vertical line is along left edge
            if grid[row_2][col_2 + 1] == "-" and grid[row_2 - 1][col_2 + 2] == "|" and grid[row_1][col_1 + 1] == "-":
                sign_block.extend([row_2 - 1, col_2 + 1])

        else:  # line is along right edge
            if grid[row_2][col_2 - 1] == "-" and grid[row_2 - 1][col_2 - 2] == "|" and grid[row_1][col_1 - 1] == "-":  # on left of line
                sign_block.extend([row_2 - 1, col_2 - 1])

    elif direction == "right":
        if current_play[0] != "A" and current_play[0] != alphas[grid_size - 1]:  # if played horizontal line is not along top or bottom edge
            if grid[row_2 - 1][col_2] == "|" and grid[row_2 - 2][col_2 - 1] == "-" and grid[row_1 - 1][col_1] == "|"\
             and grid[row_2 + 1][col_2] == "|" and grid[row_2 + 2][col_2 - 1] == "-" and grid[row_2 + 1][col_2 - 2] == "|":  # if play completes 2 blocks, on either side
                sign_block.extend([row_2 - 1, col_2 - 1, row_2 + 1, col_2 - 1])

            elif grid[row_2 - 1][col_2] == "|" and grid[row_2 - 2][col_2 - 1] == "-" and grid[row_1 - 1][col_1] == "|":  # above line
                sign_block.extend([row_2 - 1, col_2 - 1])

            elif grid[row_2 + 1][col_2] == "|" and grid[row_2 + 2][col_2 - 1] == "-" and grid[row_2 + 1][col_2 - 2] == "|":  # below line
                sign_block.extend([row_2 + 1, col_2 - 1])

        elif current_play[0] == "A":  # along top edge
            if grid[row_2 + 1][col_2] == "|" and grid[row_2 + 2][col_2 - 1] == "-" and grid[row_2 + 1][col_2 - 2] == "|":  # below line
                sign_block.extend([row_2 + 1, col_2 - 1])

        else:  # along bottom edge
            if grid[row_2 - 1][col_2] == "|" and grid[row_2 - 2][col_2 - 1] == "-" and grid[row_1 - 1][col_1] == "|":  # above line
                sign_block.extend([row_2 - 1, col_2 - 1])

    else:  # obviously, direction: left
        if current_play[0] != "A" and current_play[0] != alphas[grid_size - 1]:  # if played horizontal line is not along top or bottom edge
            if grid[row_2 + 1][col_2] == "|" and grid[row_2 + 2][col_2 + 1] == "-" and grid[row_2 + 1][col_2 + 2] == "|"\
             and grid[row_2 - 1][col_2] == "|" and grid[row_2 - 2][col_2 + 1] == "-" and grid[row_2 - 1][col_2 + 2] == "|":
                sign_block.extend([row_2 + 1, col_2 - 1, row_2 - 1, col_2 + 1])

            elif grid[row_2 + 1][col_2] == "|" and grid[row_2 + 2][col_2 + 1] == "-" and grid[row_2 + 1][col_2 + 2] == "|":  # below line
                sign_block.extend([row_2 + 1, col_2 - 1])

            elif grid[row_2 - 1][col_2] == "|" and grid[row_2 - 2][col_2 + 1] == "-" and grid[row_2 - 1][col_2 + 2] == "|":  # above line
                sign_block.extend([row_2 - 1, col_2 + 1])

        elif current_play[0] == "A":  # along top edge
            if grid[row_2 + 1][col_2] == "|" and grid[row_2 + 2][col_2 + 1] == "-" and grid[row_2 + 1][col_2 + 2] == "|":  # below line
                sign_block.extend([row_2 + 1, col_2 + 1])

        else:  # along bottom edge
            if grid[row_2 - 1][col_2] == "|" and grid[row_2 - 2][col_2 + 1] == "-" and grid[row_2 - 1][col_2 + 2] == "|":  # above line
                sign_block.extend([row_2 - 1, col_2 + 1])

    if len(sign_block) != 0:  # if our list of co-ords is no longer empty (i.e. a completed block was found)
        completed_block = True
        do_block_sign(sign_block, player_name)
    else:
        completed_block = False


def do_block_sign(sign_block, player_name):
    global grid

    grid[sign_block[0]][sign_block[1]] = player_name  # just put the player's initial in the completed block

    if len(sign_block) == 4:
        grid[sign_block[2]][sign_block[3]] = player_name  # sign_block has length 4 when single play completes 2 blocks, in which case sign both blocks


def valid_play(user_play, grid_size):
    if len(user_play) != 5 or user_play[0] not in alphas[:grid_size] or user_play[3] not in alphas[:grid_size]\
        or not user_play[1].isdigit() or not int(user_play[1]) in range(1, grid_size + 1)\
            or not user_play[4].isdigit() or not int(user_play[4]) in range(1, grid_size + 1)\
            or user_play[2] != "-" or (user_play[0] == user_play[3] and abs(int(user_play[1]) - int(user_play[4])) != 1)\
            or (user_play[1] == user_play[4] and abs(alphas.index(user_play[0]) - alphas.index(user_play[3])) != 1)\
            or (user_play[0] != user_play[3] and user_play[1] != user_play[4]):
        return False
    return True


def update_grid(current_play, player_name, grid_size):
    global grid

    row_1 = 2 * alphas.index(current_play[0])  # multiply by 2 to compensate for seperating spaces
    col_1 = 2 * (int(current_play[1]) - 1)

    row_2 = 2 * alphas.index(current_play[3])  # multiply by 2 to compensate for seperating spaces
    col_2 = 2 * (int(current_play[4]) - 1)

    direction = ""
    if row_1 == row_2:  # horizontal play
        grid[row_1][min([col_1, col_2]) + 1] = "-"  # find space to replace by adding 1 to the smaller column

        if current_play[1] > current_play[4]:  # play direction : RIGHT
            direction = "left"
        else:
            direction = "right"
    else:
        grid[min([row_1, row_2]) + 1][col_1] = "|"

        if current_play[0] > current_play[3]:  # play direction: UP
            direction = "up"
        else:
            direction = "down"

    return check_block_completed(current_play, player_name, direction, grid_size)  # to check if current play completed a block; if yes, call further functions from within


def still_space_in_grid():
    for row in range(len(grid)):
        for column in range(len(grid)):
            if grid[row][column] == " ":
                return True
    return False


def game_result(player_names):
    player = [0,0]
    total = 0

    for row in grid:
        for item in row:
            if item == player_names[0]:
                player[0] += 1
                total += 1
            elif item == player_names[1]:
                player[1] += 1
                total += 1
    if player[0] != player[1]:
        str_1 = "\n" + "*" * 14 + f"\nPlayer {player.index(max(player)) + 1} wins!" + "\n" + "*" * 14
    else:
        str_1 = "\n" + "*" * 11 + "\nIt's a tie!" + "\n" + "*" * 11

    str_2 = "\n\n" + "=" * 12 + "\n" + f"Game Scores:\n" + "=" * 12
    str_3 = f"\n\nPlayer 1: {player[0]}/{total} blocks owned.\n\n"
    str_4 = f"Player 2: {player[1]}/{total} blocks owned.\n"


    return str_1 + str_2 + str_3 + str_4


def run_game(player_names, grid_size):
    global grid, completed_block

    game_not_over = True
    current_player = 1
    name_index = 1

    print_instructions()
    create_grid(grid_size)

    display_grid(grid_size)  # display the current grid

    while game_not_over:

        # Player 1's turn
        player_name = player_names[name_index - 1]
        current_play = get_user_play(current_player, grid_size)  # prompt current user to play (current_play is a list of 2 tuples representing co-ord's)
        if current_play.lower() == "q":
            break
        update_grid(current_play, player_name, grid_size)  # update grid according to current player's play, and update block count if play completes block

        #  Next player's turn if current player did not complete a block
        if not completed_block:
            current_player = current_player % 2 + 1  # change current player, wrapping around 2 to alternate btw 1 & 2
            name_index = name_index % 2 + 1  # change current player's initial

        display_grid(grid_size)  # display the current grid

        if not still_space_in_grid():
            game_not_over = False
            print(game_result(player_names))


if __name__ == "__main__":
    if len(argv) == 4 and argv[3][5].isdigit():
        if not int(argv[3][5]) > 9:
            player_names = [argv[1][8], argv[2][8]]  # a list containing player initials
            grid_size = int(argv[3][5])  # the size of the grid, as a single number (e.g. 9 means 9x9)
            run_game(player_names, grid_size)
        else:
            print("Max grid size: 9")
