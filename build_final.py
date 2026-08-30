with open('index.html', 'r') as f:
    content = f.read()

# 1. Add Tabs CSS
css = """
  .nav-tabs { display: flex; gap: 4px; padding: 0 14px 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 12px; margin-top: 10px; }
  .nav-tab { background: transparent; color: #94a3b8; border: none; font-size: 0.85rem; font-weight: 700; padding: 8px 16px; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
  .nav-tab:hover { background: rgba(255,255,255,0.05); color: white; }
  .nav-tab.active { background: #38bdf8; color: #0b0f19; }
  .sub-matrix-table { width: 100%; border-collapse: collapse; font-size: 0.75rem; color: white; background: #0c1017; border: 1px solid #232c3d; }
  .sub-matrix-table th, .sub-matrix-table td { border: 1px solid #232c3d; padding: 4px; text-align: center; }
  .sub-matrix-table th { background: #1e293b; color: #94a3b8; font-weight: 600; }
  .sub-matrix-table td:first-child { text-align: left; font-weight: bold; color: #38bdf8; max-width: 90px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .sub-matrix-checkbox { cursor: pointer; width: 14px; height: 14px; }
  .invalid-col { background: rgba(239, 68, 68, 0.2); }
  .invalid-row { background: rgba(239, 68, 68, 0.2); }
"""
content = content.replace("</style>", css + "\n</style>")

# 2. Add Tabs HTML
tab_html = """
  <!-- TAB NAVIGATION -->
  <div class="nav-tabs">
    <button id="tab-tactics" onclick="switchTab('tactics')" class="nav-tab active">🛡️ Tactics Board</button>
    <button id="tab-subs" onclick="switchTab('subs')" class="nav-tab">⏱️ Substitution Planner</button>
  </div>
"""
content = content.replace("<div class=\"toolbar\">", tab_html + "\n  <div id=\"view-tactics\" style=\"display: block;\">\n  <div class=\"toolbar\">")

# 3. Create view-subs HTML and move the side-panel UI
# The original file has:
old_side_panel = """    <div class="side-panel">
      <div class="panel-title">
        <span id="txtSideTitle">Squad Lineup (10 Slots)</span>
      </div>

      <div class="roster-instruction" id="txtSideInstruction">
        🔄 <strong>Easy Lineup Selection:</strong> Pick players for each spot. Choosing a player already on the pitch will swap them automatically.
      </div>

      <div class="roster-cards" id="sidebarPositionsList"></div>

      <div class="coach-notes">
        <div class="panel-title" id="txtNotesTitle">Coach Match & Rotation Notes</div>
        <textarea id="coachNotes">Horizontal Pitch Strategy:
- 15m Scoring Line: Goals only count when shot or touched inside the 15m line!
- Build-up: Push wide via LB (Liv) and RB (Sai Jiya)
- Sub Rotation: Sub-DEF (Hannah) rotates with Defense; Sub-MID (Shanaya) rotates with Midfield/Attack.</textarea>
      </div>
    </div>"""

# Replace in view-tactics with nothing (we are moving it entirely out)
# Wait, let's just make the tactics wrapper block
content = content.replace(old_side_panel, "")
content = content.replace("grid-template-columns: 1fr 300px;", "display: block; max-width: 900px; margin: 0 auto;")

# Insert the view-subs right after view-tactics closes
view_subs_html = """
  </div> <!-- end view-tactics -->

  <div id="view-subs" style="display: none; max-width: 800px; margin: 0 auto; padding: 20px;">
    <div class="side-panel" style="width: 100%;">
      <div class="panel-title">
        <span id="txtSideTitle">Substitution Planner (6-Min Blocks, per Half)</span>
      </div>

      <div class="roster-instruction" id="txtSideInstruction">
        ✅ Check the box when a player is PLAYING (on the pitch). Each column should have exactly 8 active players.
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
      </div>

      <div class="panel-title" style="margin-top: 20px;">
        <span id="txtManageSquadTitle">Manage Squad List</span>
      </div>
      <div class="add-player" style="display: flex; gap: 4px; margin-bottom: 4px;">
        <input type="text" id="newPlayerInput" placeholder="Add Player Name" style="flex: 1; background: #0c1017; border: 1px solid #232c3d; color: #fff; padding: 4px 6px; border-radius: 4px; font-size: 0.72rem;">
        <button onclick="addSquadPlayer()" style="padding: 4px 8px; background: #059669; border-color: #10b981; color: white; cursor: pointer;">+</button>
      </div>
      <div id="squadListContainer" style="display: flex; flex-wrap: wrap; gap: 4px; max-height: 80px; overflow-y: auto; background: #0c1017; padding: 4px; border: 1px solid #232c3d; border-radius: 5px; margin-bottom: 10px;"></div>

      <div class="coach-notes" style="margin-top: 20px;">
        <div class="panel-title" id="txtNotesTitle">Coach Match & Rotation Notes</div>
        <textarea id="coachNotes">Horizontal Pitch Strategy:
- 15m Scoring Line: Goals only count when shot or touched inside the 15m line!
- Build-up: Push wide via LB (Liv) and RB (Sai Jiya)
- Sub Rotation: Sub-DEF (Hannah) rotates with Defense; Sub-MID (Shanaya) rotates with Midfield/Attack.</textarea>
      </div>
    </div>
  </div>
"""

content = content.replace("  <div class=\"rules-panel\" style=\"margin-top: 10px;\">", view_subs_html + "\n  <div class=\"rules-panel\" style=\"margin-top: 10px;\">")

