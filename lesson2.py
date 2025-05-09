import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("📘 Урок 2: Препятствия и логическо движение")

st.markdown("""
В този урок ще научим как да се справяме с препятствия. Кубчето не може да преминава през сивите блокове.
Опитай да стигнеш до зелената цел без да се сблъскаш!

#### Команди:
- `местя(куб, напред).`
- `местя(куб, ляво).`
- `местя(куб, дясно).`
- `местя(куб, назад).`
- `завъртам(куб, надясно).`
- `завъртам(куб, наляво).`
""")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="6" style="width: 100%;">завъртам(куб, надясно).
местя(куб, напред).</textarea>
    <button onclick="executeAll()">▶️ Изпълни</button>
    <button onclick="reset()">🔄 Нулирай</button>
  </div>
  <div style="width: 50%;">
    <canvas id="canvas" width="500" height="500" style="border: 1px solid #ccc;"></canvas>
  </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let cube = { x: 100, y: 400, size: 50, color: '#00ff00', angle: 0 };

const target = { x: 400, y: 100, size: 30, color: '#00cc88' };

const obstacles = [
  { x: 150, y: 250, width: 200, height: 20 },
  { x: 250, y: 150, width: 20, height: 100 }
];

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Obstacles
  ctx.fillStyle = '#999';
  for (let obs of obstacles) {
    ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
  }

  // Target
  ctx.fillStyle = target.color;
  ctx.fillRect(target.x - target.size/2, target.y - target.size/2, target.size, target.size);

  // Cube
  ctx.save();
  ctx.translate(cube.x, cube.y);
  ctx.rotate(cube.angle * Math.PI / 180);
  ctx.fillStyle = cube.color;
  ctx.fillRect(-cube.size/2, -cube.size/2, cube.size, cube.size);

  ctx.fillStyle = '#000';
  ctx.font = '16px Arial';
  ctx.fillText('▲', -7, -15);
  ctx.restore();
}

function reset() {
  cube = { x: 100, y: 400, size: 50, color: '#00ff00', angle: 0 };
  draw();
}

function collision(newX, newY) {
  const size = cube.size;
  for (let obs of obstacles) {
    if (
      newX + size/2 > obs.x &&
      newX - size/2 < obs.x + obs.width &&
      newY + size/2 > obs.y &&
      newY - size/2 < obs.y + obs.height
    ) return true;
  }
  return false;
}

function moveCube(direction) {
  let dx = 0, dy = 0;
  const step = 40;
  let angle = cube.angle % 360;

  if (direction === 'напред') {
    if (angle === 0) dy = -step;
    else if (angle === 90 || angle === -270) dx = step;
    else if (angle === 180 || angle === -180) dy = step;
    else if (angle === 270 || angle === -90) dx = -step;
  } else if (direction === 'назад') {
    if (angle === 0) dy = step;
    else if (angle === 90 || angle === -270) dx = -step;
    else if (angle === 180 || angle === -180) dy = -step;
    else if (angle === 270 || angle === -90) dx = step;
  }

  const newX = cube.x + dx;
  const newY = cube.y + dy;
  if (!collision(newX, newY)) {
    cube.x = newX;
    cube.y = newY;
  }
}

function rotateCube(dir) {
  if (dir === 'надясно') cube.angle += 90;
  if (dir === 'наляво') cube.angle -= 90;
}

async function executeAll() {
  const lines = document.getElementById("prologInput").value.trim().split('\\n');

  for (let line of lines) {
    line = line.trim();
    if (line.startsWith('местя')) {
      const match = line.match(/местя\\(куб,\\s*(.*?)\\)\\./);
      if (match) moveCube(match[1]);
    } else if (line.startsWith('завъртам')) {
      const match = line.match(/завъртам\\(куб,\\s*(.*?)\\)\\./);
      if (match) rotateCube(match[1]);
    }
    draw();
    await new Promise(r => setTimeout(r, 600));
  }
}

draw();
</script>
"""

components.html(html_code, height=600)

if st.button("⬅️ Обратно към Урок 1"):
    st.markdown("<meta http-equiv='refresh' content='0; url=\"/lesson1\"'>", unsafe_allow_html=True)
