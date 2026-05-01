// One-time OAuth2 setup for YouTube Data API + YouTube Analytics API.
// Captures refresh_token (long-lived, ~6mo) and writes to .env.
//
// Prereqs:
//   YT_CLIENT_ID and YT_CLIENT_SECRET must already be in .env (from Google
//   Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client ID,
//   Application type = "Desktop app").
//
// Usage:
//   cd generator && npm run audm:yt:setup

import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { URL } from 'node:url';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const ENV_PATH = path.join(ROOT, '.env');

const CALLBACK_PORT = 47823;
const REDIRECT_URI = `http://127.0.0.1:${CALLBACK_PORT}/callback`;
const SCOPES = [
  'https://www.googleapis.com/auth/youtube.readonly',
  'https://www.googleapis.com/auth/yt-analytics.readonly',
];

async function loadEnv() {
  const envText = await fs.readFile(ENV_PATH, 'utf8');
  return Object.fromEntries(
    envText.split('\n')
      .filter(line => line && !line.startsWith('#') && line.includes('='))
      .map(line => {
        const eq = line.indexOf('=');
        return [line.slice(0, eq).trim(), line.slice(eq + 1).trim()];
      }),
  );
}

async function writeEnv(updates) {
  let envText = await fs.readFile(ENV_PATH, 'utf8');
  for (const [k, v] of Object.entries(updates)) {
    const re = new RegExp(`^${k}=.*$`, 'm');
    if (re.test(envText)) {
      envText = envText.replace(re, `${k}=${v}`);
    } else {
      if (!envText.endsWith('\n')) envText += '\n';
      envText += `${k}=${v}\n`;
    }
  }
  await fs.writeFile(ENV_PATH, envText);
}

const env = await loadEnv();
const { YT_CLIENT_ID, YT_CLIENT_SECRET } = env;
if (!YT_CLIENT_ID || !YT_CLIENT_SECRET) {
  console.error('X Missing YT_CLIENT_ID / YT_CLIENT_SECRET in .env');
  console.error('   Get these from Google Cloud Console → APIs & Services → Credentials');
  console.error('   → Create OAuth 2.0 Client ID → Application type: Desktop app');
  console.error('   Then paste into .env as:');
  console.error('     YT_CLIENT_ID=<client-id>.apps.googleusercontent.com');
  console.error('     YT_CLIENT_SECRET=<secret>');
  process.exit(1);
}

console.log('YouTube OAuth2 setup');
console.log('====================\n');

const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');
authUrl.searchParams.set('client_id', YT_CLIENT_ID);
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', SCOPES.join(' '));
authUrl.searchParams.set('access_type', 'offline');
authUrl.searchParams.set('prompt', 'consent');

console.log('Starting local callback server on http://127.0.0.1:' + CALLBACK_PORT);
console.log('\n=== STEP 1 — open this URL in your browser ===\n');
console.log(authUrl.toString());
console.log('\n=== STEP 2 — sign in to the AU Dealer Math YouTube account ===');
console.log('=== STEP 3 — click "Allow" on the consent screen ===');
console.log('=== Browser will redirect to localhost — server will catch the code ===\n');

const codePromise = new Promise((resolve, reject) => {
  const server = http.createServer((req, res) => {
    if (!req.url.startsWith('/callback')) {
      res.writeHead(404).end('not found');
      return;
    }
    const params = new URL(req.url, `http://127.0.0.1:${CALLBACK_PORT}`).searchParams;
    const code = params.get('code');
    const error = params.get('error');
    if (error) {
      res.writeHead(400, { 'content-type': 'text/html' })
        .end(`<h1>Authorization failed</h1><p>${error}</p>`);
      server.close();
      reject(new Error(`OAuth error: ${error}`));
      return;
    }
    if (!code) {
      res.writeHead(400).end('missing code');
      return;
    }
    res.writeHead(200, { 'content-type': 'text/html' })
      .end('<h1>Authorized.</h1><p>You can close this tab and return to the terminal.</p>');
    server.close();
    resolve(code);
  });
  server.listen(CALLBACK_PORT, '127.0.0.1');
  setTimeout(() => {
    server.close();
    reject(new Error('Timed out waiting for OAuth callback (20 min)'));
  }, 20 * 60 * 1000);
});

let code;
try {
  code = await codePromise;
} catch (err) {
  console.error('X ' + err.message);
  process.exit(1);
}
console.log('  ok: received authorization code\n');

console.log('Exchanging code for tokens...');
const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
  method: 'POST',
  headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    code,
    client_id: YT_CLIENT_ID,
    client_secret: YT_CLIENT_SECRET,
    redirect_uri: REDIRECT_URI,
    grant_type: 'authorization_code',
  }),
});
const tokenJson = await tokenRes.json();
if (!tokenJson.refresh_token) {
  console.error('X No refresh_token returned. Response:', tokenJson);
  console.error('   If you have already authorized this app before, revoke access at:');
  console.error('   https://myaccount.google.com/permissions');
  console.error('   then re-run setup.');
  process.exit(1);
}
console.log('  ok: refresh_token received\n');

console.log('Discovering channel ID...');
const chanRes = await fetch(
  'https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true',
  { headers: { authorization: `Bearer ${tokenJson.access_token}` } },
);
const chanJson = await chanRes.json();
if (chanJson.error || !chanJson.items?.length) {
  console.error('X Could not fetch channel:', chanJson.error || chanJson);
  process.exit(1);
}
const channel = chanJson.items[0];
console.log(`  ok: channel "${channel.snippet.title}" (${channel.id})\n`);

await writeEnv({
  YT_REFRESH_TOKEN: tokenJson.refresh_token,
  YT_CHANNEL_ID: channel.id,
});

console.log('=== Setup complete ===');
console.log(`  Channel: ${channel.snippet.title}`);
console.log(`  Channel ID: ${channel.id}`);
console.log(`  YT_REFRESH_TOKEN written to .env`);
console.log(`\nNext: run "npm run audm:yt:pull" to verify analytics access.`);
