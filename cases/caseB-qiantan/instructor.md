# Case B: Wendy's Rate Decisions: Instructor Version

**Meetings 8–9. Instructor only: contains every answer and all future releases.** Meeting 9 was rewritten on 8 October for the generative-AI meeting; its old IV parts are kept at the end as a bonus (Parts B1–B4).

## 1. What the case does

Two meetings, one question: *what happens to bookings if Qiantan Hotels changes its rate, and how should it set rates?*

- **M8** answers it from the RM system's logs (adjustment and DML) and ends on the assumption the logs cannot check: unlogged overrides.
- **M9** keeps the question and brings in generative AI in both of its roles. A simulator learned from the M8 logs tests the M8 estimator against the override problem, and tests whole pricing pipelines (block A). A language model reads guest reviews for a randomized rate test's guardrail, and text becomes DML controls (block B). The M8 breakdown is the motivation for M9; do not let the two meetings read as separate cases.

Each meeting follows the course spine: estimand → identification → estimation.

| Meeting | Estimand (vs break-even) | Assignment mechanism → identification | Estimation and uncertainty | Destination |
|---|---|---|---|---|
| M8 | average price elasticity of premium bookings: local and variance-weighted (vs −1.32) | the RM system's rule; unconfoundedness given the signals **measured as of pricing time**; overlap = off-rule variation | partially linear model; DML with cross-fitting (folds by night); date-clustered SE; interactive model and the AIPW score for a yes-or-no treatment; partial-$R^2$ sensitivity with benchmarking | −1.56 (date-clustered SE 0.03), 95% CI [−1.62, −1.50]: **do not raise** |
| M9 | the elasticity again (vs −1.32); regret of a pricing pipeline against an oracle; the rise's effect on value complaints (guardrail: 5 points) | a simulator's effects are g-formula effects: the M8 assumption, with the truth planted; the Q3 test is randomized | estimator and pipeline testbeds on two simulators; backtest; PPI with a gold subsample; text embeddings as controls | Q3 test −1.72 [−2.07, −1.38]: **do not raise**; pilot DML pricing inside the logged range with a holdout; guardrail 0.03 (SE 0.023): not tripped, not cleared |

M8 numbers match `meetings/m08` and are checked by `shared/checks/slides08_check.py`. M9 numbers are the case's own (the M9 notes use a food-delivery example) and are checked by `shared/checks/case_check.py`.

**AI thread.** In M8, AI as the decision-maker: the RM system is an automated pricer, and its decisions are the confounder. This is M7's lesson with a continuous treatment: *the rule that set the treatment is what you must adjust for, and it must enter as flexibly as it was written.* In M9, generative AI as a simulator (block A) and as a source of data (block B), with the vendor's engine as a candidate decision-maker.

**Not in class time:** regression discontinuity (Handout H5, with M8) and instrumental variables beyond M2 (Handout H4). The bonus Parts B1–B4 are for students who want the IV version of Wendy's question.

## 2. Release schedule

M8 has no slack, and its block C is the proposal presentations. If the meeting runs long, cut R4 (the last-minute discount) and "One Split Is One Draw" first; keep the sensitivity frames, which R5 needs.

