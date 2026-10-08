import json, html
from problems import P

data = []
for sid, title, sub, cue, rows in P:
    probs = []
    for r in rows:
        num, t, slug, d, src = r[:5]
        probs.append({"n": num, "t": t, "s": slug, "d": d,
                      "nc": "n" in src, "g75": "g" in src, "book": "b" in src,
                      "premium": len(r) > 5})
    data.append({"id": sid, "title": title, "sub": sub, "cue": cue, "problems": probs})

json.dump(data, open("problems.json", "w"), indent=1)

page = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interview Practice Set</title>
<meta name="description" content="Coding interview practice problems grouped by pattern, from NeetCode 150, Grind 75 and the Coding Interview Refresher book, with LeetCode links and a progress tracker.">
<style>
:root{--bg:#fbfaf7;--card:#ffffff;--ink:#1d1d1f;--muted:#6b6b70;--line:#e4e2dc;--accent:#2563eb;--accent-ink:#fff;
 --easy:#1a7f4b;--easy-bg:#e3f5ea;--med:#b45309;--med-bg:#fdf0dc;--hard:#b91c1c;--hard-bg:#fde4e4;--done:#9a9aa0}
@media (prefers-color-scheme: dark){:root{--bg:#141416;--card:#1e1e22;--ink:#ececf0;--muted:#9a9aa3;--line:#2e2e34;--accent:#60a5fa;--accent-ink:#0b0b0d;
 --easy:#4ade80;--easy-bg:#14301f;--med:#fbbf24;--med-bg:#3a2a0d;--hard:#f87171;--hard-bg:#3a1414;--done:#6b6b72}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:28px 16px 80px}
header h1{font-size:28px;margin:0 0 6px}
header p{margin:0 0 14px;color:var(--muted)}
.bar{position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:5;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.bar .grow{flex:1 1 auto}
.chip{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:4px 12px;font-size:14px;cursor:pointer}
.chip.on{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.prog{font-size:14px;color:var(--muted);white-space:nowrap}
nav.toc{display:flex;flex-wrap:wrap;gap:6px 14px;margin:16px 0 8px;font-size:14px}
nav.toc a{color:var(--accent);text-decoration:none}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:18px 0}
section h2{font-size:20px;margin:0}
section .sub{color:var(--muted);font-size:13px;margin:2px 0 8px}
section .cue{margin:0 0 12px;padding:10px 12px;border-left:3px solid var(--accent);background:var(--bg);border-radius:0 8px 8px 0;font-size:15px}
section .cue b{color:var(--accent)}
ul{list-style:none;margin:0;padding:0}
li{display:flex;align-items:center;gap:10px;padding:7px 0;border-top:1px solid var(--line)}
li:first-child{border-top:0}
li input{width:18px;height:18px;flex:none;accent-color:var(--accent);cursor:pointer}
li a{color:var(--ink);text-decoration:none;flex:1 1 auto}
li a:hover{text-decoration:underline}
li.done a{color:var(--done);text-decoration:line-through}
.num{color:var(--muted);font-variant-numeric:tabular-nums;min-width:3.2em;font-size:14px}
.tag{font-size:11px;padding:1px 7px;border-radius:999px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.d{font-size:12px;padding:1px 8px;border-radius:999px;font-weight:600;white-space:nowrap}
.d.E{color:var(--easy);background:var(--easy-bg)}.d.M{color:var(--med);background:var(--med-bg)}.d.H{color:var(--hard);background:var(--hard-bg)}
.count{float:right;font-size:13px;color:var(--muted)}
footer{color:var(--muted);font-size:13px;margin-top:30px}
footer a{color:var(--accent)}
.hidden{display:none}
.sync{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:center;margin:10px 0 18px;font-size:13px;color:var(--mute)}
.sync .lnk{background:none;border:0;padding:0;color:var(--acc);font:inherit;font-size:13px;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.sync .msg{font-size:12px;color:var(--mute)}
@media (max-width:520px){.tag.src{display:none}}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>Interview practice set</h1>
<p>Problems grouped by the same patterns as the <em>Coding Interview Refresher</em> book and video. Every problem links to LeetCode. Tick a box when you have solved it from a blank file; progress is saved in this browser, and the sync links below carry it to another device.</p>
<p><a href="eval/">Eval study notes</a>: the statistics and engineering of LLM evaluation, with the eval explainer videos.</p>
</header>

<div class="bar">
 <button class="chip on" data-f="all">All</button>
 <button class="chip" data-f="nc">NeetCode 150</button>
 <button class="chip" data-f="g75">Grind 75</button>
 <button class="chip" data-f="book">Book picks</button>
 <span class="grow"></span>
 <button class="chip" data-d="E">Easy</button>
 <button class="chip" data-d="M">Medium</button>
 <button class="chip" data-d="H">Hard</button>
 <span class="prog" id="prog"></span>
</div>
<div class="sync">
 <span class="lbl">Sync across devices:</span>
 <button class="lnk" id="copylink">Copy progress link</button>
 <button class="lnk" id="export">Export file</button>
 <button class="lnk" id="import">Import file</button>
 <input type="file" id="importfile" accept="application/json,.json" hidden>
 <span class="msg" id="msg"></span>
</div>

<nav class="toc" id="toc"></nav>
<div id="root"></div>

<footer>
<p><b>How to use it.</b> Start with the four patterns in the sample video, in order. For each problem: read it, say the cue out loud, write the plan in two lines, then code it with a timer. If you needed the solution, come back to it two days later.</p>
<p>Sources: <a href="https://neetcode.io/practice">NeetCode 150</a>, <a href="https://www.techinterviewhandbook.org/grind75/">Grind 75</a>, and the book's own picks. Problems marked <span class="tag">premium</span> need a LeetCode subscription; a free near-equivalent is usually in the same section. Difficulty labels are LeetCode's.</p>
</footer>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
 var data = JSON.parse(document.getElementById('data').textContent);
 var KEY = 'practice-done-v1';
 var done = {};
 try { done = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e) {}
 var filt = 'all', diff = null;

 var root = document.getElementById('root'), toc = document.getElementById('toc');
 function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;'); }
 data.forEach(function(sec){
  var a = document.createElement('a'); a.href = '#' + sec.id; a.textContent = sec.title; toc.appendChild(a);
  var s = document.createElement('section'); s.id = sec.id;
  var h = '<span class="count" data-count></span><h2>' + esc(sec.title) + '</h2><div class="sub">' + esc(sec.sub) + '</div>' +
          '<p class="cue"><b>Cue.</b> ' + esc(sec.cue) + '</p><ul>';
  sec.problems.forEach(function(p){
   var tags = '';
   if (p.nc) tags += '<span class="tag src">NC150</span>';
   if (p.g75) tags += '<span class="tag src">G75</span>';
   if (p.book) tags += '<span class="tag src">book</span>';
   if (p.premium) tags += '<span class="tag">premium</span>';
   h += '<li data-n="' + p.n + '" data-nc="' + p.nc + '" data-g75="' + p.g75 + '" data-book="' + p.book + '" data-d="' + p.d + '">' +
        '<input type="checkbox" aria-label="done">' +
        '<span class="num">' + p.n + '</span>' +
        '<a href="https://leetcode.com/problems/' + p.s + '/" target="_blank" rel="noopener">' + esc(p.t) + '</a>' +
        tags + '<span class="d ' + p.d + '">' + {E:'Easy',M:'Medium',H:'Hard'}[p.d] + '</span></li>';
  });
  h += '</ul>';
  s.innerHTML = h; root.appendChild(s);
 });

 // ---- progress sync: a URL fragment "#p=<base64url bitmask>" or a JSON file ----
 var order = [];
 data.forEach(function(sec){ sec.problems.forEach(function(p){ order.push(String(p.n)); }); });
 var B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
 function save(){ try { localStorage.setItem(KEY, JSON.stringify(done)); } catch(err) {} }
 function solvedList(){ return Object.keys(done).filter(function(n){ return done[n]; }).map(Number).sort(function(a,b){return a-b;}); }
 function encode(){
  var bytes = [], i, j;
  for (i = 0; i < order.length; i += 8) {
   var b = 0;
   for (j = 0; j < 8 && i + j < order.length; j++) if (done[order[i+j]]) b |= (1 << j);
   bytes.push(b);
  }
  while (bytes.length && bytes[bytes.length-1] === 0) bytes.pop();
  var out = '', k;
  for (k = 0; k < bytes.length; k += 3) {
   var n = (bytes[k] << 16) | ((bytes[k+1] || 0) << 8) | (bytes[k+2] || 0);
   out += B64[(n >> 18) & 63] + B64[(n >> 12) & 63];
   if (k + 1 < bytes.length) out += B64[(n >> 6) & 63];
   if (k + 2 < bytes.length) out += B64[n & 63];
  }
  return out;
 }
 function decode(str){
  var bytes = [], buf = 0, bits = 0, i, v, list = [];
  for (i = 0; i < str.length; i++) {
   v = B64.indexOf(str[i]); if (v < 0) continue;
   buf = (buf << 6) | v; bits += 6;
   if (bits >= 8) { bits -= 8; bytes.push((buf >> bits) & 255); }
  }
  bytes.forEach(function(b, bi){ for (var j = 0; j < 8; j++) if ((b >> j) & 1) { var n = order[bi*8+j]; if (n) list.push(n); } });
  return list;
 }
 function merge(list){
  var added = 0;
  list.forEach(function(n){ n = String(n); if (order.indexOf(n) >= 0 && !done[n]) { done[n] = 1; added++; } });
  if (added) save();
  return added;
 }
 var msgEl = document.getElementById('msg'), msgT;
 function msg(t){ msgEl.textContent = t; clearTimeout(msgT); msgT = setTimeout(function(){ msgEl.textContent = ''; }, 6000); }
 function progressLink(){
  var base = location.href.split('#')[0];
  return base + '#p=' + encode();
 }
 var m = /[#&]p=([A-Za-z0-9_-]*)/.exec(location.hash);
 if (m) {
  var added = merge(decode(m[1]));
  msg(added ? 'Imported ' + added + ' solved problem' + (added === 1 ? '' : 's') + ' from the link.' : 'Link opened; nothing new to import.');
  try { history.replaceState(null, '', location.pathname + location.search); } catch(err) {}
 }
 document.getElementById('copylink').addEventListener('click', function(){
  var link = progressLink(), n = solvedList().length;
  function ok(){ msg('Link copied (' + n + ' solved). Open it on the other device.'); }
  function fallback(){ window.prompt('Copy this link and open it on the other device:', link); }
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(link).then(ok, fallback); else fallback();
 });
 document.getElementById('export').addEventListener('click', function(){
  var list = solvedList();
  var blob = new Blob([JSON.stringify({version: 1, exported: new Date().toISOString(), solved: list}, null, 1)], {type: 'application/json'});
  var a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'interview-practice-progress.json'; document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  msg('Exported ' + list.length + ' solved.');
 });
 document.getElementById('import').addEventListener('click', function(){ document.getElementById('importfile').click(); });
 document.getElementById('importfile').addEventListener('change', function(e){
  var f = e.target.files[0]; if (!f) return;
  var r = new FileReader();
  r.onload = function(){
   try {
    var obj = JSON.parse(r.result), list = Array.isArray(obj) ? obj : (obj.solved || []);
    var added = merge(list);
    msg('Imported ' + added + ' new solved problem' + (added === 1 ? '' : 's') + ' (' + list.length + ' in file).');
    render();
   } catch(err) { msg('That file is not a progress export.'); }
   e.target.value = '';
  };
  r.readAsText(f);
 });

 var items = Array.prototype.slice.call(document.querySelectorAll('li'));
 function render(){
  var shown = 0, solved = 0;
  items.forEach(function(li){
   var ok = (filt === 'all' || li.getAttribute('data-' + filt) === 'true') && (!diff || li.getAttribute('data-d') === diff);
   li.classList.toggle('hidden', !ok);
   var isDone = !!done[li.getAttribute('data-n')];
   li.classList.toggle('done', isDone);
   li.querySelector('input').checked = isDone;
   if (ok) { shown++; if (isDone) solved++; }
  });
  document.querySelectorAll('section').forEach(function(s){
   var vis = s.querySelectorAll('li:not(.hidden)'), d = s.querySelectorAll('li:not(.hidden).done');
   s.querySelector('[data-count]').textContent = d.length + ' / ' + vis.length;
   s.classList.toggle('hidden', vis.length === 0);
  });
  document.getElementById('prog').textContent = solved + ' of ' + shown + ' solved';
 }
 root.addEventListener('change', function(e){
  if (e.target.type !== 'checkbox') return;
  var n = e.target.closest('li').getAttribute('data-n');
  if (e.target.checked) done[n] = 1; else delete done[n];
  save();
  render();
 });
 document.querySelectorAll('.chip[data-f]').forEach(function(b){
  b.addEventListener('click', function(){
   filt = b.getAttribute('data-f');
   document.querySelectorAll('.chip[data-f]').forEach(function(x){ x.classList.toggle('on', x === b); });
   render();
  });
 });
 document.querySelectorAll('.chip[data-d]').forEach(function(b){
  b.addEventListener('click', function(){
   var d = b.getAttribute('data-d'); diff = (diff === d) ? null : d;
   document.querySelectorAll('.chip[data-d]').forEach(function(x){ x.classList.toggle('on', x.getAttribute('data-d') === diff); });
   render();
  });
 });
 render();
})();
</script>
</body>
</html>
'''
open("index.html", "w").write(page.replace("__DATA__", json.dumps(data, separators=(",", ":")).replace("</", "<\\/")))

readme = """# Interview practice set

Coding-interview practice problems grouped by pattern, with LeetCode links and a
progress tracker that saves in your browser.

Live page: https://pankajkgarg.github.io/interview-practice/

The sections follow the chapters of the *Coding Interview Refresher* book and the
explainer video. Each section opens with the recognition cue for its pattern.
Problems come from [NeetCode 150](https://neetcode.io/practice) (all 150),
[Grind 75](https://www.techinterviewhandbook.org/grind75/) (all 75) and the book's
own picks; the tags on each row say which.

Files:

- `index.html`: the page, self-contained.
- `problems.json`: the same data, for other tools.
- `problems.py` + `build.py`: edit the Python list and run `python3 build.py` to regenerate both.
"""
import os
if not os.path.exists("README.md"): open("README.md", "w").write(readme)  # README is hand-maintained once it exists
print("ok", len(open("index.html").read()))
