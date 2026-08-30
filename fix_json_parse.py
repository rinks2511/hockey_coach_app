import re

with open('index.html', 'r') as f:
    content = f.read()

old_squad = """  let squadLocal = JSON.parse(localStorage.getItem('hv_myra_squad'));
  let squadPlayers = (squadLocal && squadLocal.length > 0) ? squadLocal : [
    "Sai Jiya", "Defne", "Shanaya", "Alina", "Liv", "Mira", "Hannah", "Kyra", "Kate", "Liz"
  ];"""

new_squad = """  let squadLocal = null;
  try {
    const raw = localStorage.getItem('hv_myra_squad');
    if (raw) squadLocal = JSON.parse(raw);
  } catch (e) {
    console.error("Error parsing squad", e);
  }
  let squadPlayers = (squadLocal && Array.isArray(squadLocal) && squadLocal.length > 0) ? squadLocal : [
    "Sai Jiya", "Defne", "Shanaya", "Alina", "Liv", "Mira", "Hannah", "Kyra", "Kate", "Liz"
  ];"""

content = content.replace(old_squad, new_squad)

with open('index.html', 'w') as f:
    f.write(content)

print("Fixed json parse")
