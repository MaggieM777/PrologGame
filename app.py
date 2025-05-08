import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🎮 Learn Coding with Visual Prolog")

# CSS стилове за по-добър интерфейс
st.markdown("""
<style>
.code-area {
    font-family: 'Courier New', monospace !important;
    background: #f5f5f5 !important;
}
.status-info {
    padding: 10px;
    background: #e6f7ff;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

html_code = """
<div style="display: flex; gap: 20px;">
  <!-- Лява колона: Код и контроли -->
  <div style="flex: 1; min-width: 400px;">
    <h3 style="color: #2e86c1;">✏️ Вашият код</h3>
    <textarea id="codeInput" rows="10" style="width: 100%;" class="code-area">местя(куб, напред).
местя(куб, дясно).
местя(куб, напред).</textarea>
    
    <div style="margin-top: 15px; display: flex; gap: 10px;">
      <button onclick="runCode()" style="padding: 8px 15px; background: #2e86c1; color: white; border: none; border-radius: 4px;">▶️ Изпълни</button>
      <button onclick="resetScene()" style="padding: 8px 15px; background: #e74c3c; color: white; border: none; border-radius: 4px;">🔄 Нулирай</button>
    </div>
    
    <div id="status" class="status-info">ℹ️ Въведете Prolog-like команди и кликнете 'Изпълни'.</div>
    
    <h4 style="margin-top: 20px;">📌 Примерни команди:</h4>
    <pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">
местя(куб, напред).
местя(куб, ляво).
ротация(куб, 90).</pre>
  </div>
  
  <!-- Дясна колона: Визуализация -->
  <div style="flex: 1;">
    <h3 style="color: #27ae60;">👀 Визуализация</h3>
    <canvas id="gameCanvas" width="500" height="500" style="border: 1px solid #ddd; background: #f9f9f9;"></canvas>
  </div>
</div>

<script>
// ========== ИНИЦИАЛИЗАЦИЯ ==========
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');

// Обекти в сцената
let objects = {
  cube: {
    x: 250, y: 250,
    size: 40,
    color: '#e74c3c',
    angle: 0
  },
  target: {
    x: 350, y: 150,
    size: 20,
    color: '#2ecc71'
  }
};

// Начално рисуване
function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Рисуване на цел
  ctx.fillStyle = objects.target.color;
  ctx.fillRect(
    objects.target.x - objects.target.size/2,
    objects.target.y - objects.target.size/2,
    objects.target.size,
    objects.target.size
  );
  
  // Рисуване на куб
  ctx.save();
  ctx.translate(objects.cube.x, objects.cube.y);
  ctx.rotate(objects.cube.angle * Math.PI / 180);
  ctx.fillStyle = objects.cube.color;
  ctx.fillRect(
    -objects.cube.size/2,
    -objects.cube.size/2,
    objects.cube.size,
    objects.cube.size
  );
  
  // Ориентационна стрелка
  ctx.fillStyle = '#fff';
  ctx.font = '14px Arial';
  ctx.fillText('▲', -6, -10);
  ctx.restore();
}

// ========== КОМАНДИ ==========
const COMMANDS = {
  'местя': (obj, dir) => {
    const step = 40;
    switch(dir) {
      case 'напред':
        objects[obj].y -= step;
        break;
      case 'назад':
        objects[obj].y += step;
        break;
      case 'ляво':
        objects[obj].x -= step;
        break;
      case 'дясно':
        objects[obj].x += step;
        break;
    }
    return `Премести ${obj} ${dir}`;
  },
  
  'ротация': (obj, deg) => {
    objects[obj].angle += parseInt(deg);
    return `Завърти ${obj} на ${deg}°`;
  }
};

// ========== ИЗПЪЛНЕНИЕ НА КОД ==========
async function runCode() {
  const code = document.getElementById('codeInput').value;
  const lines = code.split('\n').filter(line => line.trim() !== '');
  
  statusDiv.innerHTML = '⏳ Изпълнявам...';
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    let result = parseCommand(line);
    
    statusDiv.innerHTML = `📝 ${result} (${i+1}/${lines.length})`;
    drawScene();
    await new Promise(r => setTimeout(r, 800));
  }
  
  statusDiv.innerHTML = '✅ Готово!';
  checkWinCondition();
}

function parseCommand(line) {
  // Регулярен израз за Prolog-like команди
  const match = line.match(/(\w+)\((\w+),\s*([^)]+)\)\s*\./);
  if (!match) return `❌ Грешен формат: ${line}`;
  
  const [_, cmd, obj, arg] = match;
  if (!COMMANDS[cmd]) return `❌ Непозната команда: ${cmd}`;
  
  return COMMANDS[cmd](obj, arg);
}

// ========== ДОПЪЛНИТЕЛНИ ФУНКЦИИ ==========
function resetScene() {
  objects.cube = { x: 250, y: 250, size: 40, color: '#e74c3c', angle: 0 };
  statusDiv.innerHTML = '🔄 Сцената е нулирана';
  drawScene();
}

function checkWinCondition() {
  const c = objects.cube;
  const t = objects.target;
  
  if (Math.abs(c.x - t.x) < 30 && Math.abs(c.y - t.y) < 30) {
    statusDiv.innerHTML = '🎉 Успех! Кубът достигна целта!';
  }
}

// Стартиране на приложението
drawScene();
</script>
"""

components.html(html_code, height=700)
