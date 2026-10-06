"""Build the eval study pages from the Evaluation Field Guide chapters.

python3 eval/build_eval.py <book-chapters-dir>   (needs pandoc)
The public pages leave out the personal interview material in the book.
"""
import re, sys, os, html, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "chapters")
PANDOC = shutil.which("pandoc") or __import__("pypandoc").get_pandoc_path()

# (slug, file, short title, "use this when" text)
PAGES = [
 ("ch01", "01-what-evals-are-for.md", "What evals are for",
  "You need the big picture: who consumes eval results, which decisions they drive, and what makes an eval platform good."),
 ("ch02", "02-anatomy.md", "Anatomy of an eval",
  "You want the moving parts of one eval run (problem sets, configs, inference, graders, results store) and the open frameworks that implement them."),
 ("ch03", "03-graders.md", "Graders",
  "A score looks wrong and the grader is a suspect: answer extraction, code-execution tests, or an LLM judge."),
 ("ch04", "04-throughput.md", "Throughput and scheduling",
  "Evals are too slow or too expensive, or they compete with training for GPUs."),
 ("ch05", "05-degradation-and-oncall.md", "Degradation and on-call",
  "A score moved and you must decide whether the model changed or the pipeline broke, or you are designing alerts and runbooks."),
 ("ch06", "06-design-answer.md", "Designing an eval platform",
  "You are asked to design an eval platform end to end, in a design interview or for real."),
 ("ch07", "07-score-is-an-estimate.md", "A score is an estimate",
  "You report any single number: a benchmark score, a pass rate on a slice, a judge's mean score. It answers \"how precise is this?\" with standard errors, Wilson intervals, the bootstrap and clustered questions."),
 ("ch08", "08-comparing-two-models.md", "Comparing two models",
  "Two models, prompts, graders or infra configs ran on the same questions and you must say whether the gap is real. McNemar, paired tests and what a p-value means."),
 ("ch09", "09-power-and-sample-size.md", "Power, sample size, pass@k",
  "Before running: can this benchmark even detect the change you care about? How many questions do you need? Also how to compute pass@k correctly."),
 ("ch10", "10-many-comparisons.md", "Many comparisons",
  "You look at many numbers at once (benchmarks × checkpoints, slices, regression alerts) and some will move by chance. Bonferroni, Holm, Benjamini-Hochberg."),
 ("ch11", "11-judges-and-humans.md", "Judges, agreement, rankings",
  "The grader is an LLM or a human: is the judge trustworthy (kappa), and how do you turn pairwise votes into a ranking (Bradley-Terry, Elo)?"),
 ("ch12", "12-benchmarks-and-online.md", "Benchmarks wear out",
  "A benchmark might be leaked or saturated, you want a cheaper subset, or you are measuring with live users (A/B tests)."),
 ("formulas", "91-appendix-formulas.md", "Formulas on one page",
  "The night before: every tool in one line, with its example number."),
]

# Personal interview material stays in the private book.
SCRUB = [
 ("The job you are interviewing for is about", "Eval platform engineering is about"),
 ("At Microsoft AI this is likely a separate stack, but your platform will be asked", "At many labs this is a separate stack, but the eval platform will be asked"),
 ("The role you are interviewing for is reliability and platform engineering for that system", "Eval platform engineering is reliability and platform engineering for that system"),
 ("Microsoft AI, Mustafa Suleyman's organisation that trains the MAI models, is separate from Microsoft Research, and its internal stack is not public; do not assume it uses either, but knowing they exist lets you ask a good question about it.",
  "Most labs' internal stacks are not public; knowing these open frameworks exist lets you ask a good question about whichever stack you meet."),
 ("And because the role covers European hours with colleagues presumably covering others, handover notes matter", "And when on-call follows the sun across time zones, handover notes matter"),
 ("or at 9am in Zurich", "or on a busy Monday morning"),
 ("at 6pm Zurich", "at 6pm in one time zone"),
 ("If the process gets past the screen, the most likely design question for this role is", "The most likely design question for an eval platform role is"),
 (" It ends with what is publicly known about how Microsoft AI evaluates, so you can bend the generic answer toward their reality.", ""),
 ("For this role the three", "For an eval platform role the three"),
 ("chosen for this role", "chosen for the role"),
 ("Microsoft AI's own MAI-Thinking-1 report reportedly found", "The MAI-Thinking-1 technical report reportedly found"),
 ("the monitoring side of your job, which the posting calls detecting", "the monitoring side of an eval platform, often called detecting"),
 ("where the statistics are the A/B-testing kind you may already know from Google.", "where the statistics are the familiar A/B-testing kind."),
 ("You already know A/B testing from Google, so this section only flags", "This section assumes basic A/B testing and only flags"),
 ("and is a nice thing to mention at Microsoft in particular, since it was invented there", "and was developed at Microsoft"),
]
SCRUB += [
 (" The posting's mention of \"reinforcement learning training infrastructure\" is pointing at this overlap.", " This overlap is why eval platform roles often sit next to RL training infrastructure."),
 ("the operational problems are exactly the ones the posting lists as required qualifications:", "the operational problems are classic distributed-systems ones:"),
 ("This overlap is why the posting mentions RL infrastructure.", "This overlap is why eval platforms and RL infrastructure are so often built together."),
 ("because the posting explicitly asks for \"a track record of reducing operational burden through systematic reliability improvements, automation, or tooling\", and that", "and that"),
 ("which is what the posting means by", "which is what people mean by"),
]
SCRUB += [
 ("The posting names four things you would build and extend:", "An eval platform is built from four things:"),
 ("The posting's four nouns map to", "Those four nouns map to"),
 ("The posting asks you to \"improve evaluation throughput and scheduling efficiency\".", "Every eval platform is asked to improve evaluation throughput and scheduling efficiency."),
 ("The posting asks for \"monitoring, alerting, and dashboards to proactively detect evaluation degradation\" and for on-call runbooks.", "An eval platform needs monitoring, alerting and dashboards that detect evaluation degradation early, and on-call runbooks for when it happens."),
 (" Read the MAI-Thinking-1 report's infrastructure sections yourself before the 16th.", ""),
]
CUT = [(r"\n## What the job description is really asking for\n.*?(?=\n## What \"good\")", "\n"),
       (r"\n## What Microsoft AI has said about how it evaluates\n.*?(?=\n## What to take)", "\n"),
       (r" Tie the answer to what Microsoft AI has said about itself:[^\n]*?infrastructure\.", "")]
