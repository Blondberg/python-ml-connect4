import numpy as np


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
    print("Col: ", col)
    print("Row : ", row)
    board[row][col] = token


def print_board(board):
    print("#############")

    for row in np.flip(board, 0):
        print(row)
    print("#############")


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
        player_turn = not player_turn
        turn_counter += 1


if __name__ == "__main__":
    board = setup_board(4, 3)
    print_board(board)
    play_game(board)
