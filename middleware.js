// Vorschau-Zugang (Vercel Routing Middleware)
// Solange die Website im Entwurf ist, steht vor jeder Seite und jeder Datei ein Passwort.
// Frei sind nur die Login-Seite (dist/login.html) und die Dateien, die sie selbst braucht.
//
// Passwort ändern: SHA-256 des neuen Passworts in PASSWORT_SHA256 eintragen, z. B. mit
//   node -e "crypto.subtle.digest('SHA-256',new TextEncoder().encode('NEU')).then(b=>console.log(Buffer.from(b).toString('hex')))"
// Alle bisherigen Anmeldungen werden damit ungültig.
// Livegang: diese Datei löschen – dann ist die Seite ohne Passwort erreichbar.
// Tests: node tools/test_login.mjs

const PASSWORT_SHA256 = 'c58638fde84cddd8819d0019e5418b58fef8077b71adc9bf3f5126aea0700fd4';
const COOKIE = 'gpg_vorschau';
const TAGE = 30; // so lange bleibt man angemeldet

// ohne Passwort erreichbar
const FREI = [
  /^\/login(\.html)?$/,
  /^\/assets\/fonts\/[\w.-]+$/,
  /^\/assets\/img\/(login-[\w.-]+|favicon\.svg)$/,
  /^\/robots\.txt$/,
];

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, '0')).join('');
}

// Cookie-Wert: aus dem Passwort abgeleitet, enthält es aber nicht
const token = () => sha256(PASSWORT_SHA256 + ':vorschau-grafitecture');

function readCookie(request, name) {
  for (const part of (request.headers.get('cookie') || '').split(';')) {
    const i = part.indexOf('=');
    if (i > -1 && part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return '';
}

// nur Pfade auf dieser Website als Ziel zulassen (kein offener Redirect)
function sicheresZiel(ziel) {
  if (typeof ziel !== 'string' || !/^\/(?![/\\])/.test(ziel) || /^\/login\b/.test(ziel)) return '/';
  return ziel;
}

function weiter(request, pfad, status = 302, extra = {}) {
  return new Response(null, {
    status,
    headers: { location: new URL(pfad, request.url).toString(), 'cache-control': 'no-store', ...extra },
  });
}

function json(daten, status, extra = {}) {
  return new Response(JSON.stringify(daten), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra },
  });
}

export default async function middleware(request) {
  const url = new URL(request.url);
  const pfad = url.pathname;
  const angemeldet = readCookie(request, COOKIE) === (await token());

  if (pfad === '/logout') {
    return weiter(request, '/login', 302, { 'set-cookie': `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax` });
  }

  if (pfad === '/login' || pfad === '/login.html') {
    if (request.method === 'POST') {
      let form;
      try { form = await request.formData(); } catch { form = new URLSearchParams(); }
      const ziel = sicheresZiel(String(form.get('ziel') || '/'));
      const perFetch = (request.headers.get('accept') || '').includes('application/json');
      if ((await sha256(String(form.get('passwort') || '').trim())) === PASSWORT_SHA256) {
        const cookie = `${COOKIE}=${await token()}; Path=/; Max-Age=${TAGE * 86400}; HttpOnly; Secure; SameSite=Lax`;
        return perFetch ? json({ ok: true, ziel }, 200, { 'set-cookie': cookie }) : weiter(request, ziel, 303, { 'set-cookie': cookie });
      }
      if (perFetch) return json({ ok: false }, 401);
      const zurueck = new URLSearchParams({ fehler: '1' });
      if (ziel !== '/') zurueck.set('ziel', ziel);
      return weiter(request, '/login?' + zurueck, 303);
    }
    if (angemeldet) return weiter(request, sicheresZiel(url.searchParams.get('ziel')));
    return; // Login-Seite ausliefern
  }

  if (angemeldet || FREI.some((r) => r.test(pfad))) return; // weiter zur Seite

  const ziel = pfad + url.search;
  return weiter(request, ziel === '/' ? '/login' : '/login?' + new URLSearchParams({ ziel }));
}
