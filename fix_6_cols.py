import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update HTML Sidebar UI Text
content = content.replace("<th>0-10m</th>\n              <th>10-20m</th>\n              <th>20-30m</th>", "<th>H1: 0-10m</th>\n              <th>H1: 10-20m</th>\n              <th>H1: 20-30m</th>\n              <th>H2: 0-10m</th>\n              <th>H2: 10-20m</th>\n              <th>H2: 20-30m</th>")
content = content.replace("Substitution Planner (10-Min Blocks)", "Substitution Planner (Full Match)")

# 2. Update JS Array length (3 -> 6)
content = content.replace("subMatrixState[p] = [false, false, false]", "subMatrixState[p] = [false, false, false, false, false, false]")
content = content.replace("for (let i = 0; i < 3; i++) {", "for (let i = 0; i < 6; i++) {")
content = content.replace("const colCounts = [0, 0, 0];", "const colCounts = [0, 0, 0, 0, 0, 0];")

# 3. Update Prefill logic
old_prefill = """        let defaultRest = [false, false, false];
        if (index === 0 || index === 1) defaultRest[0] = true;
        if (index === 2 || index === 3) defaultRest[1] = true;
        if (index === 4 || index === 5) defaultRest[2] = true;"""
new_prefill = """        let defaultRest = [false, false, false, false, false, false];
        // 12 rests across 10 players. 
        if (index === 0) { defaultRest[0] = true; defaultRest[3] = true; }
        else if (index === 1) { defaultRest[0] = true; defaultRest[4] = true; }
        else if (index === 2) { defaultRest[1] = true; }
        else if (index === 3) { defaultRest[1] = true; }
        else if (index === 4) { defaultRest[2] = true; }
        else if (index === 5) { defaultRest[2] = true; }
        else if (index === 6) { defaultRest[3] = true; }
        else if (index === 7) { defaultRest[4] = true; }
        else if (index === 8) { defaultRest[5] = true; }
        else if (index === 9) { defaultRest[5] = true; }"""
content = content.replace(old_prefill, new_prefill)

# 4. Update JS row validation text
# The rule: Every player should rest 1 or 2 times. If > 2, warn. If < 1, warn.
old_row_check = """      const count = subMatrixState[player] ? subMatrixState[player].filter(Boolean).length : 0;
      if (count > 1) {
        tr.classList.add('invalid-row');
        badRows = true;
        isValid = false;
      } else {
        tr.classList.remove('invalid-row');
      }"""
new_row_check = """      const count = subMatrixState[player] ? subMatrixState[player].filter(Boolean).length : 0;
      if (count < 1 || count > 2) {
        tr.classList.add('invalid-row');
        badRows = true;
        isValid = false;
      } else {
        tr.classList.remove('invalid-row');
      }"""
content = content.replace(old_row_check, new_row_check)
content = content.replace("Players shouldn't rest twice in the same half.", "Players should rest 1 or 2 times per match.")

with open('index.html', 'w') as f:
    f.write(content)

print("Expanded to 6 columns")
