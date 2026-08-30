import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update HTML Sidebar UI Text
old_th = """<th>H1: 0-10m</th>
              <th>H1: 10-20m</th>
              <th>H1: 20-30m</th>
              <th>H2: 0-10m</th>
              <th>H2: 10-20m</th>
              <th>H2: 20-30m</th>"""
new_th = """<th>H1: 0-6m</th>
              <th>H1: 6-12m</th>
              <th>H1: 12-18m</th>
              <th>H1: 18-24m</th>
              <th>H1: 24-30m</th>
              <th>H2: 0-6m</th>
              <th>H2: 6-12m</th>
              <th>H2: 12-18m</th>
              <th>H2: 18-24m</th>
              <th>H2: 24-30m</th>"""
content = content.replace(old_th, new_th)
content = content.replace("Substitution Planner (Full Match)", "Substitution Planner (Full Match, 6-Min Blocks)")

# 2. Update JS Array lengths
content = content.replace("[false, false, false, false, false, false]", "[false, false, false, false, false, false, false, false, false, false]")
content = content.replace("for (let i = 0; i < 6; i++) {", "for (let i = 0; i < 10; i++) {")
content = content.replace("const colCounts = [0, 0, 0, 0, 0, 0];", "const colCounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];")

# 3. Update Prefill logic
old_prefill = """        // 12 rests across 10 players. 
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
new_prefill = """        // 20 rests across 10 players. Each rests twice perfectly.
        const half1Rest = Math.floor(index / 2);
        const half2Rest = half1Rest + 5;
        defaultRest[half1Rest] = true;
        defaultRest[half2Rest] = true;"""
content = content.replace(old_prefill, new_prefill)

# 4. Update JS row validation text
old_row_check = """      if (count < 1 || count > 2) {"""
new_row_check = """      if (count !== 2) {"""
content = content.replace(old_row_check, new_row_check)
content = content.replace("Players should rest 1 or 2 times per match.", "Every player must rest exactly twice (once per half) for equal playtime.")

# Need to update the first prefill initialization too, the one that used to be length 3, then 6. Wait I replaced the explicit array above.
with open('index.html', 'w') as f:
    f.write(content)

print("Expanded to 10 columns (6min blocks)")
