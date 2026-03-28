const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const screenshotsDir = path.join(__dirname, 'screenshots');
const outputDir = path.join(screenshotsDir, 'png');

const files = [
  { html: 'ss1_home.html',          png: 'screenshot_1_home.png' },
  { html: 'ss2_songbook.html',      png: 'screenshot_2_songbook.png' },
  { html: 'ss3_song_detail.html',   png: 'screenshot_3_song_detail.png' },
  { html: 'ss4_bible.html',         png: 'screenshot_4_bible.png' },
  { html: 'ss5_bible_reading.html', png: 'screenshot_5_bible_reading.png' },
];

(async () => {
  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  for (const { html, png } of files) {
    const page = await browser.newPage();

    // Set viewport to exact screenshot dimensions (9:16 portrait)
    await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });

    const filePath = path.join(screenshotsDir, html);
    const fileUrl = 'file:///' + filePath.replace(/\\/g, '/');

    console.log(`Rendering ${html} ...`);
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

    // Wait a bit for fonts to load
    await new Promise(r => setTimeout(r, 2000));

    const outPath = path.join(outputDir, png);
    await page.screenshot({
      path: outPath,
      type: 'png',
      clip: { x: 0, y: 0, width: 1080, height: 1920 },
    });

    console.log(`  -> Saved ${outPath}`);
    await page.close();
  }

  await browser.close();
  console.log('\nDone! All screenshots saved to: ' + outputDir);
})();

