---
title: Which tool, when
lede: Start here. The situation decides the tool, so this page goes situation first and mechanics second. It answers the three questions from the pilot video, when to use McNemar, when to use Wilson, and where the probability in a confidence interval comes from, and then gives one table for everything else.
---

## Three different things called "p"

Most of the confusion in eval statistics comes from three unrelated numbers that all get called "p" or "probability". Keep them in separate boxes.

<div class="three">
<div><b>p̂ ("p-hat"), the score</b>The fraction of questions the model got right. 360 correct out of 500 gives p̂ = 0.72. It is the thing you measured, and it is the "p" inside the standard-error formula.</div>
<div><b>The p-value, from a test</b>Comes out of a comparison, such as McNemar. It is the chance of seeing a gap at least this big <i>if there were really no difference</i>. Small means "hard to explain as luck".</div>
<div><b>95%, the confidence level</b>A property of the method, chosen by you. If you rebuilt the benchmark many times and drew an interval each time, 95% of those intervals would contain the model's true accuracy.</div>
</div>

## Where the probability in a confidence interval comes from

A confidence interval answers one question: how much would this score move if the benchmark had been written with different questions? Here is the 72% example from the video, step by step.

1. **Model each question as a coin.** The model has some true accuracy p that you cannot see. Each question is a coin that lands "correct" with probability p. Which questions ended up in the benchmark is the randomness; that is what the interval is about.
2. **Estimate p with the score.** You saw 360 of 500 correct, so p̂ = 0.72. This is the moment in the video where "the probability is the eval score".
3. **Spread of one coin.** A coin with probability 0.72 has variance p̂(1 − p̂) = 0.72 × 0.28 = 0.2016. It is largest at 50% and shrinks towards 0% or 100%, because a coin that almost always lands the same way barely varies.
4. **Spread of the average of 500 coins.** Divide the variance by n: 0.2016 / 500 = 0.000403. Take the square root to get the standard error: 0.020, which is 2.0 percentage points.
5. **Turn it into an interval.** Averages of many coins are roughly bell-shaped, and 95% of a bell lies within 1.96 standard errors of the centre. So 72.0 ± 1.96 × 2.0 gives **68.1% to 75.9%**.
6. **Read it correctly.** Last week's 70.4 sits inside that range, so a single run cannot tell the two checkpoints apart. (To actually compare them, pair them: see McNemar below.)

The formula to remember is SE = √(p̂(1 − p̂)/n). The square root of n is why halving the error bar takes four times as many questions.

## McNemar: when to use it

**Use it when two versions of something answer the *same* questions, and each answer is right or wrong.** Situations on an eval platform where this comes up:

- **Checkpoint versus checkpoint.** "Did this week's checkpoint beat last week's on our 500-question reasoning set?" This is the pilot example.
- **A prompt or template change.** The same model with the old and new few-shot template, or the old and new system prompt.
- **An infrastructure change.** A vLLM upgrade, a new GPU type, an FP8-quantised copy versus bf16, a batching change. "Did the score move because of the infra?" This is a regression check you would run on a pinned reference model.
- **A grader change.** The same stored generations graded by extractor v1 and extractor v2. Here the "two versions" are the graders, not the models.
- **A release decision.** Model A versus model B on a fixed held-out set.

**Why it beats comparing two error bars.** On the same questions, easy questions are easy for both models and hard ones are hard for both. Those cancel out of the difference. Only the questions where the two disagree carry evidence. McNemar is a coin-flip test on just those disagreements.

**How to compute it.** Count b = questions A got right and B got wrong, and c = the reverse. If the two models were equally good, each disagreement would be a fair coin. The exact test is a binomial test of b out of b + c at one half.

```python
from scipy.stats import binomtest
b, c = 40, 55                        # A-only wins, B-only wins
binomtest(b, b + c, 0.5).pvalue      # 0.15
```

The paired interval on the difference is (c − b)/n ± 1.96·√(b + c − (c − b)²/n)/n. For the example that gives 3.0 ± 3.8 points, from −0.8 to +6.8. Report that interval first and the p-value second.

**When it is not the right tool:**

