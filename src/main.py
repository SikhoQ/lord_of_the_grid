<<<<<<< HEAD
import curses
import utils
import game


def main(stdscr):
    curses.curs_set(0)
    curses.echo()
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    stdscr.clear()
    stdscr.attron(curses.A_BOLD)

    current_row = 0
    menu = ["Play Game", "How to Play", "Exit"]
    do_menu_selection = {0: game.play_game, 1: utils.print_help,
                         2: game.do_exit_game}
    while True:
        stdscr.clear()

        utils.print_menu(stdscr, menu, current_row)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            do_menu_selection[current_row](stdscr)
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
=======
import curses
import utils
import game


def main(stdscr):
    curses.curs_set(0)
    curses.echo()
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.attron(curses.A_BOLD)

    current_row = 0
    menu = ["Play Game", "How to Play", "Exit"]
    do_menu_selection = {0: game.play_game, 1: utils.print_help,
                         2: game.do_exit_game}

    while True:
        stdscr.clear()

        utils.print_menu(stdscr, menu, current_row)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            do_menu_selection[current_row](stdscr)
        stdscr.refresh()

        if game.game_over:
            game.game_over = False
            main(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)

# TODO: fix spacing between grid and prints and make it pretty overall
>>>>>>> 910f7a4 (fixed incorrect scoring and moved gameplay details to single score card)
