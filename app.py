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
    <button onclick="executeCommandSequence()" style="margin-top: 10px; padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">▶ Изпълни последователност</button>
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

// Начална позиция на куба (червен квадрат)
let cube = {
  x: 50,  // Променено от 250 на 50 за по-добра видимост
  y: 50,
  size: 40,
  color: '#E74C3C'
};

// Функция за рисуване на куба
function drawCube() {
  ctx.fillStyle = cube.color;
  ctx.fillRect(cube.x, cube.y, cube.size, cube.size);
  
  // Бяла стрелка за ориентация
  ctx.fillStyle = '#fff';
  ctx.font = '20px Arial';
  ctx.fillText('↑', cube.x + cube.size/2 - 10, cube.y + cube.size/2 + 8);
}

// Основна функция за рисуване
function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Тънка сива мрежа за фон
  ctx.strokeStyle = '#e0e0e0';
  ctx.lineWidth = 1;
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

// Изпълнение на последователност от команди
async function executeCommandSequence() {
  const textarea = document.getElementById("prologInput");
  const commands = textarea.value.split('\n').filter(cmd => cmd.trim() !== '');
  
  statusDiv.innerHTML = '⏳ Изпълнявам команди...';
  
  for (let i = 0; i < commands.length; i++) {
    const result = executeCommand(commands[i]);
    statusDiv.innerHTML = `📝 ${result} (${i+1}/${commands.length})`;
    
    // Проверка за граници
    cube.x = Math.max(0, Math.min(canvas.width - cube.size, cube.x));
    cube.y = Math.max(0, Math.min(canvas.height - cube.size, cube.y));
    
    drawScene();
    
    // Забавяне за анимация (600ms)
    await new Promise(r => setTimeout(r, 600));
  }
  
  statusDiv.innerHTML = "✅ Готово! Всички команди са изпълнени";
}

// Първоначално рисуване
drawScene();
</script>
"""

components.html(html_code, height=600)
