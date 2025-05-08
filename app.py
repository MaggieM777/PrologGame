import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧠 2D Prolog Visualizer")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="6" style="width: 100%; font-family: monospace;">местя(куб, напред).
местя(куб, ляво).
местя(куб, дясно).
местя(куб, назад).</textarea>
    <button onclick="executeSequence()" style="margin-top: 10px; padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">▶ Изпълни</button>
    <div id="status" style="margin-top: 10px; padding: 10px; background: #f0f0f0; border-radius: 4px;"></div>
  </div>
  <div style="width: 50%;">
    <canvas id="gameCanvas" width="500" height="500" style="border: 1px solid #ddd; background: #f9f9f9;"></canvas>
  </div>
</div>

<script>
// Инициализация
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');

// Начална позиция и настройки
let cube = {
  x: 250,
  y: 250,
  size: 50,
  color: '#E74C3C'
};

// Координатна мрежа
function drawGrid() {
  ctx.strokeStyle = '#e0e0e0';
  ctx.lineWidth = 1;
  
  // Вертикални линии
  for (let x = 0; x <= canvas.width; x += 50) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
  
  // Хоризонтални линии
  for (let y = 0; y <= canvas.height; y += 50) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }
}

// Рисуване на куба
function drawCube() {
  ctx.fillStyle = cube.color;
  ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);
  
  // Ориентационна стрелка
  ctx.fillStyle = '#fff';
  ctx.font = '20px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('↑', cube.x, cube.y);
}

// Преоразмеряване на canvas при промяна на размера
function resizeCanvas() {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  drawScene();
}

// Основна функция за рисуване
function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGrid();
  drawCube();
}

// Обработка на команди
function executeCommand(command) {
  const step = 50;
  command = command.trim();
  
  if (/местя\(куб,\s*напред\)\s*\./.test(command)) {
    cube.y -= step;
    return "Движение напред";
  } 
  else if (/местя\(куб,\s*назад\)\s*\./.test(command)) {
    cube.y += step;
    return "Движение назад";
  }
  else if (/местя\(куб,\s*ляво\)\s*\./.test(command)) {
    cube.x -= step;
    return "Движение наляво";
  }
  else if (/местя\(куб,\s*дясно\)\s*\./.test(command)) {
    cube.x += step;
    return "Движение надясно";
  }
  return `Неразпозната команда: ${command}`;
}

// Изпълнение на последователност
async function executeSequence() {
  const textarea = document.getElementById("prologInput");
  const commands = textarea.value.split('\n').filter(cmd => cmd.trim() !== '');
  
  for (let i = 0; i < commands.length; i++) {
    const result = executeCommand(commands[i]);
    statusDiv.innerHTML = `Изпълнение: ${result} (${i+1}/${commands.length})`;
    drawScene();
    
    // Анимационна забавяне
    await new Promise(resolve => setTimeout(resolve, 800));
  }
  
  statusDiv.innerHTML = "Готово! Всички команди са изпълнени";
}

// Инициализация при зареждане
window.addEventListener('load', () => {
  resizeCanvas();
  drawScene();
  statusDiv.innerHTML = "Готов за изпълнение. Въведете команди и кликнете 'Изпълни'";
});

// Преоразмеряване при промяна на размера на прозореца
window.addEventListener('resize', resizeCanvas);
</script>
"""

components.html(html_code, height=650)
