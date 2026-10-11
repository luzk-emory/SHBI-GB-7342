# Case A: Lena's coupon program

**Houtan Coffee, a coffee chain, Meetings 1–7.** Fictional teaching case: the company, the people, and all data are invented.

This case is handed out one part at a time. Each part is released in class after the previous task is done. When a task says *commit*, write your answer down before the class discusses it, even if you are unsure.

Parts are labeled by meeting and release: Part M3-R2 is the second part released in Meeting 3, and a letter (Part M3-R2b) marks a short part released between two others.

The economics hold throughout unless a part says otherwise: a purchase earns **¥30 of margin**; a coupon is paid on **every** purchase its holder makes, including purchases they would have made anyway.

---

## Meeting 1: The coupon and the coin

### Part M1-R1. Marketing's pilot

Lena runs customer analytics at Houtan Coffee, a coffee chain with **10,000 loyalty members**. Marketing wants to send every member a coupon worth **¥10 off** the next purchase.

Their evidence is a Q1 pilot in one region of 1,000 members. The coupon went to 500 of them, the ones marketing judged most loyal.

| | Got coupon | No coupon |
|---|---:|---:|
| Purchase rate | 0.68 | 0.24 |

Marketing's reading: *"The coupon lifts purchases by 44 points. Send it to everyone."*

**Tasks**
1. Let $p_1$ be the purchase rate among coupon holders and $\tau$ the lift the coupon causes. Write the net value of one coupon sent.
2. What lift does the coupon need to break even? Evaluate it at marketing's $p_1$.
3. Taking marketing's 0.44 at face value, what is the coupon worth per coupon and across the base?
4. Commit: name one reason to doubt the 0.44.

### Part M1-R2. A thought experiment: Four kinds of customer

**Warm-up.** Four customers from the pilot: A got the coupon and bought; B did not get it and bought; C got it and did not buy; D did not get it and did not buy. For each, write the potential outcome you know, $Y(1)$ or $Y(0)$, and the one you don't. Which response types (below) is each customer compatible with?

Nobody can see these types; imagine that you could. For each customer there are two worlds, one with the coupon and one without. In the pilot region:

| Type | Buys without coupon? | Buys with coupon? | Count |
|---|---|---|---:|
| Lost Cause | no | no | 400 |
| Sure Thing | yes | yes | 300 |
| Persuadable | no | yes | 200 |
| Do-Not-Disturb | yes | no | 100 |

Marketing picked the 500 most loyal for the coupon:

| Type | Coupon (500) | No coupon (500) |
|---|---:|---:|
| Lost Cause | 100 | 300 |
| Sure Thing | 220 | 80 |
| Persuadable | 120 | 80 |
| Do-Not-Disturb | 60 | 40 |

**Tasks**
1. Compute the purchase rate in each arm. Check that you reproduce marketing's numbers.
2. Compute the true average effect of the coupon in the region.
3. Among the 500 who got the coupon, what was its average effect? How much of marketing's 0.44 is left over, and where does it come from?
4. What was the coupon's average effect among the 500 who did *not* get it? Check that the region's average effect is the average of the two.
5. At the recipients' effect, does a coupon to the pilot's own recipients pay?
6. For one customer of each type, what does sending the coupon change in margin (¥30 per purchase, coupon paid only on redemption, no contact fee)? Which type makes the coupon expensive, and which costs nothing?

### Part M1-R3. Who got the coupon decides the sign

Lena's CRM splits the whole base into two segments of 5,000. Take these segment numbers as given for now; estimating them comes later.

| Segment | Purchase rate with coupon | Purchase rate without | Effect |
|---|---:|---:|---:|
| Active | 0.80 | 0.75 | +0.05 |
| Lapsed | 0.30 | 0.10 | +0.20 |

Two ways a manager might have run the pilot on the whole base, with one segment treated and the other as the "control":

- (a) coupon to all active members; the lapsed are the comparison.
- (b) coupon to all lapsed members; the active are the comparison.

**Tasks.** For (a) and (b), in pairs:
1. Compute the naive treated-minus-control difference.
2. Split it into the effect on the treated plus selection bias.
3. Commit: which manager would conclude the coupon hurts?

### Part M1-R4. The Q2 test

In Q2 Lena ran a proper test in the pilot region: 500 of the 1,000 members were drawn to receive the coupon. From Lena's log:

- "The 500 recipients were drawn by a random number generator; the seed is in the log."
- "Nobody could opt in, and nobody was removed after the draw."
- "One coupon design, sent in the app, single-use, and tied to the account."
- "Store staff did not know who held a coupon."

Result: the coupon arm bought at **0.50**, the control arm at **0.40**.

