# Case B: Wendy's rate decisions

**Qiantan Hotels, Meetings 8–9.** Fictional teaching case: the company, the people, and all data are invented.

This case is handed out one part at a time. When a task says *commit*, write your answer down before the class discusses it.

Parts are labeled by meeting and release: Part M8-R2 is the second part released in Meeting 8. Bonus parts, labeled B1 to B4, are optional and not examined.

Throughout: the current midweek premium rate is **¥800** a night, and the variable cost of an occupied room is **¥200**.

---

## Meeting 8: Flexible controls and double machine learning

### Part M8-R1. The proposal

**Wendy** is commercial director of Qiantan Hotels, a group of 80 properties.

A revenue management (RM) system sets the rate for every hotel-night. It uses forecast demand, competitor rates, booking pace, and the event calendar. **No human sets these rates night by night**: the system is an automated decision-maker, and it has been for three years.

On Wendy's desk: sales proposes raising midweek premium rates by **8%** across the portfolio. Their evidence is the RM system's own reporting: nights with higher rates sell more rooms. Sales' reading: *demand is strong; the system is under-pricing.*

Wendy has three years of logs: 80 hotels × 1,095 nights, with 47 recorded signals per night.

Six comparable nights from one hotel:

| Night | Category | Rate $D$ | Bookings $Y$ |
|---|---|---:|---:|
| 1 | Standard | 30 | 110 |
| 2 | Standard | 40 | 100 |
| 3 | Standard | 50 | 90 |
| 4 | Premium | 70 | 210 |
| 5 | Premium | 80 | 200 |
| 6 | Premium | 90 | 190 |

**Tasks**
1. An 8% rise changes contribution per occupied room from ¥600 to what? For the rise to pay, bookings must fall by less than what percentage? Express the break-even as an elasticity.
2. In pairs: compute the pooled slope of $Y$ on $D$ across the six nights.
3. Commit: does Wendy raise rates?

### Part M8-R2. Subtract what the system already knew

Within each category the mean rate and mean bookings are:

| Category | Mean rate | Mean bookings |
|---|---:|---:|
| Standard | 40 | 100 |
| Premium | 80 | 200 |

What Wendy's team says about the RM system:
- "The RM system is the only thing setting rates."
- "Every input it used is in the feed."
- "Rates still move for reasons unrelated to demand."

**Tasks**
1. For each night, subtract its category's means from its rate and its bookings. Regress the bookings residual on the rate residual.
2. Why did the pooled slope and the within-category slope differ in sign? Draw the arrows.
3. For each of the team's three sentences, say what it guarantees. What does a night priced exactly by the rule contribute to the estimate?

### Part M8-R3. The real logs

| | |
|---|---:|
| Hotel-nights | 87,600 |
| Recorded signals | 47 |
| Median rate | ¥803 (5th–95th percentile: ¥439–¥1,920) |
| Median premium rooms booked | 61 |

The RM system is **rule-based**. Log rate is a step function of bucketed signals:
- six forecast-occupancy bands, plus competitor-index bands and booking-pace bands;
- an event flag interacted with a lead-time tercile;
- day-of-week and month adjustments, plus a weekend rule that differs by occupancy band.

Around that rule, rates still move for reasons tied to no recorded signal.

**Tasks. In pairs**
1. Predict three log–log slopes of bookings on rate: with no controls; controlling for the hotel; controlling for the hotel and six forecast-occupancy bands.
2. Write down the model you would fit to get the elasticity. Three proposals go on the board.
3. For each proposal, say what could go wrong with it.
4. Signals are recorded throughout the day. Name two of the 47 that would be *post-treatment* if recorded after the rate was posted. When must every control be measured?

### Part M8-R4. The last-minute discount

On some nights the RM system opens a **10% discount** for the final 48 hours. Two kinds of night, equally common:

| Night | Share of nights the system opens it | Rooms booked without it | Rooms booked with it |
|---|---:|---:|---:|
| Airport | 0.5 | 50 | 54 |
| Resort | 0.9 | 60 | 72 |

**Tasks**
1. Compare mean bookings on nights with and without the discount. Why is that not the effect?
2. What does the partially linear model estimate here? Give the ATE and the ATT. Which one does a decision to open the discount every night need?
3. The resort models are off: $\hat\mu_1 = 74$ and $\hat e = 0.8$. What do regression alone, weighting alone, and AIPW give for mean bookings with the discount at resorts?
4. Compute the AIPW score of a resort night without the discount that booked 57 rooms. Why is it so far from 12?

### Part M8-R5. One more thing, says Wendy

