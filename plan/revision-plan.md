# Course revision plan (fall 2026)

The brief for any new working session: why the course is being revised, how generative AI enters it, and the work
that remains. Status, layout, conventions and decisions on record are in `README.md`; the calendar, labs, assignments
and deadlines are in `schedule.xlsx` and the syllabus; decisions waiting on the instructor are in `FLAGS.md`; working
rules are in `AGENTS.md` and `editorial-guide.md`.

## 1. Purpose of the revision

- **Course thesis.** AI makes prediction and code cheap, so identification and verification are the scarce skills.
  - Lectures teach causal reasoning.
  - LLM and agent work happens in labs, assignments and projects.
- **What changed from the previous version.**
  - Generative AI moves from a side topic to a full meeting (M9) plus a thread through the labs and assignments.
  - Exams sit at M5 and M11. Proposals are presented at M7.
  - Classical instrumental variables (outside shifters of treatment, 2SLS, weak instruments), regression discontinuity,
    staggered DiD and synthetic DiD leave the core lectures. They become bonus reading and handouts.
  - Noncompliance in an RCT (the ITT, compliance types and the LATE) is not classical IV: it needs only potential
    outcomes and the draw, and it closes M2, in the lecture and in the notes.
  - The technical notes were rebuilt (v4) with proofs of the key results and a consistent house style.
- **Writing standard.** Readable by someone not taking the course, and not like AI-generated prose; the rules are in
  `editorial-guide.md`.

## 2. How generative AI enters the course

There are two categories, and the course keeps them distinct.

**A. Generative models as simulators.**
- **The positive case.** A generative model trained on real logs, with the effect and the confounding planted by the
  analyst. Its effects are g-formula effects, so it rests on the same unconfoundedness assumption. That assumption is
  the price of making a business decision at all: unlike research, the business cannot decline to decide.
- **Two uses.**
  - As an estimator testbed: bias and coverage on this business's data shape.
  - As a pipeline testbed: run the whole predict-then-optimise pipeline and measure regret against the oracle. This
    persuades stakeholders far more than a textbook y = ax + b.
- **Credibility checks.** Backtests against past experiments; staying within the data's support; compounding error;
  "home advantage" (rank pipelines across simulators of different model classes).
- **The negative case.** Asking a language model for counterfactuals ("silicon samples"). Here the truth is asserted
  by the model's priors, not planted by the analyst. CEVAE sits on the same side: its identification rests on
  structure it does not state.

**B. Language models as variable generators.**
- LLM labels and embeddings are measurements with error. The consequence depends on the variable's role (outcome,
  treatment, control, effect modifier).
- Differential error, meaning accuracy that differs by treatment arm, can create an effect from nothing.
- Correction uses a gold subsample (PPI, DSL).
- Embeddings can serve as DML controls, subject to leakage (text written after treatment) and overlap collapse.

**Where each piece lives:**

