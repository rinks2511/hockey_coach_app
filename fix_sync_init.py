import re

with open('index.html', 'r') as f:
    content = f.read()

old_sync = """  function syncMatrixFromTactics() {
    if (typeof subMatrixState === 'undefined') return;
    
    // First, clear the 0-6m block for everyone
    Object.keys(subMatrixState).forEach(p => subMatrixState[p][0] = false);"""

new_sync = """  function syncMatrixFromTactics() {
    if (typeof subMatrixState === 'undefined') return;
    
    // Initialize state for squad players if missing
    if (typeof squadPlayers !== 'undefined') {
      squadPlayers.forEach(p => {
        if (!subMatrixState[p]) {
          subMatrixState[p] = [true, true, true, true, true];
        }
      });
    }

    // First, clear the 0-6m block for everyone
    Object.keys(subMatrixState).forEach(p => subMatrixState[p][0] = false);"""

if old_sync in content:
    content = content.replace(old_sync, new_sync)
    print("Fixed syncMatrixFromTactics init")
else:
    print("WARNING: Could not find old_sync block")

with open('index.html', 'w') as f:
    f.write(content)

