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
