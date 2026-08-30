import re

with open('index.html', 'r') as f:
    content = f.read()

old_init = """    // Initialize new players in state
    squadPlayers.forEach(p => {
      if (!subMatrixState[p]) subMatrixState[p] = [false, false, false];
    });"""

new_init = """    // Initialize new players in state with default prefill
    squadPlayers.forEach((p, index) => {
      if (!subMatrixState[p]) {
        let defaultRest = [false, false, false];
        if (index === 0 || index === 1) defaultRest[0] = true;
        if (index === 2 || index === 3) defaultRest[1] = true;
        if (index === 4 || index === 5) defaultRest[2] = true;
        subMatrixState[p] = defaultRest;
      }
    });"""

content = content.replace(old_init, new_init)

with open('index.html', 'w') as f:
    f.write(content)

print("Prefilled matrix")
