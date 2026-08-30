const { JSDOM } = require("jsdom");
const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Bypass resizeCanvas crash for JSDOM
html = html.replace('resizeCanvas();', 'console.log("resizeCanvas bypassed");');

const dom = new JSDOM(html, { 
  url: "http://localhost/", 
  runScripts: "dangerously",
  resources: "usable"
});

const window = dom.window;

setTimeout(() => {
  try {
    const tbody = window.document.getElementById('subMatrixBody');
    console.log("Matrix rows: ", tbody ? tbody.querySelectorAll('tr').length : "NULL");
    
    const container1 = window.document.getElementById('squadListContainer');
    console.log("Squad pills (Tactics): ", container1 ? container1.querySelectorAll('span').length : "NULL");

    const container2 = window.document.getElementById('squadListContainerSubs');
    console.log("Squad pills (Subs): ", container2 ? container2.querySelectorAll('span').length : "NULL");

  } catch (e) {
    console.error("Error checking DOM:", e);
  }
}, 500);
