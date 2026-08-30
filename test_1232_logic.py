currentAssignments = {
    'gk': 'Liz',
    'ld': 'Liv',
    'rd': 'Defne',
    'lm': 'Kyra',
    'cm': 'Mira',
    'rm': 'Alina',
    'lf': 'Kate',
    'rf': 'Sai Jiya',
    'sub_def_att': 'Hannah',
    'sub_mid': 'Shanaya'
}

subMatrixState = { p: [True]*5 for p in currentAssignments.values() }

# 0-6m is already synced: sub_def_att and sub_mid are resting
subMatrixState[currentAssignments['sub_def_att']][0] = False
subMatrixState[currentAssignments['sub_mid']][0] = False

# 6-12m: Rest LD and LM
subMatrixState[currentAssignments['ld']][1] = False
subMatrixState[currentAssignments['lm']][1] = False

# 12-18m: Rest RD and CM
subMatrixState[currentAssignments['rd']][2] = False
subMatrixState[currentAssignments['cm']][2] = False

# 18-24m: Rest LF and RM
subMatrixState[currentAssignments['lf']][3] = False
subMatrixState[currentAssignments['rm']][3] = False

# 24-30m: Rest RF and sub_mid
subMatrixState[currentAssignments['rf']][4] = False
subMatrixState[currentAssignments['sub_mid']][4] = False

print("Matrix output:")
for p, arr in subMatrixState.items():
    checks = ["✅" if v else "❌" for v in arr]
    print(f"{p:<10}: {' | '.join(checks)}")
    
# Count rest blocks per player
for p, arr in subMatrixState.items():
    rests = arr.count(False)
    print(f"{p:<10} rests: {rests}")

# Count resting players per block
for i in range(5):
    rests_in_block = sum(1 for p in subMatrixState.values() if not p[i])
    print(f"Block {i} resting players: {rests_in_block}")

