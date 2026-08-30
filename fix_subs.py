import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add renderSubstitutionMatrix to window.onload
onload_old = "    renderSquadManager();"
onload_new = "    renderSquadManager();\n    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();"
content = content.replace(onload_old, onload_new)

# 2. Rename the IDs in the view-subs tab
# The view-subs tab starts at <div id="view-subs"
view_subs_idx = content.find('<div id="view-subs"')
if view_subs_idx != -1:
    before = content[:view_subs_idx]
    after = content[view_subs_idx:]
    
    # Rename IDs in the after portion
    after = after.replace('id="newPlayerInput"', 'id="newPlayerInputSubs"')
    after = after.replace('onclick="addSquadPlayer()"', 'onclick="addSquadPlayer(true)"')
    after = after.replace('id="squadListContainer"', 'id="squadListContainerSubs"')
    after = after.replace('id="coachNotes"', 'id="coachNotesSubs"')
    after = after.replace('id="txtManageSquadTitle"', 'id="txtManageSquadTitleSubs"')
    after = after.replace('id="txtNotesTitle"', 'id="txtNotesTitleSubs"')
    
    content = before + after

# 3. Update renderSquadManager to handle both containers
render_old = """  function renderSquadManager() {
    const container = document.getElementById('squadListContainer');
    if (!container) return;
    container.innerHTML = '';
    squadPlayers.forEach(player => {
      const chip = document.createElement('span');
      chip.className = 'player-chip';
      chip.style.cssText = 'background: #1c2230; padding: 2px 6px; border-radius: 10px; font-size: 0.65rem; display: inline-flex; align-items: center; gap: 4px; border: 1px solid #334155;';
      chip.innerHTML = `${player} <span onclick="deleteSquadPlayer('${player}')" style="color: #ef4444; cursor: pointer; font-weight: bold; padding: 0 2px;">&times;</span>`;
      container.appendChild(chip);
    });
  }"""

render_new = """  function renderSquadManager() {
    ['squadListContainer', 'squadListContainerSubs'].forEach(id => {
      const container = document.getElementById(id);
      if (!container) return;
      container.innerHTML = '';
      squadPlayers.forEach(player => {
        const chip = document.createElement('span');
        chip.className = 'player-chip';
        chip.style.cssText = 'background: #1c2230; padding: 2px 6px; border-radius: 10px; font-size: 0.65rem; display: inline-flex; align-items: center; gap: 4px; border: 1px solid #334155;';
        chip.innerHTML = `${player} <span onclick="deleteSquadPlayer('${player}')" style="color: #ef4444; cursor: pointer; font-weight: bold; padding: 0 2px;">&times;</span>`;
        container.appendChild(chip);
      });
    });
  }"""
content = content.replace(render_old, render_new)

# 4. Update addSquadPlayer to take an argument for which input to read
add_old = """  function addSquadPlayer() {
    const input = document.getElementById('newPlayerInput');
    const name = input.value.trim();
    if (!name) return;"""
    
add_new = """  function addSquadPlayer(fromSubs = false) {
    const input = document.getElementById(fromSubs ? 'newPlayerInputSubs' : 'newPlayerInput');
    if (!input) return;
    const name = input.value.trim();
    if (!name) return;"""
content = content.replace(add_old, add_new)

# 5. Fix coach notes syncing (add event listener to both and sync them)
notes_old = """  document.getElementById('coachNotes').addEventListener('input', (e) => {
    localStorage.setItem('hv_myra_notes', e.target.value);
  });
  const savedNotes = localStorage.getItem('hv_myra_notes');
  if (savedNotes) {
    document.getElementById('coachNotes').value = savedNotes;
  }"""
  
notes_new = """  function updateNotes(e) {
    localStorage.setItem('hv_myra_notes', e.target.value);
    const n1 = document.getElementById('coachNotes');
    const n2 = document.getElementById('coachNotesSubs');
    if(n1 && n1 !== e.target) n1.value = e.target.value;
    if(n2 && n2 !== e.target) n2.value = e.target.value;
  }
  const n1 = document.getElementById('coachNotes');
  const n2 = document.getElementById('coachNotesSubs');
  if(n1) n1.addEventListener('input', updateNotes);
  if(n2) n2.addEventListener('input', updateNotes);
  
  const savedNotes = localStorage.getItem('hv_myra_notes');
  if (savedNotes) {
    if(n1) n1.value = savedNotes;
    if(n2) n2.value = savedNotes;
  }"""
content = content.replace(notes_old, notes_new)

with open('index.html', 'w') as f:
    f.write(content)

print("Duplicates fixed, renderSubstitutionMatrix added to onload, and synced properly!")
