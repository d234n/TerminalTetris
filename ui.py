"""
=================================================
Tampilan curses, warna, pause, dan game over
=================================================
"""

import curses

from config import block_symbols, height, width


def setup_colors():
    if not curses.has_colors():
        return {}

    try:
        curses.start_color()
        purple = 129 if curses.COLORS >= 256 else curses.COLOR_MAGENTA
        orange = 208 if curses.COLORS >= 256 else curses.COLOR_YELLOW
    except curses.error:
        return {}

    try:
        curses.use_default_colors()
        background = -1
    except curses.error:
        background = curses.COLOR_BLACK

    palette = [
        curses.COLOR_CYAN,
        curses.COLOR_YELLOW,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_BLUE,
        purple,
        orange,
    ]

    color_pairs = {}
    try:
        for pair_id, symbol in enumerate(block_symbols, start=1):
            color = palette[(pair_id - 1) % len(palette)]
            curses.init_pair(pair_id, color, background)
            color_pairs[symbol] = pair_id
    except curses.error:
        return {}

    return color_pairs


def draw(stdscr, board, shape, x, y, score, best_score, block_symbol, colored_mode, color_pairs):
    stdscr.erase()

    stdscr.addstr(0, 2, "ASCII TETRIS")
    stdscr.addstr(1, 2, f"Score: {score} | Best: {best_score} | color: {'ON' if colored_mode else 'OFF'}")
    stdscr.addstr(2, 2, "+" + "." + "__" * (width + 1) + "." + "+")

    for row in range(height):
        stdscr.addstr(3 + row, 2, "|#|")

        for col in range(width):
            cell = board[row][col]

            for dx, dy in shape:
                if x + dx == col and y + dy == row:
                    cell = block_symbol
                    break

            attribute = curses.A_NORMAL
            if colored_mode and cell:
                attribute = curses.color_pair(color_pairs[cell])

            stdscr.addstr(3 + row, 5 + col * 2, cell if cell else "  ", attribute)

        stdscr.addstr(3 + row, 5 + width * 2, "|#|")

    stdscr.addstr(3 + height, 2, "|" + "%#" * (width + 2) + "|")
    stdscr.addstr(4 + height, 2, "`" + "¯¯" * (width + 2) + "´")
    stdscr.addstr(6 + height, 2, "Left/Right: move | Up: rotate")
    stdscr.addstr(7 + height, 2, "Down: faster | Space: drop | ESC: pause")

    stdscr.refresh()


def draw_pause(stdscr):
    stdscr.erase()
    stdscr.addstr(6, 12, "PAUSED")
    stdscr.addstr(7, 7, "--" * (width - 2) + "-")
    stdscr.addstr(8, 6, "[ESC] Continue")
    stdscr.addstr(9, 7, "--" * (width - 2) + "-")
    stdscr.addstr(10, 5, " [C] Change color")
    stdscr.addstr(11, 7, "--" * (width - 2) + "-")
    stdscr.addstr(12, 5, " [Q] Quit")
    stdscr.addstr(13, 7, "--" * (width - 2) + "-")

    stdscr.addstr(2, 2, "." + "__" * (width + 2) + ".")

    for row in range(height):
        stdscr.addstr(3 + row, 2, "||")

    for row in range(height):
        stdscr.addstr(3 + row, 6 + width * 2, "||")

    stdscr.addstr(3 + height, 2, "|" + "+" + "==" * (width + 1) + "+" + "|")
    stdscr.addstr(4 + height, 2, "`" + "¯¯" * (width + 2) + "´")
    stdscr.refresh()


def pause_game(stdscr):
    draw_pause(stdscr)

    stdscr.nodelay(False)
    while True:
        key = stdscr.getch()

        if key == 27:
            break

        if key in (ord("q"), ord("Q")):
            stdscr.nodelay(True)
            return True

    stdscr.nodelay(True)
    return False


def draw_terminal_size(stdscr, rows, cols):
    stdscr.erase()
    stdscr.addstr(0, 0, f"Terminal terbaca: {rows} baris x {cols} kolom")
    stdscr.addstr(1, 0, "Kirim angka ukuran terminal ini.")
    stdscr.refresh()


def draw_game_over(stdscr, score, best_score):
    stdscr.nodelay(False)
    stdscr.erase()
    stdscr.addstr(6, 10, "GAME OVER!")
    stdscr.addstr(7, 7, "--" * (width - 2) + "-")
    stdscr.addstr(8, 6, f"Final score: {score}")
    stdscr.addstr(9, 7, "--" * (width - 2) + "-")
    stdscr.addstr(10, 6, f"Best score: {best_score}")
    stdscr.addstr(11, 7, "--" * (width - 2) + "-")
    stdscr.addstr(12, 6, "Press any button")
    stdscr.addstr(13, 6, "to quit.")
    stdscr.addstr(14, 7, "--" * (width - 2) + "-")

    stdscr.addstr(2, 2, "." + "__" * (width + 2) + ".")

    for row in range(height):
        stdscr.addstr(3 + row, 2, "||")

    for row in range(height):
        stdscr.addstr(3 + row, 6 + width * 2, "||")

    stdscr.addstr(3 + height, 2, "|" + "+" + "==" * (width + 1) + "+" + "|")
    stdscr.addstr(4 + height, 2, "`" + "¯¯" * (width + 2) + "´")

    stdscr.refresh()
    stdscr.getch()