# 4. JS Logic for Matrix and Tabs
js_logic = """
  let squadLocal = null;
  try {
    const raw = localStorage.getItem('hv_myra_squad');
    if (raw) squadLocal = JSON.parse(raw);
  } catch (e) {
    console.error("Error parsing squad", e);
  }
  let squadPlayers = (squadLocal && Array.isArray(squadLocal) && squadLocal.length > 0) ? squadLocal : [
    "Sai Jiya", "Defne", "Shanaya", "Alina", "Liv", "Mira", "Hannah", "Kyra", "Kate", "Liz"
  ];

  function saveSquadLocal() {
    localStorage.setItem('hv_myra_squad', JSON.stringify(squadPlayers));
  }

  function addSquadPlayer() {
    const input = document.getElementById('newPlayerInput');
    const name = input.value.trim();
    if (name && !squadPlayers.includes(name)) {
      squadPlayers.push(name);
      renderSquadManager();
      renderSubstitutionMatrix();
      initDropdowns();
      saveSquadLocal();
      input.value = '';
    }
  }

  function deleteSquadPlayer(name) {
    const idx = squadPlayers.indexOf(name);
    if (idx > -1) {
      squadPlayers.splice(idx, 1);
      renderSquadManager();
      renderSubstitutionMatrix();
      initDropdowns();
      saveSquadLocal();
    }
  }

  function renderSquadManager() {
    const container = document.getElementById('squadListContainer');
    if (!container) return;
    container.innerHTML = '';
    squadPlayers.forEach(player => {
      const chip = document.createElement('span');
      chip.style.cssText = 'background: #1c2230; padding: 2px 6px; border-radius: 10px; font-size: 0.65rem; display: inline-flex; align-items: center; gap: 4px; border: 1px solid #334155;';
      chip.innerHTML = `${player} <span onclick="deleteSquadPlayer('${player}')" style="color: #ef4444; cursor: pointer; font-weight: bold; padding: 0 2px;">&times;</span>`;
      container.appendChild(chip);
    });
  }

  let subMatrixState = {};

  function renderSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    squadPlayers.forEach((p, index) => {
      if (!subMatrixState[p]) {
        let defaultPlay = [true, true, true, true, true];
        const restBlock = Math.floor(index / 2);
        if (restBlock >= 0 && restBlock < 5) defaultPlay[restBlock] = false;
        subMatrixState[p] = defaultPlay;
      }
    });

    Object.keys(subMatrixState).forEach(p => {
      if (!squadPlayers.includes(p)) delete subMatrixState[p];
    });

    squadPlayers.forEach(player => {
      const tr = document.createElement('tr');
      const tdName = document.createElement('td');
      tdName.innerText = player;
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

    const colCounts = [0, 0, 0, 0, 0];
    Object.values(subMatrixState).forEach(checks => {
      checks.forEach((c, i) => { if (c) colCounts[i]++; });
    });

    const table = document.getElementById('subMatrixTable');
    for (let i = 0; i < 5; i++) {
      const isColValid = colCounts[i] === 8;
      table.querySelectorAll(`tr td:nth-child(${i+2}), th:nth-child(${i+2})`).forEach(cell => {
        if (!isColValid) cell.classList.add('invalid-col');
        else cell.classList.remove('invalid-col');
      });
      if (!isColValid) {
        isValid = false;
        errors.push(`Block ${i+1} needs exactly 8 players.`);
      }
    }

    let badRows = false;
    rows.forEach(tr => {
      const player = tr.querySelector('td').innerText;
      const count = subMatrixState[player] ? subMatrixState[player].filter(Boolean).length : 0;
      if (count !== 4) {
        tr.classList.add('invalid-row');
        badRows = true;
        isValid = false;
      } else {
        tr.classList.remove('invalid-row');
      }
    });
    if (badRows) errors.push('Every player must play exactly 4 blocks per half (24 mins).');

    valMsg.innerText = isValid ? '' : errors.join(' ');
  }

  function switchTab(tab) {
    document.getElementById('view-tactics').style.display = tab === 'tactics' ? 'block' : 'none';
    document.getElementById('view-subs').style.display = tab === 'subs' ? 'block' : 'none';
    document.getElementById('tab-tactics').className = tab === 'tactics' ? 'nav-tab active' : 'nav-tab';
    document.getElementById('tab-subs').className = tab === 'subs' ? 'nav-tab active' : 'nav-tab';
  }
"""

content = content.replace("  let googleClientId", js_logic + "\n  let googleClientId")

# Remove the old renderPositionLabels sidebar rendering since it was in old_side_panel which is gone
old_sidebar_js = """    const sidebarContainer = document.getElementById('sidebarPositionsList');
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
          ${squadPlayers.map(player => `<option value="${player}">${player}</option>`).join('')}
        </select>
      `;
      sidebarContainer.appendChild(row);
      const sideSelect = document.getElementById(`select_side_${pos.id}`);
      if (sideSelect) sideSelect.value = currentAssignments[pos.id];
    });"""

content = content.replace(old_sidebar_js, "")

# 5. Fix window.onload and save/load
window_onload_fix = """    resizeCanvas();
    renderSquadManager();
    renderSubstitutionMatrix();
    initDropdowns();"""
content = content.replace("    resizeCanvas();\n    initDropdowns();\n    document.getElementById('googleClientIdInput').value = googleClientId;", window_onload_fix + "\n    document.getElementById('googleClientIdInput').value = googleClientId;")

with open('index.html', 'w') as f:
    f.write(content)
