import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update HTML
old_th = """<th>H1: 0-6m</th>
              <th>H1: 6-12m</th>
              <th>H1: 12-18m</th>
              <th>H1: 18-24m</th>
              <th>H1: 24-30m</th>
              <th>H2: 0-6m</th>
              <th>H2: 6-12m</th>
              <th>H2: 12-18m</th>
              <th>H2: 18-24m</th>
              <th>H2: 24-30m</th>"""
new_th = """<th>0-6m</th>
              <th>6-12m</th>
              <th>12-18m</th>
              <th>18-24m</th>
              <th>24-30m</th>"""
content = content.replace(old_th, new_th)
content = content.replace("Substitution Planner (Full Match, 6-Min Blocks)", "Substitution Planner (6-Min Blocks, per Half)")

# 2. Update JS Array lengths
content = content.replace("[false, false, false, false, false, false, false, false, false, false]", "[false, false, false, false, false]")
content = content.replace("for (let i = 0; i < 10; i++) {", "for (let i = 0; i < 5; i++) {")
content = content.replace("const colCounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];", "const colCounts = [0, 0, 0, 0, 0];")

# 3. Update Prefill logic
old_prefill = """        // 20 rests across 10 players. Each rests twice perfectly.
        const half1Rest = Math.floor(index / 2);
        const half2Rest = half1Rest + 5;
        defaultRest[half1Rest] = true;
        defaultRest[half2Rest] = true;"""
new_prefill = """        // 10 rests across 10 players (per half)
        const block = Math.floor(index / 2);
        defaultRest[block] = true;"""
content = content.replace(old_prefill, new_prefill)

# 4. Update JS row validation text
old_row_check = """      if (count !== 2) {"""
new_row_check = """      if (count !== 1) {"""
content = content.replace(old_row_check, new_row_check)
content = content.replace("Every player must rest exactly twice (once per half) for equal playtime.", "Every player must rest exactly once per half.")

with open('index.html', 'w') as f:
    f.write(content)

print("Reverted to 5 columns")
