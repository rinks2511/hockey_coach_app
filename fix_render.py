import re

with open('index.html', 'r') as f:
    content = f.read()

render_matrix_old = """  function renderSubstitutionMatrix() {
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
        cb.checked = subMatrixState[player][i];
        if (i === 0) cb.disabled = true;
        cb.onchange = (e) => {
          subMatrixState[player][i] = e.target.checked;
          validateSubMatrix();
        };
        td.appendChild(cb);
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    });
    
    validateSubMatrix();
  }"""

render_matrix_new = """  function renderSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    squadPlayers.forEach((p, index) => {
      if (!subMatrixState[p]) {
        let defaultPlay = [true, true, true, true, true];
        subMatrixState[p] = defaultPlay;
      }
    });

    Object.keys(subMatrixState).forEach(p => {
      if (!squadPlayers.includes(p)) delete subMatrixState[p];
    });

    const gk = currentAssignments['gk'];
    const defenders = [currentAssignments['lb'], currentAssignments['cb'], currentAssignments['rb'], currentAssignments['sub_def']].filter(Boolean);
    const attackers = [currentAssignments['lm'], currentAssignments['cm'], currentAssignments['rm'], currentAssignments['st'], currentAssignments['sub_mid']].filter(Boolean);
    const unassigned = squadPlayers.filter(p => p !== gk && !defenders.includes(p) && !attackers.includes(p));

    const groupedPlayers = [];
    if (gk) groupedPlayers.push({ player: gk, label: 'GK' });
    defenders.forEach(p => groupedPlayers.push({ player: p, label: 'DEF' }));
    attackers.forEach(p => groupedPlayers.push({ player: p, label: 'MID/ATT' }));
    unassigned.forEach(p => groupedPlayers.push({ player: p, label: 'BENCH' }));

    groupedPlayers.forEach(item => {
      const player = item.player;
      const tr = document.createElement('tr');
      
      // Background colors by group
      if (item.label === 'GK') tr.style.backgroundColor = '#1e3a8a';
      else if (item.label === 'DEF') tr.style.backgroundColor = '#064e3b';
      else if (item.label === 'MID/ATT') tr.style.backgroundColor = '#701a75';
      else tr.style.backgroundColor = '#3f3f46';
      
      const tdName = document.createElement('td');
      tdName.innerHTML = `<strong>${player}</strong> <span style="font-size:0.6rem; opacity:0.7;">(${item.label})</span>`;
      tdName.style.textAlign = 'left';
      tdName.style.paddingLeft = '10px';
      tr.appendChild(tdName);

      for (let i = 0; i < 5; i++) {
        const td = document.createElement('td');
        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.checked = subMatrixState[player][i];
        if (i === 0) cb.disabled = true;
        cb.onchange = (e) => {
          subMatrixState[player][i] = e.target.checked;
          validateSubMatrix();
        };
        td.appendChild(cb);
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    });
    
    validateSubMatrix();
  }"""

if render_matrix_old in content:
    content = content.replace(render_matrix_old, render_matrix_new)
    print("Fixed renderSubstitutionMatrix")
else:
    print("WARNING: Could not find renderSubstitutionMatrix")

with open('index.html', 'w') as f:
    f.write(content)

