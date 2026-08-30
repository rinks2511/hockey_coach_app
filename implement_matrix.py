import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update HTML Sidebar UI
old_ui = """      <div class="panel-title">
        <span id="txtSideTitle">Squad Lineup (10 Slots)</span>
      </div>

      <div class="roster-instruction" id="txtSideInstruction">
        🔄 <strong>Easy Lineup Selection:</strong> Pick players for each spot. Choosing a player already on the pitch will swap them automatically.
      </div>

      <div class="roster-cards" id="sidebarPositionsList"></div>"""

new_ui = """      <div class="panel-title">
        <span id="txtSideTitle">Substitution Planner (6-Min Blocks)</span>
      </div>

      <div class="roster-instruction" id="txtSideInstruction">
        ✅ Check the box when a player rests (on the bench). Each column should have exactly 2 resting players.
      </div>

      <div class="substitution-matrix" id="substitutionMatrixContainer">
        <table class="sub-matrix-table" id="subMatrixTable">
          <thead>
            <tr>
              <th>Player</th>
              <th>0-6m</th>
              <th>6-12m</th>
              <th>12-18m</th>
              <th>18-24m</th>
              <th>24-30m</th>
            </tr>
          </thead>
          <tbody id="subMatrixBody"></tbody>
        </table>
        <div id="subMatrixValidation" style="color: #ef4444; font-size: 0.75rem; margin-top: 5px; min-height: 14px;"></div>
      </div>"""
content = content.replace(old_ui, new_ui)

# 2. Add Matrix CSS
css = """
  .sub-matrix-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.75rem;
    color: white;
    background: #0c1017;
    border: 1px solid #232c3d;
  }
  .sub-matrix-table th, .sub-matrix-table td {
    border: 1px solid #232c3d;
    padding: 4px;
    text-align: center;
  }
  .sub-matrix-table th {
    background: #1e293b;
    color: #94a3b8;
    font-weight: 600;
  }
  .sub-matrix-table td:first-child {
    text-align: left;
    font-weight: bold;
    color: #38bdf8;
    max-width: 90px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .sub-matrix-checkbox {
    cursor: pointer;
    width: 14px;
    height: 14px;
  }
  .invalid-col { background: rgba(239, 68, 68, 0.2); }
  .invalid-row { background: rgba(239, 68, 68, 0.2); }
</style>"""
content = content.replace("</style>", css)

# 3. Modify renderPositionLabels to remove sidebarPositionsList rendering
old_render_part = """    const sidebarContainer = document.getElementById('sidebarPositionsList');
    sidebarContainer.innerHTML = '';
    positionsConfig.forEach(pos => {
      const tokenEl = document.getElementById(`pos_${pos.id}`);
      let label = "";
      if (pos.id === 'sub_def') {
        label = currentLang === 'en' ? 'SUB-DEF' : 'WIS-DEF';
      } else if (pos.id === 'sub_mid') {
        label = currentLang === 'en' ? 'SUB-MID' : 'WIS-MID';
      } else {
        label = tokenEl ? tokenEl.getAttribute('data-pos') : pos.id.toUpperCase();
      }

      const row = document.createElement('div');
      row.className = 'position-row';
      const tagClass = pos.isSubDef ? 'pos-tag tag-sub-def' : (pos.isSubMid ? 'pos-tag tag-sub-mid' : 'pos-tag');
      row.innerHTML = `
        <span class="${tagClass}" id="lbl_side_${pos.id}" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('${pos.id}')">${label}</span>
        <select class="sidebar-select" id="select_side_${pos.id}" onchange="onPositionChanged('${pos.id}', this.value)">
          <option value="">--</option>
        </select>
      `;
      sidebarContainer.appendChild(row);
    });"""

content = content.replace(old_render_part, "")

# 4. Add Matrix Logic
matrix_logic = """
  let subMatrixState = {}; // { player: [bool, bool, bool, bool, bool] }

  function renderSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    // Initialize new players in state
    squadPlayers.forEach(p => {
      if (!subMatrixState[p]) subMatrixState[p] = [false, false, false, false, false];
    });
    // Remove old players
    Object.keys(subMatrixState).forEach(p => {
      if (!squadPlayers.includes(p)) delete subMatrixState[p];
    });

    squadPlayers.forEach(player => {
      const tr = document.createElement('tr');
      const tdName = document.createElement('td');
      tdName.innerText = player;
      tdName.title = player;
      tr.appendChild(tdName);

      for (let i = 0; i < 5; i++) {
        const td = document.createElement('td');
        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.className = 'sub-matrix-checkbox';
        cb.checked = subMatrixState[player][i];
        cb.onchange = (e) => {
          subMatrixState[player][i] = e.target.checked;
          validateSubstitutionMatrix();
        };
        td.appendChild(cb);
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    });
    validateSubstitutionMatrix();
  }

  function validateSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    const valMsg = document.getElementById('subMatrixValidation');
    if (!tbody) return;

    const rows = tbody.querySelectorAll('tr');
    let isValid = true;
    let errors = [];

    // Check columns (exactly 2 per column)
    const colCounts = [0, 0, 0, 0, 0];
    Object.values(subMatrixState).forEach(checks => {
      checks.forEach((c, i) => { if (c) colCounts[i]++; });
    });

    // Color code columns
    const table = document.getElementById('subMatrixTable');
    for (let i = 0; i < 5; i++) {
      const isColValid = colCounts[i] === 2;
      table.querySelectorAll(`tr td:nth-child(${i+2}), th:nth-child(${i+2})`).forEach(cell => {
        if (!isColValid) cell.classList.add('invalid-col');
        else cell.classList.remove('invalid-col');
      });
      if (!isColValid) {
        isValid = false;
        errors.push(`Block ${i+1} needs exactly 2 resting players.`);
      }
    }

    // Color code rows (exactly 1 per row for perfect equal time, but we'll just warn if > 1 or 0)
    let badRows = false;
    rows.forEach(tr => {
      const player = tr.querySelector('td').innerText;
      const count = subMatrixState[player] ? subMatrixState[player].filter(Boolean).length : 0;
      if (count !== 1) {
        tr.classList.add('invalid-row');
        badRows = true;
        isValid = false;
      } else {
        tr.classList.remove('invalid-row');
      }
    });
    if (badRows) errors.push('Each player should rest exactly once for equal time.');

    valMsg.innerText = isValid ? '' : errors.join(' ');
  }
"""

content = content.replace("function renderSquadManager() {", matrix_logic + "\n  function renderSquadManager() {")
content = content.replace("renderSquadManager();\n    initDropdowns();", "renderSquadManager();\n    renderSubstitutionMatrix();\n    initDropdowns();")

# Update Add/Remove player logic to trigger matrix render
content = content.replace("squadPlayers.push(val);", "squadPlayers.push(val);\n      renderSubstitutionMatrix();")
content = content.replace("squadPlayers.splice(index, 1);", "squadPlayers.splice(index, 1);\n      renderSubstitutionMatrix();")


with open('index.html', 'w') as f:
    f.write(content)

print("Implemented Matrix")
