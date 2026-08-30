import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update saveTacticsLocal
save_old = """    const data = {
      assignments: currentAssignments,
      matchDate: document.getElementById('matchDatePicker').value,
      matchOpponent: document.getElementById('matchOpponent').value,
      matchHalf: document.getElementById('matchHalf').value,
      notes: document.getElementById('coachNotes').value,
      drawings: drawnObjects,
      tokenPositions: tokenPositions
    };"""

save_new = """    const data = {
      assignments: currentAssignments,
      matchDate: document.getElementById('matchDatePicker').value,
      matchOpponent: document.getElementById('matchOpponent').value,
      matchHalf: document.getElementById('matchHalf').value,
      notes: document.getElementById('coachNotes').value,
      drawings: drawnObjects,
      tokenPositions: tokenPositions,
      subMatrixState: subMatrixState
    };"""

content = content.replace(save_old, save_new)

# 2. Update loadTacticsLocal
load_old = """    if (data.notes) document.getElementById('coachNotes').value = data.notes;
    if (data.drawings) {
      drawnObjects = data.drawings;
      redrawCanvas();
    }"""

load_new = """    if (data.notes) document.getElementById('coachNotes').value = data.notes;
    if (data.subMatrixState) {
      subMatrixState = data.subMatrixState;
      renderSubstitutionMatrix();
    }
    if (data.drawings) {
      drawnObjects = data.drawings;
      redrawCanvas();
    }"""

content = content.replace(load_old, load_new)

with open('index.html', 'w') as f:
    f.write(content)

print("Added save state")
