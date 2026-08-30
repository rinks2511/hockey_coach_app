const { JSDOM } = require("jsdom");
const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

html = html.replace('resizeCanvas();', 'console.log("resizeCanvas bypassed");');

const dom = new JSDOM(html, { 
  url: "http://localhost/", 
  runScripts: "dangerously",
  resources: "usable"
});

const window = dom.window;

setTimeout(() => {
  try {
    // Simulate currentAssignments
    window.currentAssignments = {
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
    
    // Run sync
    window.syncMatrixFromTactics();
    
    // Check matrix state
    console.log("Matrix State for Hannah: ", window.subMatrixState["Hannah"][0]);
    console.log("Matrix State for Shanaya: ", window.subMatrixState["Shanaya"][0]);
    console.log("Matrix State for Liv: ", window.subMatrixState["Liv"][0]);
    console.log("Matrix State for Defne: ", window.subMatrixState["Defne"][0]);
    console.log("Matrix State for Sai Jiya: ", window.subMatrixState["Sai Jiya"][0]);
    
  } catch (e) {
    console.error("Error checking DOM:", e);
  }
}, 500);
