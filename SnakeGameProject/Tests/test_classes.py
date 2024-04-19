import sys
import pytest

sys.path.append('C:/Users/prana/PycharmProjects/SnakeGameProject/SnakeGameProject/SourceCode')
from Main import Snake, Board, GameLogic, SnakeGameGUI
def test_snake_class():
    # Test Snake class initialization
    snake = Snake(5, 5)
    assert snake.body == [(5, 5), (5, 4), (5, 3)]
    assert snake.head == [(5, 5)]
    assert snake.direction == 'RIGHT'

    # Test Snake class move method
    new_head = snake.move(10, 10)
    assert new_head == (5, 6)

def test_board_class():
    # Test Board class initialization
    board = Board(10, 10)
    assert board.width == 10
    assert board.height == 10
    assert len(board.grid) == 10
    assert all(len(row) == 10 for row in board.grid)
    assert board.obstacles == []

    # Test Board class methods
    snake = Snake(5, 5)
    board.place_snake(snake)
    assert board.grid[5][5] == 'O'
    board.place_food((3, 3))
    assert board.grid[3][3] == 'X'
    obstacles = [(2, 2), (3, 3), (4, 4)]
    board.place_obstacles(obstacles)
    assert board.grid[2][2] == 'H'
    assert board.grid[3][3] == 'H'
    assert board.grid[4][4] == 'H'

def test_game_logic_class():
    # Test GameLogic class initialization and methods
    game_logic = GameLogic(10, 10)
    assert isinstance(game_logic.snake, Snake)
    assert isinstance(game_logic.board, Board)
    assert game_logic.food is not None
    assert game_logic.obstacles is not None
    assert game_logic.speed == 1.0
    assert not game_logic.game_over

    # Test GameLogic class methods
    new_food = game_logic.generate_food()
    assert len(new_food) == 2
    assert 0 <= new_food[0] < 10
    assert 0 <= new_food[1] < 10
    obstacles = game_logic.generate_obstacles()
    assert isinstance(obstacles, list)
    for obstacle in obstacles:
        assert isinstance(obstacle, list)
        for square in obstacle:
            assert isinstance(square, tuple)
            assert len(square) == 2
            assert 0 <= square[0] < 10
            assert 0 <= square[1] < 10
