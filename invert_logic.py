import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update text instructions
content = content.replace("Check the box when a player rests (on the bench).", "Check the box when a player is PLAYING (on the pitch).")
content = content.replace("Each column should have exactly 2 resting players.", "Each column should have exactly 8 active players.")
content = content.replace("Every player must rest exactly once per half.", "Every player must play exactly 4 blocks per half (24 mins).")

# 2. Update Prefill Logic
old_prefill = """        let defaultRest = [false, false, false, false, false];
        // 10 rests across 10 players (per half)
        const block = Math.floor(index / 2);
        defaultRest[block] = true;
        subMatrixState[p] = defaultRest;"""
new_prefill = """        let defaultPlay = [true, true, true, true, true];
        // Every player rests 1 block, plays 4 blocks
        const restBlock = Math.floor(index / 2);
        defaultPlay[restBlock] = false;
        subMatrixState[p] = defaultPlay;"""
content = content.replace(old_prefill, new_prefill)

# 3. Update Validation Logic
content = content.replace("const isColValid = colCounts[i] === 2;", "const isColValid = colCounts[i] === 8;")
content = content.replace("errors.push(`Block ${i+1} needs exactly 2 resting players.`);", "errors.push(`Block ${i+1} needs exactly 8 players.`);")
content = content.replace("if (count !== 1) {", "if (count !== 4) {")

with open('index.html', 'w') as f:
    f.write(content)

print("Inverted matrix to represent PLAYING instead of RESTING")
