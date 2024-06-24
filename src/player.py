import string
from InquirerPy import inquirer


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    @staticmethod
    def get_player_initials():
        player1 = inquirer.select(message="Player 1 initial:",
                                  choices=list(string.ascii_uppercase)
                                  ).execute()
        player2 = inquirer.select(message="Player 2 initial:",
                                  choices=list(string.ascii_uppercase.replace(
                                      player1, ""))
                                  ).execute()
        return player1, player2
