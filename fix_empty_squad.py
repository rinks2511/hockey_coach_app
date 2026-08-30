import re

with open('index.html', 'r') as f:
    content = f.read()

old_init = """  let squadPlayers = JSON.parse(localStorage.getItem('hv_myra_squad')) || [
    "Sai Jiya", "Defne", "Shanaya", "Alina", "Liv", "Mira", "Hannah", "Kyra", "Kate", "Liz"
  ];"""

new_init = """  let squadLocal = JSON.parse(localStorage.getItem('hv_myra_squad'));
  let squadPlayers = (squadLocal && squadLocal.length > 0) ? squadLocal : [
    "Sai Jiya", "Defne", "Shanaya", "Alina", "Liv", "Mira", "Hannah", "Kyra", "Kate", "Liz"
  ];"""

content = content.replace(old_init, new_init)

with open('index.html', 'w') as f:
    f.write(content)

print("Fixed squad fallback logic")
