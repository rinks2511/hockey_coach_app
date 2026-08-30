import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix 1: Add syncMatrixFromTactics() to the end of onPositionChanged()
old_on_pos = """    // Update local storage
    saveTacticsLocal();
  }"""
new_on_pos = """    // Update local storage
    saveTacticsLocal();
    if (typeof syncMatrixFromTactics === 'function') syncMatrixFromTactics();
  }"""
if old_on_pos in content:
    content = content.replace(old_on_pos, new_on_pos)
    print("Fixed onPositionChanged")
else:
    print("Could not find onPositionChanged")

# Fix 2: Add syncMatrixFromTactics() to the end of loadTacticsLocal()
old_load = """    initDropdowns();
    syncBanner();
    showToast('Setup Loaded!');
  }"""
new_load = """    initDropdowns();
    syncBanner();
    showToast('Setup Loaded!');
    if (typeof syncMatrixFromTactics === 'function') syncMatrixFromTactics();
  }"""
if old_load in content:
    content = content.replace(old_load, new_load)
    print("Fixed loadTacticsLocal")
else:
    print("Could not find loadTacticsLocal")

with open('index.html', 'w') as f:
    f.write(content)

