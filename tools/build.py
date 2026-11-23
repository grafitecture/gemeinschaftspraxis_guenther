"""Baut die dreisprachige Website (dist/), eine Einzeldatei-Präsentation (praesentation/)
und einen Ordner zum Veröffentlichen als Artefakt (artefakt/).

Deutsch liegt im Wurzelverzeichnis, Englisch unter /en/, Türkisch unter /tr/."""
import base64, hashlib, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from i18n import LANGS, META, UI, PAGEMETA, SVG, DLG, TEAMTXT, FOOT
from signet_paths import SIG_VIEWBOX, SIG_GREY, SIG_BLUE

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
PRES = os.path.join(ROOT, "praesentation")
ART = os.path.join(ROOT, "artefakt")
BASE_URL = "https://www.gemeinschaftspraxis-guenther.de"
PHONE = "06204 37 04"
TEL = "+4962043704"
MAIL = "willkommen@gemeinschaftspraxis-guenther.de"
INSTA = "https://www.instagram.com/gemeinschaftspraxisguenther/"
ROUTE_G = "https://www.google.com/maps/dir/?api=1&amp;destination=Kreuzstra%C3%9Fe+13%2C+68519+Viernheim"
ROUTE_A = "https://maps.apple.com/?daddr=Kreuzstra%C3%9Fe+13,+68519+Viernheim"
TODAY = "2026-11-21"

ICONS = {
    "phone": '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 6 6L15 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 17h.01M12 17h.01"/>',
    "pill": '<path d="M10.5 20.5a5 5 0 0 1-7-7l6-6a5 5 0 0 1 7 7z"/><path d="m8.5 8.5 7 7"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5"/>',
    "syringe": '<path d="m18 2 4 4M17 7l3-3M19 9 8.5 19.5 4.5 15.5 15 5zM9 11l4 4M5 19l-3 3M14 4l6 6"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10M10 20v-6h4v6"/>',
    "alert": '<path d="M12 3 2 21h20z"/><path d="M12 10v5M12 18h.01"/>',
    "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "route": '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h8.5a3.5 3.5 0 0 0 0-7h-9a3.5 3.5 0 0 1 0-7H16"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "insta": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "bus": '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16M8 18v3M16 18v3M8 14.5h.01M16 14.5h.01"/>',
    "car": '<path d="M5 17h14v-5l-2-5H7l-2 5zM5 12h14"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/>',
    "hand": '<path d="M7 11V6a1.5 1.5 0 0 1 3 0v4M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V11M16 11V8a1.5 1.5 0 0 1 3 0v6a7 7 0 0 1-7 7h-1a6 6 0 0 1-5-2.7L3.5 15a1.6 1.6 0 0 1 2.6-1.8L7 14"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
}

# Seiten: Schlüssel, Dateiname, Quelldatei, Pfad auf der Domain
PAGES = [("start", "index.html", "index.html", "/"),
         ("faq", "faq.html", None, "/faq"),
         ("evelyne", "dr-evelyne-guenther.html", "evelyne.html", "/dr-evelyne-guenther"),
         ("andreas", "dr-andreas-guenther.html", "andreas.html", "/dr-andreas-guenther"),
         ("impfkalender", "impfkalender.html", "impfkalender.html", "/impfkalender")]
FILE = {k: fn for k, fn, _, _ in PAGES}

# Rechtstexte: nur auf Deutsch (maßgebliche Fassung), aus allen Sprachen verlinkt
LEGAL = [("impressum", "impressum.html", "impressum.html", "/impressum"),
         ("datenschutz", "datenschutz.html", "datenschutz.html", "/datenschutz")]
LEGALMETA = {
    "impressum": ("Impressum – Gemeinschaftspraxis Günther, Viernheim",
                  "Anbieterkennzeichnung der Gemeinschaftspraxis Günther nach § 5 DDG mit Kammer, Kassenärztlicher Vereinigung und berufsrechtlichen Regelungen."),
    "datenschutz": ("Datenschutzerklärung – Gemeinschaftspraxis Günther, Viernheim",
                    "Wie die Gemeinschaftspraxis Günther mit Ihren Daten umgeht: Hosting bei Vercel, keine Cookies, kein Tracking, Ihre Rechte nach der DSGVO."),
}
GT_LOGO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gt_logo.svg"), encoding="utf-8").read().strip()
GT_ARROW = ('<svg class="gt-credit__arrow" viewBox="0 0 22 10" aria-hidden="true" focusable="false">'
            '<path d="M0 5h20.5M16 .8 20.5 5 16 9.2" fill="none" stroke="currentColor" stroke-width="1.5"></path></svg>')
