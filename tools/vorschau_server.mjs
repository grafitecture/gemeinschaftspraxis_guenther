// Lokaler Testserver: liefert dist/ aus wie Vercel (Clean URLs) und schickt jede Anfrage
// vorher durch middleware.js – so lässt sich der Vorschau-Zugang lokal ausprobieren.
// Start: node tools/vorschau_server.mjs [port]   →   http://localhost:4173
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import middleware from '../middleware.js';

const DIST = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'dist');
const PORT = Number(process.argv[2] || 4173);
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.webp': 'image/webp', '.png': 'image/png', '.woff': 'font/woff', '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml' };

function datei(pfad) {
  const p = decodeURIComponent(pfad).replace(/\/+$/, '') || '/';
  for (const c of [p, p + '.html', path.join(p, 'index.html')]) {
    const abs = path.join(DIST, c);
    if (abs.startsWith(DIST) && fs.existsSync(abs) && fs.statSync(abs).isFile()) return abs;
  }
  return null;
}

http.createServer(async (req, res) => {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const request = new Request(`http://localhost:${PORT}${req.url}`, {
    method: req.method, headers: req.headers, body: ['GET', 'HEAD'].includes(req.method) ? undefined : Buffer.concat(chunks),
  });
  const r = await middleware(request);
  if (r) {
    res.writeHead(r.status, Object.fromEntries(r.headers));
    return res.end(Buffer.from(await r.arrayBuffer()));
  }
  const f = datei(new URL(request.url).pathname);
  if (!f) { res.writeHead(404); return res.end('404'); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(PORT, () => console.log(`Vorschau mit Passwort: http://localhost:${PORT}`));