| Part | Meeting, block | About | Hand out at | Hold back until the attempt |
|---|---|---|---|---|
| M8-R1 | M8 A | 0–10 | `[RELEASE R1]` "Qiantan Hotels: The Proposal" | "The Number That Decides It"; the pooled slope on "Six Comparable Nights" |
| M8-R2 | M8 A | 15–30 | `[RELEASE R2]` "Pooled, Then Within Category" | the −1.0 line; "Why Both Sides? Six Nights Again" |
| M8-R3 | M8 A | 40–50 | `[RELEASE R3]` "The Real Logs" | "Controls That Cannot Bend"; "Plug-In Failure 1: Regularization Bias" and "Plug-In Failure 2: Overfitting Bias"; "The Price Elasticity at Qiantan Hotels" |
| M8-R4 | M8 B | 75–82 | `[RELEASE R4]` "A Yes-or-No Treatment: The Last-Minute Discount" | the 13.9 line; "Two Models, Two Estimands"; "The AIPW Score" |
| M8-R5 | M8 B | 85–95 | `[RELEASE R5]` "One More Thing, Says Wendy" | "How Strong Would It Have To Be?"; "Benchmarking Against an Observed Signal" |
| M9-R1 | M9 A | 0–5 | `[RELEASE R1]` "Meeting 8 Left One Doubt" | "What the Simulator's Answer Rests On"; the data/analyst table on "Planting the Truth" |
| M9-R2 | M9 A | 15–20 | `[RELEASE R2]` "An Estimator Testbed" | "Reading the Testbed" |
| M9-R3 | M9 A | 25–30 | `[RELEASE R3]` "Three Pipelines on Two Simulators" | "Check 1" to "Check 4"; "What the Testbeds Tell Wendy" |
| M9-R4 | M9 A | 42–45 | `[RELEASE R4]` "Ask the Model Instead?" | "Planted Truth and Asserted Truth" |
| M9-R5 | M9 B | 50–55 | `[RELEASE R5]` "The Q3 Rate Test" | "The Gold Subsample"; "Differential Error, Decomposed"; "PPI on the Q3 Reviews"; "Why PPI Works Here" |
| M9-R6 | M9 B | 80–85 | `[RELEASE R6]` "Embeddings as Controls" | "Failure 1: Leakage"; "Failure 2: Overlap Collapse" |
| M9-R7 | M9 B | 95–100 | `[RELEASE R7]`, before "What Wendy Decides" | that frame (the memo can finish at home) |
| B1–B4 | take-home | | with the notes | the bonus key below |

Controlled projection copy for M8 is still required: do not project the residual rows or the −1.0 line on "Pooled, Then Within Category" before R2's attempt. **The simulation's true elasticities are never shown in lecture**; they appear only in the M8 and M9 workshop comparisons.

## 3. Key, part by part

### M8-R1
- Contribution goes from 600 to 664, up **10.7%**. Break-even: $\eta^* = \ln(600/664)/\ln(1.08) = $ **−1.32**. Bookings must fall by less than $1 - 600/664 = 9.6\%$.
- Pooled: deviations $D$ = −30, −20, −10, 10, 20, 30; $Y$ = −40, −50, −60, 60, 50, 40. Their cross-products sum to $5{,}600$ and the squared rate deviations to $2{,}800$, so the slope is **+2.0**.
- Most pairs raise rates on the pooled number. That is the point of the commit.

### M8-R2
- Residuals: $\tilde D$ = −10, 0, 10, −10, 0, 10 and $\tilde Y$ = 10, 0, −10, 10, 0, −10. The slope is $-400/400 = $ **−1.0**: same six nights, opposite sign.
- DAG: demand signals → rate (+) and demand signals → bookings (+). The omitted-variable bias is positive and large enough to flip the sign.
- Sentences:
  - *Only the RM system sets rates* → no unrecorded input moves $D$.
  - *Every input is in the feed* → nothing it saw is missing from $X$.
  - *Rates still move* → there is residual variation to compare.
  - A night priced exactly by the rule has $\tilde D = 0$ and **answers nothing**.
- Tell students to **hold onto the first sentence**; R5 breaks it.

### M8-R3
- Ladder (deck frame "Controls That Cannot Bend"): pooled +0.40; within hotel +0.49 (the system charges different rates at the same hotel on different nights); hotel × occupancy band −0.07 (right sign, almost no magnitude). Destination −1.56.
- Typical proposals and their failures:
  1. **47 linear controls: −0.54.** The rule is a staircase and the model is a ramp. It misses the bands and the weekend × band interaction.
  2. **Boosted model with price as a feature: −1.03.** Price stands in for the signals. The competitor-index share falls from 4.2% to 0.9% when the log rate is added.
  3. **Residualize both sides in-sample: −0.95.** The flexible model memorizes rows; its in-sample $R^2$ is 0.97. Well-regularized in-sample gives −1.57 and cross-fitted −1.56. The bias grows with flexibility and cannot be sized from inside the fit.