# Agentur-Feld (Grafitecture-Standard, wie auf raumrent.de)
CREDIT = ('<aside class="gt-credit" lang="de" aria-label="Über diese Website"><div class="gt-credit__in">'
          '<p class="gt-credit__by"><span class="gt-credit__lead">Entworfen, technisch betreut und weiterentwickelt von</span> '
          f'<span class="gt-credit__logo">{GT_LOGO}</span></p>'
          '<div class="gt-credit__foot"><p class="gt-credit__claim">Marken<br>mit KI.</p>'
          '<p class="gt-credit__go"><a class="gt-credit__link" href="https://www.grafitecture.de/" target="_blank" rel="noopener">'
          '<span>www.grafitecture.de</span><span class="gt-credit__sr"> (öffnet in neuem Fenster)</span>'
          f'{GT_ARROW}</a></p></div></div></aside>')


def icon(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def svg(name, lang):
    s = open(os.path.join(ROOT, "assets", "img", name), encoding="utf-8").read()
    for a, b in SVG.get(lang, []):
        s = s.replace(a, b)
    return s


def sig(cls="lg"):
    """Original-Signet inline: graue Extrusion + blaues G (für Animation und Lichtwirkung)."""
    return (f'<svg class="{cls}" viewBox="{SIG_VIEWBOX}" aria-hidden="true" focusable="false">'
            f'<g class="sg-x"><path d="{SIG_GREY[0]}" transform="{SIG_GREY[1]}"/></g>'
            f'<g class="sg-g"><path d="{SIG_BLUE[0]}" transform="{SIG_BLUE[1]}"/></g></svg>')


def gmark(cls="lg"):
    return sig(cls)


def wordmark(block=True, sig=True):
    logo = "logo-block.svg" if block else "logo-zeile.svg"
    return ((f'<img class="wm__sig" src="assets/img/signet.svg" alt="" width="33" height="47">' if sig else "")
            + f'<img class="wm__logo{"" if block else " wm__logo--zeile"}" src="assets/img/{logo}" alt="" '
            f'width="{98 if block else 236}" height="{36 if block else 21}">')


GCON = None  # ersetzt durch hero_signet()


PORTRAIT_ALT = {"evelyne": "Dr. med. Evelyne Günther", "andreas": "Dr. med. Andreas Günther"}


def portrait(k, alt=""):
    """Porträt, falls vorhanden (assets/img/team-<k>.webp), sonst graue Platzhalterfläche."""
    if os.path.exists(os.path.join(ROOT, "assets", "img", f"team-{k}.webp")):
        return (f'<img src="assets/img/team-{k}.webp" width="800" height="800" loading="lazy" '
                f'alt="{alt or PORTRAIT_ALT.get(k, "")}">')
    return '<span class="ph" aria-hidden="true"></span>'


def hero_signet():
    return f'<div class="gsig" data-light aria-hidden="true">{sig("gsig__svg")}<span class="gsig__glow"></span></div>'


HAUS = None


def haus():
    global HAUS
    if HAUS is None:
        HAUS = open(os.path.join(ROOT, "assets", "img", "haus.svg"), encoding="utf-8").read()
    return HAUS


def status(lang):
    return ('<p class="status" data-status role="status"><span class="status__dot" aria-hidden="true"></span>'
            f'<span><span data-status-text>{UI[lang]["status"]}</span>'
            '<span class="status__more" data-status-more></span></span></p>')


def chrome_attr(lang, pres):
    """In der Präsentation trägt jeder Sprachrahmen data-chrome; nur Deutsch ist anfangs sichtbar."""
    if not pres:
        return ""
    return f' data-chrome="{lang}" lang="{lang}"' + ("" if lang == "de" else " hidden")


def header(lang, active, pres=False):
    u = UI[lang]
    hrefs = ["index.html#aktuell", "index.html#sprechzeiten", "index.html#aerzte",
             "index.html#leistungen", "faq.html"]
    items = []
    for i, (href, label) in enumerate(zip(hrefs, u["nav"])):
        is_faq = i == len(hrefs) - 1
        cur = ' aria-current="page"' if (active == "faq" and is_faq) else ""
        dp = "faq" if is_faq else ""
        items.append(f'<li><a class="nav__link" href="{href}"{cur} data-page="{dp}">{label}</a></li>')
    ca = chrome_attr(lang, pres)
    return f'''<a class="skip-link" href="#inhalt"{ca}>{u["skip"]}</a>
<header class="site-header"{ca}>
  <div class="wrap site-header__in">
    <a class="wm wm--head" href="index.html" aria-label="{u["home_aria"]}">{wordmark(sig=False)}</a>
    <nav class="nav" id="nav" aria-label="{u["nav_aria"]}"><ul class="nav__list">{"".join(items)}</ul></nav>
    {{{{LANGSWITCH}}}}
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="{u["menu"]}"><span class="menu-btn__bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
  </div>
</header>'''


def footer(lang, pres=False):
    u, f = UI[lang], FOOT[lang]
    ca = chrome_attr(lang, pres)
    hours = "".join(f"<li>{h}</li>" for h in u["hours_lines"])
    return f'''<footer class="site-footer"{ca}>
  <div class="wrap">
    <div class="foot-card">
      <div class="foot-card__brand">
        <a class="wm wm--zeile" href="index.html" aria-label="{u["home_aria"]}">{wordmark(False)}</a>
        <dl class="foot-docs">
          <dt><a href="dr-evelyne-guenther.html">Dr. med. Evelyne Günther</a></dt><dd>{f["ev_role"]}</dd>
          <dt><a href="dr-andreas-guenther.html">Dr. med. Andreas Günther</a></dt><dd>{f["an_role"]}</dd>
        </dl>
      </div>
      <div>
        <h2>{u["hours"]}</h2>
        <ul class="num">{hours}</ul>
      </div>
      <div>
        <h2>{u["practice"]}</h2>
        <ul>
          <li><a href="faq.html">{u["faq"]}</a></li>
          <li><a href="impfkalender.html">{u["vacc_cal"]}</a></li>
          <li><a href="index.html#ausbildung">{u["training"]}</a></li>
          <li><a href="{INSTA}" rel="noopener">Instagram</a></li>
          <li><a href="impressum.html">{u["imprint"]}</a></li>
          <li><a href="datenschutz.html">{u["privacy"]}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-house" data-light>
      <address class="foot-house__addr">Kreuzstraße 13, 68519 Viernheim<br>{u["phone"]} <a class="num" href="tel:{TEL}">{PHONE}</a><br>{u["fax"]} <span class="num">06204 17 23</span><br><a href="mailto:{MAIL}">{MAIL.replace("@", "@<wbr>")}</a></address>
      <a class="foot-house__img" href="{ROUTE_G}" rel="noopener" aria-label="{f["to_map"]}">{haus()}</a>
    </div>
    <div class="site-footer__base">
      <span>© <span data-year>2026</span> Gemeinschaftspraxis Günther</span>
    </div>
  </div>
</footer>
''' + sos(lang, ca)


def sos(lang, ca=""):
    """Notfall-Band „Außerhalb der Sprechzeiten“ – auf jeder Seite ganz unten, nach dem Fuß."""
    return open(os.path.join(SRC, "partials", f"sos.{lang}.html"), encoding="utf-8").read().replace("__CA__", ca)


def team_html(lang, which):
    t = TEAMTXT[lang]
    cards = "".join(
        f'<li class="mate"><figure class="mate__img">{portrait(k, n)}</figure>'
        f'<h3>{n}</h3><p class="mate__role">{r}</p><p class="mate__txt">{x}</p></li>'
        for k, n, r, x in t["people"])
    return (f'<div class="head"><h2 id="team-h">{t["h"]}</h2><p class="lead">{t["lead"]}</p></div>'
            f'<ul class="team">{cards}</ul>')


def dialogs(lang):
    d = DLG[lang]
    chips = "".join(f'<label class="chip"><input type="radio" name="anliegen" value="{v}" class="sr-only"> {t}</label>'
                    for v, t in zip(["akut", "vorsorge", "befund", "impfung", "akupunktur", "anderes"], d["chips"]))
    when = "".join(f"<option>{o}</option>" for o in d["when_opts"])
    how = "".join(f'<label class="chip"><input type="radio" name="weg" value="{v}" class="sr-only"{" checked" if v == "karte" else ""}> {t}</label>'
                  for v, t in zip(["karte", "app"], d["how_opts"]))
    akut = d["akut"].format(tel=f'<a href="tel:{TEL}">{PHONE}</a>')
    return f'''<dialog class="dlg" id="dlg-termin" data-dlg="termin" data-lang="{lang}" lang="{lang}" aria-labelledby="dlg-termin-h">
  <div class="dlg__in">
    <div class="dlg__top"><h2 id="dlg-termin-h">{d["t_title"]}</h2><button class="x" type="button" data-close aria-label="{d["close"]}">×</button></div>
    <p class="demo">{d["t_demo"]}</p>
    <form>
      <div style="display:grid;gap:1.1rem">
        <fieldset class="field">
          <legend>{d["t_what"]}</legend>
          <div class="chips">{chips}</div>
        </fieldset>
        <p class="hint hint--alert" data-akut hidden>{akut}</p>
        <p class="hint" data-impf hidden>{d["impf"]}</p>
        <div class="grid2">
          <div class="field"><label for="t-arzt">{d["who"]}</label><select id="t-arzt" name="arzt"><option>{d["who_any"]}</option><option>Dr. Evelyne Günther</option><option>Dr. Andreas Günther</option></select></div>
          <div class="field"><label for="t-zeit">{d["when"]}</label><select id="t-zeit" name="zeit">{when}</select></div>
        </div>
        <div class="grid2">
          <div class="field"><label for="t-name">{d["name"]}</label><input id="t-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="t-tel">{d["cb"]}</label><input id="t-tel" name="tel" type="tel" autocomplete="tel" required></div>
        </div>
        <label class="check"><input type="checkbox" required> {d["consent"]}</label>
        <div class="btn-row"><button class="btn btn--primary" type="submit">{d["send"]}</button><button class="btn" type="button" data-close>{d["cancel"]}</button></div>
      </div>
    </form>
    <div class="done" hidden>
      <span class="done__dots" aria-hidden="true"><i></i><i></i></span>
      <h3 tabindex="-1">{d["t_done"]}</h3>
      <p class="muted">{d["t_done_p"]}</p>
      <button class="btn" type="button" data-close>{d["close"]}</button>
    </div>
  </div>
</dialog>
<dialog class="dlg" id="dlg-rezept" data-dlg="rezept" data-lang="{lang}" lang="{lang}" aria-labelledby="dlg-rezept-h">
  <div class="dlg__in">
    <div class="dlg__top"><h2 id="dlg-rezept-h">{d["r_title"]}</h2><button class="x" type="button" data-close aria-label="{d["close"]}">×</button></div>
    <p class="demo">{d["r_demo"]}</p>
    <p class="hint">{d["r_hint"]}</p>
    <form>
      <div style="display:grid;gap:1.1rem">
        <div class="grid2">
          <div class="field"><label for="r-name">{d["name"]}</label><input id="r-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="r-geb">{d["dob"]}</label><input id="r-geb" name="geb" type="date" required></div>
        </div>
        <div class="field"><label for="r-med">{d["med"]}</label><textarea id="r-med" name="med" required placeholder="{d["med_ph"]}"></textarea></div>
        <fieldset class="field">
          <legend>{d["how"]}</legend>
          <div class="chips">{how}</div>
        </fieldset>
        <div class="btn-row"><button class="btn btn--primary" type="submit">{d["r_send"]}</button><button class="btn" type="button" data-close>{d["cancel"]}</button></div>
      </div>
    </form>
    <div class="done" hidden>
      <span class="done__dots" aria-hidden="true"><i></i><i></i></span>
      <h3 tabindex="-1">{d["r_done"]}</h3>
      <p class="muted">{d["r_done_p"]}</p>
      <button class="btn" type="button" data-close>{d["close"]}</button>
    </div>
  </div>
</dialog>'''


def expand(html, lang):
    html = re.sub(r"\{\{svg:([\w.-]+)\}\}", lambda m: svg(m.group(1), lang), html)
    html = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), html)
    html = html.replace("{{gmark}}", gmark()).replace("{{gcon}}", hero_signet())
    html = re.sub(r"\{\{team:(\w+)\}\}", lambda m: team_html(lang, m.group(1)), html)
    html = re.sub(r"\{\{portrait:(\w+)\}\}", lambda m: portrait(m.group(1)), html)
    html = html.replace("{{status}}", status(lang)).replace("{{PHONE}}", PHONE).replace("{{TEL}}", TEL) \
               .replace("{{MAIL}}", MAIL).replace("{{INSTA}}", INSTA).replace("{{ROUTE_G}}", ROUTE_G) \
               .replace("{{ROUTE_A}}", ROUTE_A).replace("{{BASE}}", BASE_URL).replace("{{credit}}", CREDIT)
    return html


