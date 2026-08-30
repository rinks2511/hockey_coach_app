import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix renderSubstitutionMatrix
if "const gk = currentAssignments['gk'];" in content:
    # Use regex to find the block
    pattern = r"const gk = currentAssignments\['gk'\];.*?const midAtt = \[.*?\]\.filter\(Boolean\);"
    replacement = """const gk = currentAssignments['gk'];
    const defenders = [currentAssignments['ld'], currentAssignments['rd'], currentAssignments['lf'], currentAssignments['rf'], currentAssignments['sub_def_att']].filter(Boolean);
    const midAtt = [currentAssignments['lm'], currentAssignments['cm'], currentAssignments['rm'], currentAssignments['sub_mid']].filter(Boolean);"""
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    print("Fixed renderSubstitutionMatrix grouping")

# Fix autoFillRotation
if "const lb = currentAssignments['lb'];" in content:
    pattern_autofill = r"const lb = currentAssignments\['lb'\];.*?if \(st && subMatrixState\[st\]\) subMatrixState\[st\]\[4\] = false;"
    replacement_autofill = """const ld = currentAssignments['ld'];
    const rd = currentAssignments['rd'];
    const lf = currentAssignments['lf'];
    const rf = currentAssignments['rf'];
    const sub_def_att = currentAssignments['sub_def_att'];
    
    const lm = currentAssignments['lm'];
    const cm = currentAssignments['cm'];
    const rm = currentAssignments['rm'];
    const sub_mid = currentAssignments['sub_mid'];

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
    
    content = re.sub(pattern_autofill, replacement_autofill, content, flags=re.DOTALL)
    print("Fixed autoFillRotation logic")

with open('index.html', 'w') as f:
    f.write(content)
