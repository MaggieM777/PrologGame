import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧠 2D Prolog-like Movement")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="4" style="width: 100%;">местя(куб, напред).</textarea>
    <button onclick="executePrologCommand()">Изпълни</button>
  </div>
  <div style="width: 50%;">
    <canvas id="twoCanvas" width="500" height="500" style="border: 1px solid #ccc;"></canvas>
  </div>
</div>

<script>
  // Инициализация на 2D сцената
  const canvas = document.getElementById('twoCanvas');
  const ctx = canvas.getContext('2d');
  
  // Начална позиция на куба (квадрата)
  let cube = {
    x: 250,
    y: 250,
    size: 50,
    color: '#00ff00'
  };

  // Функция за рисуване на куба
  function drawCube() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Рисуваме квадрат
    ctx.fillStyle = cube.color;
    ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);
    
    // Добавяме текст за ориентация
    ctx.fillStyle = '#000';
    ctx.font = '16px Arial';
    ctx.fillText('▲', cube.x - 8, cube.y - 15);  // Стрелка напред
  }

  // Обработка на Prolog-like команди
  function executePrologCommand() {
    const command = document.getElementById("prologInput").value.trim();
    const step = 30;  // Стъпка на движение
    
    // Разпознаване на команди
    if (/местя\(куб,\s*напред\)\s*\./.test(command)) {
      cube.y -= step;  // Нагоре по Y (в 2D "напред" обикновено е нагоре)
    } 
    else if (/местя\(куб,\s*назад\)\s*\./.test(command)) {
      cube.y += step;
    }
    else if (/местя\(куб,\s*ляво\)\s*\./.test(command)) {
      cube.x -= step;
    }
    else if (/местя\(куб,\s*дясно\)\s*\./.test(command)) {
      cube.x += step;
    }
    else {
      alert(`Невалидна команда. Възможни опции:\n
        местя(куб, напред).\n
        местя(куб, назад).\n
        местя(куб, ляво).\n
        местя(куб, дясно).`);
    }
    
    // Проверка за граници
    cube.x = Math.max(cube.size/2, Math.min(canvas.width - cube.size/2, cube.x));
    cube.y = Math.max(cube.size/2, Math.min(canvas.height - cube.size/2, cube.y));
    
    drawCube();
  }

  // Първоначално рисуване
  drawCube();
</script>
"""

components.html(html_code, height=550)
