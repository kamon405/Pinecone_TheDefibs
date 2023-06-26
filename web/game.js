console.log('Game script loaded');
let canvas = document.getElementById("gameCanvas");
let context = canvas.getContext("2d");

// Constants
const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 600;
const CELL_SIZE = 20;
const CELLS_X = SCREEN_WIDTH / CELL_SIZE;
const CELLS_Y = SCREEN_HEIGHT / CELL_SIZE;

// Game variables
let worm = [{x: CELLS_X / 2, y: CELLS_Y / 2}];
let direction = 'UP';
let food = spawnFood();
let targetsEaten = 0;

function draw() {
    // Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Draw worm
    worm.forEach(function(part) {
        context.fillStyle = 'green';
        context.fillRect(part.x * CELL_SIZE, part.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    });

    // Draw food
    context.fillStyle = 'red';
    context.fillRect(food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
}

function update() {
    let x = worm[0].x;
    let y = worm[0].y;

    if (direction == 'UP') y--;
    else if (direction == 'DOWN') y++;
    else if (direction == 'LEFT') x--;
    else if (direction == 'RIGHT') x++;

    let newHead = {x: x % CELLS_X, y: y % CELLS_Y};
    worm.unshift(newHead);
    worm.pop();

    // Check for collision with self
    for (let i = 1; i < worm.length; i++) {
        if (worm[i].x === worm[0].x && worm[i].y === worm[0].y) {
            resetGame();
        }
    }

    // Check for collision with food
    if (worm[0].x === food.x && worm[0].y === food.y) {
        worm.push({});
        food = spawnFood();
        targetsEaten++;

        // Check if the game is won
    if (targetsEaten >= 3) {
        alert("Congratulations! You've won!");
        localStorage.setItem('gameWon', 'true'); // store a value in the local storage
        console.log(localStorage.getItem('gameWon'));
        window.location.href = "/"; // redirect to index.html
        return;
        //resetGame();
    


        }
    }
}

function gameLoop() {
    update();
    draw();
    setTimeout(gameLoop, 1000 / 15);
}

function spawnFood() {
    let x = Math.floor(Math.random() * CELLS_X);
    let y = Math.floor(Math.random() * CELLS_Y);
    return {x: x, y: y};
}

function resetGame() {
    worm = [{x: CELLS_X / 2, y: CELLS_Y / 2}];
    direction = 'UP';
    food = spawnFood();
    targetsEaten = 0;
}

window.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowUp' && direction !== 'DOWN') direction = 'UP';
    else if (event.key === 'ArrowDown' && direction !== 'UP') direction = 'DOWN';
    else if (event.key === 'ArrowLeft' && direction !== 'RIGHT') direction = 'LEFT';
    else if (event.key === 'ArrowRight' && direction !== 'LEFT') direction = 'RIGHT';
});

gameLoop();
