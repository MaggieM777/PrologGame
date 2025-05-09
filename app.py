import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Определяме коя страница да се покаже
page = st.sidebar.radio("Избери урок:", ["Урок 1", "Урок 2"])

if page == "Урок 1":
    st.title("Урок 1: Движение и Завъртане на Куб")

    st.markdown("""
    ## 📘 Инструкции:

    Този урок ще ти покаже как можеш да управляваш едно "кубче", използвайки **Prolog-подобни команди**.

    ### Команди, които можеш да използваш:

    - `местя(куб, напред).` – премества куба в посоката, в която гледа.
    - `завъртам(куб, надясно).` – завърта куба надясно.
    - `завъртам(куб, наляво).` – завърта куба наляво.

    Можеш да пишеш няколко команди една под друга и те ще се изпълняват последователно.
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
          if (cube.direction === 'east') arrow = '▶';
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
          if (rawCommands.length === 0) return;

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

    components.html(html_code, height=600)

elif page == "Урок 2":
    st.title("Урок 2: Препятствия и Логически Правила")

    st.markdown("""
    ## 📗 Цел на урока:
    В този урок ще добавим **препятствия** и ще използваме **логически правила**, за да избегнем сблъсъци.

    ### Нови неща:
    - Препятствие в центъра на платното
    - Команда: `ако_свободно(куб, напред) -> местя(куб, напред).`
    - Кубчето ще провери дали има път, преди да се премести
    """)

    html_code = """
    <div style="display: flex;">
      <div style="width: 50%; padding: 10px;">
        <textarea id="prologInput" rows="8" style="width: 100%; font-size: 16px;">завъртам(куб, надясно).
ако_свободно(куб, напред) -> местя(куб, напред).
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

        let cube = { x: 100, y: 250, size: 50, color: '#00ff00', direction: 'east' };
        const directions = ['north', 'east', 'south', 'west'];

        const obstacle = { x: 250, y: 250, size: 50 };

        function drawCube() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Draw obstacle
          ctx.fillStyle = '#ff0000';
          ctx.fillRect(obstacle.x - obstacle.size/2, obstacle.y - obstacle.size/2, obstacle.size, obstacle.size);

          // Draw cube
          ctx.fillStyle = cube.color;
          ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);

          ctx.fillStyle = '#000';
          ctx.font = '20px Arial';
          let arrow = '▲';
          if (cube.direction === 'east') arrow = '▶';
          else if (cube.direction === 'south') arrow = '▼';
          else if (cube.direction === 'west') arrow = '◀';
          ctx.fillText(arrow, cube.x - 8, cube.y + 6);
        }

        function isFreeAhead() {
          const step = 30;
          let newX = cube.x, newY = cube.y;

          if (cube.direction === 'north') newY -= step;
          else if (cube.direction === 'south') newY += step;
          else if (cube.direction === 'east') newX += step;
          else if (cube.direction === 'west') newX -= step;

          const distX = Math.abs(newX - obstacle.x);
          const distY = Math.abs(newY - obstacle.y);
          return distX >= (cube.size) || distY >= (cube.size);
        }

        function processCommand(command) {
          const step = 30;
          command = command.trim();

          if (/^местя\\(куб,\\s*напред\\)$/.test(command)) {
            if (isFreeAhead()) {
              if (cube.direction === 'north') cube.y -= step;
              else if (cube.direction === 'south') cube.y += step;
              else if (cube.direction === 'east') cube.x += step;
              else if (cube.direction === 'west') cube.x -= step;
            }
          }
          else if (/^завъртам\\(куб,\\s*наляво\\)$/.test(command)) {
            let idx = directions.indexOf(cube.direction);
            cube.direction = directions[(idx + 3) % 4];
          } 
          else if (/^завъртам\\(куб,\\s*надясно\\)$/.test(command)) {
            let idx = directions.indexOf(cube.direction);
            cube.direction = directions[(idx + 1) % 4];
          }
          else if (/^ако_свободно\\(куб,\\s*напред\\)\\s*->\\s*местя\\(куб,\\s*напред\\)$/.test(command)) {
            if (isFreeAhead()) {
              processCommand("местя(куб, напред)");
            }
          }
        }

        window.executePrologCommand = function () {
          const input = document.getElementById("prologInput").value.trim();
          const rawCommands = input.split('.').map(cmd => cmd.trim()).filter(cmd => cmd.length > 0);
          if (rawCommands.length === 0) return;

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

    components.html(html_code, height=600)
