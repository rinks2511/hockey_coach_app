import re

with open('index.html', 'r') as f:
    content = f.read()

old_func = """    positionsConfig.forEach(pos => {
      const boardSelect = document.getElementById(`select_board_${pos.id}`);
      const sideSelect = document.getElementById(`select_side_${pos.id}`);
      if (boardSelect) boardSelect.value = currentAssignments[pos.id];
      if (sideSelect) sideSelect.value = currentAssignments[pos.id];
    });
  }"""
  
new_func = """    positionsConfig.forEach(pos => {
      const boardSelect = document.getElementById(`select_board_${pos.id}`);
      const sideSelect = document.getElementById(`select_side_${pos.id}`);
      if (boardSelect) boardSelect.value = currentAssignments[pos.id];
      if (sideSelect) sideSelect.value = currentAssignments[pos.id];
    });
    
    saveTacticsLocal();
    if (typeof syncMatrixFromTactics === 'function') syncMatrixFromTactics();
  }"""

if old_func in content:
    content = content.replace(old_func, new_func)
    print("Fixed onPositionChanged")
else:
    print("Could not find onPositionChanged")

with open('index.html', 'w') as f:
    f.write(content)
