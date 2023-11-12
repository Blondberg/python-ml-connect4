import numpy as np
import random
import copy


def setup_board(cols, rows):
    """Create a new board based on set number of columns and rows

    Args:
        cols (int): number of columns
        rows (int): number of rows

    Returns:
        np.ndarray: array of size (rows, cols) filled with zeroes
    """
    return np.zeros((rows, cols))


def is_valid_col(board, col):
    """Check if top location of row is empty

    Args:
        board (np.ndarray): a game board
        col (int): zero-indexed column to check

    Returns:
        bool: True if row is empy, False otherwise
    """
    return board[len(board) - 1][col] == 0


def get_valid_cols(board):
    """Get a list of the current valid columns to drop in

    Args:
        board (np.ndarray): a game board

    Returns:
        list: list of valid column indices
    """
    return [i for i in range(len(board[0])) if is_valid_col(board, i)]


def get_valid_row(board, col):
    """Get the next valid row in a chosen column (is 0)

    Args:
        board (np.ndarray): a game board
        col (int): column to check

    Returns:
        int: index of valid row
    """
    for i in range(len(board)):
        if board[i][col] == 0:
            return i


def drop_token(board, row, col, token):
    """Sets the index at (row, col) in board to set token value

    Args:
        board (np.ndarray): a game board
        row (int): row to drop in
        col (int): col to drop in
        token (int): value of token

    Returns:
        np.ndarray: copy of board with the new change
    """
    temp_board = copy.deepcopy(board)
    temp_board[row][col] = token
    return temp_board


def print_board(board):
    """Prints the board to the screen

    Args:
        board (np.ndarray): a game board
    """
    print("#############")
    for row in np.flip(board, 0):
        print(row)
    print("#############")


def check_for_winner(board):
    """Checks if there is a winner on the board by looking for 4-in-a-row of any character except 0

    Args:
        board (np.ndarray): a game board

    Returns:
        bool: True if a winner is found, otherwise False
    """
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
                return True

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
                return True

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
                return True

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
                board = drop_token(board, row, col, 1)
            else:
                print("Not a valid move, try again")
                continue
        else:
            col = int(input("AI move:"))

            if is_valid_col(board, col):
                row = get_valid_row(board, col)
                board = drop_token(board, row, col, 2)
            else:
                print("Not a valid move, try again")
                continue

        print_board(board)
        if check_for_winner(board):
            game_over = True
            return -1 if player_turn else 10
        if not get_valid_cols(board):
            game_over = True
            return 0
        player_turn = not player_turn
        turn_counter += 1


if __name__ == "__main__":
    board = setup_board(10, 6)