- **DML** (residualize both sides + cross-fit, folds by night, date-clustered SE): −1.56 (date-clustered SE 0.03), 95% CI [−1.62, −1.50]; rows treated as independent give SE 0.01, three times too small.
  - The bias from nuisance errors is second-order: products of the two errors, plus the price model's squared error. That is why both sides are residualized.
- Task 4: same-night booking pace recorded after the rate posted is partly *caused* by the rate. So is a competitor index that reacts to Qiantan Hotels' own rate. Both are post-treatment. **Every control must be measured as of the moment the RM system set the rate**; otherwise it enters as a mediator or a collider (M7).
- Decision table (deck frame "The Price Elasticity at Qiantan Hotels", computed from −1.56):
  - +8% rate: bookings −11.3%, contribution −1.9%.
  - −4%: +0.9%. −8%: +1.7%.
  - **Do not raise.** A modest cut is worth testing deliberately.
  - The formula optimum ¥557 lies far outside the ¥703–910 range the system varied over, holding signals fixed. $\theta$ is a local slope.
  - The optimum also inherits the interval: $P^* = 200\kappa/(\kappa - 1)$ maps the CI $\kappa \in [1.50, 1.62]$ to **[¥523, ¥600]**. The whole range lies outside the support, which is one more reason to *test* a modest cut rather than jump.
- Overlap: on 12% of nights the rate is pinned to the rule. Those nights carry almost no weight. Rate model out-of-fold $R^2$ 0.91 (9% left, as in M9-R6).

### M8-R4
1. With: $(0.25 \times 54 + 0.45 \times 72)/0.70 = 65.6$. Without: $(0.25 \times 50 + 0.05 \times 60)/0.30 = 51.7$. Difference **13.9** rooms, more than either kind of night's effect. The system opens the discount mostly at resorts, which book more anyway: the decision-maker's rule is the confounder, as with the rate.
2. The partially linear model weights each kind of night by $\mathrm{Var}(D \mid X) = e(1-e)$: 0.25 and 0.09, giving $\theta = (0.5 \times 0.25 \times 4 + 0.5 \times 0.09 \times 12)/(0.5 \times 0.25 + 0.5 \times 0.09) = $ **6.1**. ATE $= 0.5(4) + 0.5(12) = $ **8.0**; ATT $= (0.25 \times 4 + 0.45 \times 12)/0.70 = $ **9.1**. Opening it every night needs the **ATE**; neither is 6.1. The choice between the partially linear and the interactive model is a choice of estimand.
3. Regression alone: $\hat\mu_1 = $ **74** (error +2.0). Weighting alone: $0.9 \times 72/0.8 = $ **81** (+9.0). AIPW: $74 + 0.9 \times (-2)/0.8 = $ **71.75** (−0.25). The AIPW error is the product $(\hat\mu_1 - \mu_1)(1 - e/\hat e) = 2 \times (1 - 0.9/0.8) = -0.25$: zero if either model is right.
4. $\phi = 12 - (57 - 60)/0.1 = $ **42.0**. A three-room surprise on a rare untreated resort night gets weight $1/(1 - 0.9) = 10$, because overlap is thin there: the binary version of the pinned nights, and why the CATE's interval is wide where $e(x)$ is near 0 or 1.

