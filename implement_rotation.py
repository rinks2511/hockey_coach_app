import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Replace autoFillRotation()
auto_fill_old = """  function autoFillRotation() {
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
  }"""

auto_fill_new = """  function autoFillRotation() {
    // 1. Reset everything EXCEPT 0-6m and GK
    const gkPlayer = currentAssignments['gk'];
    squadPlayers.forEach(p => {
      if (!subMatrixState[p]) subMatrixState[p] = [false, false, false, false, false];
      if (p !== gkPlayer) {
         for(let i=1; i<5; i++) subMatrixState[p][i] = true; // Default everyone to PLAYING
      }
    });

    // 2. Define the exact players assigned to each position
    const lb = currentAssignments['lb'];
    const cb = currentAssignments['cb'];
    const rb = currentAssignments['rb'];
    const sub_def = currentAssignments['sub_def'];
    const lm = currentAssignments['lm'];
    const cm = currentAssignments['cm'];
    const rm = currentAssignments['rm'];
    const st = currentAssignments['st'];
    const sub_mid = currentAssignments['sub_mid'];

    // 3. Mathematical Rotation for Rest (unchecking players)
    // 0-6m is already synced: sub_def and sub_mid are resting.
    
    // 6-12m: Rest LB and LM
    if (lb && subMatrixState[lb]) subMatrixState[lb][1] = false;
    if (lm && subMatrixState[lm]) subMatrixState[lm][1] = false;

    // 12-18m: Rest CB and CM
    if (cb && subMatrixState[cb]) subMatrixState[cb][2] = false;
    if (cm && subMatrixState[cm]) subMatrixState[cm][2] = false;

    // 18-24m: Rest RB and RM
    if (rb && subMatrixState[rb]) subMatrixState[rb][3] = false;
    if (rm && subMatrixState[rm]) subMatrixState[rm][3] = false;

    // 24-30m: Rest sub_def (again) and ST
    if (sub_def && subMatrixState[sub_def]) subMatrixState[sub_def][4] = false;
    if (st && subMatrixState[st]) subMatrixState[st][4] = false;

    renderSubstitutionMatrix();
    showToast('Rotation Auto-Filled!');
  }"""
if auto_fill_old in content:
    content = content.replace(auto_fill_old, auto_fill_new)
else:
    print("WARNING: Could not find autoFillRotation")

# 2. Modify renderSubstitutionMatrix to sort players by positional category
render_matrix_old = """  function renderSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    // Only show players in squadPlayers
    Object.keys(subMatrixState).forEach(p => {
      if (!squadPlayers.includes(p)) delete subMatrixState[p];
    });

    squadPlayers.forEach(player => {
      if (subMatrixState[player]) {
        const tr = document.createElement('tr');
        const tdName = document.createElement('td');
        tdName.innerText = player;
        tdName.style.textAlign = 'left';
        tdName.style.paddingLeft = '10px';
        tr.appendChild(tdName);

        for (let i = 0; i < 5; i++) {
          const td = document.createElement('td');
          const isChecked = subMatrixState[player][i] ? 'checked' : '';
          const disabled = (i === 0) ? 'disabled title="Managed by Tactics Board"' : '';
          td.innerHTML = `<input type="checkbox" onchange="toggleSubMatrix('${player}', ${i})" ${isChecked} ${disabled}>`;
          tr.appendChild(td);
        }
        tbody.appendChild(tr);
      }
    });
    
    validateSubMatrix();
  }"""

render_matrix_new = """  function renderSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    // Only show players in squadPlayers
    Object.keys(subMatrixState).forEach(p => {
      if (!squadPlayers.includes(p)) delete subMatrixState[p];
    });

    // Group players by position
    const gk = currentAssignments['gk'];
    const defenders = [currentAssignments['lb'], currentAssignments['cb'], currentAssignments['rb'], currentAssignments['sub_def']].filter(Boolean);
    const attackers = [currentAssignments['lm'], currentAssignments['cm'], currentAssignments['rm'], currentAssignments['sub_mid'], currentAssignments['st']].filter(Boolean);
    
    const unassigned = squadPlayers.filter(p => p !== gk && !defenders.includes(p) && !attackers.includes(p));

    const groupedPlayers = [];
    if (gk) groupedPlayers.push({ player: gk, label: 'GK' });
    defenders.forEach(p => groupedPlayers.push({ player: p, label: 'DEF' }));
    attackers.forEach(p => groupedPlayers.push({ player: p, label: 'MID/ATT' }));
    unassigned.forEach(p => groupedPlayers.push({ player: p, label: 'BENCH' }));

    groupedPlayers.forEach(item => {
      const player = item.player;
      if (subMatrixState[player]) {
        const tr = document.createElement('tr');
        
        // Add color coding based on position
        if (item.label === 'GK') tr.style.backgroundColor = '#1e3a8a'; // Dark blue
        else if (item.label === 'DEF') tr.style.backgroundColor = '#064e3b'; // Dark green
        else if (item.label === 'MID/ATT') tr.style.backgroundColor = '#701a75'; // Dark purple
        else tr.style.backgroundColor = '#3f3f46'; // Grey
        
        const tdName = document.createElement('td');
        tdName.innerHTML = `<strong>${player}</strong> <span style="font-size:0.6rem; opacity:0.7;">(${item.label})</span>`;
        tdName.style.textAlign = 'left';
        tdName.style.paddingLeft = '10px';
        tr.appendChild(tdName);

        for (let i = 0; i < 5; i++) {
          const td = document.createElement('td');
          const isChecked = subMatrixState[player][i] ? 'checked' : '';
          const disabled = (i === 0) ? 'disabled title="Managed by Tactics Board"' : '';
          td.innerHTML = `<input type="checkbox" onchange="toggleSubMatrix('${player}', ${i})" ${isChecked} ${disabled}>`;
          tr.appendChild(td);
        }
        tbody.appendChild(tr);
      }
    });
    
    validateSubMatrix();
  }"""
if render_matrix_old in content:
    content = content.replace(render_matrix_old, render_matrix_new)
else:
    print("WARNING: Could not find renderSubstitutionMatrix")

with open('index.html', 'w') as f:
    f.write(content)

