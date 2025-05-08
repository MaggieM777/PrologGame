import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧠 3D Cube Movement")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="commandInput" rows="4" style="width: 100%;">forward</textarea>
    <button onclick="moveCube()">Move Cube</button>
  </div>
  <div style="width: 50%;">
    <canvas id="threeCanvas" width="500" height="500" style="border: 1px solid #ccc;"></canvas>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
  let scene, camera, renderer, cube;

  function initScene() {
    // 1. Създаваме сцена
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    
    // 2. Настройваме камера
    camera = new THREE.PerspectiveCamera(75, 500/500, 0.1, 1000);
    camera.position.set(5, 5, 5);
    camera.lookAt(0, 0, 0);
    
    // 3. Създаваме рендерер
    renderer = new THREE.WebGLRenderer({canvas: document.getElementById("threeCanvas")});
    renderer.setSize(500, 500);
    
    // 4. Добавяме куб
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({color: 0x00ff00});
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    
    // 5. Добавяме помощни оси (за визуализация)
    const axesHelper = new THREE.AxesHelper(2);
    scene.add(axesHelper);
    
    animate();
  }

  function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }

  function moveCube() {
    const command = document.getElementById("commandInput").value.trim().toLowerCase();
    
    // Разстояние на движение
    const step = 1.0;
    
    switch(command) {
      case "forward":
        cube.position.z -= step;  // Z намалява = напред
        break;
      case "backward":
        cube.position.z += step;  // Z нараства = назад
        break;
      case "left":
        cube.position.x -= step;  // X намалява = наляво
        break;
      case "right":
        cube.position.x += step;  // X нараства = надясно
        break;
      case "up":
        cube.position.y += step;  // Y нараства = нагоре
        break;
      case "down":
        cube.position.y -= step;  // Y намалява = надолу
        break;
      default:
        alert(`Invalid command. Try: forward, backward, left, right, up, down`);
    }
    
    // Препоръчително: пренасочваме камерата към куба
    camera.lookAt(cube.position);
  }

  // Инициализация при зареждане
  window.onload = initScene;
</script>
"""

components.html(html_code, height=600)