### M8-R5
1. The first sentence, *the RM system is the only thing setting rates*, is false. The unlogged reason (local knowledge $U$) moves both rate and bookings.
2. No. $U$ is not in $X$, and flexibility in $g(X)$ cannot adjust for a variable that isn't there.
3. An override that moves both the same way (a wedding block raises the rate and bookings) biases the estimate **toward zero**, as the category did on the six nights, so the truth lies further below −1.32 and the decision stands. Moving them in opposite directions (a rate raised to hold rooms back) makes −1.56 **too elastic**, and the rise could pay. The logs show neither.
4. With equal shares and the residual ratio 3.0, the bound gives: partial $R^2$ of 1% → bias 0.03; 2% → 0.06; 5% → 0.15; **10% → 0.32**, range [−1.88, −1.24], which crosses −1.32. The robustness value solves $q/\sqrt{1-q} \times 3.0 = 0.24$: **$q = 7.7\%$** on each side.
5. At 1× the event flag: $\sqrt{0.06 \times 0.04/0.96} \times 3.0 = $ **0.15**, range [−1.71, −1.41]: the decision survives. At 2×: $\sqrt{0.12 \times 0.08/0.92} \times 3.0 = $ **0.31**, range [−1.87, −1.25]: it crosses. The decision is overturned at about **1.6×** the flag. That is plausible, because overrides respond to exactly the events the calendar misses, but it would also need the override to push rate and bookings in opposite directions.

   The recommendation survives **conditionally**. Sensitivity prices the doubt; it does not test the assumption. Randomized rate variation comes before any bigger move. Bridge line: *"Meeting 9 returns to the overrides."*

### M9-R1
1. **Unconfoundedness given the signals**, with positivity and consistency: the M7 and M8 assumption. The simulator learned $\E[Y \mid D, X]$ and the distribution of $X$ from the logs; sampling from it at a new rate is the g-formula. Its "bookings at another rate" are causal only if the logs' rates were as good as random given the 47 signals. The overrides are exactly where that fails.
2. **From the data:** the signals' joint distribution, the shape of demand across nights, the noise. **From the analyst:** the elasticity −1.50, the override effect (+12% demand, +10% rate), and its 8% share.
3. **No.** A simulator learned from confounded logs inherits their confounding, and the truth inside it is planted by the team. It can test whether an estimator recovers a truth on data shaped like Qiantan Hotels'. It cannot reveal Qiantan Hotels' truth.

### M9-R2
1. Bias (mean − (−1.50)): **+1.92, +0.32, +0.01, +0.09, +0.13**.
2. DML with boosted trees: unbiased with near-nominal coverage (0.94) on this data shape. The RM rule is a step function of bucketed signals with interactions. Lasso fits it with smooth linear terms, so part of the rule stays in the residuals (regularization bias), and coverage falls to 0.71.
3. If the real overrides act like the planted ones, DML is about 0.13 too close to zero, so the truth is near $-1.56 - 0.13 = $ **−1.69**. That is further from −1.32, so the decision **does not change: do not raise**.
4. Whether the real overrides look like the planted ones. Their size and correlation with demand were **chosen**; the logs cannot reveal them. Turn the dial (A4 does) and report the decision across settings: that is a sensitivity analysis, not a measurement.

### M9-R3
1. Boosted simulator: vendor 380 < DML 690 < RM 1,450. Neural: DML 760 < RM 1,520 < vendor 2,240. Worst-case regret: RM 1,520, vendor 2,240, **DML 760, the smallest**.
2. **Home advantage.** The vendor's demand model and the boosted simulator are the same model class fitted to the same logs, so the vendor's errors are the simulator's errors. The neural simulator does not share them. A pipeline should be ranked across simulators of different classes, never on its own class alone.
3. Both simulators have little data above ¥1,920 (5% of logged nights); both largely extrapolate the shapes they learned. On 14% of the vendor's nights the regret measures one model against another, not against reality. Treat those nights as untested, or cap rates at the logged range.
4. **The optimizer's curse.** Choosing, every night, the rate with the highest *predicted* contribution selects the rates where the prediction is most optimistic. This is the winner's curse of M4, and it is why the realized loss exceeds the model's average error. Errors compound: the prediction error becomes a pricing error.
5. Near current rates both simulators pass: $4.6$ is 0.2 from 4.8 and $3.4$ is 1.4 from it, about one SE. The backtest is weak evidence (it rejects neither) and says nothing above ¥1,920, where the two pipelines differ most. A backtest earns trust only in the region it covers.
6. **DML elasticity, then optimize**: the smallest worst-case regret, and it stays inside the logged range. Run it with a **holdout**: a random 10% of hotel-nights stay on the current rule (or alternate by night, a switchback), so realized contribution can be compared. Pilot the vendor's engine the same way, only with rates capped at the logged range.

