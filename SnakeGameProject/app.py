from flask import Flask, render_template, request, jsonify
from SourceCode.Main import main
from SourceCode.SnakeGame import SnakeGame

app = Flask(__name__)
game = SnakeGame()  # Create a global instance of the SnakeGame class


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    game.start_game()  # Start the game
    return jsonify(game.game_logic.get_state()), 200


@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')
    game.game_logic.move_snake(direction)  # Move the snake in the given direction
    return jsonify(game.game_logic.get_state()), 200
