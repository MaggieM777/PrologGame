import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Странично меню
page = st.sidebar.radio("Избери урок:", ["Урок 1", "Урок 2"])

if page == "Урок 1":
    st.title("Урок 1: Движение и завъртане на куб")

    st.markdown("""
    ## 📘 Инструкции:

    Този урок ще ти покаже как можеш да управляваш едно "кубче", използвайки **Prolog команди**.

    ### Команди:
    - `местя(куб, напред).`
    - `завъртам(куб, надясно).`
    - `завъртам(куб, наляво).`

    Въвеждай по няколко команди една след друга и натисни **"Изпълни"**.
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
          y: 450,
          size: 50,
          color: '#00ff00',
          direction: 'north'
        };

        const directions = ['north', 'east', 'south', 'west'];

        // Целева позиция
        const target = { x: 400, y: 400 };

        function drawScene() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Цел
          ctx.fillStyle = '#ff0000';
          ctx.fillRect(target.x - 5, target.y - 5, 10, 10);

          // Куб
          ctx.fillStyle = cube.color;
          ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);

          // Стрелка на куба
          ctx.fillStyle = '#000';
          ctx.font = '20px Arial';
          let arrow = '▲';
          if (cube.direction === 'north') arrow = '▲';
          else if (cube.direction === 'east') arrow = '▶';
          else if (cube.direction === 'south') arrow = '▼';
          else if (cube.direction === 'west') arrow = '◀';
          ctx.fillText(arrow, cube.x - 8, cube.y + 6);

          // Проверка дали куба е стигнал целта
          if (Math.abs(cube.x - target.x) < cube.size && Math.abs(cube.y - target.y) < cube.size) {
            alert("Поздравления!");
            let audio = new Audio('https://www.soundjay.com/button/beep-07.wav');
            audio.play();
          }
        }

        function processCommand(command) {
          const step = 30;
          command = command.trim();

          if (/^местя\(куб,\s*напред\)$/.test(command)) {
            if (cube.direction === 'north') cube.y -= step;
            else if (cube.direction === 'south') cube.y += step;
            else if (cube.direction === 'east') cube.x += step;
            else if (cube.direction === 'west') cube.x -= step;
          } 
          else if (/^завъртам\(куб,\s*наляво\)$/.test(command)) {
            let idx = directions.indexOf(cube.direction);
            cube.direction = directions[(idx + 3) % 4];
          } 
          else if (/^завъртам\(куб,\s*надясно\)$/.test(command)) {
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
            drawScene();
            i++;
            setTimeout(executeNext, 500);
          }

          executeNext();
        };

        drawScene();
      });
    </script>
    """
    components.html(html_code, height=600)

elif page == "Урок 2":
    st.title("Урок 2: Препятствия и Правила")

    st.markdown("""
    ## Правила

    В този урок ще използваме **правила в стил Prolog**, за да накараме куба да мисли преди да се движи.

    ### Примери:

    - `ако_свободно(куб, напред) :- местя(куб, напред).`
    - `ако_препятствие(куб, напред) :- завъртам(куб, надясно), местя(куб, напред).`

    Кубът ще избягва препятствия автоматично, ако използваш подходящи правила.
    """)

    st.markdown("⚠️ **Забележка:** Препятствието е в центъра на платното!")

    html_code = """
    <div style="display: flex;">
      <div style="width: 50%; padding: 10px;">
        <textarea id="prologInput" rows="8" style="width: 100%; font-size: 16px;">ако_свободно(куб, напред) :- местя(куб, напред).
ако_препятствие(куб, напред) :- завъртам(куб, надясно), местя(куб, напред).
ако_препятствие(куб, напред).</textarea>
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
        y: 450,
        size: 50,
        color: '#00ff00',
        direction: 'north'
      };

      let obstacle = {
        x: 250,
        y: 250,
        size: 50,
        color: '#ff0000'
      };

      const directions = ['north', 'east', 'south', 'west'];

      function drawScene() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // obstacle
        ctx.fillStyle = obstacle.color;
        ctx.fillRect(obstacle.x - obstacle.size/2, obstacle.y - obstacle.size/2, obstacle.size, obstacle.size);
        // cube
        ctx.fillStyle = cube.color;
        ctx.fillRect(cube.x - cube.size/2, cube.y - cube.size/2, cube.size, cube.size);
        // arrow
        ctx.fillStyle = '#000';
        ctx.font = '20px Arial';
        let arrow = '▲';
        if (cube.direction === 'north') arrow = '▲';
        else if (cube.direction === 'east') arrow = '▶';
        else if (cube.direction === 'south') arrow = '▼';
        else if (cube.direction === 'west') arrow = '◀';
        ctx.fillText(arrow, cube.x - 8, cube.y + 6);
      }

      function isObstacleAhead() {
        const step = 30;
        let nextX = cube.x;
        let nextY = cube.y;
        if (cube.direction === 'north') nextY -= step;
        else if (cube.direction === 'south') nextY += step;
        else if (cube.direction === 'east') nextX += step;
        else if (cube.direction === 'west') nextX -= step;

        return (
          Math.abs(nextX - obstacle.x) < cube.size &&
          Math.abs(nextY - obstacle.y) < cube.size
        );
      }

      function moveForward() {
        const step = 30;
        if (cube.direction === 'north') cube.y -= step;
        else if (cube.direction === 'south') cube.y += step;
        else if (cube.direction === 'east') cube.x += step;
        else if (cube.direction === 'west') cube.x -= step;
      }

      function turnLeft() {
        let idx = directions.indexOf(cube.direction);
        cube.direction = directions[(idx + 3) % 4];
      }

      function turnRight() {
        let idx = directions.indexOf(cube.direction);
        cube.direction = directions[(idx + 1) % 4];
      }

      function processCommand(cmd) {
        if (cmd === "местя(куб, напред)") {
          if (!isObstacleAhead()) {
            moveForward();
          }
        } else if (cmd === "завъртам(куб, наляво)") {
          turnLeft();
        } else if (cmd === "завъртам(куб, надясно)") {
          turnRight();
        } else if (cmd.startsWith("ако_свободно")) {
          if (!isObstacleAhead()) moveForward();
        } else if (cmd.startsWith("ако_препятствие")) {
          if (isObstacleAhead()) {
            turnRight();
            moveForward();
          }
        }
      }

      window.executePrologCommand = function () {
        const input = document.getElementById("prologInput").value.trim();
        const raw = input.split(".").map(c => c.trim()).filter(c => c.length > 0);

        let i = 0;

        function next() {
          if (i >= raw.length) return;
          const cmd = raw[i];
          processCommand(cmd);
          drawScene();
          i++;
          setTimeout(next, 600);
        }

        next();
      };

      drawScene();
    });
    </script>
    """
    components.html(html_code, height=650)
