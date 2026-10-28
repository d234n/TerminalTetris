"""
=================================================
Rotasi, gerakan, penghapusan baris, dan high score
=================================================
"""

from config import HIGH_SCORE_FILE, height, width


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
            value = file.read().strip()
        return int(value) if value.isdigit() else 0
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
            file.write(str(max(0, score)))
    except OSError:
        pass


def update_high_score(current_score, best_score):
    if current_score > best_score:
        best_score = current_score
        save_high_score(best_score)
    return best_score


def rotate(shape):
    return [(3 - y, x) for x, y in shape]


def can_move(board, shape, x, y):
    for dx, dy in shape:
        nx = x + dx
        ny = y + dy

        if nx < 0 or nx >= width or ny >= height:
            return False

        if ny >= 0 and board[ny][nx]:
            return False

    return True


def clear_lines(board):
    remaining = [row for row in board if not all(row)]
    cleared = height - len(remaining)

    while len(remaining) < height:
        remaining.insert(0, [""] * width)

    board[:] = remaining
    return cleared