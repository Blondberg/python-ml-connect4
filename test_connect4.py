from connect4 import *
import numpy as np


def test_setup_board():
    cols, rows = 10, 8
    board = setup_board(cols, rows)
    assert board.shape == (rows, cols)
    assert np.all(board == 0)


def test_is_valid_col():
    board = np.array(
        [
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
        ]
    )
    assert is_valid_col(board, 3)
    assert not is_valid_col(board, 1)


def test_get_valid_cols():
    board = np.array(
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 1, 0],
        ]
    )
    assert get_valid_cols(board) == [0, 1, 4]


def test_get_valid_row():
    board = np.array(
        [
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
        ]
    )
    assert get_valid_row(board, 3) == 3
    assert get_valid_row(board, 1) == 0
    assert not get_valid_row(board, 4)


def test_drop_token():
    board = np.zeros((6, 7), dtype=int)
    drop_token(board, 2, 4, 1)
    assert board[2, 4] == 1


def test_check_for_winner():
    board_win = np.array(
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    assert check_for_winner(board_win) == 1

    board_win = np.array(
        [
            [0, 0, 0, 1, 0],
            [0, 2, 0, 1, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 0, 2, 0],
            [0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
        ]
    )
    assert check_for_winner(board_win) == 2

    board_draw = np.array(
        [
            [1, 1, 2, 2, 1],
            [2, 1, 1, 1, 2],
            [1, 2, 2, 2, 1],
            [2, 2, 1, 1, 2],
            [1, 1, 2, 2, 1],
            [2, 1, 1, 1, 2],
        ]
    )
    assert check_for_winner(board_draw) == 0

    board_no_win = np.array(
        [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 2, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    assert not check_for_winner(board_no_win)