> Property revenue managers **override** the system on about **8% of nights**. They override on local knowledge: a wedding block, a competitor closing a wing, a conference that never reached the event calendar. The override is logged. **The reason is not.**

Wendy's analyst adds two numbers from the logs. The ratio $\mathrm{sd}(\tilde Y - \hat\theta\tilde D)/\mathrm{sd}(\tilde D)$ is **3.0**. Dropping the **event flag** and re-estimating, the flag explains **4%** of the leftover rate variance and **6%** of the leftover bookings variance.

**Tasks**
1. Which of the team's three sentences in Part R2 is now false? What does that do to the estimate?
2. Can a more flexible model of the signals repair it? Why or why not?
3. If an override raises both the rate and bookings, in which direction does it bias −1.56? What kind of override would bias it the other way?
4. The estimate sits 0.24 from the break-even. With the omitted-variable bound, what equal partial $R^2$ on both sides would close the gap?
5. What bias could a factor as strong as the event flag cause? Twice as strong? Is the override factor plausibly that strong, and what would you do before acting?

---

## Meeting 9: Generative AI at Qiantan Hotels

### Part M9-R1. A simulator of Qiantan Hotels

Meeting 8 ended on the overrides: about 8% of nights, logged, with no reason recorded. The elasticity of −1.56 assumed they did no harm.

Qiantan Hotels' data-science team has trained a **generative model of the logs**. Given a hotel-night's 47 signals and a rate, it draws a number of premium bookings. It was fitted on the 87,600 hotel-nights of Meeting 8. On top of what it learned, the team **planted** two things:
- a true elasticity of **−1.50** on every night;
- an **override effect**: on 8% of nights an unrecorded local event (a wedding block, a conference) raises demand by 12%, and the manager raises the rate by 10%.

**Tasks**
1. The simulator answers "how many bookings at a different rate?" for any night. What must be true of Qiantan Hotels' real logs for that answer to be a causal effect? Which meeting's assumption is it?
2. List what the simulator took from the data and what the analyst chose.
3. Commit: can the simulator tell Wendy the true elasticity of Qiantan Hotels' guests?

### Part M9-R2. An estimator testbed

The team draws 200 simulated datasets with the same hotels, nights, and signals as the real logs, and runs each estimator on each. The truth is −1.50 because they planted it.

| Estimator | Override effect planted? | Mean estimate | Share of 95% intervals covering −1.50 |
|---|---|---:|---:|
| Log–log OLS, no controls | no | +0.42 | 0.00 |
| OLS, hotel and six occupancy bands | no | −1.18 | 0.02 |
| DML, boosted-tree nuisances | no | −1.49 | 0.94 |
| DML, lasso nuisances | no | −1.41 | 0.71 |
| DML, boosted-tree nuisances | **yes** | −1.37 | 0.38 |

**Tasks**
1. Compute the bias of each row.
2. Which estimator would you use on data shaped like Qiantan Hotels'? Why does lasso do worse than boosted trees here? (Recall how the RM rule is written.)
3. With the override effect planted, DML is biased toward zero. If the real overrides behave like the planted ones, where would the true elasticity lie, given Meeting 8's −1.56? Does Wendy's decision about the 8% rise (break-even −1.32) change?
4. What can this testbed **not** tell you about the real overrides?

### Part M9-R3. A pipeline testbed

The RM vendor offers a new engine: a boosted-tree demand model fitted to the logs, and an optimizer that posts the rate with the highest **predicted** contribution, (rate − ¥200) × bookings, night by night. Wendy's analyst builds a rival: price from the DML elasticity. Both are compared with the current RM rule.

The team builds a **second simulator** from the same logs, with a neural network in place of boosted trees, and the same planted truth. On each simulator, an **oracle** knows the planted demand and posts the best rate. Regret is the oracle's contribution minus the pipeline's, per hotel-night.

| Pipeline | Regret, boosted simulator | Regret, neural simulator | Nights priced above ¥1,920 |
|---|---:|---:|---:|
| Current RM rule | ¥1,450 | ¥1,520 | 5% |
| Vendor: predict, then optimize | ¥380 | ¥2,240 | 14% |
| DML elasticity, then optimize | ¥690 | ¥760 | 3% |

¥1,920 is the 95th percentile of the rates in the logs.

**Backtest.** The team re-ran the member-rate test of six months ago (Bonus, Part B1) inside each simulator, with managers' overrides as logged. The real test measured **+4.8** extra member bookings per heads night from the rate (SE 1.3; the email's share is already removed). The boosted simulator reproduces **+4.6**, the neural one **+3.4**.