| Place | GenAI content |
|---|---|
| M3 notes and lecture | TARNet as a shared representation, between the S- and T-learners |
| Handout H2 | TARNet, CFR, DragonNet, the CEVAE critique, in-context estimators (Do-PFN), benchmark pitfalls |
| M6 notes | Predict-then-optimise → decision-focused learning → policy learning, as one spectrum; policy learning as weighted classification |
| **M9 (whole meeting)** | A: learned simulators. B: LLM-generated variables. Worked examples: courier-bonus pipelines on two simulators; LLM-coded review outcome with PPI |
| Lab 2 | AI as **tool**: an LLM writes the A/B readout; students verify it with simulation tests |
| Lab 5 | AI as **decision-maker**: an LLM ranks customers from text profiles, evaluated by IPW against model rules |
| Lab 7 (optional) | AI as **analyst**: audit a tool-calling agent's observational analysis, then add a guardrail |
| Lab 9 | AI as **source of data**: LLM labels of review text versus gold quality, PPI, embeddings as DML controls, a leakage demo, a simulator with a confounding dial (the course's LLM-coded feature lives here) |
| Lab 10 | AI as **intervention**: evaluate an AI staffing-tool rollout with DiD |
| A1 | Write the readout once by hand, then delegate it to an LLM and verify |
| A3 | A student-built simulator of real grocery data (dunnhumby), checked against the instructor's locked simulator with planted elasticities; no LLM-coded feature |
| M9 Section 3 (optional lab) | Three routes compared on the simulator: plug-in, decision-focused, policy tree |

## 3. Work remaining, in suggested order

1. **Instructor decisions and the technical pass.** Settle the items in `FLAGS.md`, then fix the technical statements
   it lists (in notes, slides and check scripts together).
2. **Slides: instructor review.** All eleven decks follow the pattern title, road map, block A, block boundary, block B,
   summary (exam meetings M5 and M11 have one lecture block), with the notes' Results in the notes' order and a
   `slidesNN_check.py` for every number.
3. **Labs 1–11.** Data and tasks are specified in the spreadsheet's Labs tab. The heaviest preparation is Lab 9
   (cached LLM outputs, gold labels) and Lab 7 (agent harness; optional for students).
4. **Assignments.**
   - A1 to A4 handouts.
   - Data and grading as in Section 6: a resampled Hillstrom file with course costs and a locked holdout (A1, A2);
     dunnhumby with a locked simulator of planted-elasticity scenarios (A3); Favorita with a planted rollout (A4).
   - Grading checks that the pipeline runs and is reasoned correctly, not a performance score.
5. **Review passes.** Pass 2: independent check of every numbered Result. Pass 3: a student reads each meeting one
   week ahead.
6. **Optional.**
   - A pricing handout, "From elasticity to price": pricing from $\hat\theta(x)$, coupon menus, capacity. Source is old
     deck L9. Handouts are numbered in meeting order, so if it is written, it takes its meeting's place and the later
     handouts renumber.
   - Tag releases when the instructor asks.
   - Seed the M8 simulation.

## 4. Open judgement calls

Decide before building the affected pieces. Calls already settled are recorded in `README.md` (Decisions on record),
the syllabus and `CHANGELOG.md`.

1. Staggered DiD: the warning frame is in the M10 deck; whether Lab 10 adds it as an optional extension.
2. The proposal is due Sunday 8 November and presented two days later.
3. Final-project appendices: an LLM review of the draft plus responses, and a planted-effect validation of the design.
4. Exam weights: Exam II covers more lectures than Exam I; consider weighting it more.

Settled on 10 October: A2 and A3 no longer pose the same decision on the same locked set (A3 moves to dunnhumby), and
the LLM-coded feature is in Lab 9, not A3 (dunnhumby has no text).

## 5. Names

All businesses, people and data in the cases and notes are fictional. Business names come from places near the
Qiantan campus; people have English names. Lab notebooks may describe the public data behind each semi-synthetic world.

| Where | Business | Person |
|---|---|---|
| Case A, M1–M7 lectures | Houtan Coffee, a coffee chain (10,000 loyalty members) | Lena, customer analytics |
| Case B, M8–M9 lectures | Qiantan Hotels, a group of 80 hotels (folder `cases/caseB-qiantan`) | Wendy, commercial director |
| Case C, M10–M11 lectures | Sanlin Home, a home-goods chain of 120 stores | Dana, store operations |
| Notes' worked examples, M1, M3, M7, M10, H5, H6 | Yangsi Fitness, a fitness-club chain | |
| Notes' worked examples, elsewhere | Pujiang Delivery, a food-delivery platform (its subscription: Pujiang Plus) | |
| Case A, bonus part | Rivergate, a fulfillment business | |

## 6. Data for labs and assignments

**Rule.** Labs use one semi-synthetic world per block, with planted truth, so students can check their own answers.
Assignments use data no lab touches; each is graded on a randomized holdout or a planted effect. Assignments train the
analysis pipeline; they are not graded on a performance score. Data problems (sparse outcomes, memorized public data,
real shocks in a window) are handled by simulation and resampling. The instructor checked the terms of every source:
non-commercial teaching use is permitted.

| Lab | Data | Real / planted |
|---|---|---|
| 1–6 | Starbucks rewards data (Kaggle), semi-synthetic: the Houtan Coffee RCT | Real customer covariates and offer portfolio. Planted: randomization, $\tau(x)$, three coupon depths, pre-period spend for CUPED, text profiles for Lab 5. Lab 3 uses three versions with different $\tau(x)$ |
| 7 | Logs from the same world, assigned by a known targeting rule | Overlap dial; truth from the RCT version |
| 8, 9 | Inside Airbnb, semi-synthetic (lodging pricing; the city is chosen later in the semester) | Real listings, host prices and review text. Planted: demand with heterogeneous elasticity $\varepsilon(x)$, and a latent quality in the text that confounds price and demand. Lab 8: DML elasticity and optimal price. Lab 9: LLM labels versus gold quality, PPI, embeddings as controls, simulator with a confounding dial |
| 10 | Rossmann store sales, planted AI-tool rollout | Real sales; planted effect and adoption rule |
| 11 | Proposition 99, plus one Rossmann flagship | Prop 99: the published estimate as benchmark. Flagship: planted effect |

| Assignment | Data | Graded on |
|---|---|---|
| A1 | Hillstrom email RCT, resampled, with course-specific costs | ATE, CUPED on `history`, SRM, break-even, and the LLM readout |
| A2 | Hillstrom, three arms | Frozen policies scored by IPW on a locked holdout of at least 20,000 rows, with paired comparisons (the Womens arm has real heterogeneity, the Mens arm almost none) |
| A3 | dunnhumby "Breakfast at the Frat" (grocery) | Display effect by IPW and AIPW with overlap (M7); price elasticity by DML and a recommended price (M8); a student-built simulator (M9). Scored by the instructor's locked simulator across planted-elasticity scenarios |
| A4 | Favorita (grocery panel), planted rollout | Adoption tied to real pre-trends; effect on margin; a small second wave for staggered timing; one flagship for synthetic control. The April 2016 earthquake sits in the window |

**Still to do for the data plan.**
1. Syllabus: Lab 2 uses the Houtan Coffee RCT, not Hillstrom; A1 names Hillstrom; Labs 8 and 9 use Airbnb; A3 is
   rewritten for dunnhumby and the locked simulator; A4 uses Favorita; learning objective 3 reads "targeting or pricing
   policy". Then `schedule.xlsx` (Labs and Assignments tabs) to match.
2. Confirm the dunnhumby columns, and whether students register and download it themselves.
3. Build, in calendar order: the Houtan Coffee world (Labs 1–7; Lab 1 is 20 Oct), the Hillstrom file (A1 out 22 Oct),
   then the A2 holdout, the Airbnb world, the dunnhumby simulator, and the Rossmann and Favorita panels.

