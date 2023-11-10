from connect4 import *
import math


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
    root_node.visits = 1

    for i in range(max_iterations):
        print("Interation: ", i)
        node = root_node

        # traverse tree to leaf
        while node.children and not is_terminal(node.state):
            node = select_child(node)
        if not is_terminal(node.state):
            child_nodes = expand(node)
            for child_node in child_nodes:
                print_board(child_node.state)
            node.children = child_nodes

            # simulation
            result = simulate(node.state)

            # backpropagation
            backpropagate(node, result)
    best_child = select_best_child(root_node)
    return best_child.state


def select_child(node):
    # select the child with highest UCB1 score
    best_child = None
    best_ucb1 = float("-inf")

    for child in node.children:
        if child.visits == 0:
            # If a child has not been visited yet, select it immediately.
            return child
        ucb1 = child.value / child.visits + 2 * math.sqrt(
            math.log(node.visits) / child.visits
        )

        if ucb1 > best_ucb1:
            best_child = child
            best_ucb1 = ucb1

    return best_child


def expand(node):
    # expands node by generating all children

    state = node.state
    valid_cols = get_valid_cols(state)
    child_nodes = []

    for col in valid_cols:
        child_state = state.copy()  # Create a copy of the current state
        row = get_valid_row(child_state, col)
        drop_token(
            child_state, row, col, 1 if np.count_nonzero(state == 0) % 2 == 0 else 2
        )
        child_nodes.append(Node(child_state, parent=node))
    return child_nodes


def simulate(state):
    while True:
        valid_cols = get_valid_cols(state)
        if not valid_cols:
            return 0  # Draw
        col = random.choice(valid_cols)
        row = get_valid_row(state, col)
        drop_token(state, row, col, 1)  # Simulate player 1's move

        if check_for_winner(state):
            return 1  # Player 1 wins

        valid_cols = get_valid_cols(state)
        if not valid_cols:
            return 0  # Draw
        col = random.choice(valid_cols)
        row = get_valid_row(state, col)
        drop_token(state, row, col, 2)  # Simulate player 2's move

        if check_for_winner(state):
            return -1  # Player 2 wins


def backpropagate(node, result):
    # Update visits and values for all nodes along path back to root
    while node.parent:
        node.visits += 1
        node.value += result
        node = node.parent


def select_best_child(node):
    # Criteria for chosing best child node (most visits)
    best_child = None
    most_visits = 0
    for child in node.children:
        if child.visits >= most_visits:
            best_child = child
    return best_child


def is_terminal(board):
    # check if the board is in a terminal state
    return (not get_valid_cols(board)) or check_for_winner(board)


if __name__ == "__main__":
    test_board = np.array(
        [
            [1, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0],
            [2, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    test_board_2 = np.flip(
        np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 2, 0, 0, 0],
                [1, 2, 0, 0, 0],
                [1, 2, 1, 0, 0],
            ]
        ),
        0,
    )
    board = setup_board(4, 4)
    best_child = mcts(test_board_2.copy(), 10000)
    print("Best Child")
    print_board(best_child)
    # print_board(best_child)
    # for node in expand(Node(test_board)):
    #     print("Printing child states")
    #     print_board(node.state)
