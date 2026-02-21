const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

const fontSize = 20;               
const speedMultiplier = 0.3;       
const trailAlpha = 0.1;           
const chars =
    "01JARVISAI@#$%&*+-=<>(){}[]ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"; 

const colors = [
    "0, 255, 0",
];

const columns = Math.floor(window.innerWidth / fontSize);
const drops = Array(columns).fill(0).map(() =>
    Math.random() * canvas.height / fontSize
);

function draw() {
    ctx.fillStyle = `rgba(5, 5, 16, ${trailAlpha})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = fontSize + "px monospace";

    for (let i = 0; i < drops.length; i++) {
        const char = chars[Math.floor(Math.random() * chars.length)];
        const color = colors[Math.floor(Math.random() * colors.length)];

        const x = i * fontSize;
        const y = drops[i] * fontSize;

        ctx.fillStyle = `rgba(${color}, 0.9)`;
        ctx.shadowColor = `rgb(${color})`;
        ctx.shadowBlur = 12;

        ctx.fillText(char, x, y);

        if (y > canvas.height && Math.random() > 0.94) {
            drops[i] = 0;
        } else {
            drops[i] += speedMultiplier;
        }
    }

    ctx.shadowBlur = 0;
    requestAnimationFrame(draw);
}

draw();