**Tasks**
1. Estimate the effect. If the thought-experiment types of Part R2 had been split at random, half of each type in each arm, what would each arm's purchase rate be?
2. For each log sentence, say what it guarantees about the comparison.
3. Recompute the break-even at the test's $p_1$. Does the coupon pay? What is the forecast across the 10,000 members, compared with marketing's?
4. The seed could have produced a different draw. One possible draw puts 195 Lost Causes, 155 Sure Things, 105 Persuadables, and 45 Do-Not-Disturbs in the coupon arm, and the rest in control. What would the estimate have been? Was that draw "broken"?

### Part M1-R5. Segment economics and data roles

Apply the same economics segment by segment, using the table in Part R3.

**Tasks**
1. For each segment compute the net value per coupon and the segment's own break-even lift.
2. Value two policies on the 10,000 members: coupon everyone; coupon the lapsed only.
3. The Q2 export has these columns: `member_id`, `coupon`, `purchase_7d`, `tier`, `recency`, `spend_q1`, `redeemed`, `app_opens_q2`, `seed`, `draw_time`. Give each column exactly one role: unit, treatment, outcome, pre-treatment covariate, post-treatment variable, or audit.
4. **Exit ticket, three sentences:** the comparison a coupon decision needs; why marketing's 0.44 misleads; one reason not to roll out even though the Q2 lift is positive.

---

## Meeting 2: Real, profitable, and where it holds

### Part M2-R1. The Q2 test, read two ways

| | Members | Bought | Purchase rate |
|---|---:|---:|---:|
| Coupon | 500 | 250 | 0.50 |
| No coupon | 500 | 200 | 0.40 |

**Marketing:** *"It was randomized, and it's significant. The coupon works. Roll it out."*
**The CFO:** *"Last week you said it loses ¥2 a coupon. Which is it?"*

**Tasks**
1. Compute the standard error of the difference without assuming any null hypothesis, and the 95% interval.
2. Test the difference against zero, then against the break-even from Meeting 1.
3. Write the net value per coupon as a combination of the two arm rates, $p_1$ and $p_0$. Give its standard error and 95% interval.
4. Commit: who is right, marketing or the CFO?
5. Marketing proposes dropping members who never opened the app from both arms: *"they never saw the coupon."* Why not? What does the comparison of all members, as drawn, estimate?
6. The 1,000 members are fixed; only the coin was random. In your Meeting 1 workshop, 200 redraws of the coin had a standard deviation of about 0.026. Is the SE from task 1 exact, too small, or conservative for this region? Why?

### Part M2-R2. Two second campaigns

Two regions propose Q3 campaigns. Each will be tested properly, with a 50/50 random draw **within its own list**. Use the segment effects of Meeting 1.

| List | Active on the list | Lapsed on the list | Total |
|---|---:|---:|---:|
| Campaign A ("loyal") | 400 | 200 | 600 |
| Campaign B ("lapsing") | 200 | 400 | 600 |
| Whole base | 5,000 | 5,000 | 10,000 |

From the campaign brief: *"The same coupon, in the same app, in the same quarter."*

**Tasks**
1. What effect will each test measure? Is either test biased?
2. For each list, compute the purchase rate with the coupon, the break-even, and the net value per coupon. Compare with the whole base.
3. Which sentence in the brief lets you carry segment effects from the Q2 test to these lists?

### Part M2-R3. The next test

The Q2 test settled one question: do not coupon everyone. Lena proposes two Q3 tests.

- **A lapsed-only coupon test.** Does the coupon pay on lapsed members? Planning values: $p_1 = 0.30$, $p_0 = 0.10$, so a lift of 0.20 against a break-even of 0.10.
- **An in-store buy-one-get-one (BOGO) offer.** It runs on the menu board, so it cannot be sent to individuals. (Part R4.)

**The constraint:** the test window reaches about 350 lapsed members, **175 per arm**. Among lapsed members in the Q2 data, Q1 purchases and the Q2 purchase outcome correlate at **0.6**.

**Tasks.** Use a 5% two-sided test with 80% power.
1. What minimum detectable effect (MDE) does the decision need?
2. What is the MDE with 175 per arm? How many per arm would be needed?
3. Adjust the outcome for Q1 purchases (CUPED). Recompute both numbers. Does the test now fit the window?
4. Why is it legitimate to use Q1 purchases here, but not `app_opens_q2`?
5. Before the lapsed test starts, list five things that must be fixed in writing, and one check you would run on the first day's data.

### Part M2-R4. The in-store offer

The BOGO goes on the menu board: everyone in a store sees it. Lena plans 50 stores, 25 per arm, with about 400 customers per store-week and 20,000 customers in all. In the Q2 data the correlation of weekly purchase between two customers of the same store (the ICC) is **0.01**.

