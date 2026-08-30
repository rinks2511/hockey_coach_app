import re

with open('index.html', 'r') as f:
    content = f.read()

old_onload = """    initDropdowns();
    renderSquadManager();
    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();
    document.getElementById('googleClientIdInput').value = googleClientId;"""

new_onload = """    initDropdowns();
    renderSquadManager();
    if (typeof syncMatrixFromTactics === 'function') syncMatrixFromTactics();
    document.getElementById('googleClientIdInput').value = googleClientId;"""

if old_onload in content:
    content = content.replace(old_onload, new_onload)
    print("Fixed window.onload")
else:
    print("WARNING: Could not find old_onload")

with open('index.html', 'w') as f:
    f.write(content)

