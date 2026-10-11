# Case C: Dana's AI assistant rollout

**A Sanlin Home, Meetings 10–11.** Fictional teaching case: the company, the vendor, the people, and all data are invented.

This case is handed out one part at a time. When a task says *commit*, write your answer down before the class discusses it.

Parts are labeled by meeting and release: Part M10-R2 is the second part released in Meeting 10. Bonus parts, labeled B1 to B3, are optional and not examined.

All sales figures are **mean weekly sales per store, in ¥000**, unless marked otherwise.

---

## Meeting 10: Before, after, and everyone else

### Part M10-R1. The assistant

**Dana** runs store operations at Sanlin Home, a home-goods chain of **120 stores**.

Last year the chain licensed **Store Assistant**, a generative-AI assistant that runs on associates' handhelds. An associate asks it a question in plain words: *"Do we have the 30 cm frying pan in stock?"*, *"What screws go with this bracket?"*, *"Is the gray sofa cover machine-washable?"* The assistant answers in seconds. It checks the back room and the three nearest stores, and it suggests add-on items for the basket.

In week 53 the first **cohort of thirty stores** went live. A second cohort of thirty is scheduled for **week 79**. It is now week 78. (The flagship store went live much earlier, on its own. It is held out today and gets its own hour next meeting.)

**On Dana's desk:** confirm cohort 2, from next week. The assistant costs **¥2,500 per store-week**:

| Cost item | ¥ per store-week |
|---|---:|
| License and usage fees | 1,700 |
| Handsets, amortized | 300 |
| Allowance for each store's "AI champion" associate | 500 |
| **Total** | **2,500** |

Gross margin on incremental sales is **25%**.

Three numbers are on her desk:

| Source | Number |
|---|---|
| Her analyst: cohort 1, weekly sales after going live against before | +¥15,000 per store-week |
| Her analyst: cohort 1 against the other stores, after going live | +¥41,000 per store-week |
| The vendor's dashboard: "AI-assisted sales" in cohort 1 stores | ¥38,000 per store-week |

The dashboard counts the value of every sale in which an associate queried the assistant during the customer's visit.

The analyst: *"Either way, it pays several times over."*
The vendor: *"Assisted sales are fifteen times the fee."*

**Tasks**
1. What weekly sales lift does the assistant need to pay for itself?
2. For each of the three numbers, say what it compares with what. Which of them could be the assistant's effect?
3. Commit: is the vendor's "fifteen times" right even on its own terms?

### Part M10-R2. Four numbers

The comparison stores are the 89 not yet on the assistant.

| | Before (weeks 27–52) | After (weeks 53–78) |
|---|---:|---:|
| Cohort 1 (30 stores) | 181 | 196 |
| Comparison (89 stores) | 151 | 155 |

From Dana's rollout file:
- "Cohorts were assigned by region, in the order the regional managers signed off, after each region's data-privacy review."
- "Associates were trained on the assistant in weeks 51–52, in paid sessions held off the shop floor."
- "The comparison stores are the 89 whose regions had not yet signed off."
- "Licenses are tied to store handsets: associates cannot use the assistant at another store. No two stores share a catchment."
- "Once the assistant took over stock checks, store managers re-planned their rotas."

**Tasks. In pairs, commit first**
1. Compute (a) cohort 1, after minus before; (b) after going live, cohort 1 minus the comparison stores; (c) the change in cohort 1 minus the change in the comparison stores.
2. Which of the three goes against the break-even? Split each of the other two into that number plus something else, and name the something else.
3. Write the estimand using potential outcomes $Y_{it}(g)$, where $g$ is the week a store goes live ($g = \infty$ if it never does). Then state the assumption that makes (c) that effect. For each rollout-file sentence, say what it supports, or what it puts at risk.
4. Commit: why might cohort 1's region have signed off first?
5. On the four cells, regress sales on store-group effects and the treatment indicator only, without period effects. What coefficient do you get, and which earlier number is it? What changes when period effects are added?

### Part M10-R3. Six quarters

Quarterly means. Cohort 1 goes live at the start of Q5.

| | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |
|---|---:|---:|---:|---:|---:|---:|
| Cohort 1 | 176 | 178 | 180 | 182 | 192 | 200 |
| Comparison | 146 | 148 | 150 | 152 | 154 | 156 |

Store-level changes (after minus before) have standard deviations of about **6** in cohort 1 and **5** in the comparison stores. Cohort 1 is in **3 regions** and the comparison stores are in **9**. Region-level changes have standard deviations of about **3** and **2.5**.

