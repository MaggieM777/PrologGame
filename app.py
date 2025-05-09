import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("Урок 1: Движение и Завъртане на Куб")

st.markdown("""
## 📘 Инструкции:

Този урок ще ти покаже как можеш да управляваш едно "кубче", използвайки **Prolog команди**.

### Команди, които можеш да използваш:

- `местя(куб, напред).` – премества куба в посоката, в която гледа.
- `завъртам(куб, надясно).` – завърта куба надясно (по часовниковата стрелка).
- `завъртам(куб, наляво).` – завърта куба наляво (противоположно на часовниковата стрелка).

След като въведеш командите, натисни **"Изпълни"**, за да ги изпълниш.
""")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="8" style="width: 100%; font-size: 16px;">местя(куб, напред).
завъртам(куб, надясно).
местя(куб, напред).</textarea>
    <button onclick="executePrologCommand()" style="margin-top: 10px; padding: 8px 16px; font-size: 16px;">Изпълни</button>
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
      direction: 'north'
    };

    const directions = ['north', 'east', 'south', 'west'];

    function drawCube() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = cube.color;
      ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);

      ctx.fillStyle = '#000';
      ctx.font = '20px Arial';
      let arrow = '▲';
      if (cube.direction === 'north') arrow = '▲';
      else if (cube.direction === 'east') arrow = '▶';
      else if (cube.direction === 'south') arrow = '▼';
      else if (cube.direction === 'west') arrow = '◀';

      ctx.fillText(arrow, cube.x - 8, cube.y + 6);
    }

    function processCommand(command) {
      const step = 30;
      command = command.trim();

      if (/^местя\\(куб,\\s*напред\\)$/.test(command)) {
        if (cube.direction === 'north') cube.y -= step;
        else if (cube.direction === 'south') cube.y += step;
        else if (cube.direction === 'east') cube.x += step;
        else if (cube.direction === 'west') cube.x -= step;
      } 
      else if (/^завъртам\\(куб,\\s*наляво\\)$/.test(command)) {
        let idx = directions.indexOf(cube.direction);
        cube.direction = directions[(idx + 3) % 4];
      } 
      else if (/^завъртам\\(куб,\\s*надясно\\)$/.test(command)) {
        let idx = directions.indexOf(cube.direction);
        cube.direction = directions[(idx + 1) % 4];
      }
    }

    window.executePrologCommand = function () {
      const input = document.getElementById("prologInput").value.trim();
      const rawCommands = input.split('.').map(cmd => cmd.trim()).filter(cmd => cmd.length > 0);

      if (rawCommands.length === 0) {
        alert("Няма открити команди.");
        return;
      }

      let i = 0;

      function executeNext() {
        if (i >= rawCommands.length) return;
        processCommand(rawCommands[i]);
        drawCube();
        i++;
        setTimeout(executeNext, 500);
      }

      executeNext();
    };

    drawCube();
  });
</script>
"""
st.markdown("---")
if st.button("➡️ Премини към Урок 2"):
    st.markdown("""
    <meta http-equiv="refresh" content="0; url='/lesson2'" />
    """, unsafe_allow_html=True)

components.html(html_code, height=600)
