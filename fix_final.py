import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Remove the injected squad functions (from saveSquadLocal at 711 to the end of renderSquadManager)
# We can find this chunk specifically because it's right before let subMatrixState = {};
injected_squad_funcs = """  function saveSquadLocal() {
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
"""

content = content.replace(injected_squad_funcs, "")

# 2. Update the ORIGINAL addSquadPlayer to call renderSubstitutionMatrix()
old_add = """    squadPlayers.push(name);
    input.value = '';
    saveSquadLocal();
    renderSquadManager();
    initDropdowns();"""
new_add = """    squadPlayers.push(name);
    input.value = '';
    saveSquadLocal();
    renderSquadManager();
    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();
    initDropdowns();"""
content = content.replace(old_add, new_add)

# 3. Update the ORIGINAL deleteSquadPlayer to call renderSubstitutionMatrix()
old_delete = """    squadPlayers = squadPlayers.filter(p => p !== name);
    
    // Fallback if deleted player was assigned"""
new_delete = """    squadPlayers = squadPlayers.filter(p => p !== name);
    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();
    
    // Fallback if deleted player was assigned"""
content = content.replace(old_delete, new_delete)

with open('index.html', 'w') as f:
    f.write(content)

print("Duplicates removed and matrix connected!")
