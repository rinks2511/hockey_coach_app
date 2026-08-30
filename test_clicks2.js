const { JSDOM } = require("jsdom");
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const dom = new JSDOM(html, { 
  url: "http://localhost/", 
  runScripts: "dangerously" 
});
const window = dom.window;
window.HTMLCanvasElement.prototype.getContext = function () {
  return {
    clearRect: function(){},
    beginPath: function(){},
    arc: function(){},
    fill: function(){},
    stroke: function(){},
    drawImage: function(){},
    fillText: function(){},
    strokeText: function(){},
    moveTo: function(){},
    lineTo: function(){},
    setLineDash: function(){},
    measureText: function(){ return {width: 10}; }
  };
};

setTimeout(() => {
  try {
    const tbody = window.document.getElementById('subMatrixBody');
    console.log("Matrix rows: ", tbody ? tbody.querySelectorAll('tr').length : "NULL");
    const container = window.document.getElementById('squadListContainer');
    console.log("Squad pills: ", container ? container.querySelectorAll('span').length : "NULL");
  } catch (e) {
    console.error("Error:", e);
  }
}, 500);
