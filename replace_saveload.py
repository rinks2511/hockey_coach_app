import re

with open('index.html', 'r') as f:
    content = f.read()

# Add loadOverlay before the closing body tag
overlay_html = """
<div id="loadOverlay" style="position: fixed; inset: 0; background: rgba(0,0,0,0.8); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 9999; font-family: system-ui;">
  <div style="background: #1e293b; padding: 30px; border-radius: 12px; width: 400px; max-width: 90%; color: white;">
    <h3 style="margin-top:0;">Load Saved Match</h3>
    <div id="savedMatchesList" style="max-height: 300px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px;"></div>
    <div style="display: flex; justify-content: flex-end; gap: 10px;">
      <button onclick="document.getElementById('loadOverlay').style.display='none'" style="background: transparent; color: white; border: 1px solid white; padding: 6px 12px; border-radius: 4px; cursor: pointer;">Cancel</button>
    </div>
  </div>
</div>
"""
content = content.replace("</body>", overlay_html + "\n</body>")

# Replace saveTacticsLocal and loadTacticsLocal
pattern = r"function saveTacticsLocal\(\) \{.*?(?=  function initDropdowns\(\) \{)"
replacement = """function saveTacticsLocal() {
    const saveName = prompt("Enter a name to save this match as:", `${document.getElementById('matchOpponent').value} - ${document.getElementById('matchHalf').value}`);
    if (!saveName) return;

    const tokenPositions = {};
    document.querySelectorAll('.token').forEach(el => {
      tokenPositions[el.id] = { left: el.style.left, top: el.style.top, role: el.getAttribute('data-pos') };
    });

    const data = {
      name: saveName,
      timestamp: Date.now(),
      formation: currentFormation,
      assignments: currentAssignments,
      matchDate: document.getElementById('matchDatePicker').value,
      matchOpponent: document.getElementById('matchOpponent').value,
      matchHalf: document.getElementById('matchHalf').value,
      notes: document.getElementById('coachNotes').value,
      drawings: drawnObjects,
      tokenPositions: tokenPositions
    };

    let savedMatches = JSON.parse(localStorage.getItem('hv_myra_saved_matches') || '{}');
    savedMatches[saveName] = data;
    localStorage.setItem('hv_myra_saved_matches', JSON.stringify(savedMatches));
    
    // Also save as default so refresh restores it
    localStorage.setItem('hv_myra_clean_pdf_board', JSON.stringify(data));
    showToast('Match Saved: ' + saveName);
  }

  function loadTacticsLocal() {
    const savedMatches = JSON.parse(localStorage.getItem('hv_myra_saved_matches') || '{}');
    const list = document.getElementById('savedMatchesList');
    list.innerHTML = '';
    
    if (Object.keys(savedMatches).length === 0) {
      list.innerHTML = '<div style="color: #94a3b8; font-size: 0.9rem;">No saved matches found.</div>';
    } else {
      Object.values(savedMatches).sort((a,b) => b.timestamp - a.timestamp).forEach(data => {
        const btn = document.createElement('button');
        btn.style.cssText = 'background: #334155; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; text-align: left; display: flex; justify-content: space-between; align-items: center;';
        
        const titleSpan = document.createElement('span');
        titleSpan.innerText = data.name;
        
        const delBtn = document.createElement('span');
        delBtn.innerHTML = '🗑️';
        delBtn.style.cursor = 'pointer';
        delBtn.onclick = (e) => {
          e.stopPropagation();
          if (confirm(`Delete saved match "${data.name}"?`)) {
            delete savedMatches[data.name];
            localStorage.setItem('hv_myra_saved_matches', JSON.stringify(savedMatches));
            loadTacticsLocal();
          }
        };

        btn.appendChild(titleSpan);
        btn.appendChild(delBtn);

        btn.onclick = () => {
          loadMatchData(data);
          document.getElementById('loadOverlay').style.display = 'none';
        };
        list.appendChild(btn);
      });
    }
    document.getElementById('loadOverlay').style.display = 'flex';
  }

  function loadMatchData(data) {
    if (data.formation && formations[data.formation]) {
      applyFormation(data.formation);
    }
    if (data.assignments) currentAssignments = data.assignments;
    if (data.matchDate) document.getElementById('matchDatePicker').value = data.matchDate;
    if (data.matchOpponent) document.getElementById('matchOpponent').value = data.matchOpponent;
    if (data.matchHalf) document.getElementById('matchHalf').value = data.matchHalf;
    if (data.notes) document.getElementById('coachNotes').value = data.notes;
    if (data.drawings) {
      drawnObjects = data.drawings;
      redrawCanvas();
    }
    if (data.tokenPositions) {
      for (const [id, pos] of Object.entries(data.tokenPositions)) {
        const el = document.getElementById(id);
        if (el) {
          el.style.left = pos.left;
          el.style.top = pos.top;
          if (pos.role && el.querySelector('.token-circle')) {
            el.setAttribute('data-pos', pos.role);
            el.querySelector('.token-circle').innerHTML = pos.role;
            const pId = id.replace('pos_', '');
            const labelEl = document.getElementById(`lbl_side_${pId}`);
            if (labelEl) labelEl.innerHTML = pos.role;
          }
        }
      }
    }
    syncBanner();
    
    positionsConfig.forEach(pos => {
      const boardSelect = document.getElementById(`select_board_${pos.id}`);
      const sideSelect = document.getElementById(`select_side_${pos.id}`);
      if (boardSelect) boardSelect.value = currentAssignments[pos.id] || '';
      if (sideSelect) sideSelect.value = currentAssignments[pos.id] || '';
    });
    showToast('Match Loaded: ' + (data.name || 'Setup'));
  }

"""
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# update window.onload where it applies default formation
onload_pattern = r"// Apply default formation if no local tactical data was loaded over it.*?applyFormation\('1-2-3-2'\);\n    \}"
onload_replace = """const rawData = localStorage.getItem('hv_myra_clean_pdf_board');
    if (!rawData) {
      applyFormation('1-2-3-2');
    } else {
      loadMatchData(JSON.parse(rawData));
    }
  };"""
content = re.sub(onload_pattern, onload_replace, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