**Tasks**
1. What is the unit of assignment, and why can it not be the customer?
2. Compute the design effect and the effective number of independent customers.
3. By what factor does the correct standard error exceed the customer-level one? Which one would marketing report?
4. Three more complications: staff could push the BOGO at the till; some customers use two stores; the offer may carry over into the following week. For each, which unit or design would protect the comparison, and what does it cost in independent units?

### Part M2-R5. The memo

Write Lena's memo on the Q2 test in four sentences, one judgment each:
1. Is the comparison causal, and for whom?
2. The estimate and its interval.
3. Against the break-even: does it pay?
4. What should the next test change?

### Part M2-R6. Who saw the coupon?

Back to marketing's proposal in Part R1: drop the members who never opened the app. Lena pulls the app log for the Q2 test. A member saw the coupon only if they opened the app during the coupon week; members in the control arm had no coupon to see.

| Arm | Members | Opened the app | Bought, among openers | Bought, among non-openers | Bought, all |
|---|---:|---:|---:|---:|---:|
| Coupon | 500 | 400 | 230 | 20 | 250 |
| No coupon | 500 | 360 | 180 | 20 | 200 |

From Lena's log:
- "The draw decided who was sent the coupon. Nobody in the control arm could get one."
- "The coupon reached a member only through the app; the push notification said *You have a new offer*, without the amount."
- "Any purchase by a member of the coupon arm got ¥10 off at the till, whether or not they had seen the coupon."

