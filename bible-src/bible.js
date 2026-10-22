/* Oakencode Bible reader — static, on-device, no tracking. */
(function () {
  "use strict";
  var TRANS = {
    kjv: { name: "King James Version", short: "KJV" },
    web: { name: "World English Bible", short: "WEB" },
    brenton: { name: "Brenton’s Septuagint", short: "Brenton" }
  };
  var TORAH_BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"];
  var app = document.getElementById("app");
  var homeStatic = document.getElementById("home-static");
  var META = null;
  var cache = {};

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function slug(name) { return name.replace(/ /g, "-"); }
  function bookMeta(name) {
    return META.books.find(function (b) { return b.name === name; });
  }
  function loadBook(t, name) {
    var key = t + "/" + name;
    if (!cache[key]) {
      cache[key] = fetch("data/" + t + "/" + slug(name) + ".json").then(function (r) {
        if (!r.ok) throw new Error("load " + key);
        return r.json();
      });
    }
    return cache[key];
  }

  /* ---------- font size ---------- */
  var FS_STEPS = [0.85, 1, 1.15, 1.3, 1.5];
  function fsIdx() {
    var i = parseInt(localStorage.getItem("bible.fsIdx") || "2", 10);
    return isNaN(i) || i < 0 || i >= FS_STEPS.length ? 2 : i;
  }
  function applyFs() {
    document.documentElement.style.setProperty("--fs", FS_STEPS[fsIdx()]);
  }
  function fsButtons() {
    return '<button type="button" class="icon-btn" id="fs-down" aria-label="Smaller text">A−</button>' +
           '<button type="button" class="icon-btn" id="fs-up" aria-label="Larger text">A+</button>';
  }
  function wireFs() {
    var d = document.getElementById("fs-down"), u = document.getElementById("fs-up");
    if (d) d.addEventListener("click", function () {
      localStorage.setItem("bible.fsIdx", Math.max(0, fsIdx() - 1)); applyFs();
    });
    if (u) u.addEventListener("click", function () {
      localStorage.setItem("bible.fsIdx", Math.min(FS_STEPS.length - 1, fsIdx() + 1)); applyFs();
    });
  }

  /* ---------- listen (device speech synthesis) ---------- */
  var listening = false;
  function stopListen() {
    if ("speechSynthesis" in window) window.speechSynthesis.cancel();
    listening = false;
  }
  function wireListen(getText) {
    var btn = document.getElementById("listen-btn");
    if (!btn) return;
    if (!("speechSynthesis" in window)) { btn.disabled = true; btn.textContent = "🔇 Listen unavailable"; return; }
    btn.addEventListener("click", function () {
      if (listening) { stopListen(); btn.textContent = "🔊 Listen"; btn.classList.remove("on"); return; }
      var u = new SpeechSynthesisUtterance(getText());
      u.rate = 0.95;
      u.onend = u.onerror = function () { listening = false; btn.textContent = "🔊 Listen"; btn.classList.remove("on"); };
      listening = true;
      btn.textContent = "⏹ Stop";
      btn.classList.add("on");
      window.speechSynthesis.speak(u);
    });
  }

  /* ---------- psalm chapter mapping, Masoretic (KJV/WEB) <-> Septuagint (Brenton) ---------- */
  function mtToLxx(mt) {
    if (mt <= 8) return [mt];
    if (mt <= 10) return [9];
    if (mt <= 113) return [mt - 1];
    if (mt <= 115) return [113];
    if (mt === 116) return [114, 115];
    if (mt <= 146) return [mt + 1];
    if (mt === 147) return [146, 147];
    return [mt];
  }
  function lxxToMt(lxx) {
    if (lxx <= 8) return [lxx];
    if (lxx === 9) return [9, 10];
    if (lxx <= 112) return [lxx + 1];
    if (lxx === 113) return [114, 115];
    if (lxx === 114 || lxx === 115) return [116];
    if (lxx <= 145) return [lxx + 1];
    if (lxx === 146 || lxx === 147) return [147];
    return [lxx];
  }
  function secondaryChapters(primaryT, secondaryT, bookName, ch) {
    if (bookName !== "Psalms" || !secondaryT) return [ch];
    var pBrenton = primaryT === "brenton", sBrenton = secondaryT === "brenton";
    if (pBrenton === sBrenton) return [ch];
    return pBrenton ? lxxToMt(ch) : mtToLxx(ch);
  }

  /* ---------- shared reader rendering ---------- */
  function chapterVerses(data, chList) {
    /* returns flat [{sep: "Chapter N" | null, v: number, text}] */
    var out = [];
    chList.forEach(function (ch, i) {
      var verses = (data && data.chapters[ch - 1]) || [];
      verses.forEach(function (text, vi) {
        out.push({ sep: chList.length > 1 && vi === 0 ? "Chapter " + ch : null, v: vi + 1, text: text });
      });
    });
    return out;
  }
  function renderCols(primaryRows, secondaryRows, primaryLabel, secondaryLabel, primaryHebrew, secondaryHebrew) {
    function cell(row, hebrew) {
      if (!row) return '<div class="vrow"><span class="vnum"></span><span class="empty">—</span></div>';
      var sep = row.sep ? '<div class="chaptersep">' + esc(row.sep) + "</div>" : "";
      return sep + '<div class="vrow' + (hebrew ? " hebrew" : "") + '">' +
        '<span class="vnum">' + row.v + '</span><span lang="' + (hebrew ? "he" : "en") + '">' + esc(row.text) + "</span></div>";
    }
    if (!secondaryRows) {
      return '<div class="cols"><div class="col"><h3>' + esc(primaryLabel) + "</h3>" +
        primaryRows.map(function (r) { return cell(r, primaryHebrew); }).join("") + "</div></div>";
    }
    var n = Math.max(primaryRows.length, secondaryRows.length), rowsHtml = "";
    for (var i = 0; i < n; i++) rowsHtml += cell(primaryRows[i], primaryHebrew) ;
    var rowsHtml2 = "";
    for (var j = 0; j < n; j++) rowsHtml2 += cell(secondaryRows[j], secondaryHebrew);
    return '<div class="cols two"><div class="col"><h3>' + esc(primaryLabel) + "</h3>" + rowsHtml +
      '</div><div class="col"><h3>' + esc(secondaryLabel) + "</h3>" + rowsHtml2 + "</div></div>";
  }
  function navRow(prev, next) {
    return '<div class="navrow">' +
      (prev ? '<a class="btn ghost" href="' + prev.href + '">← ' + esc(prev.label) + "</a>" : "<span></span>") +
      (next ? '<a class="btn ghost" href="' + next.href + '">' + esc(next.label) + " →</a>" : "<span></span>") + "</div>";
  }
  function neighbor(t, name, ch, avail) {
    var m = bookMeta(name);
    var count = m[t].chapters;
    if (ch > 1) return { book: name, ch: ch - 1, dir: "prev" };
    var idx = META.books.indexOf(m);
    for (var i = idx - 1; i >= 0; i--) {
      if (META.books[i][t]) return { book: META.books[i].name, ch: META.books[i][t].chapters, dir: "prev" };
    }
    return null;
  }
  function neighborNext(t, name, ch) {
    var m = bookMeta(name);
    var count = m[t].chapters;
    if (ch < count) return { book: name, ch: ch + 1, dir: "next" };
    var idx = META.books.indexOf(m);
    for (var i = idx + 1; i < META.books.length; i++) {
      if (META.books[i][t]) return { book: META.books[i].name, ch: 1, dir: "next" };
    }
    return null;
  }

  /* ---------- views ---------- */
  function viewBooks(t) {
    var groups = { OT: [], NT: [] };
    META.books.forEach(function (b) {
      if (b[t]) groups[b.testament].push(b);
    });
    function groupHtml(label, list) {
      if (!list.length) return "";
      return '<div class="bookgroup"><h3>' + label + '</h3><div class="pills">' +
        list.map(function (b) {
          return '<a href="#/chapters/' + t + "/" + encodeURIComponent(b.name) + '">' + esc(b.name) + "</a>";
        }).join("") + "</div></div>";
    }
    app.innerHTML = '<p><a class="backlink" href="#/">← Bible home</a></p>' +
      '<h1 class="view-title">' + esc(TRANS[t].name) + "</h1>" +
      (t === "brenton" ? '<p class="note-bar">The Old Testament in English from the Greek Septuagint. Psalm numbering follows the Greek tradition and differs from the Hebrew in places.</p>' : "") +
      groupHtml("Old Testament", groups.OT) + groupHtml("New Testament", groups.NT);
    window.scrollTo(0, 0);
  }

  function viewChapters(t, name) {
    var m = bookMeta(name);
    if (!m || !m[t]) { app.innerHTML = "<p>That book is not in this collection.</p>"; return; }
    var n = m[t].chapters, cells = "";
    for (var i = 1; i <= n; i++) {
      cells += '<a href="#/read/' + t + "/" + encodeURIComponent(name) + "/" + i + '">' + i + "</a>";
    }
    app.innerHTML = '<p><a class="backlink" href="#/books/' + t + '">← ' + esc(TRANS[t].name) + "</a></p>" +
      '<h1 class="view-title">' + esc(name) + "</h1><p class=\"muted\">Choose a chapter:</p>" +
      '<div class="chapters-grid">' + cells + "</div>";
    window.scrollTo(0, 0);
  }

  function defaultParallel(t) {
    var p = localStorage.getItem("bible.parallel");
    if (p !== null) return p;
    return t === "web" ? "kjv" : "web";
  }

  function viewRead(t, name, ch) {
    var m = bookMeta(name);
    if (!m || !m[t]) { app.innerHTML = "<p>That book is not in this collection.</p>"; return; }
    var parallel = defaultParallel(t);
    if (parallel === t || (parallel && !m[parallel])) parallel = "none";
    app.innerHTML = '<p><a class="backlink" href="#/chapters/' + t + "/" + encodeURIComponent(name) + '">← ' + esc(name) + " chapters</a></p>" +
      '<div class="reader-head"><h1>' + esc(name) + " " + ch + "</h1></div>" +
      '<div class="controls"><label for="par-sel">Read beside:</label>' +
      '<select id="par-sel">' +
      '<option value="none"' + (parallel === "none" ? " selected" : "") + ">Nothing (single column)</option>" +
      Object.keys(TRANS).filter(function (x) { return x !== t && m[x]; }).map(function (x) {
        return '<option value="' + x + '"' + (parallel === x ? " selected" : "") + ">" + esc(TRANS[x].name) + "</option>";
      }).join("") + "</select>" +
      '<span class="spacer"></span>' + fsButtons() +
      '<button type="button" class="icon-btn" id="listen-btn">🔊 Listen</button></div>' +
      '<div id="read-body"><p class="muted">Opening…</p></div>';
    wireFs();
    document.getElementById("par-sel").addEventListener("change", function (e) {
      localStorage.setItem("bible.parallel", e.target.value);
      viewRead(t, name, ch);
    });
    var prev = neighbor(t, name, ch), next = neighborNext(t, name, ch);
    var jobs = [loadBook(t, name)];
    if (parallel !== "none") jobs.push(loadBook(parallel, name));
    Promise.all(jobs).then(function (datas) {
      var primary = chapterVerses(datas[0], [ch]);
      var secondary = null;
      if (parallel !== "none") {
        var chs = secondaryChapters(t, parallel, name, ch);
        secondary = chapterVerses(datas[1], chs);
      }
      var note = "";
      if (name === "Psalms" && parallel !== "none" && (t === "brenton" || parallel === "brenton")) {
        note = '<p class="note-bar">Psalm numbering differs between the Hebrew (Masoretic) and Greek (Septuagint) traditions; chapters here are matched to the same psalm, and verse counts can differ slightly.</p>';
      }
      var body = document.getElementById("read-body");
      if (!body) return;
      body.innerHTML = note + renderCols(primary, secondary, TRANS[t].name, parallel !== "none" ? TRANS[parallel].name : "", false, false) +
        navRow(
          prev ? { href: "#/read/" + t + "/" + encodeURIComponent(prev.book) + "/" + prev.ch, label: prev.book + " " + prev.ch } : null,
          next ? { href: "#/read/" + t + "/" + encodeURIComponent(next.book) + "/" + next.ch, label: next.book + " " + next.ch } : null);
      localStorage.setItem("bible.last", JSON.stringify({ hash: location.hash, label: name + " " + ch + " · " + TRANS[t].short }));
      wireListen(function () {
        return name + ", chapter " + ch + ". " + primary.map(function (r) { return r.text; }).join(" ");
      });
    }).catch(function () {
      var body = document.getElementById("read-body");
      if (body) body.innerHTML = "<p>Sorry — that chapter could not be loaded. Check your connection and try again.</p>";
    });
    window.scrollTo(0, 0);
  }

  function viewTorahHome() {
    var weekName = window.__parashaName || null;
    var byBook = {};
    META.parashiyot.forEach(function (p) { (byBook[p.book] = byBook[p.book] || []).push(p); });
    var portionsHtml = TORAH_BOOKS.map(function (b) {
      var list = byBook[b] || [];
      return '<div class="bookgroup"><h3>' + esc(b) + '</h3><div class="pills">' +
        list.map(function (p) {
          var isWeek = weekName && normName(p.name) === normName(weekName);
          return '<a class="' + (isWeek ? "this-week" : "") + '" href="#/torah/' + encodeURIComponent(b) + "/" + p.start[0] +
            "?p=" + encodeURIComponent(p.name) + "&r=" + encodeURIComponent(p.ref) + '">' +
            p.num + ". " + esc(p.name) + (isWeek ? " · this week" : "") + "</a>";
        }).join("") + "</div></div>";
    }).join("");
    app.innerHTML = '<p><a class="backlink" href="#/">← Bible home</a></p>' +
      '<h1 class="view-title">The Torah</h1>' +
      '<p>The five books of Moses in Hebrew — the Westminster Leningrad Codex — beside the English. Choose a book to read chapter by chapter, or open any of the 54 weekly portions.</p>' +
      '<div class="bookgroup"><h3>Books</h3><div class="pills">' +
      TORAH_BOOKS.map(function (b) {
        return '<a href="#/chapters-torah/' + encodeURIComponent(b) + '">' + esc(b) + "</a>";
      }).join("") + "</div></div>" +
      "<h2 class=\"section-title\">The 54 Portions (Parashiyot)</h2>" + portionsHtml;
    window.scrollTo(0, 0);
  }
  function normName(s) {
    return String(s).toLowerCase().replace(/[’']/g, "").replace(/^parashat /, "").trim();
  }

  function viewTorahChapters(name) {
    var m = bookMeta(name);
    var n = m.wlc.chapters, cells = "";
    for (var i = 1; i <= n; i++) cells += '<a href="#/torah/' + encodeURIComponent(name) + "/" + i + '">' + i + "</a>";
    app.innerHTML = '<p><a class="backlink" href="#/torah">← The Torah</a></p>' +
      '<h1 class="view-title">' + esc(name) + ' <span class="muted">· Hebrew &amp; English</span></h1>' +
      '<div class="chapters-grid">' + cells + "</div>";
    window.scrollTo(0, 0);
  }

  function viewTorah(name, ch, params) {
    var eng = localStorage.getItem("bible.torahEng") || "kjv";
    var m = bookMeta(name);
    var banner = "";
    if (params.get("p")) {
      banner = '<div class="portion-banner"><strong>Parashat ' + esc(params.get("p")) + "</strong>" +
        (params.get("r") ? " · " + esc(params.get("r")) : "") +
        "<br><span class=\"tiny\">You are at the start of the portion; it continues through the chapters that follow.</span></div>";
    }
    app.innerHTML = '<p><a class="backlink" href="#/chapters-torah/' + encodeURIComponent(name) + '">← ' + esc(name) + " chapters</a></p>" +
      '<div class="reader-head"><h1>' + esc(name) + " " + ch + "</h1></div>" + banner +
      '<div class="controls"><label for="eng-sel">English:</label><select id="eng-sel">' +
      '<option value="kjv"' + (eng === "kjv" ? " selected" : "") + ">King James Version</option>" +
      '<option value="web"' + (eng === "web" ? " selected" : "") + ">World English Bible</option></select>" +
      '<span class="spacer"></span>' + fsButtons() +
      '<button type="button" class="icon-btn" id="listen-btn">🔊 Listen</button></div>' +
      '<div id="read-body"><p class="muted">Opening…</p></div>';
    wireFs();
    document.getElementById("eng-sel").addEventListener("change", function (e) {
      localStorage.setItem("bible.torahEng", e.target.value);
      viewTorah(name, ch, params);
    });
    var count = m.wlc.chapters;
    var prev = ch > 1 ? { book: name, ch: ch - 1 } :
      (TORAH_BOOKS.indexOf(name) > 0 ? { book: TORAH_BOOKS[TORAH_BOOKS.indexOf(name) - 1], ch: bookMeta(TORAH_BOOKS[TORAH_BOOKS.indexOf(name) - 1]).wlc.chapters } : null);
    var next = ch < count ? { book: name, ch: ch + 1 } :
      (TORAH_BOOKS.indexOf(name) < TORAH_BOOKS.length - 1 ? { book: TORAH_BOOKS[TORAH_BOOKS.indexOf(name) + 1], ch: 1 } : null);
    Promise.all([loadBook("wlc", name), loadBook(eng, name)]).then(function (datas) {
      var hebrew = chapterVerses(datas[0], [ch]);
      var english = chapterVerses(datas[1], [ch]);
      var body = document.getElementById("read-body");
      if (!body) return;
      body.innerHTML = renderCols(hebrew, english, "Hebrew · Westminster Leningrad Codex", TRANS[eng].name, true, false) +
        navRow(
          prev ? { href: "#/torah/" + encodeURIComponent(prev.book) + "/" + prev.ch, label: prev.book + " " + prev.ch } : null,
          next ? { href: "#/torah/" + encodeURIComponent(next.book) + "/" + next.ch, label: next.book + " " + next.ch } : null);
      localStorage.setItem("bible.last", JSON.stringify({ hash: location.hash, label: name + " " + ch + " · Torah" }));
      wireListen(function () {
        return name + ", chapter " + ch + ". " + english.map(function (r) { return r.text; }).join(" ");
      });
    }).catch(function () {
      var body = document.getElementById("read-body");
      if (body) body.innerHTML = "<p>Sorry — that chapter could not be loaded. Check your connection and try again.</p>";
    });
    window.scrollTo(0, 0);
  }

  function viewSearch(q) {
    app.innerHTML = '<p><a class="backlink" href="#/">← Bible home</a></p>' +
      '<h1 class="view-title">Search</h1>' +
      '<form class="searchbar" id="search-form2"><input id="search-q2" type="search" value="' + esc(q) + '" autocomplete="off">' +
      '<button class="btn" type="submit">Search</button></form>' +
      '<p class="muted" id="search-status">Searching…</p><div id="search-results"></div>';
    document.getElementById("search-form2").addEventListener("submit", function (e) {
      e.preventDefault();
      var v = document.getElementById("search-q2").value.trim();
      if (v) location.hash = "#/search/" + encodeURIComponent(v);
    });
    runSearch(q);
    window.scrollTo(0, 0);
  }

  function snippet(text, q) {
    var idx = text.toLowerCase().indexOf(q.toLowerCase());
    if (idx < 0) return null;
    var start = Math.max(0, idx - 70), end = Math.min(text.length, idx + q.length + 90);
    var raw = (start > 0 ? "…" : "") + text.slice(start, end) + (end < text.length ? "…" : "");
    var re = new RegExp("(" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
    return esc(raw).replace(re, "<mark>$1</mark>");
  }

  function runSearch(q) {
    var status = document.getElementById("search-status");
    var resultsEl = document.getElementById("search-results");
    var translations = ["kjv", "web", "brenton"];
    var results = [], CAP = 150, chain = Promise.resolve();
    META.books.forEach(function (b) {
      translations.forEach(function (t) {
        if (!b[t]) return;
        chain = chain.then(function () {
          if (results.length >= CAP) return null;
          if (status) status.textContent = "Searching " + b.name + " (" + TRANS[t].short + ")… " + results.length + " found";
          return loadBook(t, b.name).then(function (data) {
            data.chapters.forEach(function (verses, ci) {
              verses.forEach(function (text, vi) {
                if (results.length >= CAP) return;
                var sn = snippet(text, q);
                if (sn) results.push({ t: t, book: b.name, ch: ci + 1, v: vi + 1, sn: sn });
              });
            });
          }).catch(function () { return null; });
        });
      });
    });
    chain.then(function () {
      if (status) status.textContent = results.length >= CAP
        ? "Showing the first 150 results — try a longer phrase to narrow it down."
        : results.length + (results.length === 1 ? " result" : " results") + " for “" + q + "”";
      if (resultsEl) {
        resultsEl.innerHTML = results.map(function (r) {
          return '<div class="result"><a class="ref" href="#/read/' + r.t + "/" + encodeURIComponent(r.book) + "/" + r.ch + '">' +
            esc(r.book) + " " + r.ch + ":" + r.v + " · " + TRANS[r.t].short + "</a><p>" + r.sn + "</p></div>";
        }).join("") || '<p class="muted">No matches found. Check the spelling, or try a shorter word.</p>';
      }
    });
  }

  /* ---------- Hebcal: this week's Torah portion ---------- */
  function fillParasha() {
    var body = document.getElementById("parasha-body");
    if (!body) return;
    function f(d) { return d.toISOString().slice(0, 10); }
    var now = new Date(), end = new Date(now.getTime() + 14 * 864e5);
    fetch("https://www.hebcal.com/hebcal?v=1&cfg=json&s=on&start=" + f(now) + "&end=" + f(end))
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var it = (j.items || []).find(function (i) { return i.category === "parashat"; });
        if (!it) { body.textContent = "The calendar did not answer just now — the Torah button below will take you to all 54 portions."; return; }
        var name = it.title.replace(/^Parashat /, "");
        window.__parashaName = name;
        var torah = (it.leyning && it.leyning.torah) || "";
        var haft = (it.leyning && it.leyning.haftarah) || "";
        var mm = torah.match(/^(.+?) (\d+):\d+/);
        var d = new Date(it.date + "T12:00:00");
        var when = d.toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric", year: "numeric" });
        body.innerHTML = "<strong>" + esc(it.title) + "</strong>" +
          (it.hebrew ? ' <span lang="he" dir="rtl">' + esc(it.hebrew) + "</span>" : "") + "<br>" +
          esc(torah.replace("-", "–")) + (haft ? " · Haftarah: " + esc(haft.replace("-", "–")) : "") + "<br>" +
          '<span class="muted">Read this ' + esc(when) + ".</span>" +
          (mm ? '<p><a class="btn" href="#/torah/' + encodeURIComponent(mm[1]) + "/" + mm[2] +
            "?p=" + encodeURIComponent(name) + "&r=" + encodeURIComponent(torah.replace("-", "–")) + '">Read the portion — Hebrew &amp; English</a></p>' : "");
      })
      .catch(function () {
        body.textContent = "The calendar could not be reached (you may be offline) — the Torah button below will take you to all 54 portions.";
      });
  }

  /* ---------- router ---------- */
  function route() {
    stopListen();
    var hash = location.hash || "#/";
    var raw = hash.slice(2);
    var qIdx = raw.indexOf("?");
    var path = qIdx >= 0 ? raw.slice(0, qIdx) : raw;
    var params = new URLSearchParams(qIdx >= 0 ? raw.slice(qIdx + 1) : "");
    var parts = path.split("/").map(decodeURIComponent);
    var isHome = path === "" || path === "/";
    homeStatic.style.display = isHome ? "" : "none";
    if (isHome) { app.innerHTML = ""; fillParasha(); fillContinue(); return; }
    if (!META) { app.innerHTML = '<p class="muted">Loading the library…</p>'; return; }
    if (parts[0] === "books" && TRANS[parts[1]]) viewBooks(parts[1]);
    else if (parts[0] === "chapters" && TRANS[parts[1]]) viewChapters(parts[1], parts[2]);
    else if (parts[0] === "read" && TRANS[parts[1]]) viewRead(parts[1], parts[2], parseInt(parts[3], 10) || 1);
    else if (parts[0] === "torah" && parts.length === 1) viewTorahHome();
    else if (parts[0] === "chapters-torah") viewTorahChapters(parts[1]);
    else if (parts[0] === "torah") viewTorah(parts[1], parseInt(parts[2], 10) || 1, params);
    else if (parts[0] === "search") viewSearch(parts.slice(1).join("/"));
    else { app.innerHTML = '<p><a href="#/">← Bible home</a></p><p>That page is not here — the button above will take you home.</p>'; }
  }
  function fillContinue() {
    try {
      var last = JSON.parse(localStorage.getItem("bible.last") || "null");
      var row = document.getElementById("continue-row");
      var link = document.getElementById("continue-link");
      if (last && row && link) {
        link.href = last.hash;
        link.textContent = "Continue reading — " + last.label;
        row.hidden = false;
      }
    } catch (e) { /* private mode etc. */ }
  }

  /* ---------- boot ---------- */
  applyFs();
  var sf = document.getElementById("search-form");
  if (sf) sf.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = document.getElementById("search-q").value.trim();
    if (v) location.hash = "#/search/" + encodeURIComponent(v);
  });
  fetch("data/books.json").then(function (r) { return r.json(); }).then(function (m) {
    META = m;
    route();
  }).catch(function () {
    app.innerHTML = "<p>The library could not be loaded — please check your connection and refresh.</p>";
  });
  window.addEventListener("hashchange", route);
  route();
})();
