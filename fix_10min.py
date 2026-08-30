import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update HTML Sidebar UI Text
content = content.replace("Substitution Planner (6-Min Blocks)", "Substitution Planner (10-Min Blocks)")
content = content.replace("<th>0-6m</th>\n              <th>6-12m</th>\n              <th>12-18m</th>\n              <th>18-24m</th>\n              <th>24-30m</th>", "<th>0-10m</th>\n              <th>10-20m</th>\n              <th>20-30m</th>")

# 2. Update JS Array length (5 -> 3)
content = content.replace("subMatrixState[p] = [false, false, false, false, false]", "subMatrixState[p] = [false, false, false]")
content = content.replace("for (let i = 0; i < 5; i++) {", "for (let i = 0; i < 3; i++) {")
content = content.replace("const colCounts = [0, 0, 0, 0, 0];", "const colCounts = [0, 0, 0];")

# 3. Update JS row validation text
content = content.replace("count !== 1", "count > 1") # Allowing 0 rests per half is fine now. Warn if they rest >1 time in a single half.
content = content.replace("Each player should rest exactly once for equal time.", "Players shouldn't rest twice in the same half.")

with open('index.html', 'w') as f:
    f.write(content)

print("Changed to 10min")
