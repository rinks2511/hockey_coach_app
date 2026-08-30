import re

with open('index.html', 'r') as f:
    content = f.read()

old_sync = """    // Then, set the 0-6m block for everyone on the pitch
    const gkPlayer = currentAssignments['gk'];
    Object.values(currentAssignments).forEach(p => {
      if (p && subMatrixState[p]) {
        subMatrixState[p][0] = true;
      }
    });"""
    
new_sync = """    // Then, set the 0-6m block for everyone on the pitch (excluding subs)
    const gkPlayer = currentAssignments['gk'];
    for (const [posId, p] of Object.entries(currentAssignments)) {
      if (posId === 'sub_def' || posId === 'sub_mid') continue;
      if (p && subMatrixState[p]) {
        subMatrixState[p][0] = true;
      }
    }"""

if old_sync in content:
    content = content.replace(old_sync, new_sync)
    print("Fixed syncMatrixFromTactics")
else:
    print("Could not find sync block")

with open('index.html', 'w') as f:
    f.write(content)
