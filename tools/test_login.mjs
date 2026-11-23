// Tests für die Passwort-Sperre (middleware.js) – ausführen mit: node tools/test_login.mjs
import assert from 'node:assert/strict';
import middleware from '../middleware.js';

const BASE = 'https://gemeinschaftspraxisguenther.vercel.app';
const PW = 'e&a';
const get = (path, cookie) => new Request(BASE + path, { headers: cookie ? { cookie } : {} });
const post = (path, fields, headers = {}) => new Request(BASE + path, {
  method: 'POST', body: new URLSearchParams(fields),
  headers: { 'content-type': 'application/x-www-form-urlencoded', ...headers },
});
const loc = (res) => new URL(res.headers.get('location'), BASE);
let n = 0;
const t = async (name, fn) => { await fn(); n++; console.log('ok –', name); };

// Ohne Anmeldung
await t('Startseite leitet zur Login-Seite', async () => {
  const r = await middleware(get('/'));
  assert.equal(r.status, 302);
  assert.equal(loc(r).pathname, '/login');
  assert.equal(loc(r).searchParams.get('ziel'), null);
  assert.equal(r.headers.get('cache-control'), 'no-store');
});
await t('Unterseite merkt sich das Ziel', async () => {
  const r = await middleware(get('/en/faq?x=1'));
  assert.equal(r.status, 302);
  assert.equal(loc(r).searchParams.get('ziel'), '/en/faq?x=1');
});
await t('Fotos und Seiten-CSS sind gesperrt', async () => {
  for (const p of ['/assets/img/foto-empfang.webp', '/assets/css/site.css', '/faq.html', '/sitemap.xml', '/llms.txt']) {
    const r = await middleware(get(p));
    assert.equal(r?.status, 302, p);
  }
});
await t('Login-Seite und ihre Dateien sind frei', async () => {
  for (const p of ['/login', '/login.html', '/assets/fonts/fira-sans-Regular.woff', '/assets/img/login-abend.webp',
    '/assets/img/login-abend-800.webp', '/assets/img/favicon.svg', '/robots.txt']) {
    assert.equal(await middleware(get(p)), undefined, p);
  }
});
await t('Pfad-Tricks öffnen nichts', async () => {
  for (const p of ['/login/../index.html', '/loginx', '/assets/img/login-abend.webp/../foto-empfang.webp', '/assets/fonts/../css/site.css']) {
    const r = await middleware(get(p));
    // URL normalisiert ../ – entscheidend ist nur: keine gesperrte Datei ohne Anmeldung
    const path = new URL(BASE + p).pathname;
    if (!/^\/login(\.html)?$/.test(path)) assert.equal(r?.status, 302, p);
  }
});

// Anmelden
await t('Falsches Passwort (Formular) → zurück mit Fehler', async () => {
  const r = await middleware(post('/login', { passwort: 'falsch', ziel: '/faq' }));
  assert.equal(r.status, 303);
  assert.equal(loc(r).pathname, '/login');
  assert.equal(loc(r).searchParams.get('fehler'), '1');
  assert.equal(loc(r).searchParams.get('ziel'), '/faq');
  assert.equal(r.headers.get('set-cookie'), null);
});
await t('Falsches Passwort (fetch) → 401', async () => {
  const r = await middleware(post('/login', { passwort: 'E&A' }, { accept: 'application/json' }));
  assert.equal(r.status, 401);
  assert.deepEqual(await r.json(), { ok: false });
});
let cookie;
await t('Richtiges Passwort (Formular) → Cookie und Ziel', async () => {
  const r = await middleware(post('/login', { passwort: PW, ziel: '/dr-evelyne-guenther' }));
  assert.equal(r.status, 303);
  assert.equal(loc(r).pathname, '/dr-evelyne-guenther');
  const sc = r.headers.get('set-cookie');
  assert.match(sc, /^gpg_vorschau=[0-9a-f]{64}; Path=\/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax$/);
  cookie = sc.split(';')[0];
});
await t('Richtiges Passwort (fetch) → JSON mit Ziel', async () => {
  const r = await middleware(post('/login', { passwort: PW, ziel: '/tr' }, { accept: 'application/json' }));
  assert.equal(r.status, 200);
  assert.deepEqual(await r.json(), { ok: true, ziel: '/tr' });
  assert.equal(r.headers.get('set-cookie').split(';')[0], cookie);
});
await t('Fremdes Ziel wird ignoriert (kein offener Redirect)', async () => {
  for (const z of ['https://example.com', '//example.com', '/\\example.com', 'javascript:alert(1)', '/login']) {
    const r = await middleware(post('/login', { passwort: PW, ziel: z }));
    assert.equal(loc(r).origin, BASE, z);
    assert.equal(loc(r).pathname, '/', z);
  }
});
await t('Leerzeichen um das Passwort werden toleriert', async () => {
  const r = await middleware(post('/login', { passwort: ' e&a ' }));
  assert.equal(r.status, 303);
  assert.ok(r.headers.get('set-cookie'));
});

// Angemeldet
await t('Mit Cookie ist alles frei', async () => {
  for (const p of ['/', '/en', '/assets/img/foto-empfang.webp', '/impressum']) {
    assert.equal(await middleware(get(p, `foo=1; ${cookie}; bar=2`)), undefined, p);
  }
});
await t('Angemeldet auf /login → weiter zum Ziel', async () => {
  const r = await middleware(get('/login?ziel=%2Ffaq', cookie));
  assert.equal(r.status, 302);
  assert.equal(loc(r).pathname, '/faq');
});
await t('Gefälschtes Cookie wird abgewiesen', async () => {
  const r = await middleware(get('/', 'gpg_vorschau=' + '0'.repeat(64)));
  assert.equal(r.status, 302);
  assert.equal(loc(r).pathname, '/login');
});
await t('Abmelden löscht das Cookie', async () => {
  const r = await middleware(get('/logout', cookie));
  assert.equal(r.status, 302);
  assert.equal(loc(r).pathname, '/login');
  assert.match(r.headers.get('set-cookie'), /^gpg_vorschau=; Path=\/; Max-Age=0/);
});

console.log(`\n${n} Tests bestanden.`);
