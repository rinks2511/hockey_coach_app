const { JSDOM } = require("jsdom");
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });
const window = dom.window;

// Simulate clicks
try {
  window.applyFormation('1-2-4-1');
  console.log("Success: 1-2-4-1");
  window.applyFormation('1-3-3-1');
  console.log("Success: 1-3-3-1");
} catch (e) {
  console.error("Error in applyFormation:", e);
}

try {
  window.setLanguage('nl');
  console.log("Success: setLanguage nl");
} catch(e) {
  console.error("Error in setLanguage:", e);
}
