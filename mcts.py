from connect4 import *
import math
import copy
import numpy as np
import random


class Node:
    # In connect 4 the state is the current board setup for the node
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0


def mcts(root_state, max_iterations):
    root_node = Node(root_state)

    for _ in range(max_iterations):
        # Traverse tree (selection)
        leaf = selection(root_node)
        simulation_result = simulate(leaf.state)
        backpropagate(leaf, simulation_result)

    best_child = select_best_child(root_node)
    return best_child.state


def selection(node):
    """Traverse tree until leaf node is found based on UCB1

    Args:
        node (Node): root node for selection
    """
    # Traverse the tree
    while node.children and not is_terminal(node.state):
        node = select_child(node)

    if not is_terminal(node.state):
        node.children = expand_node(node)
        node = select_child(node)
    return node


def simulate(state):
    sim_state = state.copy()
    current_player = 2  # Start with AI (player 2)

    while True:
        valid_cols = get_valid_cols(sim_state)
        if not valid_cols:
            return 0  # draw

        col = random.choice(valid_cols)
        row = get_valid_row(sim_state, col)
        sim_state = drop_token(sim_state, row, col, current_player)

        if check_for_winner(sim_state):
            return (
                -1 if current_player == 1 else 1
            )  # -1 for player 1 win, 1 for player 2 win

        # Switch to the next player
        current_player = 3 - current_player  # Alternates between 1 and 2


def select_child(node):
    # select the child with highest UCB1 score. Used for traversing the tree
    best_child = None
    best_ucb1 = float("-inf")

    for child in node.children:
        if child.visits == 0:
            # If a child has not been visited yet, select it immediately.
            return child

        ucb1 = child.value / child.visits + np.sqrt(
            2 * np.log(node.visits) / child.visits
        )

        if ucb1 > best_ucb1:
            best_child = child
            best_ucb1 = ucb1

    return best_child


def expand_node(node):
    """Expands a node by generating all child nodes

    Args:
        node (Node): node object acting as root

    Returns:
        List(Node): a list of all the child nodes
    """
    state = node.state
    valid_cols = get_valid_cols(state)
    child_nodes = []

    for col in valid_cols:
        child_state = copy.deepcopy(state)
        row = get_valid_row(child_state, col)
        current_player = (
            1 if np.count_nonzero(state == 1) <= np.count_nonzero(state == 2) else 2
        )
        child_state = drop_token(child_state, row, col, current_player)
        child_node = Node(child_state, parent=node)
        child_nodes.append(child_node)

    return child_nodes


def backpropagate(node, result):
    # Update visits and values for all nodes along path back to root
    while node:
        node.visits += 1
        node.value += result
        node = node.parent


def select_best_child(node):
    """Choose the best child of node (the move to make) based on number of visits

    Args:
        node (Node): root node for selection

    Returns:
        Node: the best child node
    """
    best_child = None
    most_visits = 0
    for child in node.children:
        if child.visits > most_visits:
            best_child = child
            most_visits = child.visits
    return best_child


def is_terminal(board):
    """Check if the board is in a terminal state

    Args:
        board (np.ndarray): a game board

    Returns:
        bool: True if terminal, False otherwise
    """
    terminal = (not get_valid_cols(board)) or check_for_winner(board)
    return terminal


if __name__ == "__main__":
    board = setup_board(4, 4)
    board = np.array(
        [
            [2, 2, 2, 1, 0, 0],
            [1, 2, 1, 1, 0, 0],
            [2, 1, 2, 0, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
        ]
    )

    # [0 0 1 0 0 0]
    # [0 0 1 0 0 0]
    # [0 0 1 0 0 0]
    # [0 0 2 1 0 0]
    # [1 2 1 1 0 0]
    # [2 2 2 1 0 0]
    # print_board(selection(Node(board)).state)

    best_move = mcts(board, 100000)
    print("The selected board is: ")
    print_board(board)
    print("The best move is: ")
    print_board(best_move)

    # board = setup_board(4, 4)

    # while True:
    #     print_board(board)

    #     # Player move
    #     player_col = int(input("Player move: "))
    #     if is_valid_col(board, player_col):
    #         player_row = get_valid_row(board, player_col)
    #         board = drop_token(board, player_row, player_col, 1)
    #     else:
    #         print("Not a valid move, try again.")
    #         continue

    #     # Check for player win or draw
    #     if check_for_winner(board):
    #         print("Player wins!")
    #         break
    #     if not get_valid_cols(board):
    #         print("It's a draw!")
    #         break

    #     print_board(board)

    #     # AI move using MCTS
    #     board = mcts(board, 100000)

    #     # Check for AI win or draw
    #     if check_for_winner(board):
    #         print("AI wins!")
    #         break
    #     if not get_valid_cols(board):
    #         print("It's a draw!")
    #         break
