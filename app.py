import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧠 2D Prolog Movement Visualizer")

html_code = """
<div style="display: flex; gap: 20px;">
  <!-- Code Editor Column -->
  <div style="flex: 1; min-width: 300px;">
    <h3 style="color: #2e86c1;">✏️ Prolog Commands</h3>
    <textarea id="codeInput" rows="8" style="width: 100%; font-family: monospace;">местя(куб, напред).
местя(куб, дясно).
местя(куб, назад).
местя(куб, ляво).</textarea>
    
    <button onclick="executeSequence()" style="margin-top: 10px; padding: 8px 15px; background: #2e86c1; color: white; border: none; border-radius: 4px; cursor: pointer;">▶ Run Commands</button>
    <div id="status" style="margin-top: 10px; padding: 10px; background: #e6f7ff; border-radius: 4px;"></div>
  </div>
  
  <!-- Visualization Column -->
  <div style="flex: 1;">
    <h3 style="color: #27ae60;">🟩 Cube Movement</h3>
    <canvas id="gameCanvas" width="400" height="400" style="border: 1px solid #ddd; background: #f9f9f9;"></canvas>
  </div>
</div>

<script>
// ========== INITIALIZATION ==========
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');

// Cube settings
let cube = {
  x: 50,
  y: 50,
  size: 60,
  color: '#2ecc71'
};

// Draw grid background
function drawGrid() {
  ctx.strokeStyle = '#e0e0e0';
  ctx.lineWidth = 1;
  
  // Vertical lines
  for (let x = 0; x <= canvas.width; x += 50) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
  
  // Horizontal lines
  for (let y = 0; y <= canvas.height; y += 50) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }
}

// Draw the cube
function drawCube() {
  ctx.fillStyle = cube.color;
  ctx.fillRect(cube.x, cube.y, cube.size, cube.size);
  
  // Draw orientation marker
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 24px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('↑', cube.x + cube.size/2, cube.y + cube.size/2);
}

// Main drawing function
function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGrid();
  drawCube();
}

// Command execution
function executeCommand(command) {
  const step = 50;
  command = command.trim();
  
  if (/местя\(куб,\s*напред\)\s*\./.test(command)) {
    cube.y -= step;
    return "Moving forward";
  } 
  else if (/местя\(куб,\s*назад\)\s*\./.test(command)) {
    cube.y += step;
    return "Moving backward";
  }
  else if (/местя\(куб,\s*ляво\)\s*\./.test(command)) {
    cube.x -= step;
    return "Moving left";
  }
  else if (/местя\(куб,\s*дясно\)\s*\./.test(command)) {
    cube.x += step;
    return "Moving right";
  }
  return `Unknown command: ${command}`;
}

// Execute command sequence with animation
async function executeSequence() {
  const textarea = document.getElementById("codeInput");
  const commands = textarea.value.split('\n').filter(cmd => cmd.trim() !== '');
  
  statusDiv.innerHTML = '⏳ Starting execution...';
  
  for (let i = 0; i < commands.length; i++) {
    const result = executeCommand(commands[i]);
    statusDiv.innerHTML = `📝 ${result} (${i+1}/${commands.length})`;
    
    // Boundary check
    cube.x = Math.max(0, Math.min(canvas.width - cube.size, cube.x));
    cube.y = Math.max(0, Math.min(canvas.height - cube.size, cube.y));
    
    drawScene();
    await new Promise(r => setTimeout(r, 800));
  }
  
  statusDiv.innerHTML = "✅ All commands executed!";
}

// Initial setup
drawScene();
statusDiv.innerHTML = "🟢 Ready for commands";
</script>
"""

components.html(html_code, height=550)