**Tasks. In pairs, commit first**
1. Compute three comparisons: all members as drawn; openers only (marketing's proposal); members who **saw** the coupon against everyone who did not.
2. What share of the coupon arm saw the coupon? Divide the comparison of all members as drawn by that share. What does the ratio measure, and for whom?
3. Members in the coupon arm who never opened the app would not have seen a coupon in either arm. What is their purchase rate? Use it, and the control arm, to find the purchase rate that members who *would* see a coupon have without it. Check that their treated rate minus this untreated rate gives the ratio from task 2.
4. Why are the openers in the two arms not the same people? Which way does the openers-only comparison miss, and why?
5. Match each log sentence to the assumption it supports. Suppose the notification had said *¥10 off your next coffee*. Which assumption would that threaten, and in which direction would the ratio move?
6. Among members who see the coupon, does it pay? (Use the break-even rule from Meeting 1 with their purchase rate when they see it.) Lena's team proposes a text message to reach the non-openers. What does the ratio tell you about that proposal, and what does it not?

---

## Meeting 3: Coupon whom?

### Part M3-R1. Two lists for 5,000 coupons

The CFO has approved **5,000 coupons** for Q3, half the base. Two lists are on Lena's desk.

- **Marketing's data science team:** a purchase model on last year's transactions. *Send to the 5,000 members most likely to buy. "They are our best customers. They will redeem."*
- **Lena:** send to the 5,000 members the coupon *moves* most. *"That is exactly the problem."*

On the two segments of Meeting 1, marketing's model ranks the active members first; Lena's rule ranks the lapsed first.

From Lena's documentation of the Q2 export:
- "The Q2 draw was 50/50 in every region, tier, and store."
- "All CRM fields were frozen the day before the draw."
- "Members who joined during Q2 were not in the draw."

**Tasks**
1. Write the rule for sending a coupon to a customer with fields $x$, in terms of their lift $\tau(x)$ and their purchase rate with the coupon $\mu_1(x)$.
2. Value each list: net per coupon, and total for 5,000 coupons.
3. For each documentation sentence, say what it buys. Which sentence matters for the Q3 list rather than for the Q2 estimate?

### Part M3-R2. Four customers

Lena fits the interaction model $Y = \alpha + \tau D + \beta X + \gamma (D \times X)$ with $X = 1$ for active members and $X = 0$ for lapsed. From the four cell means: $\hat\alpha = 0.10$, $\hat\tau = 0.20$, $\hat\beta = 0.65$, $\hat\gamma = -0.15$.

| Customer | Segment | Coupon $D$ | Bought $Y$ | $\hat\mu_0(x)$ | $\hat\mu_1(x)$ | Coupon? |
|---|---|---:|---:|---|---|---|
| A | active | 1 | 1 | | | |
| B | active | 0 | 1 | | | |
| C | lapsed | 1 | 0 | | | |
| D | lapsed | 0 | 0 | | | |

**Tasks**
1. Fill in both predicted columns for every row, whichever arm the row was in, then the decision.
2. Recover the average effect on the base (half active, half lapsed) from the coefficients.
3. Recode the field as $L = 1$ for lapsed. Write $\tau$ as a function of $L$. Did anything substantive change?
4. What is the average effect on a list that is 80% active and 20% lapsed? Why is the coefficient on $D$ (0.20) not the answer for either list?

### Part M3-R2b. Is the gap itself noise?

Behind the segment rates: in the Q2 test, 200 members per arm in each segment.

| Segment | Coupon: bought / members | No coupon: bought / members |
|---|---:|---:|
| Active | 160 / 200 | 150 / 200 |
| Lapsed | 60 / 200 | 20 / 200 |

**Tasks**
1. Estimate each segment's effect and its standard error.
2. Estimate the gap between the two effects and its standard error. Is the heterogeneity distinguishable from noise?
3. An analyst writes: *"The effect is significant for lapsed members and not for active ones, so the coupon works differently."* What is wrong with the argument?

### Part M3-R3. Same fit, opposite decisions

Two models of the two-segment world, each fitted to 10,000 members split 50/50:

- **Model I** (interaction): reproduces the four cell means exactly.
- **Model A** (additive, no $D \times X$ term): $\hat\mu = 0.1375 + 0.575x + 0.125D$.

**Tasks**
1. Give each model's predicted lift for active and for lapsed members.
2. Compute each model's outcome RMSE. (Hint: with the true cell purchase rates $p$, the irreducible part is the average of $p(1-p)$ over the four cells.)
3. Each model ranks members by predicted lift and sends 5,000 coupons. What does each list earn? (If a model ties everyone, it picks at random.)
4. Commit: how much does RMSE differ, and how much does the decision differ?
5. The same lesson, one row at a time. For lapsed members the truth is $\mu_1 = 0.30$, $\mu_0 = 0.10$. T-learner A predicts 0.35 and 0.15; T-learner B predicts 0.33 and 0.07. Which fits each outcome better? Which gets the effect right?

### Part M3-R4. The Q2 export

| | |
|---|---|
| CRM fields, frozen before the draw | 14 |
| Coupon arm / control arm | 50% / 50% |
| Coupons available for the Q3 list | 5,000 |

Four learners, each fitted on the same training folds:
1. interaction OLS: $D$, the 14 fields, and $D$ times each field;
2. S-learner with lasso;
3. S-learner with boosted trees;
4. T-learner with boosted trees.

**Task.** In pairs, predict and commit: which learner has the best out-of-fold outcome RMSE? Which list of 5,000 earns the most? Are they the same learner?

### Part M3-R6. A column written by a language model

Marketing has a new idea. Members leave free-text feedback in the app ("moved offices, not near a store any more", "too expensive now", "love the new oat latte"). The data science team proposes to have a **language model read each member's text and label them "drifting away: yes/no"**, then use the label as the targeting field in place of the CRM's lapsed flag.

On 200 members whose CRM status is known, the model's label was right **80% of the time** in each group.

**Tasks**
1. Some comments were written *after* the Q2 coupons went out. Which comments may be used to build a pre-treatment field, and why?
2. Suppose the true effect modifier is exactly the lapsed flag, and the model's label is wrong for 20% of lapsed and 20% of active members. Among the 5,000 members labeled "drifting", what are the coupon's lift and the purchase rate with the coupon? What is a coupon worth there?
3. What does the 5,000-coupon list built on the label earn, compared with the list built on the true flag?
4. What does labeling error do to the *gap* between the two groups' estimated effects?
5. Commit: how accurate must the label be for the labeled list to break even?

---

## Meeting 4: Honest segments

### Part M4-R1. A segment card

Store managers will not run a black-box score. They want a **card**: at most four segments, each marked *coupon* or *no coupon*.

Last year a consultant searched hundreds of segment definitions in a test like this one and reported a "hidden gem" segment with a spectacular lift. The rollout delivered a fraction of it.

This time the CFO has set a rule. Lena's Region 2 coupon test (4,000 members, a 50/50 draw, as in Q2) is split at random into two halves of 2,000:

| Step | Data | Output |
|---|---|---|
| H1 discovery | half A, outcomes visible | a partition, submitted in writing |
| H2 estimation | half B, outcomes locked until H1 is in | one number per segment |
| H3 recommendation | H2's numbers only | the card |

From the CFO's rule and Lena's log:
- "Members were split into halves by a random draw on member ID, before anyone looked."
- "Half B's outcomes were held by the CFO's office until every partition was submitted."
- "Each half kept its own 50/50 coupon draw."

**Task.** Which of the three sentences is most often broken in practice, and how?

### Part M4-R2. Region 2: Two fields, four cells

Two CRM fields: **customer type** (executive or analyst, from the job-title field) and **spending history** (high or low). These are the population truths a perfect analysis would find. The data only ever shows noisy versions.

| Type | Spending | Share | Rate with coupon | Rate without | Effect |
|---|---|---:|---:|---:|---:|
| Executive | High | 25% | 0.65 | 0.60 | +0.05 |
| Executive | Low | 25% | 0.35 | 0.30 | +0.05 |
| Analyst | High | 25% | 0.50 | 0.30 | +0.20 |
| Analyst | Low | 25% | 0.20 | 0.00 | +0.20 |

**Tasks**
1. Which field modifies the effect, and which only shifts the purchase level?
2. For each line, compute its own break-even lift and the net value per coupon.
3. Which line is closest to its break-even, and by how much?

### Part M4-R3. H1: Search, then commit

On half A, Lena's causal tree (all 14 fields, depth 2) returns four leaves:

| Leaf | Half-A lift | Break-even |
|---|---:|---:|
| Analyst, low spend | 0.23 | 0.067 |
| Analyst, high spend | 0.21 | 0.167 |
| Executive, app user | 0.19 | 0.167 |
| Executive, no app | 0.01 | 0.167 |

(Executives average a purchase rate of 0.50 with the coupon, hence their break-even.)

**Tasks**
1. **In pairs, in writing, now:** submit the partition (four leaf definitions) and the card you would print. Half B's outcomes are released only after every pair has submitted.
2. **Two noisy splits.** On a discovery sample with an overall lift of 0.10, split A shows leaf lifts (0.02, 0.18) and split B (0.09, 0.11), each on half the members. Score both with $\Delta = 0.5(\hat\tau_L - 0.10)^2 + 0.5(\hat\tau_R - 0.10)^2$. Which wins? Fresh data give split A (0.08, 0.12). What happened to the gap?
3. By hand: 20 candidate segments all have a true lift of 0.125, each estimated with an SE of 0.04. The expected largest of 20 standard normal draws is 1.87. What lift does the best-looking segment show on average? Compare it with the analyst–high break-even.
4. **A second split costs information.** A leaf has 250 members per arm, buying at 0.50 with the coupon and 0.30 without. Compute the SE of its lift. Split it into two halves with the same rates. What are the new SEs? What would all 500 per arm give, and what was gained by splitting?

### Part M4-R4. H2: The same leaves on half B

Buyers / members in each arm:

| Leaf | Coupon | No coupon |
|---|---:|---:|
| Analyst, low spend | 50 / 250 | 0 / 250 |
| Analyst, high spend | 125 / 250 | 80 / 250 |
| Executive, app user | 100 / 200 | 92 / 200 |
| Executive, no app | 150 / 300 | 132 / 300 |

**Tasks**
1. Compute each leaf's half-B lift and its SE.
2. Revise your card. Which lines changed, and in which direction did every leaf the search liked move? What happened to the leaf the search disliked?

### Part M4-R5. H3: The card

Honest intervals from half B. The 98.75% intervals (lift ± 2.50 SE) hold all four lines at once with probability 0.95.

| Leaf | 95% interval | 98.75% interval | Break-even |
|---|---|---|---:|
| Analyst, low spend | [0.15, 0.25] | [0.14, 0.26] | 0.067 |
| Analyst, high spend | [0.10, 0.26] | [0.07, 0.29] | 0.167 |
| Executive, app user | [−0.06, 0.14] | [−0.08, 0.16] | 0.167 |
| Executive, no app | [−0.02, 0.14] | [−0.04, 0.16] | 0.167 |

**Tasks**
1. Write the card. For the analyst–high line answer two questions: is the effect real? does it pay?
2. A colleague proposes to merge the two executive leaves into one line and re-estimate it on half B. May the card print them as one line? May the merged estimate be reported?

---

## Meeting 5: What is the list worth?

### Part M5-R1. The engine wants to run the send

The 5,000 Q3 coupons go out next month. The chain has just licensed an **automated campaign engine**: it builds targeting lists from the Q2 export and would send the coupons itself. Three lists are on Lena's desk, each built on the training folds of the Q2 export:

| List | How it was built |
|---|---|
| Segment rule | All 5,000 lapsed members. No model. |
| Forest, top 5,000 | The engine: top 5,000 by a causal forest's predicted lift (Meeting 4) |
| Forest, engine's cut-off | The same ranking, cut where the engine itself chooses |

The CFO asks one question: *what will each list earn, compared with sending nothing?* Nobody's individual effect is observed. The CFO's rule: nothing the engine proposes goes live until it has been valued on a fold of the Q2 test it has never seen. That fold's outcomes stay locked until each list is **frozen**.

**Tasks**
1. Define a list's gain over sending nothing, per member of the base.
2. By hand, on the 10,000-member base, value three lists: coupon nobody; coupon everyone; the segment rule.
3. What number must a model's list beat?

### Part M5-R2. Denominators

The top 20% of an evaluation fold of 5,000, ranked by one model. Within the top group the arms are random, not equal:

| | Members | Bought | Rate |
|---|---:|---:|---:|
| Coupon arm | 540 | 216 | 0.40 |
| Control arm | 460 | 138 | 0.30 |

**Tasks**
1. An analyst reports "78 extra purchases" (216 − 138). What is wrong with it? What is the right number of incremental purchases in the group?
2. Report the lift per member targeted, and the incremental purchases per member of the fold.

### Part M5-R3. Freeze, then evaluate

The rules for the evaluation fold:
- "The evaluation fold was drawn at random from the Q2 export before any model was fitted."
- "Its 50/50 coupon draw is intact."
- "Its outcomes are released only after each list is frozen: a file of the list's decision for every fold member, and a timestamped code snapshot."

A member's profit under decision $d$ is $(30 - 10d)\,Y(d)$. With a known coin probability of 0.5, each listed member contributes $+40$ if they were in the coupon arm and bought, $-60$ if they were in the control arm and bought, and 0 otherwise. Unlisted members contribute 0. The gain estimate is the average contribution.

A small evaluation fold of 80 members, 50/50 within each segment:

| Segment | Arm | Members | Bought |
|---|---|---:|---:|
| Lapsed | coupon | 20 | 6 |
| Lapsed | control | 20 | 2 |
| Active | coupon | 20 | 16 |
| Active | control | 20 | 15 |

**Tasks**
1. Why do the contributions take the values $+40$ and $-60$?
2. Estimate the gain per member for (a) the segment rule, (b) coupon everyone, (c) coupon the active only.
3. Give the standard error of the segment rule's estimate. Could two lists that differ by ¥1 be told apart on this fold?
4. The third rule sentence is an honesty rule. From which earlier meeting?
5. In another region the coin sent coupons to only 25% of members. What do a listed coupon-arm buyer and a listed control-arm buyer contribute there?

### Part M5-R4. The fold is unlocked

The forest split each segment in two groups of 2,500:

| Group | Rate without | Rate with | Lift | Net per coupon (¥) |
|---|---:|---:|---:|---:|
| L1 (lapsed) | 0.05 | 0.40 | 0.35 | 6.50 |
| L2 (lapsed) | 0.15 | 0.20 | 0.05 | −0.50 |
| A1 (active) | 0.75 | 0.95 | 0.20 | −3.50 |
| A2 (active) | 0.75 | 0.65 | −0.10 | −9.50 |

Gain per member of the base (¥) on an evaluation fold of 5,000, each list frozen before the fold was opened:

| List | Groups | Gain | SE | Gain minus segment rule | Paired SE | Unpaired SE |
|---|---|---:|---:|---:|---:|---:|
| Segment rule | L1, L2 | 1.50 | 0.20 | | | |
| Forest, top 5,000 | L1, A1 | 0.75 | 0.35 | −0.75 | 0.36 | 0.41 |
| Forest, engine's cut-off (2,500) | L1 | 1.625 | 0.14 | +0.125 | 0.15 | 0.25 |

**Tasks**
1. Why does the forest's top 5,000 earn less than the segment rule, although the forest ranks effects better?
2. On the selection fold the engine compared ten cut-offs and reported the best. Why would its selection-fold value have been too high, even if each cut-off's estimate was unbiased? Which number goes in the CFO's forecast?
3. Why can't you combine the two lists' SEs as if independent to judge the difference between them? What does pairing change here?
4. Write two sentences to the CFO: which list goes live, how sure you are, and the fallback.

---

## Meeting 6: Who gets the push?

### Part M6-R1. The Q4 push

Marketing wants to reach Region 2 in Q4 with something cheaper than the ¥10 coupon: an **app push notification** carrying a ¥5-off coupon for a seasonal drink. Each purchase the push causes earns ¥30 of margin.

A two-week push test in Region 2 (50/50 within every cell, 10,000 members) gave the Meeting 4 pattern again:

| Type | Spending | Estimated lift | Members |
|---|---|---:|---:|
| Analyst | High | 20% | 2,500 |
| Analyst | Low | 20% | 2,500 |
| Executive | High | 5% | 2,500 |
| Executive | Low | 5% | 2,500 |

From the test log and the Q4 plan:
- "The push test drew 50/50 within every type × spending cell."
- "Q4 sends the same push, the same ¥5 coupon, to the same members."
- "Each member receives at most one push; the coupon is single-use."

**Tasks.** Build the list one friction at a time; each step adds one thing.
1. **Free push.** Suppose, for now, that the push and its coupon cost nothing: ignore redemptions and opt-outs. Who gets one? Why could you *not* use these effects for a push sent without the coupon?
2. **A hidden cost.** 1% of notified members switch notifications off for good, at a long-run cost of ¥150 each. What is the cost per push, and the lift threshold? Who gets a push?

### Part M6-R2. The coupon is paid on redemption

Now add the ¥5 coupon. It is paid only when the member buys. Push-test purchase rates by cell:

| Type | Spending | Rate without push | Rate with push |
|---|---|---:|---:|
| Analyst | Low | 0% | 20% |
| Analyst | High | 30% | 50% |
| Executive | Low | 30% | 35% |
| Executive | High | 60% | 65% |

**Tasks**
1. For each cell compute the expected cost per push (opt-out plus expected coupon payout) and the net value.
2. Split the net value into three parts: incremental buyers, the "sure-thing" cost, and the opt-out cost. Why are two cells with the same lift no longer interchangeable?
3. **A cap.** Product management caps pushes at 1,000 a day. On a one-day send, 5,000 analysts with positive net value compete for 1,000 slots. A causal forest splits the 2,500 analyst–low members three ways: 500 at a lift of 0.30, 1,000 at 0.20, and 1,000 at 0.15. What does the capped list earn with and without the forest?
4. If every analyst gets a push, what is the expected total cost? Finance asks: *"What is the chance we exceed ¥18,000?"* What do you need in order to answer?

### Part M6-R3. Finance's memo

> The Q4 push may spend at most **¥8,000 of expected cost**, with **at most a 5% chance** of overrunning it. Product's cap of 1,000 pushes a day stands.

**Tasks**
1. Rank the cells by benefit per yuan of cost. Fill the ¥8,000 in that order. Which cell is marginal? What is the next ¥1 of budget worth?
2. Add the 5% overrun guarantee. (A member costs ¥6.50 if they redeem and ¥1.50 if not.) How many marginal-cell members leave the list, and what does the guarantee cost in expected net?
3. Does the daily cap bind?
4. Write the final list: pushes, expected cost, and expected net by cell.
5. *(Optional)* The net value of a push is $v = 25\mu_1 - 30\mu_0 - 1.50$. For analyst–high, the arm rates are estimated with independent errors, and the lift's SE is 3%. Put a one-sided 95% lower bound on $v$ itself. Does analyst–high stay on the list?

---

## Meeting 7: When the logs must answer

### Part M7-R1. The program on trial

In Q3 the engine's targeting rule went live. It sent the **5,000** ¥10 coupons of Meeting 3, half the 10,000-member base, choosing members by a **score** built from recency, tier, and spend. A daily contact cap throttled the sends.

The CFO wants the program reviewed. Sales has pulled the Q3 logs:

| | Got coupon | No coupon |
|---|---:|---:|
| Purchase rate | 0.40 | 0.62 |

Sales' reading: *"The coupon repels customers. Kill it."*
And **the CFO will not fund another experiment.** The Q3 logs must answer.

From Lena's description of the program:
- "Coupons were assigned by the scoring rule and by nothing else."
- "Every field the rule read is in the export."
- "The daily cap meant no score band was sent coupons on every day."
- "One coupon design, one channel, one redemption rule."

**Tasks**
1. Compute the break-even lift for last quarter's recipients.
2. Commit: what else could produce sales' pattern? Give the direction of the bias.
3. For each description sentence, say which assumption it is evidence for.

### Part M7-R2. Two kinds of customer

The scoring rule mostly sent coupons to lapsed members, the ones Meetings 3–5 said to target.

| Segment | Members | Coupon share | Coupon | No coupon | Purchase rate (coupon / no coupon) |
|---|---:|---:|---:|---:|---|
| Active | 5,000 | 0.20 | 1,000 | 4,000 | 0.80 / 0.75 |
| Lapsed | 5,000 | 0.80 | 4,000 | 1,000 | 0.30 / 0.10 |

**Tasks. In pairs**
1. Compute the overall purchase rate in each arm, then the difference within each segment.
2. Split the pooled difference into the effect on recipients plus selection bias.
3. Compute the three averages the CFO could ask for (everyone, recipients, non-recipients). Which does *"keep the program as run?"* need? Does it clear the break-even?
4. Commit: does the CFO kill the program?
5. To estimate the effect on recipients, controls are reweighted by $e/(1-e)$: 0.25 for active controls and 4 for lapsed controls. How many *effective* controls does the estimate rest on? Use $(\sum w)^2 / \sum w^2$.
6. *(Optional)* Regress purchase on the coupon and a lapsed dummy. What does the coefficient on the coupon estimate?

### Part M7-R3. The app-open column

A junior analyst argues: *"Customers who never open the app cannot see the coupon. Restrict to app openers; it makes the comparison fairer."*

Take a clean case: 1,000 customers, coupon **randomized** 50/50, and suppose the coupon has **no effect at all**. Half the customers have high intent and buy regardless; half have low intent and never buy. A customer opens the app if they received a coupon **or** have high intent.

| | Customers | Open the app | Buy |
|---|---:|---:|---:|
| Coupon, high intent | 250 | 250 | 250 |
| Coupon, low intent | 250 | 250 | 0 |
| No coupon, high intent | 250 | 250 | 250 |
| No coupon, low intent | 250 | 0 | 0 |

**Task. In pairs:** compute the coupon "effect" among app openers. Commit before the answer.

### Part M7-R4. The real logs

The engine's score reads **14 CRM fields** and cuts them into four bands; each band had a daily send probability, throttled by the cap. **The purchase column stays locked.**

| Band | Segment | Members | Coupon | No coupon |
|---|---|---:|---:|---:|
| 1 | active | 2,500 | 200 | 2,300 |
| 2 | active | 2,500 | 800 | 1,700 |
| 3 | lapsed | 2,500 | 1,550 | 950 |
| 4 | lapsed | 2,500 | 2,450 | 50 |
| Total | | 10,000 | 5,000 | 5,000 |

**Tasks. In pairs**
1. Reconstruct $\hat e$ by band and the ATT weights $\hat e/(1-\hat e)$.
2. Which band's comparison is thin? Compute the effective number of non-recipients, $(\sum w)^2 / \sum w^2$.
3. Trim at $[0.05, 0.95]$. Whom does the ATT now describe?
4. Write the design record (estimand, estimator, trimming rule, balance check) before seeing any purchase.
5. What does the engine's rule become in this analysis?

### Part M7-R4b. Opening the outcomes

Lena's design record is written and dated. The purchase column opens:

| Band | Coupon: bought | No coupon: bought |
|---|---:|---:|
| 1 | 160 / 200 | 1,725 / 2,300 |
| 2 | 640 / 800 | 1,275 / 1,700 |
| 3 | 465 / 1,550 | 95 / 950 |
| 4 | 735 / 2,450 | 5 / 50 |

**Tasks. In pairs**
1. Compute the pooled effect, the IPW effect on all recipients (all four bands), the trimmed effect (bands 1 to 3), and the effect in band 4.
2. Each population has its own break-even, $10p_1/30$, where $p_1$ is its purchase rate with the coupon. Give each population's break-even and net per coupon.
3. Write Lena's memo to the CFO: what to keep, what to stop, and what to report separately.

---

## Take-home (Meeting 7): The Rivergate control audit

*A different firm. Rivergate is a fictional fulfilment business, not Houtan Coffee.*

Mei manages operations at Rivergate. She must decide whether to fund four weeks of training for the 200 pickers eligible next quarter: 100 high-skill and 100 low-skill. Training costs **¥1,800 per participant**. Each additional correctly fulfilled order contributes **¥80**. For planning, assume a weekly effect persists for the four weeks and orders are not taken from co-workers.

An earlier pilot was **voluntary**. Output is mean correct orders per worker in the same follow-up week:

| Skill | Trained workers | Trained output | Untrained workers | Untrained output |
|---|---:|---:|---:|---:|
| High | 20 | 90 | 80 | 80 |
| Low | 80 | 60 | 20 | 54 |

Finance's reading: *"Trained pickers produce 8.8 fewer orders a week. Cancel it."*

The pilot export contains these columns besides training and output:

| Column | What it records |
|---|---|
| Skill grade | assessed in the month before sign-up |
| Tenure | months employed at the sign-up date |
| Follow-up shift | shift worked in the follow-up week; trained pickers were moved to day shift after the course |
| Supervisor rating | rating given at the end of the follow-up week |
| Completed course | whether the worker finished all sessions (some dropped out) |

**Tasks** (30–45 minutes; submit with Notebook 7)
1. Reproduce finance's −8.8. Then compute the difference within each skill group.
2. For each column, say whether it belongs in the adjustment set, and why. Use timing and cause, not correlation.
3. Name one thing that plausibly drove sign-up and output but is **not** in the export. Which direction would it bias the within-skill differences?
4. Assuming exchangeability within skill, compute the effect for the 200 pickers Mei would train next, and for the pilot's own volunteers. Which does her decision need?
5. Does training pay for the 200? For each skill group separately? Write three sentences to Mei: the decision, the assumption it rests on, and what would change it.
