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


def scores(grid, player1, player2):
    scores_dict = {player1.name: 0, player2.name: 0}
    for row in grid.grid:
        for cell in row:
            if cell == player1.name:
                scores_dict[player1.name] += 1
            elif cell == player2.name:
                scores_dict[player2.name] += 1
    return scores_dict


def game_ended(grid):
    for row in grid.grid:
        if " " in row:
            return False
    return True
