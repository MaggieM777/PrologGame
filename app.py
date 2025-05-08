import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧠 2D Prolog-like Movement")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="6" style="width: 100%; font-family: monospace;">местя(куб, напред).
местя(куб, назад).
местя(куб, ляво).
местя(куб, дясно).</textarea>
    <button onclick="executeCommandSequence()" style="margin-top: 10px; padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">▶ Изпълни</button>
    <div id="status" style="margin-top: 10px; padding: 10px; background: #f0f0f0; border-radius: 4px;"></div>
  </div>
  <div style="width: 50%;">
    <canvas id="gameCanvas" width="500" height="500" style="border: 1px solid #ddd; background: #f9f9f9;"></canvas>
  </div>
</div>

<script>
// ========== ИНИЦИАЛИЗАЦИЯ ==========
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');

// Ключова промяна: Обърната Y координатна система
let cube = {
  x: 250,
  y: 250,  // Y нараства надолу в Canvas 2D
  size: 50,
  color: '#E74C3C'  // Ярко червен цвят
};

// Функция за рисуване на куба
function drawCube() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Координатна мрежа за ориентация
  ctx.strokeStyle = '#e0e0e0';
  for (let x = 0; x <= canvas.width; x += 50) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
  for (let y = 0; y <= canvas.height; y += 50) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }
  
  // Рисуване на куба (центриран)
  ctx.fillStyle = cube.color;
  ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);
  
  // Ориентационна стрелка
  ctx.fillStyle = '#fff';
  ctx.font = '16px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('↑', cube.x, cube.y);
}

// Обработка на команди с правилни посоки
function executeCommand(command) {
  const step = 40;
  command = command.trim();
  
  if (/местя\(куб,\s*напред\)\s*\./.test(command)) {
    cube.y -= step;  // Нагоре = намалява Y
  } 
  else if (/местя\(куб,\s*назад\)\s*\./.test(command)) {
    cube.y += step;  // Надолу = увеличава Y
  }
  else if (/местя\(куб,\s*ляво\)\s*\./.test(command)) {
    cube.x -= step;
  }
  else if (/местя\(куб,\s*дясно\)\s*\./.test(command)) {
    cube.x += step;
  }
}

// Изпълнение на последователност
async function executeCommandSequence() {
  const textarea = document.getElementById("prologInput");
  const commands = textarea.value.split('\n').filter(cmd => cmd.trim() !== '');
  
  for (let i = 0; i < commands.length; i++) {
    executeCommand(commands[i]);
    
    // Гранични проверки
    cube.x = Math.max(cube.size/2, Math.min(canvas.width - cube.size/2, cube.x));
    cube.y = Math.max(cube.size/2, Math.min(canvas.height - cube.size/2, cube.y));
    
    drawCube();
    await new Promise(r => setTimeout(r, 600));
  }
}

// Първоначално рисуване
window.onload = drawCube;
</script>
"""

components.html(html_code, height=600)
