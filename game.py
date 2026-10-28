"""
=================================================
Loop utama game
=================================================
"""

import curses
import random
import time

from config import block_symbols, height, shapes, width
from game_logic import can_move, clear_lines, load_high_score, rotate, update_high_score
from ui import draw, draw_game_over, draw_terminal_size, pause_game, setup_colors


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)

    board = [[""] * width for _ in range(height)]
    score = 0
    best_score = load_high_score()
    game_over = False

    shape = random.choice(shapes)
    block_symbol = random.choice(block_symbols)
    x, y = 3, 0

    last_fall = time.monotonic()
    fall_delay = 0.5

    color_pairs = setup_colors()
    colored_mode = False

    while not game_over:
        rows, cols = stdscr.getmaxyx()

        if rows < height + 7 or cols < 38:
            draw_terminal_size(stdscr, rows, cols)
            time.sleep(0.1)
            continue

        key = stdscr.getch()

        if key == 27:
            should_quit = pause_game(stdscr)

            if should_quit:
                break

            last_fall = time.monotonic()
            continue

        if key in (ord("q"), ord("Q")):
            break
        elif key in (ord("c"), ord("C")) and color_pairs:
            colored_mode = not colored_mode

        if key == curses.KEY_LEFT:
            if can_move(board, shape, x - 1, y):
                x -= 1
        elif key == curses.KEY_RIGHT:
            if can_move(board, shape, x + 1, y):
                x += 1
        elif key == curses.KEY_UP:
            rotated = rotate(shape)
            if can_move(board, rotated, x, y):
                shape = rotated
        elif key == curses.KEY_DOWN:
            if can_move(board, shape, x, y + 1):
                y += 1
        elif key == ord(" "):
            while can_move(board, shape, x, y + 1):
                y += 1
            last_fall = 0

        now = time.monotonic()

        if now - last_fall >= fall_delay:
            if can_move(board, shape, x, y + 1):
                y += 1
            else:
                for dx, dy in shape:
                    nx = x + dx
                    ny = y + dy

                    if 0 <= ny < height:
                        board[ny][nx] = block_symbol

                cleared = clear_lines(board)
                score += cleared * 100
                best_score = update_high_score(score, best_score)

                shape = random.choice(shapes)
                block_symbol = random.choice(block_symbols)
                x, y = 3, 0

                if not can_move(board, shape, x, y):
                    game_over = True

            last_fall = now

        draw(stdscr, board, shape, x, y, score, best_score, block_symbol, colored_mode, color_pairs)
        time.sleep(0.03)

    draw_game_over(stdscr, score, best_score)