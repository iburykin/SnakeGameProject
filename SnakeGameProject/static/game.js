function startGame() {
    fetch('/start_game', { method: 'POST' })
        .then(response => response.json())
        .then(updateGameView);
}

function move(direction) {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction: direction }),
    })
    .then(response => response.json())
    .then(updateGameView);
}

function updateGameView(gameState) {
    // Update the game view based on the game state
    // This will depend on how you've structured your HTML and CSS
}