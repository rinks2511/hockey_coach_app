import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update updatePosition to sync the matrix
update_pos_old = """    currentAssignments[posId] = selectedPlayer;
    if (previousPlayerAtThisPos && previousPlayerAtThisPos !== selectedPlayer) {
      if (document.getElementById(`pos_${posId}`)) {
        document.getElementById(`pos_${posId}`).querySelector('.static-pill').innerText = selectedPlayer;
      }
    }
    
    // Update local storage
    saveBoardLocal();
  }"""
  
update_pos_new = """    currentAssignments[posId] = selectedPlayer;
    if (previousPlayerAtThisPos && previousPlayerAtThisPos !== selectedPlayer) {
      if (document.getElementById(`pos_${posId}`)) {
        document.getElementById(`pos_${posId}`).querySelector('.static-pill').innerText = selectedPlayer;
      }
    }
    
    // Update local storage
    saveBoardLocal();
    syncMatrixFromTactics();
  }"""
content = content.replace(update_pos_old, update_pos_new)

# 2. Add syncMatrixFromTactics and autoFillRotation
sync_funcs = """  function syncMatrixFromTactics() {
    if (typeof subMatrixState === 'undefined') return;
    
    // First, clear the 0-6m block for everyone
    Object.keys(subMatrixState).forEach(p => subMatrixState[p][0] = false);
    
    // Then, set the 0-6m block for everyone on the pitch
    const gkPlayer = currentAssignments['gk'];
    Object.values(currentAssignments).forEach(p => {
      if (p && subMatrixState[p]) {
        subMatrixState[p][0] = true;
      }
    });
    
    // Lock GK for the whole match
    if (gkPlayer && subMatrixState[gkPlayer]) {
      for(let i=0; i<5; i++) subMatrixState[gkPlayer][i] = true;
    }
    
    renderSubstitutionMatrix();
  }

  function autoFillRotation() {
    // 1. Reset everything EXCEPT 0-6m and GK
    const gkPlayer = currentAssignments['gk'];
    squadPlayers.forEach(p => {
      if (!subMatrixState[p]) subMatrixState[p] = [false, false, false, false, false];
      if (p !== gkPlayer) {
         for(let i=1; i<5; i++) subMatrixState[p][i] = false;
      }
    });
    
    // 2. Identify the field players
    const fieldPlayers = squadPlayers.filter(p => p !== gkPlayer);
    
    // 3. We need 7 field players per block (blocks 1, 2, 3, 4).
    // We already have block 0 set by the tactics board.
    // Total blocks to fill = 7 spots * 4 blocks = 28 spots.
    // We want to distribute them evenly among the field players.
    
    // Let's just track how many blocks each player has played so far
    const playedCounts = {};
    fieldPlayers.forEach(p => {
      playedCounts[p] = subMatrixState[p][0] ? 1 : 0;
    });
    
    for (let blockIndex = 1; blockIndex < 5; blockIndex++) {
      // Sort players by least played to prioritize them for this block
      fieldPlayers.sort((a, b) => playedCounts[a] - playedCounts[b]);
      
      // Select the first 7 players
      for (let i = 0; i < 7; i++) {
        const p = fieldPlayers[i];
        if (p) {
          subMatrixState[p][blockIndex] = true;
          playedCounts[p]++;
        }
      }
    }
    
    renderSubstitutionMatrix();
    showToast('Rotation Auto-Filled!');
  }
"""

content = content.replace("  function saveSquadLocal() {", sync_funcs + "\n  function saveSquadLocal() {")

# 3. Add Auto-Fill Button to the Substitution Planner UI
sub_planner_title_old = """      <div class="panel-title">
        <span id="txtSideTitle">Substitution Planner (6-Min Blocks, per Half)</span>
      </div>"""
      
sub_planner_title_new = """      <div class="panel-title" style="display: flex; justify-content: space-between; align-items: center;">
        <span id="txtSideTitle">Substitution Planner (6-Min Blocks, per Half)</span>
        <button onclick="autoFillRotation()" style="padding: 4px 10px; background: #3b82f6; border-color: #2563eb; color: white; border-radius: 4px; font-size: 0.75rem; cursor: pointer;">⚡ Auto-Fill Rotation</button>
      </div>"""
content = content.replace(sub_planner_title_old, sub_planner_title_new)

# 4. Make 0-6m column read-only in the matrix (disable checkbox if blockIndex == 0)
matrix_render_old = """        for (let i = 0; i < 5; i++) {
          const td = document.createElement('td');
          const isChecked = subMatrixState[player][i] ? 'checked' : '';
          td.innerHTML = `<input type="checkbox" onchange="toggleSubMatrix('${player}', ${i})" ${isChecked}>`;
          tr.appendChild(td);
        }"""
        
matrix_render_new = """        for (let i = 0; i < 5; i++) {
          const td = document.createElement('td');
          const isChecked = subMatrixState[player][i] ? 'checked' : '';
          const disabled = (i === 0) ? 'disabled title="Managed by Tactics Board"' : '';
          td.innerHTML = `<input type="checkbox" onchange="toggleSubMatrix('${player}', ${i})" ${isChecked} ${disabled}>`;
          tr.appendChild(td);
        }"""
content = content.replace(matrix_render_old, matrix_render_new)

# 5. Connect sync to saveBoardLocal just in case it loads from localstorage
load_board_old = """  function loadBoardLocal() {
    const raw = localStorage.getItem('hv_myra_board');
    if (raw) {
      try {
        const data = JSON.parse(raw);
        if (data.assignments) currentAssignments = data.assignments;
      } catch(e) {}
    }
  }"""
load_board_new = """  function loadBoardLocal() {
    const raw = localStorage.getItem('hv_myra_board');
    if (raw) {
      try {
        const data = JSON.parse(raw);
        if (data.assignments) currentAssignments = data.assignments;
      } catch(e) {}
    }
    if (typeof syncMatrixFromTactics === 'function') setTimeout(syncMatrixFromTactics, 100);
  }"""
content = content.replace(load_board_old, load_board_new)


with open('index.html', 'w') as f:
    f.write(content)

