const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true
  });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://www.artillery.io/');
  await page.getByLabel('Main navigation').getByRole('link', { name: 'Documentation' }).click();
  await page.getByRole('link', { name: 'Run Your First Test', exact: true }).click();
  await page.getByRole('link', { name: 'Integrations' }).click();
  await page.getByRole('link', { name: 'Artillery Artillery Docs' }).click();

  // ---------------------
  await context.close();
  await browser.close();
})();
