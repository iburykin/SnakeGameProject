import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SourceCode.Snake import Snake
from SourceCode.Board import Board
from SourceCode.GameLogic import GameLogic


# Tests for Snake class
def test_move():
    snake = Snake(5, 5)
    snake.direction = 'UP'
    assert snake.move(10, 10) == (4, 5)
    snake.direction = 'DOWN'
    assert snake.move(10, 10) == (6, 5)
    snake.direction = 'LEFT'
    assert snake.move(10, 10) == (5, 4)
    snake.direction = 'RIGHT'
    assert snake.move(10, 10) == (5, 6)


# Tests for Board class
def test_place_snake():
    board = Board(10, 10)
    snake = Snake(5, 5)
    board.place_snake(snake)
    assert board.grid[5][5] == 'H'
    assert board.grid[5][4] == 'B'
    assert board.grid[5][3] == 'B'


def test_place_food():
    board = Board(10, 10)
    board.place_food((5, 5))
    assert board.grid[5][5] == 'F'


def test_place_obstacles():
    board = Board(10, 10)
    board.place_obstacles([(5, 5), (5, 6)])
    assert board.grid[5][5] == 'O'
    assert board.grid[5][6] == 'O'


# Tests for GameLogic class
def test_move_snake():
    game = GameLogic(10, 10, 'Test')
    game.move_snake('UP')
    assert game.snake.head[0] == (4, 5)

