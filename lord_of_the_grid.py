# import sys.argv to allow players to put their initial when launching the game
# e.g. python3 lord_of_the_grid.py player1=S player2=K
# also to allow players to choose grid size, min 4 (i.e. 4x4) - max 20

from sys import argv

# boolean to check if current move completed a block; if so, player goes again
completed_block = False

grid = []  # game grid

# to be used in play prompt and input validation
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def print_instructions():
    print("\n")
    print(" " * 4 + "*" * 30)
    print("     Welcome to Lord of the Grid!")
    print(" " * 4 + "*" * 30, end="\n\n\n")
    print("""    > The objective of the game is to own as many blocks as\
 possible by \n         connecting\
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
    # spaces between neighbouring 'dots' both horizontally and
    # vertically (to be replaced by connecting lines during play)
    for i in range(grid_size):
        grid.append(["+", " "] * grid_size)
        grid[-1].pop()  # remove last spaces in each list (useless)
        if i != grid_size - 1:
            grid.append([" "] * grid_size * 2)  # add vertical spaces
            grid[-1].pop()  # remove last spaces in each list (useless)


def display_grid(grid_size):
    print("\n\n" + " "*7, end="")  # print spaces before the 1

    # printing column labels (1 to grid_size)
    for i in range(1, grid_size + 1):
        print(i, end=" "*5)

    print("\n\n")

    i = 0
    for this_line in grid:
        if "+" in this_line:
            print(f"{alpha[i]}", end=" "*6)
            i += 1
        else:
            print(" "*7, end="")
        for item in this_line:
            print(item, end=" "*2)
        print()


def get_user_play(current_player, grid_size):
    print(f"\n\n\nPlayer {current_player}'s turn\n===============\n")

    player_prompt = f"Choose adjacent cells (format e.g. A1-A2)\
 [min: A1  max: {alpha[grid_size - 1]}{grid_size}] to connect ['q' to quit]: "
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

    # multiply by 2 to compensate for seperating spaces
    row1 = 2 * alpha.index(current_play[0])
    col1 = 2 * (int(current_play[1]) - 1)

    # multiply by 2 to compensate for seperating spaces
    row2 = 2 * alpha.index(current_play[3])
    col2 = 2 * (int(current_play[4]) - 1)

    sign_block = []

    if direction == "up":
        # if the played vertical line is not along the edges
        if current_play[1] != "1" and current_play[1] != str(grid_size):
            # if play completes 2 blocks, either side of line
            if grid[row2][col2 - 1] == "-" and\
                grid[row2 + 1][col2 - 2] == "|"\
                    and grid[row1][col1 - 1] == "-"\
                    and grid[row2][col2 + 1] == "-"\
                    and grid[row2 + 1][col2 + 2] == "|"\
                    and grid[row1][col1 + 1] == "-":
                sign_block.extend([row1 - 1, col1 + 1, row1 - 1, col1 - 1])

            # on the left of vertical line
            elif grid[row2][col2 - 1] == "-"\
                    and grid[row2 + 1][col2 - 2] == "|"\
                    and grid[row1][col1 - 1] == "-":
                sign_block.extend([row1 - 1, col1 - 1])

            # on the right of vertical line
            elif grid[row2][col2 + 1] == "-"\
                    and grid[row2 + 1][col2 + 2] == "|"\
                    and grid[row1][col1 + 1] == "-":
                sign_block.extend([row1 - 1, col1 + 1])

        # played vertical line is along left edge
        elif current_play[1] == "1":
            if grid[row2][col2 + 1] == "-"\
                    and grid[row2 + 1][col2 + 2] == "|"\
                    and grid[row1][col1 + 1] == "-":
                sign_block.extend([row1 - 1, col1 + 1])

        # played vertical line is along right edge
        else:
            # on the left of vertical line
            if grid[row2][col2 - 1] == "-"\
                    and grid[row2 + 1][col2 - 2] == "|"\
                    and grid[row1][col1 - 1] == "-":
                sign_block.extend([row1 - 1, col1 - 1])

    elif direction == "down":
        # if the played vertical line is not along the edges
        if current_play[1] != "1" and current_play[1] != str(grid_size):
            # if play completes 2 blocks, either side of line
            if grid[row2][col2 - 1] == "-"\
                    and grid[row2 - 1][col2 - 2] == "|"\
                    and grid[row1][col1 - 1] == "-"\
                    and grid[row2][col2 + 1] == "-"\
                    and grid[row2 - 1][col2 + 2] == "|"\
                    and grid[row1][col1 + 1] == "-":
                sign_block.extend([row2 - 1, col2 - 1, row2 - 1, col2 + 1])

            # on left of line
            elif grid[row2][col2 - 1] == "-"\
                    and grid[row2 - 1][col2 - 2] == "|"\
                    and grid[row1][col1 - 1] == "-":
                sign_block.extend([row2 - 1, col2 - 1])

            # on right of line
            elif grid[row2][col2 + 1] == "-"\
                    and grid[row2 - 1][col2 + 2] == "|"\
                    and grid[row1][col1 + 1] == "-":
                sign_block.extend([row2 - 1, col2 + 1])

        # played vertical line is along left edge
        elif current_play[1] == "1":
            if grid[row2][col2 + 1] == "-"\
                    and grid[row2 - 1][col2 + 2] == "|"\
                    and grid[row1][col1 + 1] == "-":
                sign_block.extend([row2 - 1, col2 + 1])

        # line is along right edge
        else:
            # on left of line
            if grid[row2][col2 - 1] == "-"\
                    and grid[row2 - 1][col2 - 2] == "|"\
                    and grid[row1][col1 - 1] == "-":
                sign_block.extend([row2 - 1, col2 - 1])

    elif direction == "right":
        # if played horizontal line is not along top or bottom edge
        if current_play[0] != "A" and current_play[0] != alpha[grid_size - 1]:
            # if play completes 2 blocks, on either side
            if grid[row2 - 1][col2] == "|"\
                    and grid[row2 - 2][col2 - 1] == "-"\
                    and grid[row1 - 1][col1] == "|"\
                    and grid[row2 + 1][col2] == "|"\
                    and grid[row2 + 2][col2 - 1] == "-"\
                    and grid[row2 + 1][col2 - 2] == "|":
                sign_block.extend([row2 - 1, col2 - 1, row2 + 1, col2 - 1])

            # above line
            elif grid[row2 - 1][col2] == "|"\
                    and grid[row2 - 2][col2 - 1] == "-"\
                    and grid[row1 - 1][col1] == "|":
                sign_block.extend([row2 - 1, col2 - 1])

            # below line
            elif grid[row2 + 1][col2] == "|"\
                    and grid[row2 + 2][col2 - 1] == "-"\
                    and grid[row2 + 1][col2 - 2] == "|":
                sign_block.extend([row2 + 1, col2 - 1])

        elif current_play[0] == "A":  # along top edge
            # below line
            if grid[row2 + 1][col2] == "|"\
                    and grid[row2 + 2][col2 - 1] == "-"\
                    and grid[row2 + 1][col2 - 2] == "|":
                sign_block.extend([row2 + 1, col2 - 1])

        else:  # along bottom edge
            # above line
            if grid[row2 - 1][col2] == "|"\
                    and grid[row2 - 2][col2 - 1] == "-"\
                    and grid[row1 - 1][col1] == "|":
                sign_block.extend([row2 - 1, col2 - 1])

    else:  # obviously, direction: left
        # if played horizontal line is not along top or bottom edge
        if current_play[0] != "A"\
                and current_play[0] != alpha[grid_size - 1]:
            if grid[row2 + 1][col2] == "|"\
                    and grid[row2 + 2][col2 + 1] == "-"\
                    and grid[row2 + 1][col2 + 2] == "|"\
                    and grid[row2 - 1][col2] == "|"\
                    and grid[row2 - 2][col2 + 1] == "-"\
                    and grid[row2 - 1][col2 + 2] == "|":
                sign_block.extend([row2 + 1, col2 - 1, row2 - 1, col2 + 1])

            # below line
            elif grid[row2 + 1][col2] == "|"\
                    and grid[row2 + 2][col2 + 1] == "-"\
                    and grid[row2 + 1][col2 + 2] == "|":
                sign_block.extend([row2 + 1, col2 - 1])

            # above line
            elif grid[row2 - 1][col2] == "|"\
                    and grid[row2 - 2][col2 + 1] == "-"\
                    and grid[row2 - 1][col2 + 2] == "|":
                sign_block.extend([row2 - 1, col2 + 1])
        # along top edge
        elif current_play[0] == "A":
            # below line
            if grid[row2 + 1][col2] == "|"\
                    and grid[row2 + 2][col2 + 1] == "-"\
                    and grid[row2 + 1][col2 + 2] == "|":
                sign_block.extend([row2 + 1, col2 + 1])

        else:  # along bottom edge
            # above line
            if grid[row2 - 1][col2] == "|"\
                    and grid[row2 - 2][col2 + 1] == "-"\
                    and grid[row2 - 1][col2 + 2] == "|":
                sign_block.extend([row2 - 1, col2 + 1])

    # if our list of co-ords is no longer empty (completed block was found)
    if len(sign_block) != 0:
        completed_block = True
        do_block_sign(sign_block, player_name)
    else:
        completed_block = False


def do_block_sign(sign_block, player_name):
    global grid

    # just put the player's initial in the completed block
    grid[sign_block[0]][sign_block[1]] = player_name

    if len(sign_block) == 4:
        # sign_block has length 4 when single play completes 2 blocks,
        # in which case sign both blocks
        grid[sign_block[2]][sign_block[3]] = player_name


def valid_play(user_play, grid_size):
    u_p = user_play  # to shorten our lines:)
    if len(u_p) != 5\
            or u_p[0] not in alpha[:grid_size]\
            or u_p[3] not in alpha[:grid_size]\
            or not u_p[1].isdigit()\
            or not int(u_p[1]) in range(1, grid_size + 1)\
            or not u_p[4].isdigit()\
            or not int(u_p[4]) in range(1, grid_size + 1)\
            or u_p[2] != "-"\
            or (u_p[0] == u_p[3]
                and abs(int(u_p[1]) - int(u_p[4])) != 1)\
            or (u_p[1] == u_p[4]
                and abs(alpha.index(u_p[0]) - alpha.index(u_p[3])) != 1)\
            or (u_p[0] != u_p[3] and u_p[1] != u_p[4]):
        return False
    return True


def update_grid(current_play, player_name, grid_size):
    global grid
    player = player_name  # again, for shorter lines:)

    # multiply by 2 to compensate for seperating spaces
    row1 = 2 * alpha.index(current_play[0])
    col1 = 2 * (int(current_play[1]) - 1)

    # multiply by 2 to compensate for seperating spaces
    row2 = 2 * alpha.index(current_play[3])
    col2 = 2 * (int(current_play[4]) - 1)

    direction = ""
    if row1 == row2:  # horizontal play
        # find space to replace by adding 1 to the smaller column
        grid[row1][min([col1, col2]) + 1] = "-"

        # play direction : RIGHT
        if current_play[1] > current_play[4]:
            direction = "left"
        else:
            direction = "right"
    else:
        grid[min([row1, row2]) + 1][col1] = "|"

        if current_play[0] > current_play[3]:  # play direction: UP
            direction = "up"
        else:
            direction = "down"

    # to check if current play completed a block;
    # if yes, call further functions from within
    return check_block_completed(current_play, player, direction, grid_size)


def still_space_in_grid():
    for row in range(len(grid)):
        for column in range(len(grid)):
            if grid[row][column] == " ":
                return True
    return False


def game_result(player_names):
    player = [0, 0]
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
        str_1 = "\n" + "*" * 14 + f"\nPlayer\
 {player.index(max(player)) + 1} wins!" + "\n" + "*" * 14
    else:
        str_1 = "\n" + "*" * 11 + "\nIt's a tie!" + "\n" + "*" * 11

    str_2 = "\n\n" + "=" * 12 + "\n" + "Game Scores:\n" + "=" * 12
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

    # display the current grid
    display_grid(grid_size)

    while game_not_over:

        # Player 1's turn
        player_name = player_names[name_index - 1]

        # prompt current user to play
        # (current_play is a list of 2 tuples representing co-ord's)
        current_play = get_user_play(current_player, grid_size)

        if current_play.lower() == "q":
            break

        # update grid according to current player's play,
        # and update block count if play completes block
        update_grid(current_play, player_name, grid_size)

        #  Next player's turn if current player did not complete a block
        if not completed_block:
            # change current player, wrapping around 2 to alternate btw 1 & 2
            current_player = current_player % 2 + 1
            # change current player's initial
            name_index = name_index % 2 + 1

        display_grid(grid_size)  # display the current grid

        if not still_space_in_grid():
            game_not_over = False
            print(game_result(player_names))


if __name__ == "__main__":
    if len(argv) == 4:
        player1 = "".join([player1[-1] for player1 in argv if "player1=" in
                           player1.lower() and len(player1) == 9]).upper()
        player2 = "".join([player2[-1] for player2 in argv if "player2=" in
                           player2.lower() and len(player2) == 9]).upper()
        grid_size = int("".join([size[-1] for size in argv if "size=" in
                                 size.lower() and size[-1].isdigit()]))
        if player1 and player2 and grid_size:
            player_names = player1 + player2
            run_game(player_names, grid_size)
    else:
        output = "python3 lord_of_the_grid.py [arg1] [arg2] [arg3]"
        print("***HOW TO RUN***".center(39))
        print(("=" * 14).center(39), end="\n\n")
        print(f"      {output}".center(39))
        print("e.g.  python3 lord_of_the_grid.py size=6 player1=S player2=M\n")
