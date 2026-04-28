const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const { themes, themeToCssVars } = require('./themes');
const { renderAllPages } = require('./pages/index');

async function build() {
  const theme = themes['au-dealer-math'];
  const css = fs.readFileSync(path.join(__dirname, 'base.css'), 'utf-8');

  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&family=Inter:wght@300;400;500;700&family=Fraunces:opsz,wght@9..144,400;9..144,700&display=swap" rel="stylesheet">
        <style>
          :root {
            ${themeToCssVars(theme)}
          }
          ${css}
        </style>
      </head>
      <body>
        ${renderAllPages(theme)}
      </body>
    </html>
  `;

  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');

  const outDir = path.join(__dirname, 'output');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const outPath = path.join(outDir, 'au-dealer-math-7-lines.pdf');
  await page.pdf({
    path: outPath,
    format: 'A4',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });

  await browser.close();
  console.log(`PDF built: ${outPath}`);
}

build().catch(err => {
  console.error(err);
  process.exit(1);
});