BANNED = ["six months", "posting", "interviewing for", "Zurich", "from Google", "the 16th", "this role", "Mirosław", "Karla"]

CSS = open(os.path.join(HERE, "src", "style.css")).read()

def page(title, body, nav=""):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Eval study notes</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<p class="crumb"><a href="index.html">Eval study notes</a> · <a href="../">Coding practice set</a></p>
{body}
{nav}
<footer>Adapted from the <em>Evaluation Field Guide</em> (October 2026). Numbers in the statistics chapters come from simulations made for the book.</footer>
</div></body></html>'''

def md2html(md):
    return subprocess.run([PANDOC, "-f", "markdown-implicit_figures+pipe_tables", "-t", "html5", "--mathjax"],
                          input=md, capture_output=True, text=True, check=True).stdout

def figures(t):
    def sub(m):
        n = m.group(1); cap = re.search(r'Caption:\s*"(.*?)"', m.group(2))
        cap = cap.group(1) if cap else ""
        f = "fig-" + n.replace(".", "-") + ".png"
        if not os.path.exists(os.path.join(SRC, "..", "img", f)): return ""
        shutil.copy(os.path.join(SRC, "..", "img", f), os.path.join(HERE, "img", f))
        return f'<figure><img src="img/{f}" alt="{html.escape(cap)}"><figcaption>Figure {n}. {html.escape(cap)}</figcaption></figure>'
    return re.sub(r'^\[IMAGE (\d+\.\d+) — (.*)\]\s*$', sub, t, flags=re.M)

def chapter(i, slug, fn, short, when):
    t = open(os.path.join(SRC, fn)).read()
    t = re.sub(r"^# Part [IV]+:.*\n", "", t, flags=re.M)
    for a, b in SCRUB: t = t.replace(a, b)
    for a, b in CUT: t = re.sub(a, b, t, flags=re.S)
    for w in BANNED: assert w not in t, (fn, w)
    t = re.sub(r"^# (Chapter \d+|Appendix A) — ", "# ", t, count=1, flags=re.M)
    t = figures(t)
    h = md2html(t)
    h = h.replace("</h1>", f'</h1>\n<div class="when"><b>Use this when</b>{html.escape(when)}</div>', 1)
    prev = PAGES[i-1] if i > 0 else None; nxt = PAGES[i+1] if i+1 < len(PAGES) else None
    nav = '<nav class="pn">' + (f'<a href="{prev[0]}.html">← {prev[2]}</a>' if prev else "<span></span>") + \
          (f'<a href="{nxt[0]}.html">{nxt[2]} →</a>' if nxt else "") + "</nav>"
    open(os.path.join(HERE, slug + ".html"), "w").write(page(short, h, nav))

def simple(name):
    t = open(os.path.join(HERE, "src", name + ".md")).read()
    fm = dict(re.findall(r"^(\w+): (.*)$", t.split("---")[1], flags=re.M))
    body = t.split("---", 2)[2]
    h = f"<h1>{html.escape(fm['title'])}</h1>\n<p class=\"lede\">{html.escape(fm['lede'])}</p>\n" + md2html(body)
    open(os.path.join(HERE, name + ".html"), "w").write(page(fm["title"], h))

for i, p in enumerate(PAGES): chapter(i, *p)
simple("which-test")
simple("index")
print("built", len(PAGES) + 2, "pages")
