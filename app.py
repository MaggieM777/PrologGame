import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🧠 Learn Prolog with 3D Visualization")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="10" style="width: 100%;">move(forward).</textarea>
    <button onclick="runProlog()">Run</button>
  </div>
  <div style="width: 50%;">
    <canvas id="threeCanvas" width="400" height="400" style="border: 1px solid #ccc;"></canvas>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/tau-prolog@0.3.1/modules/core.min.js"></script>

<script>
  let scene, camera, renderer, cube;

  function initScene() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, 400 / 400, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("threeCanvas") });
    renderer.setSize(400, 400);
    camera.position.z = 5;

    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    animate();
  }

  function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }

  function moveObject(direction) {
    if (direction === "forward") {
      cube.position.z -= 0.5;
    } else if (direction === "backward") {
      cube.position.z += 0.5;
    } else if (direction === "left") {
      cube.position.x -= 0.5;
    } else if (direction === "right") {
      cube.position.x += 0.5;
    }
  }

  function runProlog() {
    const code = document.getElementById("prologInput").value;
    
    // Създаваме Prolog сесия
    const session = pl.create(1000);
    
    // Зареждаме кода
    session.consult(code, {
      success: function() {
        // Изпълняваме заявката
        session.query("move(Direction).", {
          success: function(goal) {
            session.answer({
              success: function(answer) {
                // Взимаме посоката от отговора
                const direction = answer.links.Direction.id;
                moveObject(direction);
              },
              fail: function() {
                alert("No solution found.");
              }
            });
          },
          error: function(err) {
            alert("Query error: " + err);
          }
        });
      },
      error: function(err) {
        alert("Consult error: " + err);
      }
    });
  }

  // Инициализираме сцената при зареждане
  window.onload = initScene;
</script>
"""

components.html(html_code, height=500)