# ---------------------------------------------------------------- URLs und Sprachwechsel

def url_path(lang, key):
    """Pfad auf der Live-Domain (cleanUrls)."""
    p = dict((k, path) for k, _, _, path in PAGES)[key]
    if lang == "de":
        return p
    return f"/{lang}" if p == "/" else f"/{lang}{p}"


def rel_href(from_lang, to_lang, key):
    fn = FILE[key]
    if from_lang == to_lang:
        return fn
    if from_lang == "de":
        return f"{to_lang}/{fn}"
    if to_lang == "de":
        return f"../{fn}"
    return f"../{to_lang}/{fn}"


def route_name(lang, key):
    if lang == "de":
        return key
    return lang if key == "start" else f"{lang}-{key}"


def lang_switch(lang, key, pres):
    items = []
    for L in LANGS:
        href = "#" + route_name(L, key) if pres else rel_href(lang, L, key)
        cur = ' aria-current="true"' if L == lang else ""
        items.append(f'<li><a href="{href}" lang="{META[L]["html"]}" hreflang="{META[L]["html"]}"{cur}>{META[L]["name"]}</a></li>')
    return (f'<details class="lang"><summary aria-label="{UI[lang]["lang"]}: {META[lang]["name"]}">'
            f'<span>{META[lang]["code"]}</span></summary><ul>{"".join(items)}</ul></details>')


