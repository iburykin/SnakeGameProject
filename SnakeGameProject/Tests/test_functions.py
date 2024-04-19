import pytest
import sys
sys.path.append('C:/Users/prana/PycharmProjects/SnakeGameProject/SnakeGameProject/SourceCode')
from Main import Snake, Board, GameLogic

def test_snake_init():
    snake = Snake(10, 10)
    assert len(snake.body) == 3
    assert snake.direction == 'RIGHT'

def test_snake_move():
    snake = Snake(10, 10)
    new_head = snake.move(20, 20)
    assert isinstance(new_head, tuple)  # New head should be a tuple

def test_board_init():
    board = Board(20, 20)
    assert board.width == 20
    assert board.height == 20

def test_board_place_snake():
    board = Board(20, 20)
    snake = Snake(10, 10)
    board.place_snake(snake)
    assert board.grid[10][10] == 'O'  # Snake body should be placed on the board

def test_board_place_food():
    board = Board(20, 20)
    board.place_food((5, 5))
    assert board.grid[5][5] == 'X'  # Food should be placed on the board

def test_board_place_obstacles():
    board = Board(20, 20)
    board.place_obstacles([(15, 15), (16, 16)])
    assert board.grid[15][15] == 'H'  # Obstacles should be placed on the board
    assert board.grid[16][16] == 'H'

def test_game_logic_init():
    # Test initialization of GameLogic
    game_logic = GameLogic(20, 20)
    assert game_logic.width == 20
    assert game_logic.height == 20
    assert len(game_logic.snake.body) == 3
    assert game_logic.game_over == False

def test_game_logic_generate_food():
    # Test generate_food function
    game_logic = GameLogic(20, 20)
    food = game_logic.generate_food()
    assert isinstance(food, tuple)
    assert len(food) == 2
    assert 0 <= food[0] < 20
    assert 0 <= food[1] < 20

def test_game_logic_generate_obstacles():
    # Test generate_obstacles function
    game_logic = GameLogic(20, 20)
    obstacles = game_logic.generate_obstacles()
    assert isinstance(obstacles, list)
    for obstacle in obstacles:
        assert isinstance(obstacle, list)
        for square in obstacle:
            assert isinstance(square, tuple)
            assert len(square) == 2
            assert 0 <= square[0] < 20
            assert 0 <= square[1] < 20

def test_game_logic_move_snake():
    # Test move_snake function
    game_logic = GameLogic(20, 20)
    game_logic.move_snake()
    assert len(game_logic.snake.body) == 3  # Snake should have moved forward
    assert len(game_logic.snake.head) == 1  # Snake's head should have moved forward

def test_game_logic_update_board():
    # Test update_board function
    game_logic = GameLogic(20, 20)
    game_logic.update_board()
    assert isinstance(game_logic.board, Board)
    assert game_logic.board.width == 20
    assert game_logic.board.height == 20
    assert game_logic.board.grid != [[' ' for _ in range(20)] for _ in range(20)]