### M9-R4
1. In R1 the analyst planted the truth on top of what was learned from Qiantan Hotels' own logs, so an estimator can be checked against it. Here the truth is **asserted**: it is whatever the language model's priors say about guests in general. Nobody planted it, and nothing ties it to Qiantan Hotels' guests.
2. Believe the evidence with a design: M8 (−1.56, conditional on its assumption), the testbed (direction of the override bias), and above all a randomized test. The Q3 test (R5) settles it: −1.72. The synthetic number is a hypothesis, not evidence.
3. **No.** A testbed needs a known truth on the business's data shape; the synthetic guests' truth is unknown. (CEVAE sits on the same side: its identification rests on structure it does not state.)

### M9-R5
1. Model labels: $0.22 - 0.15 = $ **0.07**, which trips the 5-point guardrail.
2. Gold rates: higher $36/200 = 0.18$, current $28/200 = 0.14$, effect **0.04**. Higher arm: catches $34/36 = 0.944$, flags $12/164 = 0.073$. Current arm: catches $26/28 = 0.929$, flags $4/172 = 0.023$.
3. **Differential error.** On higher-rate nights more reviews mention the price without complaining (*"worth it even at this price"*), and the model flags them, so the false-positive share is three times higher. The treatment changed the text, and with it the model's error.
4. Non-differential error with the current arm's shares scales the effect by $26/28 - 4/172 = 0.905$: $0.905 \times 0.04 = $ **0.036**, attenuated toward zero. The actual 0.07 is **inflated**: differential error manufactured about 0.03 of the effect.
5. PPI. Higher: model rate in the subsample $46/200 = 0.23$, correction $0.18 - 0.23 = -0.05$, corrected **0.17**. Current: $30/200 = 0.15$, correction $-0.01$, corrected **0.14**. Effect **0.03**.
   - **Unbiased:** each arm's correction is estimated from a random subsample *of that arm*, so the corrected rate is unbiased whatever the error looks like, provided the gold labels are right.
   - **More precise:** the 5,000 model labels carry the level; gold labels only estimate a small correction, whose variance (about 0.07 and 0.03 per review) is far below the outcome's (about 0.15 and 0.12).
   - SEs: $\sqrt{0.22 \cdot 0.78/5000 + 0.0675/200} = 0.019$ and $\sqrt{0.15 \cdot 0.85/5000 + 0.0299/200} = 0.013$, so 0.023 for the effect; gold alone $\sqrt{0.18 \cdot 0.82/200 + 0.14 \cdot 0.86/200} = 0.037$. (The gold reviews are a subsample of the 5,000, so this SE is a slight approximation; the notes say how.)
6. Corrected 0.03, 95% CI $[-0.015, 0.075]$. Below the guardrail at the point estimate, but the interval includes 5 points: **not tripped, not cleared**. A larger gold sample would settle it; here the bookings result makes it moot.
7. $\ln(1 - 0.124)/\ln 1.08 = $ **−1.72**; interval from $-12.4\% \pm 1.96 \times 1.2\%$: **[−2.07, −1.38]**. That is consistent with M8 (−1.56) and the testbed (about −1.69), and it excludes the break-even of −1.32, narrowly. **Do not raise.**