def foot_langs(lang, key, pres):
    links = []
    for L in LANGS:
        href = "#" + route_name(L, key) if pres else rel_href(lang, L, key)
        cur = ' aria-current="true"' if L == lang else ""
        links.append(f'<a href="{href}" lang="{META[L]["html"]}" hreflang="{META[L]["html"]}"{cur}>{META[L]["name"]}</a>')
    return f'<nav class="foot-langs" aria-label="{UI[lang]["lang"]}">{"".join(links)}</nav>'


# ---------------------------------------------------------------- FAQ

def load_faq(lang):
    fn = "faq.json" if lang == "de" else f"faq.{lang}.json"
    return json.load(open(os.path.join(SRC, fn), encoding="utf-8"))


def strip(html):
    t = re.sub(r"</(p|li)>", " ", html)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", t).strip()


def faq_body(lang):
    u = UI[lang]
    groups = load_faq(lang)
    topics = "".join(f'<a href="#t-{g["id"]}">{g["title"]}</a>' for g in groups)
    parts = []
    for g in groups:
        qs = "".join(
            f'<details class="q" id="{it["id"]}"><summary>{it["q"]}</summary><div class="q__a">{it["a"]}</div></details>'
            for it in g["items"])
        parts.append(f'<section class="faq-group" id="t-{g["id"]}" aria-labelledby="h-{g["id"]}"><h2 id="h-{g["id"]}">{g["title"]}</h2>{qs}</section>')
    n = sum(len(g["items"]) for g in groups)
    title = PAGEMETA[lang]["faq"][0].split(" – ")[0]
    return f'''<div class="subpage">
<div class="wrap">
  <div class="faq-hero">
    <p class="person__crumb"><a href="index.html">{u["crumb_home"]}</a> / {title}</p>
    <h1>{title}</h1>
    <p class="lead">{u["faq_lead"].format(n=n)}</p>
    <nav class="topics" aria-label="{u["topics"]}">{topics}</nav>
  </div>
  <div class="faq-layout">
    <div>
      {"".join(parts)}
    </div>
  </div>
</div>
<div style="height:var(--space-2xl)"></div>
</div>'''


