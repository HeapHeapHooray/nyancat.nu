const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const ball = { x: 300, y: 200, dx: 4, dy: 4, radius: 8 };
const paddleHeight = 80;
const paddleWidth = 10;
const p1 = { x: 10, y: 160, score: 0 };
const p2 = { x: 580, y: 160, score: 0 };

document.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    p1.y = e.clientY - rect.top - paddleHeight / 2;
});

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw center line
    ctx.strokeStyle = "rgba(0, 255, 204, 0.2)";
    ctx.setLineDash([5, 15]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    
    // Draw ball
    ctx.fillStyle = "#00ffcc";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw paddles
    ctx.fillRect(p1.x, p1.y, paddleWidth, paddleHeight);
    ctx.fillRect(p2.x, p2.y, paddleWidth, paddleHeight);
    
    // Update score text
    document.getElementById("score").textContent = `${p1.score} - ${p2.score}`;
}

function update() {
    ball.x += ball.dx;
    ball.y += ball.dy;
    
    // Wall bounce (top/bottom)
    if (ball.y - ball.radius < 0 || ball.y + ball.radius > canvas.height) {
        ball.dy *= -1;
    }
    
    // AI player simple follow
    const p2Center = p2.y + paddleHeight / 2;
    if (p2Center < ball.y - 10) {
        p2.y += 3.5;
    } else if (p2Center > ball.y + 10) {
        p2.y -= 3.5;
    }
    
    // Paddle collision
    if (ball.x - ball.radius < p1.x + paddleWidth && ball.y > p1.y && ball.y < p1.y + paddleHeight) {
        ball.dx *= -1.1; // speed up slightly on hit
    }
    if (ball.x + ball.radius > p2.x && ball.y > p2.y && ball.y < p2.y + paddleHeight) {
        ball.dx *= -1.1;
    }
    
    // Score
    if (ball.x < 0) {
        p2.score++;
        resetBall();
    } else if (ball.x > canvas.width) {
        p1.score++;
        resetBall();
    }
}

function resetBall() {
    ball.x = 300;
    ball.y = 200;
    ball.dx = ball.dx > 0 ? -4 : 4;
    ball.dy = Math.random() > 0.5 ? 4 : -4;
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
