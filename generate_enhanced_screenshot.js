const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const screenshotsDir = path.join(__dirname, 'screenshots');
const outputDir = path.join(screenshotsDir, 'png');

// Generate the enhanced graphical Bible screenshot with mockup
const enhancedFile = {
  html: 'mockup_bible.html',
  png: 'mockup_bible_screenshot.png'
};

(async () => {
  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();

  // Set viewport for mockup dimensions
  await page.setViewport({ width: 1200, height: 2000, deviceScaleFactor: 1 });

  const filePath = path.join(screenshotsDir, enhancedFile.html);
  const fileUrl = 'file:///' + filePath.replace(/\\/g, '/');

  console.log(`Rendering enhanced Bible mockup: ${enhancedFile.html} ...`);
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for fonts and animations to load
  await new Promise(r => setTimeout(r, 3000));

  const outPath = path.join(outputDir, enhancedFile.png);
  await page.screenshot({
    path: outPath,
    type: 'png',
    clip: { x: 0, y: 0, width: 1200, height: 2000 },
  });

  console.log(`  -> Saved mockup screenshot: ${outPath}`);
  await page.close();
  await browser.close();

  console.log('\nPhone mockup Bible screenshot generated!');
  console.log('Features:');
  console.log('• Realistic iPhone-style phone frame');
  console.log('• Premium gradients and shadows');
  console.log('• Marketing text overlay with feature badges');
  console.log('• Enhanced typography with Playfair Display');
  console.log('• Professional device mockup presentation');
  console.log('• Perfect for app store marketing');
})();