# ---------------------------------------------------------------- Strukturierte Daten

def jsonld(lang, key):
    if key == "faq":
        groups = load_faq(lang)
        ents = [{"@type": "Question", "name": it["q"], "acceptedAnswer": {"@type": "Answer", "text": strip(it["a"])}}
                for g in groups for it in g["items"]]
        title = PAGEMETA[lang]["faq"][0].split(" – ")[0]
        data = [{"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": META[lang]["inlang"],
                 "url": BASE_URL + url_path(lang, "faq"),
                 "about": {"@id": BASE_URL + "/#praxis"}, "dateModified": TODAY, "mainEntity": ents},
                {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": UI[lang]["crumb_home"], "item": BASE_URL + url_path(lang, "start")},
                    {"@type": "ListItem", "position": 2, "name": title, "item": BASE_URL + url_path(lang, "faq")}]}]
        return json.dumps(data, ensure_ascii=False, indent=1)
    if key == "impfkalender":
        title = PAGEMETA[lang][key][0].split(" – ")[0]
        data = [{"@context": "https://schema.org", "@type": "MedicalWebPage", "url": BASE_URL + url_path(lang, key),
                 "name": PAGEMETA[lang][key][0], "description": PAGEMETA[lang][key][1], "inLanguage": META[lang]["inlang"],
                 "about": {"@id": BASE_URL + "/#praxis"}, "isPartOf": {"@id": BASE_URL + "/#website"},
                 "lastReviewed": TODAY, "dateModified": TODAY},
                {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": UI[lang]["crumb_home"], "item": BASE_URL + url_path(lang, "start")},
                    {"@type": "ListItem", "position": 2, "name": title, "item": BASE_URL + url_path(lang, key)}]}]
        return json.dumps(data, ensure_ascii=False, indent=1)
    if lang == "de":
        return open(os.path.join(SRC, "jsonld", key + ".json"), encoding="utf-8").read()
    # Übersetzte Seiten verweisen auf die eine Praxis bzw. Person (deutsche Kanonik)
    about = {"start": "/#praxis", "evelyne": "/dr-evelyne-guenther#person", "andreas": "/dr-andreas-guenther#person"}[key]
    typ = "WebPage" if key == "start" else "ProfilePage"
    data = {"@context": "https://schema.org", "@type": typ, "url": BASE_URL + url_path(lang, key),
            "name": PAGEMETA[lang][key][0], "description": PAGEMETA[lang][key][1], "inLanguage": META[lang]["inlang"],
            ("about" if key == "start" else "mainEntity"): {"@id": BASE_URL + about},
            "isPartOf": {"@id": BASE_URL + "/#website"}, "dateModified": TODAY}
    return json.dumps(data, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- Seiten

def page_body(lang, key, src):
    if key == "faq":
        return expand(faq_body(lang), lang)
    sub = "" if lang == "de" else lang + "/"
    return expand(open(os.path.join(SRC, "pages", sub + src), encoding="utf-8").read(), lang)


def legal_body(key, src):
    return '<div class="subpage">\n' + expand(open(os.path.join(SRC, "legal", src), encoding="utf-8").read(), "de") + '\n</div>'


def legal_jsonld(key):
    path = dict((k, pth) for k, _, _, pth in LEGAL)[key]
    return json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": BASE_URL + path,
                       "name": LEGALMETA[key][0], "inLanguage": "de-DE",
                       "isPartOf": {"@id": BASE_URL + "/#website"}, "dateModified": TODAY}, ensure_ascii=False, indent=1)