### M9-R6
1. Listing pages **as of each night** are pre-treatment: written before the rate, they proxy for quality, a confounder. Legitimate. That night's **reviews** are written after the stay: caused by the rate (value perceptions) and by bookings (crowding). They are post-treatment, and they encode the outcome. **Leakage**; never a control.
2. DML uses only the variation in the rate left after the controls, so its SE scales roughly as $1/\sqrt{\text{share left}}$: from 9% to 1% is a factor of $\sqrt{9} = 3$ (0.03 → 0.09); from 9% to 6%, $\sqrt{1.5} = 1.22$ (0.04). **Overlap collapse**: almost no rate variation remains that the text cannot predict.
3. The reviews carry part of the effect and the outcome itself. Controlling for them absorbs the effect (as a mediator would) and opens collider paths, which pulls the estimate toward zero: −0.97.

### M9-R7 (model memo)
> Do not raise midweek premium rates by 8%. The Q3 test puts the elasticity at −1.72 (95% CI −2.07 to −1.38), past the break-even of −1.32, and it agrees with Meeting 8's −1.56 once the override bias the testbed found is allowed for. Pilot DML-based pricing, with rates capped at the logged range and 10% of hotel-nights held out on the current rule. Pilot the vendor's engine only on the same terms: it won only on a simulator built like itself. The synthetic-guest report is not evidence; its −0.9 is the model's prior, and the Q3 test contradicts it. On reviews, the model's labels said complaints rose 7 points, but the gold-corrected rise is 3 points, with an interval up to 7.5, so the guardrail neither tripped nor cleared. The advice rests on Q3 at 40 hotels carrying over to all 80.

Grade on the same five dimensions as Case A.

## Bonus key (Parts B1–B4)

These are the keys of the former Meeting 9 (instrumental variables), unchanged except for the part numbers. The full-test ladder and the city hotels (former R4) and the IV memo (former R6) were dropped.

### B1
1. Contribution goes from 600 to 536. Bookings must rise more than $600/536 - 1 = $ **11.9%**. $\eta^* = \ln(600/536)/\ln(0.92) = $ **−1.35**. M8's DML said −1.56, but only if the overrides did no harm.
2. The coin randomizes **what members were offered**. It does not randomize **what they were shown**, because managers could block or add.

### B2
1. As shown: $(350 \cdot 64 + 50 \cdot 40)/400 = 61.0$ vs $(150 \cdot 90 + 450 \cdot 70)/600 = 75.0$, a difference of **−14.0**.
2. As assigned: heads 71.8, tails 67.0, **ITT = +4.8**.
3. First stage: $0.70 - 0.10 = $ **0.60**.
4. Most pairs who used row 1 say "never cut". Same log, opposite sign: managers chose which heads to honor.
5. Ratio: $4.8/0.60 = $ **8.0** extra bookings on nights the coin switched the rate on, for the **compliers**. $SE(\mathrm{ITT}) = 20\sqrt{2/500} = 1.26$, so $SE \approx 1.26/0.60 = 2.1$ and the CI is [3.9, 12.1].

   On a base of 60, that is an elasticity from −0.75 to −2.21. **It straddles −1.35**: a thousand nights cannot decide. Cluster by date in the full test.
6. Night types:
   - always-takers (dead nights; the manager applies the rate by hand): 0.10;
   - never-takers (near sell-out; the manager blocks it): 0.30;
   - compliers: 0.60;
   - defiers assumed 0.
7. $\ln(68/60)/\ln(0.92) = $ **−1.50**: past break-even, on complier nights.
8. Sentences:
   - within hotel × month → **independence given strata**;
   - one thing changed → **exclusion**;
   - most heads honored → **relevance** (0.70 vs 0.10);
   - none reversed → **monotonicity**.

   Randomization buys only the first. Hold onto the second.

