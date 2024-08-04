import curses
import string

player = 1


class Player:

    @staticmethod
    def get_player_initial(stdscr, alphas):
        global player

        curses.curs_set(1)

        prompt = f"Enter player {player} initial (A - Z): "

        stdscr.clear()

        height, width = stdscr.getmaxyx()
        x = width // 2 - len(prompt) // 2
        y = height // 2

        stdscr.addstr(y, x, prompt)
        stdscr.refresh()

        player_initial = stdscr.getch()

        if player_initial in range(65, 91):
            unicode_to_ascii = {key: string.ascii_uppercase[key - 65]
                                for key in range(65, 91)}
        elif player_initial in range(97, 123):
            unicode_to_ascii = {key: string.ascii_lowercase[key - 97]
                                for key in range(97, 123)}

        message = ""

        if player_initial in range(65, 91) or\
           player_initial in range(97, 123):
            player_initial = unicode_to_ascii[player_initial]
            if player_initial not in alphas:
                message = "Initial already taken"
        else:
            message = "Invalid initial"

        if message:
            x = width // 2 - len(message) // 2
            stdscr.clear()
            stdscr.addstr(y, x, message)
            stdscr.refresh()
            curses.napms(1300)

            return Player.get_player_initial(stdscr, alphas)

        curses.napms(850)

        player = 2 if player == 1 else 1
        alphas = alphas.replace(player_initial.lower(), "")
        alphas = alphas.replace(player_initial.upper(), "")

        curses.curs_set(0)
        return player_initial.upper(), alphas
