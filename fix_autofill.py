import re

with open('index.html', 'r') as f:
    content = f.read()

auto_fill_old = """  function autoFillRotation() {
    // 1. Reset everything EXCEPT 0-6m and GK
    const gkPlayer = currentAssignments['gk'];
    squadPlayers.forEach(p => {
      if (!subMatrixState[p]) subMatrixState[p] = [false, false, false, false, false];
      if (p !== gkPlayer) {
         for(let i=1; i<5; i++) subMatrixState[p][i] = false;
      }
    });
    
    // 2. Identify the field players
    const fieldPlayers = squadPlayers.filter(p => p !== gkPlayer);
    
    // 3. We need 7 field players per block (blocks 1, 2, 3, 4).
    // We already have block 0 set by the tactics board.
    // Total blocks to fill = 7 spots * 4 blocks = 28 spots.
    // We want to distribute them evenly among the field players.
    
    // Let's just track how many blocks each player has played so far
    const playedCounts = {};
    fieldPlayers.forEach(p => {
      playedCounts[p] = subMatrixState[p][0] ? 1 : 0;
    });
    
    for (let blockIndex = 1; blockIndex < 5; blockIndex++) {
      // Sort players by least played to prioritize them for this block
      fieldPlayers.sort((a, b) => playedCounts[a] - playedCounts[b]);
      
      // Select the first 7 players
      for (let i = 0; i < 7; i++) {
        const p = fieldPlayers[i];
        if (p) {
          subMatrixState[p][blockIndex] = true;
          playedCounts[p]++;
        }
      }
    }
    
    renderSubstitutionMatrix();
    showToast('Rotation Auto-Filled!');
  }"""

auto_fill_new = """  function autoFillRotation() {
    // 1. Reset everything EXCEPT 0-6m and GK
    const gkPlayer = currentAssignments['gk'];
    squadPlayers.forEach(p => {
      if (!subMatrixState[p]) subMatrixState[p] = [false, false, false, false, false];
      if (p !== gkPlayer) {
         for(let i=1; i<5; i++) subMatrixState[p][i] = true; // Default everyone to PLAYING
      }
    });

    // 2. Define the exact players assigned to each position
    const lb = currentAssignments['lb'];
    const cb = currentAssignments['cb'];
    const rb = currentAssignments['rb'];
    const sub_def = currentAssignments['sub_def'];
    const lm = currentAssignments['lm'];
    const cm = currentAssignments['cm'];
    const rm = currentAssignments['rm'];
    const st = currentAssignments['st'];
    const sub_mid = currentAssignments['sub_mid'];

    // 3. Mathematical Rotation for Rest (unchecking players)
    // 0-6m is already synced: sub_def and sub_mid are resting.
    
    // 6-12m: Rest LB and LM
    if (lb && subMatrixState[lb]) subMatrixState[lb][1] = false;
    if (lm && subMatrixState[lm]) subMatrixState[lm][1] = false;

    // 12-18m: Rest CB and CM
    if (cb && subMatrixState[cb]) subMatrixState[cb][2] = false;
    if (cm && subMatrixState[cm]) subMatrixState[cm][2] = false;

    // 18-24m: Rest RB and RM
    if (rb && subMatrixState[rb]) subMatrixState[rb][3] = false;
    if (rm && subMatrixState[rm]) subMatrixState[rm][3] = false;

    // 24-30m: Rest sub_def (again) and ST
    if (sub_def && subMatrixState[sub_def]) subMatrixState[sub_def][4] = false;
    if (st && subMatrixState[st]) subMatrixState[st][4] = false;

    renderSubstitutionMatrix();
    showToast('Rotation Auto-Filled!');
  }"""

if auto_fill_old in content:
    content = content.replace(auto_fill_old, auto_fill_new)
    print("Fixed autoFillRotation")
else:
    print("WARNING: Could not find autoFillRotation")

with open('index.html', 'w') as f:
    f.write(content)

