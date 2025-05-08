import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧠 2D Prolog Sequence Executor")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="6" style="width: 100%;">местя(куб, напред).
местя(куб, ляво).
местя(куб, дясно).
местя(куб, назад).</textarea>
    <button onclick="executeSequence()">Изпълни последователност</button>
    <div id="status" style="margin-top: 10px; color: #666;"></div>
  </div>
  <div style="width: 50%;">
    <canvas id="twoCanvas" width="500" height="500" style="border: 1px solid #ccc;"></canvas>
  </div>
</div>

<script>
  // Инициализация
  const canvas = document.getElementById('twoCanvas');
  const ctx = canvas.getContext('2d');
  const statusDiv = document.getElementById('status');
  
  let cube = {
    x: 250,
    y: 250,
    size: 50,
    color: '#00ff00'
  };

  // Рисуване на куба
  function drawCube() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = cube.color;
    ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);
    ctx.fillStyle = '#000';
    ctx.font = '16px Arial';
    ctx.fillText('▲', cube.x - 8, cube.y - 15);
  }

  // Изпълнение на единична команда
  function executeCommand(command) {
    const step = 30;
    command = command.trim();
    
    if (/местя\(куб,\s*напред\)\s*\./.test(command)) {
      cube.y -= step;
      return "Изпълнено: местя(куб, напред)";
    } 
    else if (/местя\(куб,\s*назад\)\s*\./.test(command)) {
      cube.y += step;
      return "Изпълнено: местя(куб, назад)";
    }
    else if (/местя\(куб,\s*ляво\)\s*\./.test(command)) {
      cube.x -= step;
      return "Изпълнено: местя(куб, ляво)";
    }
    else if (/местя\(куб,\s*дясно\)\s*\./.test(command)) {
      cube.x += step;
      return "Изпълнено: местя(куб, дясно)";
    }
    return `Неразпозната команда: ${command}`;
  }

  // Изпълнение на всички команди последователно
  async function executeSequence() {
    const textarea = document.getElementById("prologInput");
    const commands = textarea.value.split('\n').filter(cmd => cmd.trim() !== '');
    
    for (let i = 0; i < commands.length; i++) {
      const result = executeCommand(commands[i]);
      statusDiv.innerHTML = `${result} (${i+1}/${commands.length})`;
      drawCube();
      
      // Добавяме забавяне за визуализация
      await new Promise(resolve => setTimeout(resolve, 800));
    }
    
    statusDiv.innerHTML = "Готово!";
  }

  // Първоначално рисуване
  drawCube();
</script>
"""

components.html(html_code, height=600)
