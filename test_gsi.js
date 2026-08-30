const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    // Capture console logs
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    
    console.log("Navigating to http://localhost:8080...");
    await page.goto('http://localhost:8080', { waitUntil: 'networkidle0' });
    
    // Check if the overlay is visible
    const overlayDisplay = await page.$eval('#googleAuthSetupOverlay', el => el.style.display);
    console.log("Overlay display:", overlayDisplay);
    
    // Click the sign in button if possible
    console.log("Waiting for GSI to initialize...");
    await new Promise(r => setTimeout(r, 2000)); // wait for GSI script to load and init
    
    await browser.close();
  } catch(e) {
    console.error("Puppeteer error:", e);
  }
})();
