import numpy as np
from mcts import (
    Node,
    mcts,
    is_terminal,
    select_child,
    expand_node,
    simulate,
    backpropagate,
    select_best_child,
)
from connect4 import (
    setup_board,
    get_valid_cols,
    get_valid_row,
    drop_token,
    check_for_winner,
    print_board,
)


def test_node_creation():
    state = np.zeros((6, 7), dtype=int)
    node = Node(state)
    assert node.state.shape == state.shape
    assert node.parent is None
    assert not node.children
    assert node.visits == 0
    assert node.value == 0


def test_mcts():
    root_state = np.zeros((6, 7), dtype=int)
    max_iterations = 100
    final_state = mcts(root_state, max_iterations)
    assert isinstance(final_state, np.ndarray)


def test_is_terminal():
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
    assert is_terminal(board_win)

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
    assert is_terminal(board_draw)

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
    assert not is_terminal(board_no_win)


def test_select_child():
    state = np.zeros((6, 7), dtype=int)
    root_node = Node(state)
    child_node_1 = Node(state, parent=root_node)
    child_node_2 = Node(state, parent=root_node)
    root_node.children = [child_node_1, child_node_2]
    selected_child = select_child(root_node)
    assert selected_child in root_node.children


def test_expand_node():
    state = np.zeros((6, 7), dtype=int)
    node = Node(state)
    expanded_nodes = expand_node(node)
    assert expanded_nodes
    for child in expanded_nodes:
        assert isinstance(child, Node)
        assert child.parent == node


def test_simulate():
    state = np.zeros((6, 7), dtype=int)
    result = simulate(state)
    assert result in [-1, 0, 1]


def test_backpropagate():
    board = np.zeros((6, 7), dtype=int)
    root_node = Node(board)
    root_node.children = expand_node(root_node)

    for child in root_node.children:
        backpropagate(child, 1)

    assert root_node.visits == len(root_node.children)


def test_select_best_child():
    state = np.zeros((6, 7), dtype=int)
    root_node = Node(state)
    child_node_1 = Node(state, parent=root_node)
    child_node_2 = Node(state, parent=root_node)
    root_node.children = [child_node_1, child_node_2]
    best_child = select_best_child(root_node)
    assert best_child in root_node.children
