import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🎮 Learn Prolog with Interactive Game")

# CSS стилове за по-добър интерфейс
st.markdown("""
<style>
.code-area {
    font-family: 'Courier New', monospace !important;
    background: #f5f5f5 !important;
    border: 1px solid #ddd !important;
    border-radius: 4px !important;
    padding: 10px !important;
}
.status-info {
    padding: 10px;
    background: #e6f7ff;
    border-radius: 5px;
    margin: 10px 0;
}
button {
    padding: 8px 15px;
    background: #2e86c1;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
}
button:hover {
    background: #1a5276;
}
button.danger {
    background: #e74c3c;
}
button.danger:hover {
    background: #b03a2e;
}
.lesson {
    background: #f9f9f9;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
    border-left: 4px solid #2e86c1;
}
.right-column {
    min-width: 520px !important;
}
</style>
""", unsafe_allow_html=True)

html_code = """
<div style="display: flex; gap: 20px;">
  <!-- Лява колона: Код и контроли -->
  <div style="flex: 1; min-width: 400px;">
    <h3 style="color: #2e86c1;">✏️ Вашият Prolog код</h3>
    <textarea id="codeInput" rows="10" style="width: 100%;" class="code-area">местя(куб, напред).
местя(куб, дясно).
местя(куб, напред).</textarea>
    
    <div style="margin-top: 15px; display: flex; gap: 10px;">
      <button onclick="runCode()">▶️ Изпълни</button>
      <button onclick="resetScene()" class="danger">🔄 Нулирай</button>
      <button onclick="showHint()">💡 Подсказка</button>
    </div>
    
    <div id="status" class="status-info">ℹ️ Въведете Prolog команди и кликнете 'Изпълни'.</div>
    
    <div class="lesson">
      <h4>📚 Урок 1: Основни команди</h4>
      <p>Използвайте тези команди за да движите куба:</p>
      <pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">
местя(куб, напред).   - премества куба напред
местя(куб, назад).    - премества куба назад
местя(куб, ляво).     - премества куба наляво
местя(куб, дясно).    - премества куба надясно
ротация(куб, 90).     - завърта куба на 90 градуса</pre>
    </div>
    
    <div class="lesson">
      <h4>🎯 Задача</h4>
      <p>Направете куба да достигне зеления квадрат (целта).</p>
      <p>Можете да изпълнявате команди една по една или да напишете няколко наведнъж.</p>
    </div>
  </div>
  
  <!-- Дясна колона: Визуализация -->
  <div style="flex: 1;" class="right-column">
    <h3 style="color: #27ae60;">👀 Визуализация</h3>
    <div style="width: 500px; height: 500px; border: 1px solid #ddd; background: #f9f9f9;">
      <canvas id="gameCanvas" width="500" height="500"></canvas>
    </div>
    <div style="margin-top: 10px;">
      <button onclick="showLevel(1)">Ниво 1</button>
      <button onclick="showLevel(2)">Ниво 2</button>
      <button onclick="showLevel(3)">Ниво 3</button>
    </div>
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
  },
  obstacles: []
};

// Нива на играта
const levels = {
  1: {
    cube: { x: 250, y: 450, size: 40, color: '#e74c3c', angle: 0 },
    target: { x: 250, y: 100, size: 20, color: '#2ecc71' },
    obstacles: []
  },
  2: {
    cube: { x: 100, y: 450, size: 40, color: '#e74c3c', angle: 0 },
    target: { x: 400, y: 100, size: 20, color: '#2ecc71' },
    obstacles: [
      { x: 100, y: 300, width: 300, height: 20, color: '#7f8c8d' },
      { x: 300, y: 200, width: 20, height: 100, color: '#7f8c8d' }
    ]
  },
  3: {
    cube: { x: 50, y: 450, size: 40, color: '#e74c3c', angle: 0 },
    target: { x: 450, y: 50, size: 20, color: '#2ecc71' },
    obstacles: [
      { x: 0, y: 350, width: 300, height: 20, color: '#7f8c8d' },
      { x: 200, y: 250, width: 300, height: 20, color: '#7f8c8d' },
      { x: 300, y: 150, width: 20, height: 100, color: '#7f8c8d' }
    ]
  }
};

// Начално рисуване
function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Рисуване на препятствия
  objects.obstacles.forEach(obs => {
    ctx.fillStyle = obs.color;
    ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
  });
  
  // Рисуване на цел
  ctx.fillStyle = objects.target.color;
  ctx.fillRect(
    objects.target.x - objects.target.size/2,
    objects.target.y - objects.target.size/2,
    objects.target.size,
    objects.target.size
  );
  
  // Рисуване на куб
  console.log('Drawing cube at:', objects.cube.x, objects.cube.y); // Debugging position
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
    let newX = objects[obj].x;
    let newY = objects[obj].y;
    
    switch(dir) {
      case 'напред':
        newY -= step;
        break;
      case 'назад':
        newY += step;
        break;
      case 'ляво':
        newX -= step;
        break;
      case 'дясно':
        newX += step;
        break;
    }
    
    // Проверка за сблъсък с препятствия
    if (!checkCollision(newX, newY, objects[obj].size)) {
      objects[obj].x = newX;
      objects[obj].y = newY;
      return `Премести ${obj} ${dir}`;
    } else {
      return `❌ Не може да премине ${dir} (препятствие)`;
    }
  },
  
  'ротация': (obj, deg) => {
    objects[obj].angle += parseInt(deg);
    return `Завърти ${obj} на ${deg}°`;
  }
};

// Проверка за сблъсък с препятствия
function checkCollision(x, y, size) {
  const halfSize = size / 2;
  const cubeRect = {
    left: x - halfSize,
    right: x + halfSize,
    top: y - halfSize,
    bottom: y + halfSize
  };
  
  for (const obs of objects.obstacles) {
    const obsRect = {
      left: obs.x,
      right: obs.x + obs.width,
      top: obs.y,
      bottom: obs.y + obs.height
    };
    
    if (cubeRect.right > obsRect.left && 
        cubeRect.left < obsRect.right && 
        cubeRect.bottom > obsRect.top && 
        cubeRect.top < obsRect.bottom) {
      return true;
    }
  }
  
  // Проверка за граници на canvas
  if (cubeRect.left < 0 || cubeRect.right > canvas.width || 
      cubeRect.top < 0 || cubeRect.bottom > canvas.height) {
    return true;
  }
  
  return false;
}

// ========== ИЗПЪЛНЕНИЕ НА КОД ==========

async function runCode() {
  const code = document.getElementById('codeInput').value;
  const lines = code.split('\n').filter(line => line.trim() !== '');
  
  if (lines.length === 0) {
    statusDiv.innerHTML = 'ℹ️ Няма команди за изпълнение';
    return;
  }
  
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
  objects.cube = { ...levels[1].cube };
  objects.target = { ...levels[1].target };
  objects.obstacles = [];
  statusDiv.innerHTML = '🔄 Сцената е нулирана';
  drawScene();
}

function showLevel(levelNum) {
  const level = levels[levelNum];
  if (!level) return;
  
  objects.cube = { ...level.cube };
  objects.target = { ...level.target };
  objects.obstacles = level.obstacles.map(obs => ({ ...obs }));
  
  statusDiv.innerHTML = `🆕 Заредено ниво ${levelNum}`;
  drawScene();
}

function showHint() {
  const currentLevel = Object.keys(levels).find(l => 
    objects.cube.x === levels[l].cube.x && 
    objects.cube.y === levels[l].cube.y
  ) || 1;
  
  const hints = {
    1: "Опитай: местя(куб, напред). местя(куб, напред). местя(куб, напред).",
    2: "Опитай комбинация от движение напред и надясно, след което отново напред.",
    3: "Трябва да заобиколиш препятствията. Опитай да завъртиш куба и да се движиш в различни посоки."
  };
