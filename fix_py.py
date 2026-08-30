import re

with open('replace_saveload.py', 'r') as f:
    content = f.read()

content = content.replace("loadMatchData(JSON.parse(rawData));\n    }\"\"\"", "loadMatchData(JSON.parse(rawData));\n    }\n  };\"\"\"")

with open('replace_saveload.py', 'w') as f:
    f.write(content)

with open('refactor.py', 'r') as f:
    content = f.read()

content = content.replace("showToast(`Applied Horizontal ${name}`);\n  }\"\"\"", "\"\"\"")
content = content.replace("showToast(`Applied Horizontal ${name}`);\n  }", "")

with open('refactor.py', 'w') as f:
    f.write(content)
