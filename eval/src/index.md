---
title: Eval study notes
lede: The statistics and engineering behind evaluating language models, situation first. Companion to the eval explainer videos, the same way the coding practice set goes with the coding videos.
---

<div class="when"><b>Start here</b><a href="which-test.html">Which tool, when</a> covers the three different things called "p", where the probability in a confidence interval comes from, when to use McNemar, when to use Wilson, and one table that maps each situation to its tool.</div>

## Videos

<div class="card">
<h3>Full video: eval statistics and platform in twelve chapters (46:05)</h3>
<p><a href="https://drive.google.com/file/d/1I_PlQbd7GyH_peAV1gqEeD10iIUWkCj-/view">Watch on Google Drive</a> (private to the owner) · <a href="videos/eval-stats-full-context.txt">Context file</a>: the whole narration plus what is on screen, as one text file. Attach it to a chat with Claude or ChatGPT and ask about any part. Drive has no chapter menu, so drag to the time below; each chapter also shows its title on screen.</p>
<ul class="toc">
<li><span class="ts">0:37</span> 1. A score is an estimate: standard error and confidence intervals. <a href="ch07.html">Read more</a></li>
<li><span class="ts">5:24</span> 2. Small samples and extreme rates: the Wilson interval. <a href="which-test.html#wilson-interval-when-to-use-it">Read more</a></li>
<li><span class="ts">9:49</span> 3. Two models, same questions: pairing, McNemar and the p-value. <a href="ch08.html">Read more</a></li>
<li><span class="ts">15:25</span> 4. Metrics without a formula: the bootstrap, and grouped questions. <a href="ch07.html#the-bootstrap-for-everything-that-is-not-a-pass-rate">Read more</a></li>
<li><span class="ts">19:25</span> 5. Can this benchmark see the change? power and sample size. <a href="ch09.html">Read more</a></li>
<li><span class="ts">23:03</span> 6. Sampling many answers: pass@k done right. <a href="ch09.html#passk-and-its-unbiased-estimator">Read more</a></li>
<li><span class="ts">26:23</span> 7. Many benchmarks, many checkpoints: multiple comparisons. <a href="ch10.html">Read more</a></li>
<li><span class="ts">30:01</span> 8. Can you trust the judge? agreement and Cohen&#x27;s kappa. <a href="ch11.html">Read more</a></li>
<li><span class="ts">33:37</span> 9. From votes to a ranking: Bradley-Terry and Elo. <a href="ch11.html#from-pairwise-verdicts-to-a-ranking-bradley-terry-and-elo">Read more</a></li>
<li><span class="ts">36:51</span> 10. Leaked or worn out? contamination, and comparing different question sets. <a href="ch12.html">Read more</a></li>
<li><span class="ts">40:20</span> 11. Model or pipeline? detecting evaluation degradation. <a href="ch05.html">Read more</a></li>
<li><span class="ts">43:49</span> 12. Which tool, when: the whole map. <a href="which-test.html">Read more</a></li>
</ul>
</div>

<div class="card">
<h3>Pilot: four ideas (14:50), superseded by the full video</h3>
<p><a href="https://drive.google.com/file/d/1VIIvCtqnyxxvy1k036hx0RXDWol578zc/view">Watch on Google Drive</a> (private to the owner) · <a href="videos/eval-stats-pilot-context.txt">Context file</a>: the whole narration plus what is on screen, as one text file. Attach it to a chat with Claude or ChatGPT and ask about any part.</p>
<ul class="toc">
<li><span class="ts">0:31</span> 1. A benchmark score is an estimate: standard error, confidence interval, Wilson. <a href="ch07.html">Read more</a></li>
<li><span class="ts">4:20</span> 2. Comparing two models: pairing, McNemar, what a p-value means. <a href="ch08.html">Read more</a></li>
<li><span class="ts">8:13</span> 3. The bootstrap, and questions that come in groups. <a href="ch07.html#the-bootstrap-for-everything-that-is-not-a-pass-rate">Read more</a></li>
<li><span class="ts">11:13</span> 4. Many benchmarks, many checkpoints: multiple comparisons. <a href="ch10.html">Read more</a></li>
</ul>
</div>

## Statistics behind an eval number

<ol class="toc" start="7">
<li><a href="ch07.html">A score is an estimate</a>: how precise is one number?</li>
<li><a href="ch08.html">Comparing two models</a>: is the gap real?</li>
<li><a href="ch09.html">Power, sample size, pass@k</a>: can this benchmark detect the change at all?</li>
<li><a href="ch10.html">Many comparisons</a>: which of fifty movements are real?</li>
<li><a href="ch11.html">Judges, agreement, rankings</a>: can you trust the grader?</li>
<li><a href="ch12.html">Benchmarks wear out</a>: contamination, saturation, online tests</li>
</ol>
<p><a href="formulas.html">All the formulas on one page</a></p>

## Engineering an eval platform

<ol class="toc">
<li><a href="ch01.html">What evals are for</a></li>
<li><a href="ch02.html">Anatomy of an eval</a></li>
<li><a href="ch03.html">Graders</a></li>
<li><a href="ch04.html">Throughput and scheduling</a></li>
<li><a href="ch05.html">Degradation and on-call</a></li>
<li><a href="ch06.html">Designing an eval platform</a></li>
</ol>
