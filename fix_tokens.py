import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace hardcoded coordinates in window.onload or wherever init default coordinates are
old_coords = """  let drawnObjects = [];
  
  const tokenInitPositions = {
    gk: { x: 400, y: 490 },
    lb: { x: 150, y: 380 },
    cb: { x: 400, y: 380 },
    rb: { x: 650, y: 380 },
    lm: { x: 150, y: 250 },
    cm: { x: 400, y: 250 },
    rm: { x: 650, y: 250 },
    st: { x: 400, y: 100 }
  };"""

# 1-2-3-2 Shape:
# GK: 400, 490
# LD: 250, 380
# RD: 550, 380
# LM: 150, 250
# CM: 400, 250
# RM: 650, 250
# LF: 250, 100
# RF: 550, 100
new_coords = """  let drawnObjects = [];
  
  const tokenInitPositions = {
    gk: { x: 400, y: 490 },
    ld: { x: 250, y: 380 },
    rd: { x: 550, y: 380 },
    lm: { x: 150, y: 250 },
    cm: { x: 400, y: 250 },
    rm: { x: 650, y: 250 },
    lf: { x: 250, y: 100 },
    rf: { x: 550, y: 100 }
  };"""

content = content.replace(old_coords, new_coords)


old_html = """      <!-- Defense -->
      <label>LB:</label> <select id="select_board_lb" onchange="onPositionChanged('lb', this.value)"></select>
      <label>CB:</label> <select id="select_board_cb" onchange="onPositionChanged('cb', this.value)"></select>
      <label>RB:</label> <select id="select_board_rb" onchange="onPositionChanged('rb', this.value)"></select>
      <label class="sub-label">SUB (DEF):</label> <select id="select_board_sub_def" onchange="onPositionChanged('sub_def', this.value)"></select>
      
      <!-- Midfield -->
      <label>LM:</label> <select id="select_board_lm" onchange="onPositionChanged('lm', this.value)"></select>
      <label>CM:</label> <select id="select_board_cm" onchange="onPositionChanged('cm', this.value)"></select>
      <label>RM:</label> <select id="select_board_rm" onchange="onPositionChanged('rm', this.value)"></select>
      <label class="sub-label">SUB (MID):</label> <select id="select_board_sub_mid" onchange="onPositionChanged('sub_mid', this.value)"></select>

      <!-- Attack -->
      <label>ST:</label> <select id="select_board_st" onchange="onPositionChanged('st', this.value)"></select>"""

new_html = """      <!-- Defense -->
      <label>LD:</label> <select id="select_board_ld" onchange="onPositionChanged('ld', this.value)"></select>
      <label>RD:</label> <select id="select_board_rd" onchange="onPositionChanged('rd', this.value)"></select>
      <label class="sub-label">SUB (DEF/ATT):</label> <select id="select_board_sub_def_att" onchange="onPositionChanged('sub_def_att', this.value)"></select>
      
      <!-- Midfield -->
      <label>LM:</label> <select id="select_board_lm" onchange="onPositionChanged('lm', this.value)"></select>
      <label>CM:</label> <select id="select_board_cm" onchange="onPositionChanged('cm', this.value)"></select>
      <label>RM:</label> <select id="select_board_rm" onchange="onPositionChanged('rm', this.value)"></select>
      <label class="sub-label">SUB (MID):</label> <select id="select_board_sub_mid" onchange="onPositionChanged('sub_mid', this.value)"></select>

      <!-- Attack -->
      <label>LF:</label> <select id="select_board_lf" onchange="onPositionChanged('lf', this.value)"></select>
      <label>RF:</label> <select id="select_board_rf" onchange="onPositionChanged('rf', this.value)"></select>"""

content = content.replace(old_html, new_html)

with open('index.html', 'w') as f:
    f.write(content)

print("Updated HTML and canvas coordinates.")
