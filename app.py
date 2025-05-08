import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧠 Куб с посока и завъртане")

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
  document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('twoCanvas');
    const ctx = canvas.getContext('2d');

    let cube = {
      x: 250,
      y: 250,
      size: 50,
      color: '#00ff00',
      direction: 'north'  // Начална посока
    };

    const directions = ['north', 'east', 'south', 'west'];

    function drawCube() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = cube.color;
      ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);

      // Нарисувай стрелка според посоката
      ctx.fillStyle = '#000';
      ctx.font = '20px Arial';
      let arrow = '▲';
      if (cube.direction === 'north') arrow = '▲';
      else if (cube.direction === 'east') arrow = '▶';
      else if (cube.direction === 'south') arrow = '▼';
      else if (cube.direction === 'west') arrow = '◀';

      ctx.fillText(arrow, cube.x - 8, cube.y + 6);
    }

    window.executePrologCommand = function () {
      const command = document.getElementById("prologInput").value.trim();
      const step = 30;

      if (/местя\(куб,\s*напред\)\s*\./.test(command)) {
        if (cube.direction === 'north') cube.y -= step;
        else if (cube.direction === 'south') cube.y += step;
        else if (cube.direction === 'east') cube.x += step;
        else if (cube.direction === 'west') cube.x -= step;
      } 
      else if (/завъртам\(куб,\s*наляво\)\s*\./.test(command)) {
        let idx = directions.indexOf(cube.direction);
        cube.direction = directions[(idx + 3) % 4]; // Завъртане наляво
      } 
      else if (/завъртам\(куб,\s*надясно\)\s*\./.test(command)) {
        let idx = directions.indexOf(cube.direction);
        cube.direction = directions[(idx + 1) % 4]; // Завъртане надясно
      }
      else {
        alert(`Невалидна команда. Примери:
местя(куб, напред).
завъртам(куб, наляво).
завъртам(куб, надясно).`);
      }

      cube.x = Math.max(cube.size/2, Math.min(canvas.width - cube.size/2, cube.x));
      cube.y = Math.max(cube.size/2, Math.min(canvas.height - cube.size/2, cube.y));

      drawCube();
    };

    drawCube();
  });
</script>
"""

components.html(html_code, height=550)