**Tasks**
1. Compute the gap in each quarter, and each quarter's gap minus the Q4 gap. What does the pre-period show? What does the post-period show?
2. The panel has 119 stores × 78 weeks = 9,282 store-weeks. Why would treating store-weeks as independent give the wrong standard error? Compute the DiD's 95% interval treating **stores** as independent, then **regions** (use the $t$ distribution with 10 degrees of freedom, critical value 2.23). Does either interval clear the break-even?
3. Suppose cohort 1's region drifts up by $\delta$ per quarter relative to the comparison, too slowly to see before going live. The DiD compares Q5–Q6 with Q3–Q4. What drift would erase the margin over break-even? Would the pre-period have shown it?
4. Parallel in yuan or parallel in percent? Compute the effect both ways. Which scale do the pre-period gaps support?
5. Convert both intervals from task 2 into **yuan of margin per store-week**. Does the store-level interval exclude a loss?
6. Using the six quarters, compute the TWFE coefficient with store and quarter effects, and the event-study coefficients with Q4 as the base. Suppose each coefficient has SE 1.22 and the three pre-period coefficients are independent. Fit a linear drift to them by least squares: what drift can the pre-period rule out? Find $\delta^*$ for the four-cell DiD, for TWFE on six quarters, and for the Q6 coefficient.

### Part M10-R4. Store-weeks

The panel has 119 stores × 78 weeks = 9,282 store-weeks. Suppose a store's weekly sales shocks, net of its own level and the chain's week, follow an AR(1) with autocorrelation 0.8.

**Tasks**
1. A store's change $\Delta_i$ is its 26-week after-mean minus its 26-week before-mean. Compute $\mathrm{Var}(\Delta_i)$ relative to $\sigma^2(1/26 + 1/26)$, which is what independent weeks imply.
2. By what factor is a standard error that treats store-weeks as independent too small? Using the store-level SE from Part R3, what would that SE be, and would its 95% interval clear the break-even?

### Part M10-R5. The analyst's draft

Seven sentences from the draft memo. **In pairs:** for each, say what is wrong, or that nothing is.

1. "Cohort 1 sales rose by ¥15,000 per store-week after going live."
2. "On 9,282 store-weeks the effect is significant at $p < 0.001$ (SE 0.47)."
3. "We control for weekly staff hours, which differ across stores."
4. "Stores that closed during the period were dropped."
5. "The pre-period is weeks 1–52."
6. "Pre-period coefficients are flat, so parallel trends holds."
7. "The vendor's dashboard confirms the result: assisted sales of ¥38,000 per store-week."

Then write Dana's memo in five sentences: the number, its interval, the assumption, the drift that would change the decision, and the decision on cohort 2.

---

## Meeting 11: The flagship store

### Part M11-R1. One store, two years ahead

It is now **week 104**. Meeting 10 confirmed cohort 1: against the 89 stores not yet on it, the assistant added **¥11,000** a store-week (SE 1,220) in its first two quarters. On Dana's desk: extend it to the **59 stores** still without it, at ¥2,500 per store-week.

There is one more piece of evidence. The **flagship** store went live in **week 20**, alone, thirty-three weeks before anyone else, and has 84 weeks live. It was the vendor's **co-development store**. For its first six months a vendor engineer worked on site, and the vendor tuned the assistant on the flagship's own catalog and customers' questions.

Its before/after difference is **+¥18,700** per week. Dana asks: *how much of that is the assistant?*

A 2 × 2 needs a control. Which store?
- the chain's other large-format store? It is in a different city;
- the average of all 59 never-treated stores? A different format, with a different trend;
- a weighted average of never-treated stores, weighted so that it tracked the flagship before week 20?

**Tasks**
1. What is wrong with each of the first two controls?
2. What exactly was the "treatment" at the flagship? Is it the same treatment the 59 remaining stores would get?

### Part M11-R2. Three donors, by hand

The flagship goes live after week 3.

| | Week 1 | Week 2 | Week 3 | Week 4 (live) |
|---|---:|---:|---:|---:|
| Flagship | 100 | 110 | 120 | **141** |
| Donor A | 90 | 100 | 110 | 118 |
| Donor B | 110 | 120 | 130 | 138 |
| Donor C | 120 | 140 | 160 | 165 |

**Tasks. In pairs**
1. Find non-negative weights summing to one that reproduce the flagship's three pre-period values exactly.
2. Use them to estimate the week-4 effect.

### Part M11-R3. Before the post-period, and after

**Tasks**
1. On the real flagship, the weights are fitted on weeks 1–19. Before anyone looks at weeks 20 onwards, what would you fix in writing? How could you use weeks 15–19 to test the synthetic store?
2. Treated as if live in week 20, each of the 59 donors gets its own synthetic control. The flagship's post/pre gap ratio ranks 1st of 60. Is that a p-value of 1/60? What would have to be true for it to be one?
3. The flagship's city also has four small never-treated stores that share no staff or customers with it. How would you use them to check whether a local demand boom, not the assistant, explains the flagship's rise? What result would worry you?
4. Move the go-live date back to week 10 and refit on weeks 1–9. What should the synthetic store show in weeks 10–19, and what would it mean if it showed a gap?
5. Return to the three donors of Part R2. Remove donor B from the pool. What is the best you can do, and what is the effect? Then remove donor A instead. Which of these estimates would you report, and what range?

