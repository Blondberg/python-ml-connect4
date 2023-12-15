import numpy as np
import random
import copy


class Board(object):
    def __init__(self, board, last_move=[None, None]) -> None:
        self.board = board
        self.last_move = last_move

    def is_valid_col(self, col):
        """Check if top location of row is empty

        Args:
            board (np.ndarray): a game board
            col (int): zero-indexed column to check

        Returns:
            bool: True if row is empy, False otherwise
        """
        try:
            return self.board[len(self.board) - 1][col] == 0
        except IndexError as e:
            return False

    def get_valid_row(self, col):
        """Get the next valid row in a chosen column (is 0)

        Args:
            board (np.ndarray): a game board
            col (int): column to check

        Returns:
            int: index of valid row, -1 if nothing is found
        """
        for i in range(len(self.board)):
            if self.board[i][col] == 0:
                return i

        return -1

    def legal_moves(self):
        """Get a list of the current valid columns to drop in

        Returns:
            list: list of valid column indices
        """
        return [i for i in range(len(self.board[0])) if self.is_valid_col(i)]

    def drop_token(self, row, col, token):
        """Sets the index at (row, col) in board to set token value

        Args:
            row (int): row to drop in
            col (int): col to drop in
            token (int): value of token

        Returns:
            Board: a copy of the board with the next move set
        """
        temp_board = copy.deepcopy(self)
        temp_board.board[row][col] = token
        return temp_board

    def print(self):
        """Prints the board to the screen

        Args:
            board (np.ndarray): a game board
        """
        print("#############")
        for row in np.flip(self.board, 0):
            print(row)
        print("#############")

    def check_for_winner(self):
        """Checks if there is a winner on the board by looking for 4-in-a-row of any character except 0

        Args:
            board (np.ndarray): a game board

        Returns:
            bool: Winner character, empty if no winner
        """
        num_cols = len(self.board[0])
        num_rows = len(self.board)
        # check rows
        for row in self.board:
            for col in range(len(row) - 3):
                if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != 0:
                    return row[col]
        # check columns
        for col in range(num_cols):
            for row in range(len(self.board) - 3):
                if (
                    self.board[row][col]
                    == self.board[row + 1][col]
                    == self.board[row + 2][col]
                    == self.board[row + 3][col]
                    != 0
                ):
                    return self.board[row][col]

        # Check upward diagonals
        for row in range(num_rows - 3):
            for col in range(num_cols - 3):
                if (
                    self.board[row][col]
                    == self.board[row + 1][col + 1]
                    == self.board[row + 2][col + 2]
                    == self.board[row + 3][col + 3]
                    != 0
                ):
                    return self.board[row][col]

        # Check downward diagonals
        for row in range(3, num_rows):
            for col in range(num_cols - 3):
                if (
                    self.board[row][col]
                    == self.board[row - 1][col + 1]
                    == self.board[row - 2][col + 2]
                    == self.board[row - 3][col + 3]
                    != 0
                ):
                    return self.board[row][col]

        return ""

    def play_game(self):
        turn_counter = 0
        game_over = False
        player_turn = True

        while not game_over:
            if player_turn:
                try:
                    col = int(input("Player move:"))
                except ValueError as e:
                    print("Not a valid move input, try again")
                    continue
                if self.is_valid_col(col):
                    row = self.get_valid_row(col)
                    self = self.drop_token(row, col, 1)
                else:
                    print("Not a valid move, try again")
                    continue
            else:
                try:
                    col = int(input("AI move:"))
                except ValueError as e:
                    print("Not a valid move input, try again")

                if self.is_valid_col(col):
                    row = self.get_valid_row(col)
                    self = self.drop_token(row, col, 2)
                else:
                    print("Not a valid move, try again")
                    continue

            self.print()
            if self.check_for_winner():
                game_over = True
                return -1 if player_turn else 10
            if not self.legal_moves():
                game_over = True
                return 0
            player_turn = not player_turn
            turn_counter += 1


if __name__ == "__main__":
    game_board = np.zeros((6, 4))

    board = Board(game_board)
    board.print()
    board.play_game()
