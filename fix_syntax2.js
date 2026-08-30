const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Fix the else else syntax error
html = html.replace(/\s*\} else \{\n\s*\/\/ If we did load, maybe we shouldn't overwrite. But wait, local load is done manually via loadTacticsLocal\(\)\n\s*\/\/ Let's just apply it by default so it looks right on fresh load\n\s*applyFormation\('1-2-3-2'\);\n\s*\}/g, '');

fs.writeFileSync('index.html', html);
console.log("Else block fixed.");
