/* Gemeinschaftspraxis Günther – Interaktionen (ohne Abhängigkeiten), Deutsch · Englisch · Türkisch */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  /* ------------------------------------------------------------------
     Praxisdaten – an EINER Stelle pflegen
     ------------------------------------------------------------------ */
  var HOURS = { 1: [[9, 11], [16, 18]], 2: [[9, 11], [16, 18]], 3: [[9, 11]], 4: [[9, 11], [16, 18]], 5: [[9, 13]] };
  var LAB = { 1: [8, 9], 2: [8, 9], 3: [8, 9], 4: [8, 9], 5: [8, 9] };
  var CLOSED = [
    { from: "2026-12-28", to: "2026-12-31", label: {
      de: "Praxisurlaub – die Vertretung nennt Ihnen unser Anrufbeantworter",
      en: "Holiday closure – our answering machine will tell you who is covering",
      tr: "Tatil – yerimize bakan muayenehaneyi telesekreterimiz bildirir" } }
  ];
  var HOLIDAYS = {
    "2026-12-25": { de: "1. Weihnachtsfeiertag", en: "Christmas Day", tr: "Noel (resmî tatil)" },
    "2026-12-26": { de: "2. Weihnachtsfeiertag", en: "Boxing Day (public holiday)", tr: "Noel’in ikinci günü (resmî tatil)" },
    "2027-01-01": { de: "Neujahr", en: "New Year’s Day", tr: "Yılbaşı" }
  };

  /* ------------------------------------------------------------------
     Texte je Sprache
     ------------------------------------------------------------------ */
  var T = {
    de: {
      days: ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
      tomorrow: "morgen",
      t: function (h) { var hh = Math.floor(h), mm = Math.round((h - hh) * 60); return hh + (mm ? ":" + String(mm).padStart(2, "0") : "") + " Uhr"; },
      range: function (a, b) { return T.de.t(a).replace(" Uhr", "") + "–" + T.de.t(b); },
      openUntil: function (t) { return "Jetzt geöffnet – bis " + t; },
      againToday: function (r) { return "Heute noch einmal " + r; },
      callUs: "Rufen Sie gern an: 06204\u00a037\u00a004",
      closedToday: "Heute geschlossen",
      backOn: function (d, t) { return ". Wieder da: " + d + " ab " + t; },
      lab: function (t) { return "Blutabnahme läuft – Sprechstunde ab " + t; },
      labMore: "Blutabnahme Montag bis Freitag, 8 bis 9 Uhr",
      lunch: function (t) { return "Mittagspause – ab " + t + " geöffnet"; },
      laterToday: function (t) { return "Heute ab " + t + " geöffnet"; },
      bookNow: "Termin jetzt schon online anfragen",
      closedNow: function (d, t) { return "Gerade geschlossen" + (d ? " – " + d + " ab " + t : ""); },
      urgent: "Dringend? Ärztlicher Bereitschaftsdienst 116\u00a0117. Bei Lebensgefahr 112.",
      copied: "Kopiert", menu: "Menü", close: "Schließen",
      v: { flu: "Grippe", covid: "Corona", rsv: "RSV", pneu: "Pneumokokken", shingles: "Gürtelrose", td: "Tetanus und Diphtherie",
           yearlyNow: "jährlich, am besten jetzt", yearly: "jährlich", indiv: "individuell besprechen", once: "einmalig",
           standard: "Standardimpfung", someCond: "bei bestimmten Vorerkrankungen", two: "2 Impfungen",
           from18: "ab 18 bei erhöhtem Risiko", every10: "alle 10 Jahre auffrischen" }
    },
    en: {
      days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      tomorrow: "tomorrow",
      t: function (h) { var hh = Math.floor(h), mm = Math.round((h - hh) * 60), ap = hh < 12 ? "am" : "pm", h12 = hh % 12 || 12; return h12 + (mm ? ":" + String(mm).padStart(2, "0") : "") + " " + ap; },
      range: function (a, b) { return T.en.t(a) + "–" + T.en.t(b); },
      openUntil: function (t) { return "Open now – until " + t; },
      againToday: function (r) { return "Open again today " + r; },
      callUs: "Feel free to call: 06204\u00a037\u00a004",
      closedToday: "Closed today",
      backOn: function (d, t) { return ". Back " + d + " from " + t; },
      lab: function (t) { return "Blood tests now – consultations from " + t; },
      labMore: "Blood tests Monday to Friday, 8 to 9 am",
      lunch: function (t) { return "Lunch break – open again from " + t; },
      laterToday: function (t) { return "Open today from " + t; },
      bookNow: "You can already request an appointment online",
      closedNow: function (d, t) { return "Closed right now" + (d ? " – open " + d + " from " + t : ""); },
      urgent: "Urgent? Out-of-hours medical service 116\u00a0117. Life-threatening: 112.",
      copied: "Copied", menu: "Menu", close: "Close",
      v: { flu: "Flu", covid: "COVID-19", rsv: "RSV", pneu: "Pneumococcus", shingles: "Shingles", td: "Tetanus and diphtheria",
           yearlyNow: "every year, ideally now", yearly: "every year", indiv: "to be discussed individually", once: "once",
           standard: "standard vaccination", someCond: "with certain pre-existing conditions", two: "2 doses",
           from18: "from 18 if at increased risk", every10: "booster every 10 years" }
    },
    tr: {
      days: ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"],
      tomorrow: "yarın",
      t: function (h) { var hh = Math.floor(h), mm = Math.round((h - hh) * 60); return hh + "." + String(mm).padStart(2, "0"); },
      range: function (a, b) { return T.tr.t(a) + "–" + T.tr.t(b); },
      openUntil: function (t) { return "Şu an açık – kapanış saati " + t; },
      againToday: function (r) { return "Bugün tekrar " + r; },
      callUs: "Bizi arayabilirsiniz: 06204\u00a037\u00a004",
      closedToday: "Bugün kapalı",
      backOn: function (d, t) { return ". Tekrar açık: " + d + ", saat " + t; },
      lab: function (t) { return "Kan alma saati – muayene başlangıcı " + t; },
      labMore: "Kan alma pazartesiden cumaya, saat 8–9",
      lunch: function (t) { return "Öğle arası – açılış saati " + t; },
      laterToday: function (t) { return "Bugün açılış saati " + t; },
      bookNow: "Randevu talebinizi şimdiden gönderebilirsiniz",
      closedNow: function (d, t) { return "Şu an kapalı" + (d ? " – açılış: " + d + ", saat " + t : ""); },
      urgent: "Acil mi? Nöbetçi doktor 116\u00a0117. Hayati tehlikede 112.",
      copied: "Kopyalandı", menu: "Menü", close: "Kapat",
      v: { flu: "Grip", covid: "Covid-19", rsv: "RSV", pneu: "Pnömokok", shingles: "Zona", td: "Tetanoz ve difteri",
           yearlyNow: "her yıl, en iyisi şimdi", yearly: "her yıl", indiv: "kişiye özel değerlendirilir", once: "tek doz",
           standard: "standart aşı", someCond: "belirli kronik hastalıklarda", two: "2 doz",
           from18: "risk varsa 18 yaştan itibaren", every10: "10 yılda bir rapel" }
    }
  };
  function langOf(el) {
    var c = el && el.closest ? el.closest("[data-lang],[data-chrome]") : null;
    var l = c ? (c.getAttribute("data-lang") || c.getAttribute("data-chrome")) : document.documentElement.lang;
    l = (l || "de").slice(0, 2);
    return T[l] ? l : "de";
  }

  /* ------------------------------------------------------------------
     Uhrzeit in Viernheim (Europe/Berlin)
     ------------------------------------------------------------------ */
  function berlinNow() {
    var parts = new Intl.DateTimeFormat("de-DE", {
      timeZone: "Europe/Berlin", year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", hourCycle: "h23"
    }).formatToParts(new Date());
    var o = {};
    parts.forEach(function (p) { o[p.type] = p.value; });
    var d = new Date(Date.UTC(+o.year, +o.month - 1, +o.day));
    return { date: d, iso: o.year + "-" + o.month + "-" + o.day, dow: d.getUTCDay(), h: +o.hour + (+o.minute) / 60 };
  }
  var forced = null;
  try { forced = new URLSearchParams(location.search).get("jetzt"); } catch (e) { forced = null; } // z. B. ?jetzt=2026-11-23T09:30
  function now() {
    if (forced) {
      var m = forced.match(/(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
      if (m) {
        var d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
        return { date: d, iso: m[1] + "-" + m[2] + "-" + m[3], dow: d.getUTCDay(), h: +m[4] + (+m[5]) / 60 };
      }
    }
    return berlinNow();
  }
  function isoOf(d) { return d.toISOString().slice(0, 10); }
  function closure(iso, l) {
    if (HOLIDAYS[iso]) return HOLIDAYS[iso][l];
    for (var i = 0; i < CLOSED.length; i++) if (iso >= CLOSED[i].from && iso <= CLOSED[i].to) return CLOSED[i].label[l];
    return null;
  }
  function slots(d) { return closure(isoOf(d), "de") ? [] : (HOURS[d.getUTCDay()] || []); }
  function nextOpen(n, l) {
    var L = T[l];
    for (var i = 1; i < 21; i++) {
      var d = new Date(n.date.getTime() + i * 864e5);
      var s = slots(d);
      if (s.length) {
        var name = i === 1 ? L.tomorrow : (i < 7 ? L.days[d.getUTCDay()] : L.days[d.getUTCDay()] + ", " + d.getUTCDate() + "." + (d.getUTCMonth() + 1) + ".");
        return { label: name, start: s[0][0] };
      }
    }
    return null;
  }

  function computeStatus(l) {
    var L = T[l], n = now(), today = slots(n.date), why = closure(n.iso, l), lab = !why && LAB[n.dow];
    var r = { open: false, text: "", more: "" };
    for (var i = 0; i < today.length; i++) {
      if (n.h >= today[i][0] && n.h < today[i][1]) {
        r.open = true;
        r.text = L.openUntil(L.t(today[i][1]));
        r.more = today[i + 1] ? L.againToday(L.range(today[i + 1][0], today[i + 1][1])) : L.callUs;
        return r;
      }
    }
    var later = today.filter(function (s) { return s[0] > n.h; })[0];
    var nx = nextOpen(n, l);
    if (why) {
      r.text = L.closedToday;
      r.more = why + (nx ? L.backOn(nx.label, L.t(nx.start)) : "");
    } else if (lab && n.h >= lab[0] && n.h < lab[1]) {
      r.open = true;
      r.text = L.lab(L.t(later ? later[0] : 9));
      r.more = L.labMore;
    } else if (later) {
      r.text = today[0][0] < n.h ? L.lunch(L.t(later[0])) : L.laterToday(L.t(later[0]));
      r.more = L.bookNow;
    } else {
      r.text = L.closedNow(nx && nx.label, nx && L.t(nx.start));
      r.more = L.urgent;
    }
    return r;
  }

  function renderStatus() {
    var cache = {};
    function st(l) { return cache[l] || (cache[l] = computeStatus(l)); }
    document.querySelectorAll("[data-status]").forEach(function (el) {
      var s = st(langOf(el));
      el.classList.toggle("is-open", s.open);
      var t = el.querySelector("[data-status-text]"), m = el.querySelector("[data-status-more]");
      if (t) t.textContent = s.text;
      if (m) m.textContent = s.more;
    });
    // Licht an = Praxis offen: das G im Hero leuchtet, im Haus im Fuß gehen die Fenster an
    document.querySelectorAll("[data-light]").forEach(function (el) {
      el.classList.toggle("is-open", st(langOf(el)).open);
    });
    // Kontextabhängige Haupt-Aktion: offen → anrufen, geschlossen → online anfragen
    document.querySelectorAll("[data-cta-swap]").forEach(function (box) {
      var s = st(langOf(box));
      var call = box.querySelector('[data-cta="call"]'), book = box.querySelector('[data-cta="book"]');
      if (!call || !book) return;
      call.classList.toggle("btn--primary", s.open);
      book.classList.toggle("btn--primary", !s.open);
      if (s.open) box.insertBefore(call, book); else box.insertBefore(book, call);
    });
    // Sprechzeiten: heutigen Tag markieren
    var n = now();
    document.querySelectorAll(".times tr[data-dow]").forEach(function (row) {
      var days = row.getAttribute("data-dow").split(" ").map(Number);
      row.classList.toggle("is-today", days.indexOf(n.dow) > -1);
    });
  }
  renderStatus();
  setInterval(renderStatus, 60000);

  /* ------------------------------------------------------------------
     Impf-Check nach STIKO 2026 (je Sprache ein Widget)
     ------------------------------------------------------------------ */
  document.querySelectorAll("[data-vacc]").forEach(function (vacc) {
    var V = T[langOf(vacc)].v, state = { age: "60", risk: false };
    var out = vacc.querySelector("[data-vacc-out]");
    function list() {
      var a = state.age, r = state.risk, L = [];
      var s60 = a === "60" || a === "75";
      if (s60 || r) L.push([V.flu, V.yearlyNow]);
      if (a === "75") L.push([V.covid, V.yearly]);
      else if (r) L.push([V.covid, V.indiv]);
      if (a === "75" || (a === "60" && r)) L.push([V.rsv, V.once]);
      if (s60) L.push([V.pneu, V.standard]);
      else if (r) L.push([V.pneu, V.someCond]);
      if (s60) L.push([V.shingles, V.two]);
      else if (r) L.push([V.shingles, V.from18]);
      L.push([V.td, V.every10, true]);
      out.innerHTML = L.map(function (x) {
        return '<li class="' + (x[2] ? "is-grey" : "") + '"><b>' + x[0] + "</b><span>" + x[1] + "</span></li>";
      }).join("");
    }
    vacc.querySelectorAll("[data-age]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.age = b.getAttribute("data-age");
        vacc.querySelectorAll("[data-age]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        list();
      });
    });
    var rk = vacc.querySelector("[data-risk]");
    if (rk) rk.addEventListener("change", function () { state.risk = rk.checked; list(); });
    list();
  });

  /* ------------------------------------------------------------------
     Kopf: Menü, Schatten, Sprachwahl
     ------------------------------------------------------------------ */
  var headers = document.querySelectorAll(".site-header");
  headers.forEach(function (h) {
    var nav = h.querySelector(".nav"), mb = h.querySelector(".menu-btn");
    if (!nav || !mb) return;
    var L = T[langOf(h)];
    function set(o) {
      nav.classList.toggle("is-open", o);
      mb.setAttribute("aria-expanded", String(o));
      mb.setAttribute("aria-label", o ? L.close : L.menu);
    }
    mb.addEventListener("click", function () { set(!nav.classList.contains("is-open")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) set(false); });
  });
  // Logo im Kopf: beim Öffnen groß und dicht über der Hero-Überschrift. Beim Scrollen fährt zuerst nur das Logo
  // nach oben und skaliert auf seine Endgröße in der Kopfzeile – die Seite steht so lange still (--pin);
  // erst wenn das Logo angekommen ist, scrollt die Seite. Seiten ohne Hero: Logo steht oben und skaliert
  // in den ersten 160 px Scrollweg.
  var root = document.documentElement, ticking = false, drop = 0, shrink = 0;
  function visibleEl(sel) {
    var l = document.querySelectorAll(sel);
    for (var i = 0; i < l.length; i++) if (l[i].offsetParent) return l[i];
    return null;
  }
  function onScroll() {
    var y = Math.max(window.scrollY, 0);
    headers.forEach(function (h) { h.classList.toggle("is-scrolled", y > 8); });
    var hs = drop > 0 ? Math.min(y / drop, 1) : Math.min(y / 160, 1);
    root.style.setProperty("--hs", hs.toFixed(3));
    root.style.setProperty("--lift", Math.max(drop - y, 0).toFixed(1) + "px");
    root.style.setProperty("--pin", drop > 0 ? (Math.min(y, drop) + hs * shrink).toFixed(1) + "px" : "0px");
    ticking = false;
  }
  function measureLogo() {
    var h1 = visibleEl(".hero h1"), logo = visibleEl(".site-header .wm--head .wm__logo"), head = visibleEl(".site-header");
    drop = 0; shrink = 0;
    root.style.setProperty("--pin", "0px");
    if (h1 && logo && head) {
      root.style.setProperty("--lift", "0px");
      root.style.setProperty("--hs", "1");
      var headEnd = head.offsetHeight;
      root.style.setProperty("--hs", "0");
      shrink = Math.max(0, head.offsetHeight - headEnd);
      var fs = parseFloat(getComputedStyle(h1).fontSize) || 40;
      var gap = Math.max(14, fs * 0.35);
      var h1Top = h1.getBoundingClientRect().top + window.scrollY;
      var logoBottom = logo.getBoundingClientRect().bottom; // Kopf ist sticky und steht immer oben
      drop = Math.max(0, Math.round(h1Top - gap - logoBottom));
    }
    root.classList.toggle("has-pin", drop > 0);
    onScroll();
  }
  function remeasure() { requestAnimationFrame(measureLogo); }
  // Sprungziele auf der Startseite: Position so berechnen, wie sie nach der Logo-Phase steht (--pin voll)
  function scrollToEl(el, smooth) {
    var pin = parseFloat(root.style.getPropertyValue("--pin")) || 0;
    var hs = parseFloat(root.style.getPropertyValue("--hs")) || 0;
    var pad = parseFloat(getComputedStyle(root).scrollPaddingTop) || 0;
    // Position im Ausgangszustand (Kopf groß, nichts verschoben) + Logo-Phase − Scroll-Abstand
    var top = el.getBoundingClientRect().top + window.scrollY - pin + hs * shrink + drop - pad;
    window.scrollTo({ top: Math.max(0, top), behavior: smooth ? "smooth" : "instant" });
  }
  function fixHash() {
    if (!(drop > 0) || !location.hash) return;
    var el = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (el && el.offsetParent) scrollToEl(el, false);
  }
  function remeasureFix() { requestAnimationFrame(function () { measureLogo(); fixHash(); }); }
  document.addEventListener("click", function (e) {
    if (!(drop > 0) || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href*="#"]');
    if (!a || a.hasAttribute("data-open")) return;
    var url = new URL(a.getAttribute("href"), location.href);
    if (url.pathname !== location.pathname || url.search !== location.search || url.hash.length < 2) return;
    var el = document.getElementById(decodeURIComponent(url.hash.slice(1)));
    if (!el || !el.offsetParent) return;
    e.preventDefault();
    scrollToEl(el, true);
    if (history.pushState) history.pushState(null, "", url.hash);
  });
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener("resize", remeasure);
  window.addEventListener("hashchange", remeasureFix);
  window.addEventListener("load", remeasureFix);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);
  onScroll();
  remeasure();
  document.addEventListener("click", function (e) {
    document.querySelectorAll("details.lang[open]").forEach(function (d) {
      if (!d.contains(e.target) || e.target.closest("a")) d.removeAttribute("open");
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.querySelectorAll("details.lang[open]").forEach(function (d) { d.removeAttribute("open"); d.querySelector("summary").focus(); });
  });

  /* ------------------------------------------------------------------
     Dialoge: Termin anfragen / Folgerezept (Prototyp – sendet nichts)
     ------------------------------------------------------------------ */
  function dialogFor(name, l) {
    return document.querySelector('dialog[data-dlg="' + name + '"][data-lang="' + l + '"]') ||
           document.querySelector('dialog[data-dlg="' + name + '"]');
  }
  document.addEventListener("click", function (e) {
    var op = e.target.closest("[data-open]");
    if (op) {
      var d = dialogFor(op.getAttribute("data-open"), langOf(op));
      if (d && d.showModal) {
        e.preventDefault();
        d.querySelector("form").hidden = false;
        var dn = d.querySelector(".done"); if (dn) dn.hidden = true;
        try { d.showModal(); } catch (err) { d.setAttribute("open", ""); }
      }
    }
    var cl = e.target.closest("[data-close]");
    if (cl) { var dd = cl.closest("dialog"); if (dd) dd.close(); }
  });
  document.querySelectorAll("dialog.dlg").forEach(function (d) {
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
    var f = d.querySelector("form");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      f.hidden = true;
      var dn = d.querySelector(".done");
      if (dn) { dn.hidden = false; var h = dn.querySelector("h3"); if (h) h.focus(); }
      f.reset();
      d.querySelectorAll("[data-akut],[data-impf]").forEach(function (x) { x.hidden = true; });
    });
    f.addEventListener("change", function (e) {
      if (e.target.name === "anliegen") {
        d.querySelectorAll("[data-akut]").forEach(function (x) { x.hidden = e.target.value !== "akut"; });
        d.querySelectorAll("[data-impf]").forEach(function (x) { x.hidden = e.target.value !== "impfung"; });
      }
    });
  });

  /* Adresse kopieren */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var txt = b.getAttribute("data-copy"), o = b.textContent;
      var done = function () { b.textContent = T[langOf(b)].copied; setTimeout(function () { b.textContent = o; }, 1600); };
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, done);
        else done();
      } catch (err) { done(); }
    });
  });

  /* ------------------------------------------------------------------
     FAQ: Live-Suche (je FAQ-Seite getrennt)
     ------------------------------------------------------------------ */
  document.querySelectorAll("[data-faq-search]").forEach(function (search) {
    var scope = search.closest("[data-route]") || document;
    var qs = Array.prototype.slice.call(scope.querySelectorAll(".q"));
    var groups = scope.querySelectorAll(".faq-group");
    var empty = scope.querySelector(".empty");
    var norm = function (s) { return s.toLocaleLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ı/g, "i"); };
    var idx = qs.map(function (q) { return norm(q.textContent); });
    search.addEventListener("input", function () {
      var v = norm(search.value.trim()), words = v.split(/\s+/).filter(Boolean), hits = 0;
      qs.forEach(function (q, i) {
        var ok = words.every(function (w) { return idx[i].indexOf(w) > -1; });
        q.classList.toggle("is-hidden", !ok);
        if (ok) hits++;
        if (words.length && v.length > 2) q.open = ok; else if (!words.length) q.open = false;
      });
      groups.forEach(function (g) { g.classList.toggle("is-hidden", !g.querySelector(".q:not(.is-hidden)")); });
      if (empty) empty.classList.toggle("is-visible", hits === 0);
    });
  });
  function openFromHash() {
    var id = decodeURIComponent(location.hash.replace(/^#/, ""));
    var el = id && document.getElementById(id);
    if (el && el.tagName === "DETAILS") el.open = true;
  }
  window.addEventListener("hashchange", openFromHash);
  openFromHash();

  /* ------------------------------------------------------------------
     Präsentationsmodus: alle Seiten und Sprachen in einer Datei.
     Routen sind einfache Hash-Namen: #start, #faq, #en, #en-faq, #tr-evelyne …
     ------------------------------------------------------------------ */
  var routes = document.querySelectorAll("[data-route]");
  if (routes.length > 1) {
    var current = null;
    var show = function () {
      var h = decodeURIComponent(location.hash.replace(/^#/, "")), name = null, target = null;
      if (h && document.querySelector('[data-route="' + h + '"]')) name = h;
      else if (h) {
        var el = document.getElementById(h);
        if (el) {
          var r = el.closest("[data-route]");
          if (r) { name = r.getAttribute("data-route"); target = el; }
          else { el.focus && el.focus(); return; }
        }
      }
      if (!name) { if (current) return; name = "start"; }
      var route = document.querySelector('[data-route="' + name + '"]');
      var lang = route.getAttribute("data-lang"), page = route.getAttribute("data-page");
      var changed = name !== current;
      routes.forEach(function (r) { r.hidden = r !== route; });
      document.querySelectorAll("[data-chrome]").forEach(function (c) { c.hidden = c.getAttribute("data-chrome") !== lang; });
      document.documentElement.lang = lang;
      document.querySelectorAll(".nav__link").forEach(function (a) {
        if (a.getAttribute("data-page") === "faq" && page === "faq") a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
      });
      document.querySelectorAll("details.lang[open]").forEach(function (d) { d.removeAttribute("open"); });
      if (route.getAttribute("data-title")) document.title = route.getAttribute("data-title");
      current = name;
      if (target) { if (target.tagName === "DETAILS") target.open = true; target.scrollIntoView(); }
      else if (changed) window.scrollTo(0, 0);
      renderStatus();
    };
    window.addEventListener("hashchange", show);
    show();
  }

  document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = String(new Date().getFullYear()); });
})();