| Situation | Use instead |
|---|---|
| Different question sets (two benchmark versions, two user groups) | Unpaired two-proportion test, or the Newcombe interval for the difference |
| Scores are not right/wrong (judge score 1 to 10, F1, BLEU) | Paired t-test on per-question differences, or a paired bootstrap |
| Several samples per question (pass@1 averaged over 8 samples) | Average per question first, then a paired bootstrap or paired t-test on those averages |
| Three or more systems | Pairwise McNemar with a Holm correction (or Cochran's Q as an overall test first) |

**One line for the interview:** "On the same items I never compare two error bars. I look at the discordant pairs. McNemar is a sign test on the questions where the two disagree, and it is why the platform must store per-question results."

## Wilson interval: when to use it

**Use it for a single pass rate whenever n is small or the rate is near 0% or 100%. In practice, use it by default:** when the simple interval is fine, Wilson agrees with it.

Situations where the simple ±1.96·SE interval (the "Wald" interval) breaks:

- **Small benchmarks.** AIME has 30 questions. At 1 of 30 correct, Wald gives −3.1% to 9.8%, which includes impossible negative accuracies. Wilson gives **0.6% to 16.7%**.
- **Slices.** Per-language or per-category breakdowns with 20 to 80 items each.
- **Rare events.** Refusal rate, harmful-output rate, crash or extraction-failure rate. For 3 failures in 2,000 runs, Wilson gives 0.05% to 0.44%.
- **Saturated benchmarks.** At 485 of 500 (97%), Wald's upper end is 98.5%. Wilson pulls the interval in from the edge (95.1% to 98.2%) instead of running it towards 100%.
- **Zero observed failures.** 0 of 100 does not mean "never". Wilson's upper bound is 3.7%, and the quick rule of three says about 3/n.

**Why Wald breaks.** It assumes a symmetric bell around p̂, but near 0 or 1 the true distribution is lopsided and squashed against the wall. Wilson solves the problem the other way round. It asks which true values of p would make the observed score unsurprising, which keeps it inside 0 to 1 and gives it honest coverage.

```python
from statsmodels.stats.proportion import proportion_confint
proportion_confint(1, 30, method="wilson")          # (0.006, 0.167)
proportion_confint(1, 30, method="beta")            # Clopper-Pearson, more conservative
```

If guaranteed coverage matters, as in a safety sign-off, use Clopper-Pearson ("exact"). It is a bit wider than Wilson.

## Everything else: situation to tool

| You have | You want to know | Reach for | Read |
|---|---|---|---|
| One pass rate | How precise is it? | Wilson interval (Wald is fine for large n and mid-range scores) | [Ch 7](ch07.html) |
| One score that is not a pass rate (mean judge score, F1, p95 latency) | How precise is it? | Bootstrap: resample questions, recompute, take the 2.5th and 97.5th percentiles | [Ch 7](ch07.html) |
| Questions that come in groups (5 questions per passage, tasks per repo) | How precise is it, honestly? | Cluster bootstrap or clustered standard errors; resample the groups | [Ch 7](ch07.html) |
| Two systems, same questions, right/wrong | Is the gap real? | McNemar, plus the paired interval on the difference | [Ch 8](ch08.html) |
| Two systems, same questions, continuous scores | Is the gap real? | Paired t-test, paired bootstrap or permutation test | [Ch 8](ch08.html) |
| Two systems, different questions | Is the gap real? | Two-proportion test or Newcombe interval | [Ch 8](ch08.html) |
| A benchmark, before you run it | Can it even detect a 2-point change? | Minimum detectable effect ≈ 2.8 × SE of the difference | [Ch 9](ch09.html) |
| k samples per problem | What is pass@k? | The unbiased estimator 1 − C(n−c, k)/C(n, k) | [Ch 9](ch09.html) |
| Many benchmarks × checkpoints, or many slices | Which movements are real? | Holm for release gates; Benjamini-Hochberg for dashboards | [Ch 10](ch10.html) |
| An LLM judge and some human labels | Can I trust the judge? | Cohen's kappa plus the confusion matrix; human-human agreement as the ceiling | [Ch 11](ch11.html) |
| Pairwise preference votes | A ranking with error bars | Bradley-Terry fit, with bootstrap rank ranges | [Ch 11](ch11.html) |
| A score that looks too good | Is the test set leaked? | Contamination checks: n-gram overlap, perturbed or fresh versions | [Ch 12](ch12.html) |
| Live users | Did the change help? | A/B test randomised by user, CUPED, no peeking without a sequential method | [Ch 12](ch12.html) |