### Part M11-R4. Synthetic control or DiD?

Dana's analyst prefers a plain difference-in-differences: the flagship against the **equal-weighted** average of the three donors in Part R2, with weeks 1–3 as the pre-period and week 4 as the post-period.

**Tasks**
1. Compute that DiD. Compare it with your synthetic-control estimate.
2. Now compute the DiD against the equal-weighted average of donors A and B only. Why does it match the synthetic control here?
3. Both methods compare the flagship with a weighted average of donors. What does each choose, and what does each allow for that the other does not?

### Part M11-R5. The memo

Two bodies of evidence are on Dana's desk: Meeting 10's cohort estimate and the flagship. Write the memo in five sentences or fewer:
1. what to do about the 59 stores;
2. what to budget per store-week, **in yuan of margin**, not sales (margin is 25% of sales);
3. the assumption it rests on;
4. what the flagship number is and is not;
5. how the remaining rollout should be scheduled so that the next review has a clean comparison.

---

## Bonus (not examined): The staggered rollout

These parts are optional. The week-104 situation is the same as in Part M11-R1.

### Part B1. Extend it to everyone?

It is now **week 104**.
- The **flagship** store went live in week 20, alone.
- **Cohort 1** (30 stores) went live in week 53 and **cohort 2** (30 stores) in week 79.
- **59 stores** are still without the assistant.

In week 66 the vendor pushed **version 2** of the assistant, with a larger model and better stock look-ups, to every store then using it. Cohort 2 started on version 2. As cohort 1 had, cohort 2's associates trained off the shop floor in the two weeks before going live (weeks 77–78).

**On Dana's desk:** extend the assistant to the remaining 59 stores, at ¥2,500 per store-week.

Her analyst has two numbers, and they disagree:

| | ¥ per store-week |
|---|---:|
| Two-way fixed effects on the full panel | +6,100 |
| Cohort 1, before vs after going live | +14,300 |

**Tasks**
1. One number is below the break-even and one is above. Before any calculation, commit: which do you trust more, and why?
2. Every store-week has two clocks: the calendar week, and the week since that store went live. Give an example of a reason the assistant's effect could depend on each clock.

### Part B2. Three stores, three weeks

Store E goes live in week 2, store L in week 3, store N never. Bold cells are treated. A common trend of +4 per week runs through all three stores.

| | Week 1 | Week 2 | Week 3 |
|---|---:|---:|---:|
| E (live week 2) | 100 | **112** | **124** |
| L (live week 3) | 200 | 204 | **216** |
| N (never) | 300 | 304 | 308 |

**Tasks. In pairs, compute four difference-in-differences and commit:**
1. E against N, weeks 1 → 2;
2. E against N, weeks 1 → 3;
3. L against N, weeks 2 → 3;
4. L against **E**, weeks 2 → 3, using the store already on the assistant as the control.

Then: what is the true effect in each treated store-week? Why does comparison 4 get it wrong, when there is no noise in these numbers?

### Part B3. The cohort panel

| | Stores | Went live in week | Weeks live in the panel |
|---|---:|---:|---:|
| Cohort 1 | 30 | 53 | 52 |
| Cohort 2 | 30 | 79 | 26 |
| Never treated | 59 | never | 0 |

The flagship is held out of this panel.

From the rollout file:
- "Cohorts were assigned by region, in the order the regional managers signed off."
- "No store was moved between cohorts after the schedule was set."
- "The never-treated stores are the ones whose regions have not yet signed off."

**Tasks**
1. **Predict and commit**, in ¥000 per store-week: the static TWFE coefficient on the cohort panel; the average effect in the first week live (event time 0), cohorts against never-treated stores; the average effect at event time 12.
2. For each rollout-file sentence, say what it buys and what it does not.
3. **Choose controls before computing anything.** Fill in the table: for each target, which stores may serve as the comparison, which may not, and why?

   | Target | Base week | Eligible comparison stores | Excluded, and why |
   |---|---|---|---|
   | Cohort 1, weeks 53–76 | | | |
   | Cohort 1, weeks 77–104 | | | |
   | Cohort 2, weeks 79–104 | | | |

   Why should the base week not be the week just before going live?
4. **Version 2.** Cohort 1 received version 2 at its event week 13. Cohort 2 had version 2 from event week 0. Suppose part of the growth in the effect comes from version 2, not from associates learning the tool. What pattern in the cohort-by-week effects would show it? Why can the two causes not be separated by averaging over cohorts at each event time?
