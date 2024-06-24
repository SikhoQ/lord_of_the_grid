from InquirerPy import inquirer


class InputHandler:
    @staticmethod
    def get_grid_size():
        return inquirer.select(message="Grid size:",
                               choices=list(range(2, 10))).execute()

    @staticmethod
    def get_current_play():
        return input("Enter play (e.g. A1-A2): ").upper()

    @staticmethod
    def pause_and_prompt():
        input("Press [ENTER] to continue")

    @staticmethod
    def valid_input_length(play):
        return len(play) == 5

    @staticmethod
    def valid_input_format(play, grid_size):
        alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if play[0] in alphas[:grid_size] and play[3] in alphas[:grid_size]:
            try:
                if 1 <= int(play[1]) <= grid_size and 1 <= int(play[4]) <= grid_size:
                    return play[2] == "-"
            except ValueError:
                return False
        return False