def head(lang, key, css_tag, ld, extra_robots=True):
    if key in LEGALMETA:
        title, desc = LEGALMETA[key]
        path = dict((k, pth) for k, _, _, pth in LEGAL)[key]
        alts = ""
    else:
        title, desc = PAGEMETA[lang][key]
        path = url_path(lang, key)
        alts = "\n".join(f'<link rel="alternate" hreflang="{META[L]["html"]}" href="{BASE_URL}{url_path(L, key)}">' for L in LANGS)
        alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE_URL}{url_path("de", key)}">'
    robots = '<meta name="robots" content="noindex, nofollow"><!-- Prototyp: vor dem Livegang entfernen -->' if extra_robots else ""
    return f'''<!DOCTYPE html>
<html lang="{META[lang]["html"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE_URL}{path}">
{alts}
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:locale" content="{META[lang]["og"]}">
<meta property="og:site_name" content="Gemeinschaftspraxis Günther">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}/assets/img/og-bild.png">
{robots}
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
{css_tag}
{ld}
</head>'''


def versioned(rel):
    """Adresse mit Inhalts-Prüfsumme (?v=…): /assets wird ein Jahr „immutable“ gecacht,
    eine geänderte Datei bekommt so eine neue Adresse und wird sofort neu geladen."""
    data = open(os.path.join(ROOT, rel), "rb").read()
    return f"{rel}?v={hashlib.sha1(data).hexdigest()[:10]}"


def bust_assets(html):
    """Hängt an jede verlinkte Datei unter assets/ (Bilder, Logos, Favicon) die Prüfsumme an."""
    def rep(m):
        rel = m.group(2)
        return f'{m.group(1)}="{versioned(rel)}"' if os.path.isfile(os.path.join(ROOT, rel)) else m.group(0)
    return re.sub(r'(src|href)="(assets/[^"?#]+)"', rep, html)


def css_link():
    return f'<link rel="stylesheet" href="{versioned("assets/css/site.css")}">'


def js_script(defer=True):
    return f'<script src="{versioned("assets/js/site.js")}"{" defer" if defer else ""}></script>'


