from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from SourceCode.Snake import Snake
from SourceCode.SnakeGame import SnakeGame
from SourceCode.GameLogic import GameLogic

app = Flask(__name__)
game = None

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['snake_game']
collection = db['game_sessions']


@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    size = int(request.json.get('size', 10))  # Convert size to integer
    nickname = request.json.get('nickname')  # Get the nickname from the request
    game = SnakeGame(size, nickname)  # Create a new game instance
    game.start_game()  # Start the game
    return jsonify(game.get_state()), 200


@app.route('/get_state', methods=['GET'])
def get_state():
    if game is None or game.game_logic.game_over:
        return jsonify(game.get_state()), 400
    game.game_logic.update_game()  # Update the game state
    return jsonify(game.get_state()), 200


@app.route('/update_direction', methods=['POST'])
def update_direction():
    direction = request.json.get('direction')
    # Check if the new direction is opposite to the current direction
    opposite_directions = [('UP', 'DOWN'), ('DOWN', 'UP'), ('LEFT', 'RIGHT'), ('RIGHT', 'LEFT')]
    if (game.game_logic.snake.direction, direction) not in opposite_directions:
        game.game_logic.snake.direction = direction  # Update the direction of the snake
    return jsonify(game.get_state()), 200

# Function to store game result in MongoDB
@app.route('/submit_score', methods=['POST'])
def submit_score():
    score_data = request.json
    name = score_data['name']
    score = score_data['score']
    map_size = score_data['map_size']
    collection.insert_one({'name': name, 'score': score, 'map_size': map_size})
    return jsonify({"status": "success"}), 200

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    top_scores = collection.find().sort('score', -1).limit(10)
    leaderboard_data = [{'name': entry['name'], 'score': entry['score'], 'map_size': entry['map_size']} for entry in top_scores]
    return render_template('leaderboard.html', leaderboard=leaderboard_data)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except OSError:
        print("Stopping the game through IDE")