### B3
1. ITT becomes 6.0, the ratio 10.0, and the elasticity $\ln(70/60)/\ln(0.92) = $ **−1.85**. Bias $= 1.2/0.60 = 2.0$ bookings: **the ratio divides the violation by the first stage.** Nothing in the test log shows it.
2. The old-engine hotels' first stage is zero by construction, so their heads–tails gap of 1.2 is the email alone. Corrected ratio $(6.0 - 1.2)/0.60 = $ **8.0**.
   - The correction assumes the email works the same everywhere: a patch, not a proof.
   - The clean fix is design: send the email on both sides of the coin.
   - A zero-first-stage group is almost the only place exclusion can be tested.
3. Within type: resort $4.8/0.60 = 8.0$; airport $4.8/0.60 = 8.0$. Pooled: heads $(350 \cdot 84.8 + 150 \cdot 54.8)/500 = 75.8$ and tails $(150 \cdot 80 + 350 \cdot 50)/500 = 59.0$, so the ratio is $16.8/0.60 = $ **28.0**. Heads nights are mostly resort nights. **Here controls buy independence, not precision.**
4. Controls:
   - **Required:** hotel × month, which sets the coin's probability.
   - **Optional:** the 47 signals, which shrink the SE.
   - **Never:** "manager overrode" and "rate shown", which the coin caused (M7's bad controls).
   - 2SLS is FWL applied to the ratio. Running the two stages by hand gives the right point estimate but the **wrong SE**, because the fitted regressor is treated as data. Take the SE from the IV routine.
5. With direct effect $a$: $\text{LATE} = (6.0 - a)/0.60$, and the elasticity is $\ln\{(60 + \text{LATE})/60\}/\ln 0.92$.

   | $a$ | 0 | 1.2 | **1.71** | 2.4 |
   |---|---|---|---|---|
   | elasticity | −1.85 | −1.50 | **−1.35 (break-even)** | −1.14 |

   The old-engine placebo measured 1.2, only about 0.5 bookings from the point where the cut stops paying. The data cannot say which column is true; the table prices the doubt.
6. **If the email continues, it is part of the policy, not a bias.** Exclusion matters only for attributing effects to the *rate*. Wendy then needs the effect of the program as it will run, which is the ITT side (ITT 6.0 bookings per heads night, with managers' overrides included), converted to contribution. The email-corrected elasticity answers a different question: the member rate *without* the email. Make students say which program they are pricing.

### B4

| Candidate | Relevance | Independence | Exclusion | Monotonicity |
|---|---|---|---|---|
| Competitor's rate | ✓ the system reacts to it | ✗ competitors see the same demand | ✗ guests compare rates directly | ? |
| Rainfall | ? weak | ✓ | ✗ rain moves demand itself | ? |
| System outage | ✓ | ? outages cluster at peak load | ✓ plausible | ✗ freezing raises some rates, lowers others |
| Manager on shift | ✓ managers differ | ✓ if the rota is set in advance | ? managers also upsell and handle groups | ? strict on weddings, lenient on conferences |
| Member-rate coin | ✓ 0.60 | ✓ within strata | ✗ the email, fixable | ✓ no reversals |

Most fail on **exclusion**, which the data cannot test in general. The coin passes because someone designed it, and even it failed once.


## 4. Deck issues found while aligning the case

The issues listed here earlier are resolved in the rebuilt decks:

1. **M8 release order** (resolved): "Predict Before You Look" and "The Ladder" are gone, and `[RELEASE R3]` sits on "The Real Logs", the first frame with the log summary and the RM rule. (The R1 frame names the 80 hotels and 47 signals, as Part R1 does.)
2. **M8 outputs as figures** (resolved): "The Exhibit" and "Wendy's Table" are gone. The decision table is in the text of "The Price Elasticity at Qiantan Hotels", and every M8 number is checked by `shared/checks/slides08_check.py`.
3. **The M9 deck is replaced.** The old IV deck's frames (Wald ratio, ladder, $F = 410$) survive only in git history (commit `5522695`) and in the bonus parts. The new deck follows the M9 notes' order with this case's numbers.
4. **Case framing** (resolved): "Qiantan Hotels: The Proposal" states that the RM system is an automated decision-maker.
