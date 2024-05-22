let gameIntervalId = null;

function setCellSize(boardSize) {
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const maxCellWidth = Math.floor(viewportWidth / boardSize);
    const maxCellHeight = Math.floor(viewportHeight / boardSize);
    const cellSize = Math.min(maxCellWidth, maxCellHeight) - 2;
    const triangleSize = Math.floor(cellSize / 2);
    const style = document.createElement('style');
    style.innerHTML = `
        .row > div {
            width: ${cellSize}px;
            height: ${cellSize}px;
        }
    `;
    document.head.appendChild(style);
}

function startGame() {
        // Start the background music
        const music = document.getElementById('background-music');
        music.play();

    document.getElementById('endgameWindow').style.display = 'none';

    const nickname = document.getElementById('nickname').value;
    // Validate the nickname
    if (nickname === "" || nickname.length > 20) {
        alert('Please enter a valid nickname. It should be less than 20 characters and not empty.');
        return;
        }

    let size = document.getElementById('size').value;
    // Validate the size
    if (size < 5 || size > 25) {
        alert('Please enter a valid size between 5 and 25');
        return;
    }

    setCellSize(size);

    fetch('/start_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ size: size, nickname: nickname }),
    })

    .then(response => response.json())

    .then(() => {
        updateGameView();
        document.getElementById('startingWindow').style.display = 'none';
        document.getElementById('gameWindow').style.display = 'block';
    })

    .catch(error => console.error('Error starting game:', error));
}

function submitScore(name, score, map_size) {
    fetch('/submit_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, score: score, map_size: map_size }),
    })

    .then(response => response.json())

    .then(data => {
        if (data.status === 'success') {
            console.log('Score submitted successfully.');
        }
    })

    .catch(error => console.error('Error submitting score:', error));
}

function endGame(gameState) {
        // Stop the background music
    const music = document.getElementById('background-music');
    music.pause();
    music.currentTime = 0;  // Reset the music to the start
    const nickname = document.getElementById('nickname').value;
    const size = document.getElementById('size').value;
    submitScore(nickname, gameState.score, size);
    document.getElementById('gameWindow').style.display = 'none';
    document.getElementById('endgameWindow').style.display = 'block';
    document.getElementById('endgame-text').innerText = gameState.endgame_text;
    document.getElementById('new-game-button').addEventListener('click', startGame);
}

function updateGameView() {
    fetch('/get_state')
        .then(response => response.json())
        .then(gameState => {
            if (gameState.game_over) {
                if (gameIntervalId !== null) {
                    clearInterval(gameIntervalId);
                    gameIntervalId = null;
                }
                endGame(gameState);
            } else {
                const gameBoard = document.getElementById('game-board');
                gameBoard.innerHTML = '';
                document.getElementById('nicknameDisplay').innerText = "Nickname: " + document.getElementById('nickname').value;
                document.getElementById('scoreDisplay').innerText = "Score: " + gameState.score;
                gameState.board.forEach(row => {
                    const rowDiv = document.createElement('div');
                    rowDiv.className = 'row';
                    row.forEach(cell => {
                        const cellDiv = document.createElement('div');
                        if (cell === ' ') {
                            cellDiv.className = 'empty';
                        } else if (cell === 'H') {
                            cellDiv.className = 'head ' + gameState.snake_direction.toLowerCase();
                        } else if (cell === 'B') {
                            cellDiv.className = 'snake';
                        } else if (cell === 'F') {
                            cellDiv.className = 'food';
                        } else if (cell === 'O') {
                            cellDiv.className = 'obstacle';
                        }
                        rowDiv.appendChild(cellDiv);
                    });
                    gameBoard.appendChild(rowDiv);
                });
                if (gameIntervalId !== null) {
                    clearInterval(gameIntervalId);
                }
                gameIntervalId = setInterval(updateGameView, 1000 / gameState.speed);
            }
        })
        .catch(error => {
            if (gameIntervalId !== null) {
                clearInterval(gameIntervalId);
                gameIntervalId = null;
            }
        });
}


document.addEventListener('keydown', function(event) {
    let direction;
    switch (event.code) {
        case 'ArrowUp': direction = 'UP'; break;
        case 'ArrowDown': direction = 'DOWN'; break;
        case 'ArrowLeft': direction = 'LEFT'; break;
        case 'ArrowRight': direction = 'RIGHT'; break;
        default: return;
    }
    fetch('/update_direction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: direction }),
    })
    .then(response => response.json())
    .catch(error => console.error('Error updating direction:', error));
});

document.getElementById("home-button").onclick = function() {
    // Redirect to the home screen
    window.location.href = "/";
};

document.getElementById("volume-slider").addEventListener('input', function() {
    const music = document.getElementById('background-music');
    music.volume = this.value;
});