def build_dist():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"),
                    ignore=shutil.ignore_patterns("raum-*.svg", "hero-praxis.svg", "_alt", "team-evelyne.svg", "team-andreas.svg", "logo-g.svg"))
    for lang in LANGS:
        outdir = DIST if lang == "de" else os.path.join(DIST, lang)
        os.makedirs(outdir, exist_ok=True)
        for key, fn, src, _ in PAGES:
            body = page_body(lang, key, src)
            ld = f'<script type="application/ld+json">{jsonld(lang, key)}</script>'
            html = (head(lang, key, css_link(), ld)
                    + f'\n<body>\n{header(lang, key)}\n<main id="inhalt">\n{body}\n</main>\n{footer(lang)}\n{dialogs(lang)}\n'
                    + js_script() + '\n</body>\n</html>\n')
            html = html.replace("{{LANGSWITCH}}", lang_switch(lang, key, False)).replace("{{FOOTLANGS}}", foot_langs(lang, key, False))
            html = bust_assets(html)
            if lang != "de":
                html = html.replace('src="assets/', 'src="../assets/').replace('href="assets/', 'href="../assets/')
                for _, lfn, _, _ in LEGAL:
                    html = html.replace(f'href="{lfn}"', f'href="../{lfn}"')
            open(os.path.join(outdir, fn), "w", encoding="utf-8").write(html)
    for key, fn, src, _ in LEGAL:
        body = legal_body(key, src)
        ld = f'<script type="application/ld+json">{legal_jsonld(key)}</script>'
        html = (head("de", key, css_link(), ld)
                + f'\n<body>\n{header("de", key)}\n<main id="inhalt">\n{body}\n</main>\n{footer("de")}\n{dialogs("de")}\n'
                + js_script() + '\n</body>\n</html>\n')
        html = html.replace("{{LANGSWITCH}}", lang_switch("de", "start", False)).replace("{{FOOTLANGS}}", foot_langs("de", "start", False))
        html = bust_assets(html)
        open(os.path.join(DIST, fn), "w", encoding="utf-8").write(html)
    for extra in ("robots.txt", "llms.txt"):
        p = os.path.join(SRC, extra)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(DIST, extra))
    write_sitemap()


