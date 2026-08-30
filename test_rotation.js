const { JSDOM } = require("jsdom");
const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
// Bypass canvas error in JSDOM
html = html.replace('resizeCanvas();', 'console.log("resizeCanvas bypassed");');

const dom = new JSDOM(html, { 
  url: "http://localhost/", 
  runScripts: "dangerously",
  resources: "usable"
});

const window = dom.window;

setTimeout(() => {
  try {
    const w = window;
    
    // 1. Add players to squad
    w.squadPlayers = ["Liz", "Liv", "Defne", "Sai Jiya", "Hannah", "Kyra", "Mira", "Alina", "Shanaya", "Kate"];
    w.squadPlayers.forEach(p => {
       w.subMatrixState[p] = [false, false, false, false, false];
    });

    // 2. Assign positions
    w.currentAssignments = {
      gk: "Liz",
      lb: "Liv",
      cb: "Defne",
      rb: "Sai Jiya",
      sub_def: "Hannah",
      lm: "Kyra",
      cm: "Mira",
      rm: "Alina",
      sub_mid: "Shanaya",
      st: "Kate"
    };
    
    // 3. Sync from Tactics
    if (typeof w.syncMatrixFromTactics === 'function') {
      w.syncMatrixFromTactics();
    } else {
      console.log("syncMatrixFromTactics not found");
    }
    
    // 4. Run Auto Fill
    if (typeof w.autoFillRotation === 'function') {
      w.autoFillRotation();
    } else {
      console.log("autoFillRotation not found");
    }

    // 5. Output the results
    console.log("--- RESULTS FOR AUTOFILL ---");
    w.squadPlayers.forEach(p => {
      const state = w.subMatrixState[p].map(b => b ? "✅" : "❌").join(" | ");
      console.log(`${p.padEnd(10)}: ${state}`);
    });
    
    console.log("\n--- DOM TABLE ---");
    const tbody = w.document.getElementById('subMatrixBody');
    if (tbody) {
      const rows = tbody.querySelectorAll('tr');
      rows.forEach(tr => {
         const nameTd = tr.querySelector('td').textContent;
         console.log(nameTd);
      });
    }

  } catch (e) {
    console.error("Test Failed:", e);
  }
}, 500);
