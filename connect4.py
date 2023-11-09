import numpy as np
import random


def setup_board(cols, rows):
    return np.zeros((rows, cols))


def is_valid_col(board, col):
    # check if top location of row is empty
    return board[len(board) - 1][col] == 0


def get_valid_cols(board):
    # Get a list of the current valid columns to drop in
    return [i for i in range(len(board[0])) if is_valid_col(board, i)]


def get_valid_row(board, col):
    # Get the next valid row in a chosen column
    for i in range(len(board)):
        if board[i][col] == 0:
            return i


def drop_token(board, row, col, token):
    board[row][col] = token


def print_board(board):
    print("#############")

    for row in np.flip(board, 0):
        print(row)
    print("#############")


def check_for_winner(board):
    num_cols = len(board[0])
    num_rows = len(board)
    # check rows
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != 0:
                return row[col]
    # check columns
    for col in range(num_cols):
        for row in range(len(board) - 3):
            if (
                board[row][col]
                == board[row + 1][col]
                == board[row + 2][col]
                == board[row + 3][col]
                != 0
            ):
                return board[row][col]

    # Check upward diagonals
    for row in range(num_rows - 3):
        for col in range(num_cols - 3):
            if (
                board[row][col]
                == board[row + 1][col + 1]
                == board[row + 2][col + 2]
                == board[row + 3][col + 3]
                != 0
            ):
                return board[row][col]

    # Check downward diagonals
    for row in range(3, num_rows):
        for col in range(num_cols - 3):
            if (
                board[row][col]
                == board[row - 1][col + 1]
                == board[row - 2][col + 2]
                == board[row - 3][col + 3]
                != 0
            ):
                return board[row][col]

    return False


def play_game(board):
    turn_counter = 0
    game_over = False
    player_turn = True

    while not game_over:
        if player_turn:
            col = int(input("Player move:"))

            if is_valid_col(board, col):
                row = get_valid_row(board, col)
                drop_token(board, row, col, 1)
            else:
                print("Not a valid move, try again")
                continue
        else:
            col = int(input("AI move:"))

            if is_valid_col(board, col):
                row = get_valid_row(board, col)
                drop_token(board, row, col, 2)
            else:
                print("Not a valid move, try again")
                continue

        print_board(board)
        if check_for_winner(board):
            game_over = True
            return 1 if player_turn else -1
        if not get_valid_cols(board):
            game_over = True
            return 0
        player_turn = not player_turn
        turn_counter += 1


def play_game_training(board):
    turn_counter = 0
    game_over = False
    player_turn = True

    while not game_over:
        if player_turn:
            col = random.choice(get_valid_cols(board))

            if is_valid_col(board, col):
                row = get_valid_row(board, col)
                drop_token(board, row, col, 1)
            else:
                continue
        else:
            col = random.choice(get_valid_cols(board))

            if is_valid_col(board, col):
                row = get_valid_row(board, col)
                drop_token(board, row, col, 2)
            else:
                continue

        if check_for_winner(board):
            game_over = True
            return 1 if player_turn else -1
        if not get_valid_cols(board):
            game_over = True
            return 0

        player_turn = not player_turn
        turn_counter += 1


if __name__ == "__main__":
    for i in range(10):
        board = setup_board(10, 6)
        result = play_game_training(board)
        print(result)
