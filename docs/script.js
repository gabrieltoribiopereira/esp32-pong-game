const canvasP1 = document.getElementById('canvasP1');
const ctx1 = canvasP1.getContext('2d');
const canvasP2 = document.getElementById('canvasP2');
const ctx2 = canvasP2.getContext('2d');
const btnStart = document.getElementById('btnStart');

// Configuracion del juego
const PADDLE_HEIGHT = 15;
const PADDLE_WIDTH = 4;
const BALL_SIZE = 2;
const OLED_WIDTH = 128;
const OLED_HEIGHT = 64;

// Estado de la partida
let y1 = 25;
let y2 = 25;
let bx = 64;
let by = 32;
let dx = 1.5;
let dy = 1.5;
let score1 = 0;
let score2 = 0;
let gameOver = false;
let winner = "";

// Para controlar las palas
const keys = {};

window.addEventListener('keydown', (e) => {
    keys[e.key.toLowerCase()] = true;
    keys[e.key] = true;
});

window.addEventListener('keyup', (e) => {
    keys[e.key.toLowerCase()] = false;
    keys[e.key] = false;
});

function resetGame() {
    y1 = 25;
    y2 = 25;
    bx = 64;
    by = 32;
    dx = Math.random() > 0.5 ? 1.5 : -1.5;
    dy = Math.random() > 0.5 ? 1.5 : -1.5;
    gameOver = false;
    winner = "";
}

btnStart.addEventListener('click', resetGame);

function update() {
    if (gameOver) return;

    // Mover pala 1 (con la W)
    if (keys['w']) y1 -= 2;
    else y1 += 2;

    // Mover pala 2 (con las flechas)
    if (keys['ArrowUp']) y2 -= 2;
    else y2 += 2;

    y1 = Math.max(0, Math.min(OLED_HEIGHT - PADDLE_HEIGHT, y1));
    y2 = Math.max(0, Math.min(OLED_HEIGHT - PADDLE_HEIGHT, y2));

    // Movimiento de la pelota
    bx += dx;
    by += dy;

    // Rebotes en las paredes
    if (by <= 0 || by >= OLED_HEIGHT - BALL_SIZE) {
        dy = -dy;
        by = Math.max(0, Math.min(OLED_HEIGHT - BALL_SIZE, by));
    }

    // Choque con la pala 1
    if (bx <= PADDLE_WIDTH && by + BALL_SIZE >= y1 && by <= y1 + PADDLE_HEIGHT) {
        dx = Math.abs(dx) * 1.05;
        dy *= 1.05;
        bx = PADDLE_WIDTH + 1;
    }

    // Choque con la pala 2
    if (bx >= OLED_WIDTH - PADDLE_WIDTH - BALL_SIZE && by + BALL_SIZE >= y2 && by <= y2 + PADDLE_HEIGHT) {
        dx = -Math.abs(dx) * 1.05;
        dy *= 1.05;
        bx = OLED_WIDTH - PADDLE_WIDTH - BALL_SIZE - 1;
    }

    // Puntuacion
    if (bx < 0) {
        winner = "P2";
        gameOver = true;
    } else if (bx > OLED_WIDTH) {
        winner = "P1";
        gameOver = true;
    }
}

function drawOnCanvas(ctx) {
    // Limpiar la pantalla
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, OLED_WIDTH, OLED_HEIGHT);

    if (gameOver) {
        ctx.fillStyle = '#AEEEEE';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', OLED_WIDTH / 2, 25);
        ctx.fillText('Winner: ' + winner, OLED_WIDTH / 2, 45);
        return;
    }

    // Dibujar las palas
    ctx.fillStyle = '#AEEEEE';
    ctx.fillRect(0, y1, PADDLE_WIDTH, PADDLE_HEIGHT);
    ctx.fillRect(OLED_WIDTH - PADDLE_WIDTH, y2, PADDLE_WIDTH, PADDLE_HEIGHT);

    // Dibujar la pelota
    ctx.fillRect(bx, by, BALL_SIZE, BALL_SIZE);
}

function loop() {
    update();
    drawOnCanvas(ctx1);
    drawOnCanvas(ctx2);
    requestAnimationFrame(loop);
}

loop();

// Logica para que funcione el boton de los esquemas
const btnSchematics = document.getElementById('btnSchematics');
const schematicsModal = document.getElementById('schematicsModal');
const modalClose = document.getElementById('modalClose');

btnSchematics.addEventListener('click', () => {
    schematicsModal.classList.add('active');
});

modalClose.addEventListener('click', () => {
    schematicsModal.classList.remove('active');
});

schematicsModal.addEventListener('click', (e) => {
    if (e.target === schematicsModal) {
        schematicsModal.classList.remove('active');
    }
});

window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        schematicsModal.classList.remove('active');
        videoModal.classList.remove('active');
        videoPlayer.pause();
    }
});

// Logica para que funcione el boton del video
const btnVideo = document.getElementById('btnVideo');
const videoModal = document.getElementById('videoModal');
const videoModalClose = document.getElementById('videoModalClose');
const videoPlayer = document.getElementById('videoPlayer');

btnVideo.addEventListener('click', () => {
    videoModal.classList.add('active');
});

videoModalClose.addEventListener('click', () => {
    videoModal.classList.remove('active');
    videoPlayer.pause();
});

videoModal.addEventListener('click', (e) => {
    if (e.target === videoModal) {
        videoModal.classList.remove('active');
        videoPlayer.pause();
    }
});
