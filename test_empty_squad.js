const { JSDOM } = require("jsdom");
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const dom = new JSDOM(html, { 
  url: "http://localhost/", 
  runScripts: "dangerously" 
});
const window = dom.window;
window.localStorage.setItem('hv_myra_squad', JSON.stringify([]));

setTimeout(() => {
  try {
    const tbody = window.document.getElementById('subMatrixBody');
    console.log("tbody HTML: ", tbody ? tbody.innerHTML : "NULL");
  } catch (e) {
    console.error("Error:", e);
  }
}, 500);
