import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SourceCode.Snake import Snake
from SourceCode.Board import Board
from SourceCode.GameLogic import GameLogic


@pytest.fixture
def game():
    return GameLogic(10, 10, "Test Player")


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
def test_move_snake(game):
    game.move_snake('UP')
    assert game.snake.head[0] == (4, 5)


def test_food_generation(game):
    # Generate food multiple times and check if it always returns a valid position
    for _ in range(10):
        game.food = None  # Reset food
        game.generate_obstacles()  # Generate obstacles
        food = game.generate_food()
        assert food is None or food not in game.obstacles


def test_food_generation_inside_obstacle(game):
    # Generate obstacles on all blocks except one
    obstacles = []
    for y in range(10):
        row = []
        for x in range(10):
            if (y, x) != (0, 0):  # Exclude position (0, 0)
                position = (y, x)
                row.append(position)
        obstacles.append(row)

    game.obstacles = obstacles  # Set the obstacles for the game

    # Call the generate_food function
    generated_food = game.generate_food()

    # Check if the generated food is in a block with obstacles or not
    assert generated_food is not None
    assert generated_food in sum(obstacles, []), f"Generated food position: {generated_food}, Expected position in obstacles"


def test_food_generated_on_start(game):
    # Check if food is generated when the game starts
    assert game.food is not None






def test_food_generated_on_start(game):
    # Check if food is generated when the game starts
    assert game.food is not None
