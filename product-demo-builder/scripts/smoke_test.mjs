#!/usr/bin/env node
/** Optional browser smoke test. It reports a clear skip when Playwright is unavailable. */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const htmlPath = process.argv[2];
if (!htmlPath) {
  console.error('Usage: node smoke_test.mjs <index.html>');
  process.exit(2);
}

let playwright;
try {
  playwright = await import('playwright');
} catch {
  console.log(JSON.stringify({ status: 'skipped', reason: 'Playwright is not installed' }, null, 2));
  process.exit(0);
}

const browser = await playwright.chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const errors = [];
page.on('pageerror', (error) => errors.push(error.message));
await page.goto(pathToFileURL(path.resolve(htmlPath)).href);

const checks = [];
async function check(name, fn) {
  try { await fn(); checks.push({ name, passed: true }); }
  catch (error) { checks.push({ name, passed: false, error: error.message }); }
}

async function reloadHome(viewport = { width: 1440, height: 1000 }) {
  await page.setViewportSize(viewport);
  await page.reload();
  await page.locator('[data-screen="share"]').waitFor();
}

await check('initial share screen', async () => page.locator('[data-screen="share"]').waitFor());
await check('main sharing flow', async () => {
  await reloadHome();
  await page.locator('[data-action="select-user"]').first().click();
  await page.locator('[role="dialog"]').waitFor();
  await page.locator('[data-action="confirm-share"]').click();
  await page.locator('.toast', { hasText: '分享成功' }).waitFor();
  await page.locator('[data-screen="share"]').waitFor();
});
await check('account input flow', async () => {
  await reloadHome();
  await page.locator('[data-action="open-account"]').click();
  await page.locator('#account-input').fill('demo-user@example.invalid');
  await page.locator('[data-action="lookup-user"]').click();
  await page.locator('[role="dialog"]').waitFor();
  await page.locator('[data-action="confirm-share"]').click();
  await page.locator('.toast', { hasText: '分享成功' }).waitFor();
});
await check('loading failure and empty states', async () => {
  await reloadHome();
  await page.locator('[data-action="open-qr"]').click();
  await page.locator('[data-target="qr-stage"]').first().click();
  await page.locator('[data-screen="qr"][data-state="loading"]').waitFor();
  await page.locator('[data-screen="qr"][data-state="normal"]').waitFor({ timeout: 3000 });
  await page.locator('[data-action="back"]').click();
  await page.locator('[data-control="qr"][data-value="failed"]').click();
  await page.locator('[data-screen="share"][data-state="failed"]').waitFor();
  await page.locator('[data-control="recent"][data-value="empty"]').click();
  await page.locator('.empty', { hasText: '暂无最近联系人' }).waitFor();
});
await check('modal confirm and cancel', async () => {
  await reloadHome();
  await page.locator('[data-action="select-user"]').first().click();
  await page.locator('[data-action="close-modal"]').click();
  if (await page.locator('[role="dialog"]').count()) throw new Error('dialog remained after cancel');
  await page.locator('[data-action="clear-recent"]').click();
  await page.locator('[data-action="confirm-clear"]').click();
  await page.locator('.toast', { hasText: '最近联系人已清空' }).waitFor();
  await page.locator('.empty', { hasText: '暂无最近联系人' }).waitFor();
});
await check('back reset and list operations', async () => {
  await reloadHome();
  await page.locator('[data-action="open-account"]').click();
  await page.locator('[data-action="back"]').click();
  await page.locator('[data-screen="share"]').waitFor();
  await page.locator('[data-action="open-manage"]').click();
  const before = await page.locator('[data-action="delete-contact"]').count();
  if (before < 1) throw new Error('member list has no removable item');
  await page.locator('[data-action="delete-contact"]').first().click();
  await page.locator('[data-action="confirm-delete"]').click();
  await page.locator('.toast', { hasText: '成员已移除' }).waitFor();
  const after = await page.locator('[data-action="delete-contact"]').count();
  if (after !== before - 1) throw new Error(`member count did not decrease: ${before} -> ${after}`);
  await page.locator('[data-action="reset"]').click();
  await page.locator('[data-screen="share"][data-state="normal"]').waitFor();
});
await check('small-screen phone stage', async () => {
  await reloadHome({ width: 390, height: 844 });
  const phone = await page.locator('.phone').boundingBox();
  if (!phone || phone.width > 390.5 || phone.x < -0.5) throw new Error(`phone stage overflows viewport: ${JSON.stringify(phone)}`);
  await page.locator('[data-action="open-account"]').click();
  await page.locator('#account-input').waitFor();
});

await browser.close();
const passed = errors.length === 0 && checks.every((item) => item.passed);
console.log(JSON.stringify({ status: passed ? 'passed' : 'failed', checks, pageErrors: errors }, null, 2));
process.exit(passed ? 0 : 1);
