const currentAssignments = {
    gk: 'Liz',
    lb: 'Liv',
    cb: 'Defne',
    rb: 'Sai Jiya',
    sub_def: 'Hannah',
    lm: 'Kyra',
    cm: 'Mira',
    rm: 'Alina',
    sub_mid: 'Shanaya',
    st: 'Kate'
};
const subMatrixState = {};
const squadPlayers = ['Liz', 'Liv', 'Defne', 'Sai Jiya', 'Hannah', 'Kyra', 'Mira', 'Alina', 'Shanaya', 'Kate'];

if (typeof squadPlayers !== 'undefined') {
  squadPlayers.forEach(p => {
    if (!subMatrixState[p]) {
      subMatrixState[p] = [true, true, true, true, true];
    }
  });
}

Object.keys(subMatrixState).forEach(p => subMatrixState[p][0] = false);

const gkPlayer = currentAssignments['gk'];
for (const [posId, p] of Object.entries(currentAssignments)) {
  if (posId === 'sub_def' || posId === 'sub_mid') continue;
  if (p && subMatrixState[p]) {
    subMatrixState[p][0] = true;
  }
}

console.log(subMatrixState);
