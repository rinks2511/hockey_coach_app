import re

with open('index.html', 'r') as f:
    content = f.read()

old_validation = """    let badRows = false;
    rows.forEach(tr => {
      const player = tr.querySelector('td').innerText;
      const count = subMatrixState[player] ? subMatrixState[player].filter(Boolean).length : 0;
      if (count !== 4) {
        tr.classList.add('invalid-row');
        badRows = true;
        isValid = false;
      } else {
        tr.classList.remove('invalid-row');
      }
    });
    if (badRows) errors.push('Every player must play exactly 4 blocks per half (24 mins).');"""

new_validation = """    // Row validation is relaxed because mathematically:
    // - GK plays 5 blocks
    // - 4 Defenders sharing 3 spots over 5 blocks means someone must play 3 blocks
    // - 5 Attackers sharing 4 spots over 5 blocks means everyone plays 4 blocks
    // We just ensure they don't play 0 blocks
    rows.forEach(tr => {
      const player = tr.querySelector('td').innerText;
      const count = subMatrixState[player] ? subMatrixState[player].filter(Boolean).length : 0;
      if (count === 0) {
        tr.classList.add('invalid-row');
        isValid = false;
        errors.push(`Player ${player} is playing 0 blocks.`);
      } else {
        tr.classList.remove('invalid-row');
      }
    });"""

if old_validation in content:
    content = content.replace(old_validation, new_validation)
    print("Fixed validation")
else:
    print("WARNING: Could not find old_validation")

with open('index.html', 'w') as f:
    f.write(content)

