import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("3D Prolog-like Movement")

html_code = """
<div style="display: flex;">
  <div style="width: 50%; padding: 10px;">
    <textarea id="prologInput" rows="4" style="width: 100%;">местя(куб, напред).</textarea>
    <button onclick="executePrologCommand()">Изпълни</button>
  </div>
  <div style="width: 50%;">
    <canvas id="threeCanvas" width="500" height="500" style="border: 1px solid #ccc;"></canvas>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
  let scene, camera, renderer, cube;

  function initScene() {
    // 1. Създаваме 3D сцена
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    
    // 2. Настройка на камерата
    camera = new THREE.PerspectiveCamera(75, 500/500, 0.1, 1000);
    camera.position.set(3, 3, 3);
    camera.lookAt(0, 0, 0);
    
    // 3. Създаване на рендерер
    renderer = new THREE.WebGLRenderer({canvas: document.getElementById("threeCanvas")});
    renderer.setSize(500, 500);
    
    // 4. Добавяне на куб
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({color: 0x00ff00, wireframe: false});
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    
    // 5. Помощни оси
    const axesHelper = new THREE.AxesHelper(2);
    scene.add(axesHelper);
    
    animate();
  }

  function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }

  function executePrologCommand() {
    const command = document.getElementById("prologInput").value.trim();
    
    // Разпознаване на Prolog-like команди
    if (/местя\(куб,\s*напред\)\s*\./.test(command)) {
      cube.position.z -= 1;
    } 
    else if (/местя\(куб,\s*назад\)\s*\./.test(command)) {
      cube.position.z += 1;
    }
    else if (/местя\(куб,\s*ляво\)\s*\./.test(command)) {
      cube.position.x -= 1;
    }
    else if (/местя\(куб,\s*дясно\)\s*\./.test(command)) {
      cube.position.x += 1;
    }
    else if (/местя\(куб,\s*горе\)\s*\./.test(command)) {
      cube.position.y += 1;
    }
    else if (/местя\(куб,\s*долу\)\s*\./.test(command)) {
      cube.position.y -= 1;
    }
    else {
      alert(`Невалидна команда. Възможни опции:\n
        местя(куб, напред).\n
        местя(куб, назад).\n
        местя(куб, ляво).\n
        местя(куб, дясно).\n
        местя(куб, горе).\n
        местя(куб, долу).`);
    }
    
    // Камерата следи куба
    camera.lookAt(cube.position);
  }

  // Инициализация при зареждане
  window.onload = initScene;
</script>
"""

components.html(html_code, height=600)