**Tasks. In pairs, commit first**
1. Rank the pipelines on each simulator. Which pipeline has the smallest worst-case regret?
2. Why does the vendor's pipeline do best on one simulator and worst on the other?
3. 14% of the vendor's rates lie above ¥1,920, the 95th percentile of the logged rates, where the logs are thin. What do both simulators know about bookings there? What does that do to the regret numbers on those nights?
4. The vendor's optimizer picks, every night, the rate its model likes most. Why does that make its errors larger than its demand model's average error?
5. What does the backtest support, and what not? Would you trust either simulator more after it?
6. Recommend a pipeline to Wendy, and the check you would run when it goes live.

### Part M9-R4. Ask the model instead?

A second vendor offers "synthetic guests": a language model plays 10,000 guests, each shown a Qiantan hotel at ¥800 and at ¥864 and asked whether they would book. Its report: **elasticity −0.9**. *"Demand is inelastic. Raise rates."*

**Tasks**
1. In the simulator of Part R1, where did the truth come from? Where does it come from here?
2. Against Meeting 8's −1.56 and the break-even of −1.32, the two answers point in opposite directions. Which do you believe, and what evidence could settle it?
3. Could the synthetic guests serve as a testbed for Qiantan Hotels' estimators? Why or why not?

### Part M9-R5. Reviews, read by a model

Wendy did not take the 8% rise on trust. In Q3 she tested it: at 40 hotels, a coin chose each hotel-week's midweek premium rate, the current one or 8% higher. Bookings are the main outcome. The guardrail is guest reviews: *stop the rise if complaints about price or value go up by more than 5 points.*

**Bookings.** On higher-rate weeks, midweek premium bookings were **12.4% lower** (SE 1.2%).

Nobody can read 10,000 reviews, so a language model labels each one: complains about price or value, yes or no. A random 200 reviews per arm were also labeled by trained staff (the gold labels).

| | Higher rate | Current rate |
|---|---:|---:|
| Reviews | 5,000 | 5,000 |
| Share the model labels "complaint" | 0.22 | 0.15 |

In the gold subsample:

| | Higher rate | Current rate |
|---|---:|---:|
| Gold complaints, model says yes | 34 | 26 |
| Gold complaints, model says no | 2 | 2 |
| Gold non-complaints, model says yes | 12 | 4 |
| Gold non-complaints, model says no | 152 | 168 |

**Tasks**
1. Estimate the effect of the rise on complaints using the model's labels. Does it trip the guardrail?
2. From the gold subsample: the true complaint rate in each arm, and the effect. For each arm, the share of complaints the model catches and the share of non-complaints it flags.
3. Is the model's error the same in both arms? Read a few reviews from higher-rate nights in your head: why might it differ?
4. Suppose the error had been the same in both arms, with the current-rate arm's two shares. What would the model-labeled effect have been, given the gold effect? In which direction does error of that kind push an estimate?
5. Prediction-powered inference (PPI): for each arm, take the model's rate on all 5,000 reviews and correct it by the average of (gold − model) in that arm's subsample. Give the corrected rates and the effect. Its standard error is about 0.023; the gold labels alone give about 0.037. Why is PPI unbiased, even though the model's error differs between arms? Why is it more precise than the gold labels alone?
6. Does the guardrail trip?
7. Convert the bookings result into an elasticity, with a 95% interval. Compare it with Meeting 8's −1.56 and the break-even of −1.32.

### Part M9-R6. Text as controls

Back to Meeting 8's elasticity. Each hotel has a listing page, and each stay a review. The team turns text into **embeddings** and adds them as controls in the DML of Meeting 8.

| Controls | Share of log-rate variance left after the controls | Elasticity (SE) |
|---|---:|---:|
| 47 signals | 9% | −1.56 (0.03) |
| + embeddings of the listing pages, as of each night | 6% | −1.58 (0.04) |
| + embeddings of that night's guest reviews | 1% | −0.97 (0.09) |

**Tasks**
1. Which text is a legitimate control and which is not? Draw where each sits relative to the rate and bookings.
2. Why does the standard error grow as the share of variance left falls? By roughly what factor from 9% to 1%?
3. Why does the last estimate move toward zero?

### Part M9-R7. The memo

Write the memo to Wendy, in five sentences or fewer:
1. the 8% rise: what Meeting 8, the testbed, and the Q3 test together say;
2. the vendor's engine: adopt, reject, or pilot, and how;
3. the synthetic-guest report;
4. whether the review guardrail tripped, and the number;
5. the assumption that could still overturn your advice.

---

## Bonus (not examined): The member-rate coin