def write_sitemap():
    rows = []
    for lang in LANGS:
        for key, _, _, _ in PAGES:
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{META[L]["html"]}" href="{BASE_URL}{url_path(L, key)}"/>' for L in LANGS)
            rows.append(f'  <url>\n    <loc>{BASE_URL}{url_path(lang, key)}</loc>\n    <lastmod>{TODAY}</lastmod>{alts}\n  </url>')
    for _, _, _, pth in LEGAL:
        rows.append(f'  <url>\n    <loc>{BASE_URL}{pth}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
    open(os.path.join(SRC, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write(xml)


# ---------------------------------------------------------------- Präsentation (eine Datei, Hash-Routen)

KEEP_IDS = {"inhalt"}


def pres_links(html, lang):
    """Seitenlinks auf Hash-Routen umbiegen; IDs der Fremdsprachen mit Präfix eindeutig machen."""
    p = "" if lang == "de" else lang + "-"
    if p:
        html = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{m.group(1) if m.group(1) in KEEP_IDS else p + m.group(1)}"', html)
        html = re.sub(r'\bfor="([^"]+)"', lambda m: f'for="{p}{m.group(1)}"', html)
        html = re.sub(r'\b(aria-labelledby|aria-controls|aria-describedby)="([^"]+)"',
                      lambda m: f'{m.group(1)}="' + " ".join(p + x for x in m.group(2).split()) + '"', html)
        html = re.sub(r'href="#([\w-]+)"', lambda m: f'href="#{m.group(1) if m.group(1) in KEEP_IDS else p + m.group(1)}"', html)
    for key, fn, _, _ in PAGES:
        esc = re.escape(fn)
        html = re.sub(rf'href="{esc}#([\w-]+)"', lambda m: f'href="#{p}{m.group(1)}"', html)
        html = html.replace(f'href="{fn}"', f'href="#{route_name(lang, key)}"')
    for key, fn, _, _ in LEGAL:
        html = html.replace(f'href="{fn}"', f'href="#{key}"')
    return html


def build_presentation(inline=True):
    css = open(os.path.join(ROOT, "assets", "css", "site.css"), encoding="utf-8").read()
    js = open(os.path.join(ROOT, "assets", "js", "site.js"), encoding="utf-8").read()
    if inline:
        def font64(m):
            f = os.path.join(ROOT, "assets", "fonts", m.group(1))
            return 'url("data:font/woff;base64,' + base64.b64encode(open(f, "rb").read()).decode() + '")'
        css_tag = "<style>" + re.sub(r'url\("\.\./fonts/([\w-]+\.woff)"\)', font64, css) + "</style>"
        js_tag = f"<script>{js}</script>"
    else:
        css_tag = css_link()
        js_tag = js_script(defer=False)
    tops, mains, bottoms, dlgs, lds = [], [], [], [], []
    for lang in LANGS:
        ca = chrome_attr(lang, True)
        top = header(lang, "start", pres=True)
        tops.append(pres_links(top, lang).replace("{{LANGSWITCH}}", lang_switch(lang, "start", True)))
        bottoms.append(pres_links(footer(lang, pres=True), lang).replace("{{FOOTLANGS}}", foot_langs(lang, "start", True))
                       + ("" if inline else f'\n<p class="draft-line"{ca}>{UI[lang]["preview"]}</p>'))
        dlgs.append(pres_links(dialogs(lang), lang))
        for key, fn, src, _ in PAGES:
            body = pres_links(page_body(lang, key, src), lang)
            rn = route_name(lang, key)
            hid = "" if rn == "start" else " hidden"
            mains.append(f'<div data-route="{rn}" data-page="{key}" data-lang="{lang}" lang="{META[lang]["html"]}" '
                         f'data-title="{PAGEMETA[lang][key][0]}"{hid}>\n{body}\n</div>')
        lds.append(f'<script type="application/ld+json">{jsonld(lang, "faq")}</script>')
    for key, fn, src, _ in LEGAL:
        body = pres_links(legal_body(key, src), "de")
        mains.append(f'<div data-route="{key}" data-page="{key}" data-lang="de" lang="de" '
                     f'data-title="{LEGALMETA[key][0]}" hidden>\n{body}\n</div>')
    lds.insert(0, f'<script type="application/ld+json">{jsonld("de", "start")}</script>')
    html = (head("de", "start", css_tag, "\n".join(lds))
            + "\n<body>\n" + "\n".join(tops) + '\n<main id="inhalt">\n' + "\n".join(mains) + "\n</main>\n"
            + "\n".join(bottoms) + "\n" + "\n".join(dlgs) + f"\n{js_tag}\n</body>\n</html>\n")
    # Die Präsentation verlinkt keine weiteren Sprachversionen auf der Live-Domain
    html = re.sub(r'<link rel="alternate" hreflang=[^>]+>\n?', "", html)
    if inline:
        fav = "data:image/svg+xml;base64," + base64.b64encode(open(os.path.join(ROOT, "assets/img/favicon.svg"), "rb").read()).decode()
        html = html.replace('href="assets/img/favicon.svg"', f'href="{fav}"')
        # SVG-Bilder (Logo im Kopf und Fuß, Signet) direkt einbetten, sonst fehlen sie in der Einzeldatei
        def svg64(m):
            f = os.path.join(ROOT, "assets", "img", m.group(1))
            return 'src="data:image/svg+xml;base64,' + base64.b64encode(open(f, "rb").read()).decode() + '"'
        html = re.sub(r'src="assets/img/([\w.-]+\.svg)"', svg64, html)

        # Jedes Bild nur einmal einbetten: Daten in einer Tabelle, die img-Elemente holen sie per Schlüssel
        names = sorted(set(re.findall(r'src="assets/img/([\w.-]+\.(?:webp|png|jpg))"', html)))
        table = {}
        for n in names:
            f = os.path.join(ROOT, "assets", "img", n)
            mime = "image/webp" if n.endswith(".webp") else ("image/png" if n.endswith(".png") else "image/jpeg")
            table[n] = "data:" + mime + ";base64," + base64.b64encode(open(f, "rb").read()).decode()
        blank = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
        html = re.sub(r'src="assets/img/([\w.-]+\.(?:webp|png|jpg))"', lambda m: f'src="{blank}" data-img="{m.group(1)}"', html)
        loader = ("<script>(function(){var I=" + json.dumps(table) + ";document.querySelectorAll('img[data-img]')"
                  ".forEach(function(i){var s=I[i.getAttribute('data-img')];if(s)i.src=s;});})();</script>")
        html = html.replace(f"\n{js_tag}\n", f"\n{loader}\n{js_tag}\n")
        os.makedirs(PRES, exist_ok=True)
        open(os.path.join(PRES, "praxis-guenther-praesentation.html"), "w", encoding="utf-8").write(html)
    else:
        if os.path.exists(ART):
            shutil.rmtree(ART)
        os.makedirs(ART)
        html = html.replace("<title>Hausarzt Viernheim – Gemeinschaftspraxis Günther, Innere Medizin</title>",
                            "<title>Gemeinschaftspraxis Günther – Entwurf</title>")
        html = bust_assets(html)
        open(os.path.join(ART, "index.html"), "w", encoding="utf-8").write(html)
        used = set(re.findall(r'"assets/img/([\w.-]+)', html))
        for sub in ("css", "js", "fonts"):
            shutil.copytree(os.path.join(ROOT, "assets", sub), os.path.join(ART, "assets", sub),
                            ignore=shutil.ignore_patterns("OFL.txt"))
        os.makedirs(os.path.join(ART, "assets", "img"))
        for f in used:
            shutil.copy(os.path.join(ROOT, "assets", "img", f), os.path.join(ART, "assets", "img", f))


if __name__ == "__main__":
    build_dist()
    build_presentation(inline=True)
    build_presentation(inline=False)
    size = os.path.getsize(os.path.join(PRES, "praxis-guenther-praesentation.html")) // 1024
    print("dist:", sorted(os.listdir(DIST)), "| präsentation:", size, "KB | artefakt:", len(os.listdir(os.path.join(ART, "assets", "img"))), "Bilder")
