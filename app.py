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

<script src="https://unpkg.com/three@0.160.1/build/three.min.js"></script>
<script src="https://unpkg.com/tau-prolog@0.3.1/modules/core.js"></script>

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

  function moveObject() {
    cube.position.z -= 1;
  }

  function runProlog() {
    let code = document.getElementById("prologInput").value;
    let session = pl.create();
    session.consult("move(forward). " + code, {
      success: function () {
        session.query("move(forward).", {
          success: function (goal) {
            session.answer({
              success: function () {
                moveObject();
              },
              fail: function () {
                alert("Incorrect or missing rule.");
              }
            });
          }
        });
      },
      error: function (err) {
        alert("Syntax error: " + err);
      }
    });
  }

  initScene();
</script>
"""

# Embed the entire interface
components.html(html_code, height=500)
