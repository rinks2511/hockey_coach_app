import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update positionsConfig
old_config = """  const positionsConfig = [
    { id: 'gk', default: 'Liz' },
    { id: 'lb', default: 'Liv' },
    { id: 'cb', default: 'Defne' },
    { id: 'rb', default: 'Sai Jiya' },
    { id: 'sub_def', default: 'Hannah', isSubDef: true },
    { id: 'lm', default: 'Kyra' },
    { id: 'cm', default: 'Mira' },
    { id: 'rm', default: 'Alina' },
    { id: 'sub_mid', default: 'Shanaya', isSubMid: true },
    { id: 'st', default: 'Kate' }
  ];"""

new_config = """  const positionsConfig = [
    { id: 'gk', default: 'Liz' },
    { id: 'ld', default: 'Liv' },
    { id: 'rd', default: 'Defne' },
    { id: 'lm', default: 'Kyra' },
    { id: 'cm', default: 'Mira' },
    { id: 'rm', default: 'Alina' },
    { id: 'lf', default: 'Kate' },
    { id: 'rf', default: 'Sai Jiya' },
    { id: 'sub_def_att', default: 'Hannah', isSubDef: true },
    { id: 'sub_mid', default: 'Shanaya', isSubMid: true }
  ];"""

content = content.replace(old_config, new_config)


# 2. Update renderSubstitutionMatrix grouping
old_group = """    const gk = currentAssignments['gk'];
    const defenders = [currentAssignments['lb'], currentAssignments['cb'], currentAssignments['rb'], currentAssignments['sub_def']].filter(Boolean);
    const midAtt = [currentAssignments['lm'], currentAssignments['cm'], currentAssignments['rm'], currentAssignments['st'], currentAssignments['sub_mid']].filter(Boolean);"""

new_group = """    const gk = currentAssignments['gk'];
    const defenders = [currentAssignments['ld'], currentAssignments['rd'], currentAssignments['lf'], currentAssignments['rf'], currentAssignments['sub_def_att']].filter(Boolean);
    const midAtt = [currentAssignments['lm'], currentAssignments['cm'], currentAssignments['rm'], currentAssignments['sub_mid']].filter(Boolean);"""

content = content.replace(old_group, new_group)


# 3. Update autoFillRotation logic
old_autofill = """    // 2. Define the exact players assigned to each position
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
    if (st && subMatrixState[st]) subMatrixState[st][4] = false;"""

new_autofill = """    // 2. Define the exact players assigned to each position
    const ld = currentAssignments['ld'];
    const rd = currentAssignments['rd'];
    const lf = currentAssignments['lf'];
    const rf = currentAssignments['rf'];
    const sub_def_att = currentAssignments['sub_def_att'];
    
    const lm = currentAssignments['lm'];
    const cm = currentAssignments['cm'];
    const rm = currentAssignments['rm'];
    const sub_mid = currentAssignments['sub_mid'];

    // 3. Mathematical Rotation for Rest (unchecking players)
    // 0-6m is already synced: sub_def_att and sub_mid are resting.
    
    // 6-12m: Rest LD and LM
    if (ld && subMatrixState[ld]) subMatrixState[ld][1] = false;
    if (lm && subMatrixState[lm]) subMatrixState[lm][1] = false;

    // 12-18m: Rest RD and CM
    if (rd && subMatrixState[rd]) subMatrixState[rd][2] = false;
    if (cm && subMatrixState[cm]) subMatrixState[cm][2] = false;

    // 18-24m: Rest LF and RM
    if (lf && subMatrixState[lf]) subMatrixState[lf][3] = false;
    if (rm && subMatrixState[rm]) subMatrixState[rm][3] = false;

    // 24-30m: Rest RF and sub_mid
    if (rf && subMatrixState[rf]) subMatrixState[rf][4] = false;
    if (sub_mid && subMatrixState[sub_mid]) subMatrixState[sub_mid][4] = false;"""

content = content.replace(old_autofill, new_autofill)


# 4. Update syncMatrixFromTactics
old_sync = """    for (const [posId, p] of Object.entries(currentAssignments)) {
      if (posId === 'sub_def' || posId === 'sub_mid') continue;
      if (p && subMatrixState[p]) {"""

new_sync = """    for (const [posId, p] of Object.entries(currentAssignments)) {
      if (posId === 'sub_def_att' || posId === 'sub_mid') continue;
      if (p && subMatrixState[p]) {"""

content = content.replace(old_sync, new_sync)

with open('index.html', 'w') as f:
    f.write(content)

print("Updated positions, grouping, autofill, and sync logic.")
