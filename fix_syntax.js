const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldSquad = `let squadPlayers = JSON.parse(localStorage.getItem('hv_myra_squad')) || [
    "Sai Jiya", "Defne", "Shanaya", "Alina", "Liv", "Mira", "Hannah", "Kyra", "Kate", "Liz"
  ];`;

html = html.replace(oldSquad, '');

fs.writeFileSync('index.html', html);
console.log("Fixed syntax");