These parts are optional. They use the same hotels, and Part M9-R3's backtest refers to Part B1's test.

### Part B1. The member-rate test

Meeting 8's estimate rests on an assumption the logs cannot check: nothing unrecorded moved both rates and bookings. The overrides break it.

**What Wendy did next.** For six months the booking engine flipped a coin for every premium hotel-night:
- **heads:** loyalty members see a **member rate 8% below** the system's rate;
- **tails:** they see the system's rate.

Managers kept their override. On a heads night they could block the member rate; on a tails night they could apply it by hand.

On Wendy's desk: make the member rate permanent, portfolio-wide.

**Tasks**
1. An 8% member rate changes contribution per occupied room from ¥600 to what? By what percentage must bookings rise for the cut to pay? Express the break-even as an elasticity.
2. What did the coin make random, and what did it not?

### Part B2. The test log

One thousand premium hotel-nights from hotels where the coin was 50/50. Member bookings per night:

| Coin | Member rate shown? | Nights | Mean bookings |
|---|---|---:|---:|
| Heads | yes | 350 | 64.0 |
| Heads | no | 150 | 90.0 |
| Tails | yes | 50 | 40.0 |
| Tails | no | 450 | 70.0 |

Nightly bookings have a standard deviation of about 20.

From Wendy's description of the test:
- "The engine drew the coin within each hotel and month; resorts drew heads more often than airport hotels."
- "Heads changed one thing: the rate members were shown."
- "Managers honored most heads and added the member rate on few tails."
- "A manager could block the member rate or add it by hand; none reversed the coin."

**Tasks. In pairs, commit first**
1. Compare bookings on nights the member rate was **shown** with nights it was not.
2. Compare bookings on **heads** nights with tails nights.
3. Compare the share of nights the rate was shown on heads nights with the share on tails nights.
4. Commit: does Wendy roll it out?

Then:

5. Combine 2 and 3 into one number. What does it measure, and for which nights? Give its standard error (treat the share of nights the rate was shown as known) and a 95% interval.
6. Classify nights by what would have been shown under each coin. What share of nights is of each kind?
7. Complier nights book 60 without the member rate. Convert your number into an elasticity. Does it clear the break-even?
8. Match each of the four description sentences to the assumption it supports.

### Part B3. Two things nobody mentioned

**Marketing's email.** Marketing confirms that on every heads night the engine also emailed *"Members' Week at Qiantan Hotels"* to members who had searched that hotel, **whether or not the manager blocked the rate**.

**Two old-engine hotels.** Two hotels ran an old booking engine that **could not display** member rates. Their coin still flipped and the email still went out.

| Old-engine hotels, 200 nights | Heads | Tails |
|---|---:|---:|
| Mean member bookings | 51.2 | 50.0 |

**Two kinds of hotel.** The coin was 70/30 at resorts and 30/70 at airport hotels, and resorts book more:

| Hotel | Nights | Heads nights | Tails mean | Heads mean |
|---|---:|---:|---:|---:|
| Resort | 500 | 350 | 80.0 | 84.8 |
| Airport | 500 | 150 | 50.0 | 54.8 |

The share of nights the member rate was shown is 0.70 on heads and 0.10 on tails in both kinds of hotel.

**Tasks**
1. Suppose the email alone adds 1.2 bookings on every heads night. Recompute the ratio and the elasticity. How large is the bias, and why is it larger than 1.2?
2. What do the old-engine hotels measure? Correct the ratio.
3. Compute the ratio within each kind of hotel, then pooled across both, ignoring hotel type. Why do they differ?
4. Which controls must the analysis include, which may it include, and which must it never include?
5. Let $a$ be the email's direct effect on bookings per heads night, whatever its size. Write the complier elasticity as a function of $a$, using the hand log with the email (ITT 6.0). How large would $a$ have to be for the member rate to stop paying? Compare it with what the old-engine hotels measured.
6. The permanent program would keep sending the "Members' Week" email. Is the email's effect still a bias? Which number does Wendy's decision need?

### Part B4. Candidate-instrument audit

Analysts across the group propose other instruments for the rate. **In pairs:** mark each assumption ✓, ✗, or ?, with one reason.

| Candidate | Relevance | Independence | Exclusion | Monotonicity |
|---|---|---|---|---|
| A competitor's rate the same night | | | | |
| Rainfall in the city | | | | |
| Nights the RM system was down and rates froze at yesterday's level | | | | |
| Which revenue manager was on shift | | | | |
| The member-rate coin | | | | |

Then answer: which assumption do most candidates fail, and why can the data not settle it?
