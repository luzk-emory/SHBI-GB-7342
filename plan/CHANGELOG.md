# Changelog

Newest first. Each entry describes the repository as of its date and is not revised afterwards. Entries before the
8 October renumbering use the old handout numbers: old H1 (IV) is now H4, H2 (RD) is H5, H3 (staggered adoption) is H6,
H4 (interference) is H1, H5 (sequential decisions) is H3, and H6 (neural estimators) is H2. Entries before 9 October
number the labs from 0 (old Lab N is now Lab N+1).

## One build script (2026-10-11)

- `shared/build.sh` replaces `build.sh`, `build_all.sh` and `cloud-setup.sh`. It runs from anywhere in the repository with targets `all` (default), `mNN`, `mNN/<document>`, `syllabus`, `notation` and `setup`; uses tectonic when installed and pdflatex otherwise (`ENGINE=` to choose); builds the answer key automatically for any document with `\answer` (the `nokey` option is gone); syncs the style copy into each meeting it builds; and prints one line per document with its errors, undefined references and overfull boxes. Tested with pdflatex and with tectonic 0.15 on a local TeX Live bundle: all 47 documents build.
- M5 notes: the PAV exercise's number lists now wrap, which removed a 120pt overflow under tectonic.
- README, AGENTS, the editorial guide and the style file's comment describe the new commands.

## Names and data plan (2026-10-10)

- Names (instructor's decision): businesses named after places near the Qiantan campus, people with English names. Case A's unnamed coffee chain is Houtan Coffee and Lin is Lena; Case B's Meridian Hotels is Qiantan Hotels and Wen is Wendy (folder `cases/caseB-meridian` renamed `cases/caseB-qiantan`); Case C's unnamed home-goods chain is Sanlin Home, and Dana stays. The notes' FitLife is Yangsi Fitness and QuickBite is Pujiang Delivery (QuickBite Plus is Pujiang Plus). Applied to slides, notes, handouts, cases, the syllabus, check scripts, and the README; citations (Lin 2013, Zheng Wen) unchanged. Two M9 sentences shortened to keep a frame on its page.
- Data plan for labs and assignments recorded in `revision-plan.md` Sections 5 and 6: one semi-synthetic world per lab block (Houtan Coffee RCT from the Starbucks rewards data, Inside Airbnb, Rossmann, Proposition 99), separate data for assignments (Hillstrom, dunnhumby, Favorita), graded on the pipeline rather than a score. The LLM-coded feature moves from A3 to Lab 9. Syllabus and `schedule.xlsx` edits are listed there as the next step.
- Syllabus and `schedule.xlsx` (11 Oct) follow the data plan: learning objective 3 says "targeting or pricing policy"; assignments are graded on the pipeline, not a score; A1 names Hillstrom (resampled, course costs); A2 becomes "Email whom, and at what budget?" on Hillstrom's three arms with a locked holdout; A3 becomes "Promote and price from the logs" on dunnhumby with a locked simulator, and loses its LLM-coded-feature placeholder; A4 uses Favorita; Labs 1 to 7 use the Houtan Coffee world, Labs 8 and 9 Airbnb (Lab 8 adds the optimal price, Lab 9 a simulator with a confounding dial); the tooling appendix merges the A2 and A3 grading rows. Judgment calls 4 and 8 updated.

## Admin files brought up to date (2026-10-10)

- `plan/design-plan.md` removed: the v4 notes plan is complete, its status section had gone out of date (H4 and H5 now restate the Meeting 2 results), and its live decisions are in the README, the notes, and the syllabus. It stays in git history.
- `README.md` is the single place for status, layout, conventions, and open items: layout adds the editorial guide, FLAGS, the old decks, the scan, and the setup script; status reflects the editorial pass and the open pull requests; open items point to `FLAGS.md`; conventions keep the document design that was recorded only in the design plan.
- `plan/revision-plan.md` cut to the purpose of the revision, how generative AI enters the course, work remaining, and the open judgement calls. Removed: the copy of the schedule (in `schedule.xlsx` and the syllabus), the status table (in the README), and the slide-rebuild notes, which are done and allowed slides to point to the notes, against the editorial guide. Proposals are presented at M7, not M8.
- `AGENTS.md`: the checks cover notes, handouts, slides, and cases; build commands for handouts and slides; instructor decisions go to `FLAGS.md`.
- This changelog gains a header with the old-to-new handout and lab numbering.
- Case instructor files: references to `course-spine.md` and the Codex review (documents outside the repository) removed, and a note on an M1 deck bullet that no longer exists.

## Editorial pass, Meetings 9 to 11 (2026-10-09)

- Under `plan/editorial-guide.md`, for the M9 to M11 slides and notes and Handout H6. Formulas, numbers, results, and box wording unchanged (the M9 pitfall box spells out "language-model label" identically in both files); a math and number diff against the previous commit shows only removed meeting pointers, bold removed inside math, and restated definitions.
- Self-containment: the M9 notes restate the two Handout H2 results they pointed to, the M10 notes the two Handout H6 points, and M11 defines the adoption-date notation it used from Meeting 10. The pointer from M10 to Meeting 11 is a concept preview. Abbreviations (DML, RM, VAE, DiD) spelled out at first use. Internal script paths removed from the rendered notes.
- References: every reading list is Chicago author-date; three works cited but missing from their lists added (3 failures to 0).
- Slides: emphasis bold (31 hits to 8, the rest defined terms and labels), colons and fragments (37 to 9, the rest lead-ins and reference entries), question titles (4 to 2, both answered on the frame), voice.
- Case C's rollout-file quote spells "Licenses", matching the M10 deck.
- New flags in `plan/FLAGS.md`, among them technical points for a later pass: the M10 event-study standard errors and pre-trend independence, the M11 symbol clashes ($\lambda$, $\mu$, $w$ against $\omega$), the M9 $V$ clash with policy value, and the PPI gold-sample caveat in the M9 notes.

## Editorial pass, Meetings 5 to 8 (2026-10-09)

- Under `plan/editorial-guide.md`, for the M5 to M8 slides, notes, and handouts H3 to H5. Formulas, numbers, results, and box wording unchanged; a math and number diff against the previous commit shows only removed meeting and result numbers, added years, spelled-out small numbers, and the restated content below.
- Handouts self-contained: H4 restates the Meeting 2 notation, exclusion, monotonicity, compliance types, and the LATE theorem in place of citing Section 1.9, Assumptions 1.11 and 1.12, and Results 1.13 to 1.15; H5 restates the LATE theorem in place of Result 1.15; H3 drops its meeting pointers. The M6 and M8 notes restate what they used to send readers to Handouts H1 and H3 for.
- Forward references to later meetings replaced by concept previews (11 scan hits to 0); cross-meeting numbers (4 to 0); citations missing from a document's list added (9 failures to 0); the M7 deck gains a References frame; every reading list is Chicago author-date.
- Slides: emphasis bold (30 hits to 10, the rest defined terms and structural labels), colons and fragments (49 to 14, the rest lead-ins, labels, and reference entries), en-dashes between words in cell labels made hyphens (39 to 8, the rest joint names and ranges), voice. Internal script paths removed from the M8 rendered text.
- New flags in `plan/FLAGS.md`, among them three technical statements left for a technical pass: M5's "reach times average effect" (net value), the fuzzy RD box in H5 without exclusion, and undefined $\text{LATE}_C$ and $\text{LATE}_D$ in H4's defiers box.

## Editorial pass, Meetings 1 to 4 (2026-10-09)

- Under `plan/editorial-guide.md`, for the M1 to M4 slides, notes and handouts H1 and H2. Formulas, numbers, results and the wording of Result, Assumption and Definition boxes unchanged; a math and number diff against the previous commit shows only notation-preserving edits (bold removed inside math, "one percent" written as $0.01$, small numbers in words).
- Forward references to later meetings replaced by concept previews (26 scan hits to 0); cross-meeting Result numbers replaced by the named concept (2 to 0); cross-artifact references removed or restated (5 to 0; the H1 handout restates the two results it used to point to).
- References: each deck has a References frame before Summary; reading lists in notes and handouts are Chicago author-date entries with their annotations kept; every in-text citation is in its document's list (4 failures to 0). Details that could not be verified are left out and logged in `plan/FLAGS.md`.
- Slides: emphasis bold reduced to defined terms and one key phrase per frame (25 hits to 10, the rest structural); colons, fragments and framing openers rewritten (46 to 14, the rest lead-ins and labels); prose moved toward the old decks' voice.
- Style: `readinglist` uses `xltabular`, so long lists break across pages and each document keeps a single list.
- `editorial_scan.py`: the cross-artifact rule no longer matches "assignment" as a concept, reference entries, or reading-list rows.

## Spelling pass (2026-10-09)

- US spelling throughout the student-facing materials, the case instructor files, and the schedule workbook (553 lines in 36 files; 11 workbook cells), under `plan/editorial-guide.md` Section 3. Labels, references, file names, URLs, code, and published titles unchanged. Curly quotes in the Markdown cases straightened.
- Serial commas: 274 added (cases 28, M1-M4 72, M5-M8 93, M9-M11 and syllabus 81), author lists included, as Chicago style does. No other wording changed.
- `slides08_check.py` follows the new spelling of the Case B sentence it quotes.

## Editorial guide (2026-10-09)

- New `plan/editorial-guide.md`: the editorial standard for student-facing materials, fitted to this repository (student-facing and excluded paths; carve-outs for answer keys, release markers, case instructor files and the schedule workbook; dash rules; US English with serial commas, converted first in a separate mechanical pass; labels Meeting N, Block A/B/C, Lab N, Handout HN and case part IDs; slide exceptions for the Summary and End of Block A frames and for bold; self-containment with the Meeting 1 course map and notes' reading-list exceptions; Chicago author-date references, with a References frame per deck; build and check rules). `AGENTS.md` points to it.
- New `shared/checks/editorial_scan.py`: the automated checks of guide Section 11 (failures and review candidates), run on the student-facing files after removing answer blocks and LaTeX comments.
- New `plan/FLAGS.md`: data-source and license questions (Dominick's, Rossmann, the hotel reviews, the coupon RCT, Hillstrom and Proposition 99), the brand color and the inherited Case A example, and the open `\tbd` decisions in the syllabus.
- No course material changed.

## Calendar, labs and assignments (2026-10-09)

- Dates: Tuesdays and Thursdays, 20 October to 1 December 2026; no meeting on Thursday 26 November (Thanksgiving). M11 (Exam II) and M12 (final presentations) are now Tuesdays. `schedule.xlsx` gains a Date column and a Thanksgiving row; the syllabus's week headers and meeting rows carry the dates.
- Labs renumbered 1 to 11, Lab N with Meeting N (old Lab 0 is Lab 1, and so on). Ten labs are graded, 1 point each, Lab 1 included; Lab 7 (observational methods, then the agent audit) is optional and ungraded, done at home, and its methods are graded in A3. Lab 8 (DML) runs in class. Lab 5 stays a separate CATE-evaluation lab (adds isotonic recalibration, freeze-then-evaluate and a paired comparison); Lab 6 adds an optional group constraint. Lab notebooks carry no fixed deadlines.
- Proposal presentations move from M8 to M7, block C (Tue 10 Nov).
- Assignments: A1 M1-M2 (22 Oct to 30 Oct); A2 M3-M6 (3 Nov to 15 Nov); A3 M7-M9 (10 Nov to 20 Nov): regression, IPW and AIPW (the Lab 7 methods), then DML, with a simulator of the coupon logs as the evaluation testbed (an LLM-coded feature to be decided); A4 M10-M11 (19 Nov to 29 Nov): DiD on the AI-assistant rollout and a synthetic control for the flagship. The hotel-simulator pipeline assignment is retired.
- Final slides, abstract and report are due together on Tue 8 Dec, a week after the presentations; draft to peer pair Thu 3 Dec, peer review returned Sun 6 Dec.
- Updated: `schedule.xlsx` (Schedule, Labs, Assignments, Deadlines, Judgment calls), the syllabus (meetings line, AI roles, how a meeting runs, assessment, assignments, labs, project milestones, deadline rules and table, AI-use policy, weekly schedule, tooling appendix), the brief (Sections 2, 3, 4, 5 and 7), README, and Case A's lab references (the M3-R6 opener is now Lab 3).

## Slides rebuild (2026-10-08)

### Schedule and syllabus
- `schedule.xlsx`: M5B adds isotonic recalibration and the paired comparison of two policies; M6A adds the price of fairness and capacity (critical fractile); M6B replaces "plug-in vs direct learning" with the predict-then-optimise / decision-focused / policy-learning spectrum; M7B adds the outcome-free design stage. New column G lists each meeting's handout.
- `syllabus.tex`, draft 3, regenerated from the spreadsheet: Tuesday/Thursday calendar; exams at M5 and M11 (block A); proposal presentations at M8; assignments A1 to A4 and Labs 0 to 10 replace projects P1 to P4 and notebooks; handouts H1 to H6 (not examined); examinable material is the slides plus notes Sections 1 and 2; AI policy per lab and assignment; bonus reading; final-project appendices as in judgement call 6; lecture cases versus the notes' worked examples. M9 (generative AI) replaces IV in the "where the counterfactual comes from" table. Weights carried over from draft 2 and marked for confirmation. Undecided items are shown in red brackets (`\tbd`), replacing the `soul` highlighter, which is not in the course's TeX setup.

### Meetings 7 to 11 (slides), schedule and syllabus
- M7 (34 frames, coffee chain): block A identification and adjustment (Assumptions 1.1-1.3; Results 1.4-1.7: standardisation and IPW, the balancing property, what regression estimates; good and bad controls including M-bias; the app-open collider), block B overlap, design and double robustness (an exact four-band export of the engine's rule, overlap and trimming, the design record, Result 1.8 AIPW, LaLonde, sensitivity). The base is the 10,000 members of M3 to M5 (was a 40,000 export); simulated ladder values replaced by exact cell counts.
- M8 (35 frames, Meridian): the notes' order (the partially linear model and FWL before the plug-in failures; overlap before the interactive model). Six nights carry FWL, Result 1.4 and cross-fitting by hand; a last-minute discount carries the interactive model and AIPW; Result 1.6 with a robustness value (7.7%) and benchmarking. The interval is now [-1.62, -1.50] (date-clustered SE 0.03), replacing the asymmetric [-1.64, -1.51]. The three unverifiable figures are no longer used. To confirm: the event-flag benchmark (partial R² 0.04 and 0.06) is a given, and the residual-SD ratio 3.0 equals the notes' worked example's.
- M9 (36 frames, new, Meridian): replaces the IV deck. Block A simulators (Results 1.1-1.2; planted truth; estimator and pipeline testbeds; regret; backtests, support, compounding error, home advantage; silicon samples), block B LLM-generated variables (Results 1.3-1.5; coded outcomes and modifiers; labels by role; PPI and DSL; embeddings, leakage, overlap collapse). Uses Case B's checked numbers.
- M10 (31 frames, retail): block A panel basics (adoption-date outcomes, regression to the mean, fixed effects, Results 1.1-1.2), block B DiD (Results 1.5-1.9, event study, breakdown drift, one change per store, clustering) and one warning frame on staggered timing. The cohort estimate is exact: 11 (SE 1.22; quarters 8 and 14), replacing the simulated 12.4 (SE 1.2).
- M11 (21 frames, new, retail; one lecture block): replaces the staggered-DiD deck. Definition 1.1 and Results 1.2-1.3 on the flagship and three donors by hand; the placebo rank is a p-value only if the flagship was as likely as any donor to be treated. Dana's table and the recommendation use M10's exact cohort numbers (+¥250 of margin on average; -¥500 then +¥1,000). To confirm: the flagship's results (¥18,700, 15.9, range 13.1 to 17.4, rank 1 of 60) are case givens with no simulation script.
- Cases aligned with the M7 to M11 decks: Case A M7 on the 10,000 base (R2 counts x10; R4 replaced by the four-band export; new R4b with purchases by band; keys and release rows); Case B M8 (new R4 on the last-minute discount; R5 adds the sensitivity tasks; interval [-1.62, -1.50]) and M9 (R3 task on the 95th percentile; release rows); Case C M10 (R4 rewritten on AR(1) store-weeks; R5 and the memo at 11 (SE 1.22)) and M11 (R1 at ¥11,000 against the 89 not-yet-treated stores; leave-one-out moves from R2 to R3; R5 margins +¥250, -¥500, +¥1,000). The flagship's results are labelled case givens. `case_check.py` covers every new number.
- New check scripts `slides07_check.py` to `slides11_check.py` (0 mismatches). No deck carries notes or handout pointers, lab material, critique frames or in-class prompts.
- `schedule.xlsx` and the syllabus: M7, M8, M10 and M11 rows follow the notes' order (M7: IPW and balancing in block A, AIPW after design; M8: the partially linear model before the plug-in failures, overlap before the interactive model; M10: clustered SEs move to block B; M11: factor-model rationale, design stage and the p-value condition added). The syllabus M9 row adds the missing simulator topics, and its case is no longer marked undecided.

### Meetings 4 to 6 (slides), Case A, schedule and syllabus
- M4 (33 frames): block A causal trees and honesty (Results 1.1-1.3; the winner's curse by hand; the discover/estimate/recommend protocol on Region 2's coupon test, now 4,000 members in two halves of 2,000), block B causal forests (Result 1.4, local centering, interval cautions, variable importance, Result 1.5, GATES). Half-B results now come from explicit counts; the simulated forest sub-segment (38%) and the merged executive interval are dropped.
- M5 (21 frames, one lecture block): Results 1.1-1.9 in the notes' order. New exact example: the forest splits each segment into two groups (L1, L2, A1, A2), carrying the gain, profit and Qini curves, RATE, ranking versus calibration, and the evaluation of three frozen lists (segment rule ¥1.50, forest top 5,000 ¥0.75, engine's cut-off ¥1.625; paired SEs 0.36 and 0.15). Isotonic recalibration on six bins; Result 1.8 with an exact K-candidate example; the paired SE by hand on the 80 rows. All simulated values (1.46 to 2.31) dropped.
- M6 (34 frames): block A allocation (Results 1.1-1.9) on the Region 2 push, with new coupon depths, the price of fairness (North/South, ¥470), and capacity with the critical fractile (two stores; plan for 480); block B policy learning (Results 1.10-1.11, the spectrum, DR scores, weighted classification on eight members, policy trees, regret, holdouts, bandits, what the sum assumes). The conservative rule now bounds net value, not the lift.
- New check scripts `slides04_check.py`, `slides05_check.py`, `slides06_check.py` (0 mismatches). No deck carries notes or handout pointers, lab material or in-class prompts.
- Case A: release table retimed for M4 to M6 (M4 all in block A; M5 in block B; M6 in block A). M4-R1 states the test size; M4-R3 gains the two-noisy-splits, winner's-curse and split-cost tasks (the split-cost task now uses 250 per arm at 0.50/0.30); M4-R4 gives counts; M4-R5 gives 95% and 98.75% intervals for the four committed leaves and drops the forest sub-segment. M5-R1's T-learner list becomes the engine's cut-off; M5-R4 uses the four-group example and paired SEs. M6's cap task moves to R2 with a one-day send (¥3,500 vs ¥4,750); the take-home check bounds money (-¥0.73). Instructor keys follow.
- `schedule.xlsx` and the syllabus: M4, M5 and M6 rows reordered to follow the notes (winner's curse before honesty; policy value before curves and calibration; sure-thing cost, spending risk and "what the sum assumes" added; EWM before weighted classification).

### Meeting 3 (slides)
- Rebuilt on the coffee-chain case (Case A, M3 releases R1, R2, R2b, R3), aligned with the M3 notes: Assumptions 1.1-1.2 and Results 1.3-1.11 with the notes' numbers and wording, in the notes' order. Block A follows notes 1.1 to 1.4 (estimand, prognostic versus modifier, identification and the support/confounding distinction, the targeting rule and the value of targeting, the interaction model, the gap test, multiple testing and GATEs); block B follows 1.5 and 1.6 (S-, T- and X-learners, transformed outcome, DR pseudo-outcome, R-learner, TARNet, why outcome accuracy cannot choose, fit/choose/assess, pitfalls).
- 30 frames: title, road map, block A 13, block boundary, block B 14, summary. Removed: the course-map frame (its M9 box was out of date), Today's Plan, critique C2, the two discussion frames (now one self-contained "Support or Confounding?" table), the in-pairs prediction frame and "The Ladder" (its numbers were unchecked `\NUM` placeholders from a simulation that does not exist yet), the Lab 2 frame and the deadline line. All CARRIED comments are gone.
- New, on the coffee-chain numbers: the value of targeting (-¥1.75 for everyone, ¥0 for nobody, +¥1.50 per member for the rule), multiple testing (p = 0.008 for the gap: it stands if pre-specified, fails Bonferroni at 0.0036 if found among 14 fields), the S-learner penalty on the 800-member segment test (lambda = 50 keeps 80% of beta and half of gamma), the X-learner, the transformed outcome and DR pseudo-outcome (SD 1.76 against 0.83 for active members), the R-learner's l(x), TARNet (new material; carried on the coffee chain's 14 CRM fields, to be confirmed by the instructor) and Result 1.11 tied to the 0.0375 of "Same RMSE, Opposite Decisions". The T-learner illustration now uses fits 0.35/0.15 and 0.33/0.07, distinct from the notes' 0.34/0.14 and 0.32/0.08; Case A Part M3-R3 task 5 and its key follow.
- New check script `shared/checks/slides03_check.py` (0 mismatches). Case A's release table updated; M3-R4 (the ladder) is on hold until a seeded simulation exists.
- `schedule.xlsx` and the syllabus: M3 block A no longer lists BLP, which the notes teach in M4.

### Slide design principles; M1 and M2 decks brought into line
- New principles (instructor): slide 2 is a road map of the meeting's topics; slides are self-contained (no lab previews, case-handout instructions, in-class prompts or other course logistics); every deck ends with its summary. Recorded in `revision-plan.md`, Section 6.
- M1: new road-map frame; removed the exit ticket, the case-handout instruction on the type table, the project remark on the data-roles frame, and the notes and Lab 0 lines in the summary. "Your Turn: Compare Only Customers Who Opened the App?" becomes a question with its answer on the frame (the collider). Still 44 frames.
- M2: new road-map frame; removed the Lab 0 remark on the design-based frame, "In pairs, commit first", and the notes, Lab 1 and A1 lines in the summary. 37 frames.

### Planning documents brought up to date
- `revision-plan.md`: status table (M2 notes Section 1.9, H4 refocus, renumbering, schedule columns, rebuilt M1 and M2 decks with their checks, case checks, the merge state of this branch, no tags yet, `map.md` still missing; the README no longer claims a `v4.1` tag); work remaining now starts at M3 slides and the syllabus's `\tbd` items; slide-rebuild notes updated (50 carried frames left in M3 to M6, critique frames C2 to C6 left, notes' order wins, a check script per deck); decisions of 8 October listed one per line.
- `design-plan.md`: retitled as the design record, with a new Section 0 (what was built, actual page counts, changes since v4.1, where files are). It now uses the new handout numbers; the handout table gains built lengths and H4's classical-IV scope; the M2 coverage row adds Section 1.9; notes on how `v4notes.sty`, the separate key files and `notes-v4.tex` delivery became `coursenotes.sty`, `\def\KEY{}` and single files in git; new Decision 5 (noncompliance belongs to M2).

### Handouts renumbered in meeting order; schedule columns
- Handouts now follow the meetings: H1 interference (M2, was H4), H2 neural estimators (M3, was H6), H3 sequential decisions (M6, was H5), H4 instrumental variables (M7, was H1), H5 regression discontinuity (M8, was H2), H6 staggered adoption (M10, was H3). Files, headers, check scripts (`handoutHN_check.py`, `h5_sim.py`, `h6_check.py`, `meetings/m08/h5_bins.csv`) and every reference in the notes, handouts, slides, cases, syllabus, schedule, README and brief were updated. M4's protocol steps H1-H3 (discover, estimate, recommend) are unrelated and unchanged. Two references now point to Meeting 2 instead of the IV handout (M1 notes on monotonicity; the RD handout's use of the LATE theorem). Entries below this one, `design-plan.md` and the pass-1 review keep the old numbers, with a mapping note.
- `schedule.xlsx`: the Misc column is split into Release and Due. The syllabus's weekly table follows: the handout moves into the Block C cell, and a new "Out / due" column lists releases and deadlines.

### Handout H1 (instrumental variables)
- Refocused on classical IV, with no overlap with M2 Section 1.9. Section 1 now opens with "From a randomised offer to an outside shifter" (independence and relevance stated; exclusion, monotonicity and Results 1.13-1.15 cited from M2, not restated), adds "Arguing for an instrument" (origin of Z, balance, zero-first-stage groups, placebo outcomes), and keeps complier means, exclusion and monotonicity failures, 2SLS with strata, the delta method, Anderson-Rubin and locality. The former Results "Two effects of the instrument", "Type shares" and "The LATE theorem" are removed (they are M2 Results 1.13-1.15).
- New worked example: a QuickBite Plus campaign chosen by city managers, not randomised. Pooled ratio 4.4 (confounded by city size) against 1.2 within size and by 2SLS with size indicators (SE about 0.22); compliers order 5.8 without Plus and 7.0 with it; billboards give a direct effect of 0.05 (measured on corporate accounts), corrected LATE 1.0; the campaign and Plus decisions. The weak-instrument and rainfall exercises are kept. `handoutH1_check.py` rewritten for the new numbers.

### Meeting 2 (slides)
- Rebuilt on the coffee-chain case (Case A, M2 releases R1 to R4 and R6; R5 memo at home), aligned with the M2 notes: Results 1.1 to 1.16 with the notes' numbers and wording, in the notes' order. Block A follows notes 1.1 to 1.5 (analyse as drawn, sample-ratio check, Fisher, Neyman and the conservative SE, superpopulation and robust SEs, the break-even test, net value, transport); block B follows 1.6 to 1.9 (the next test, sample size, CUPED, interference and the design effect, peeking, noncompliance and the LATE).
- 36 frames: title, block A 15, block boundary, block B 18, summary. Removed: the map frame (in M1), Today's Plan, critique C1, the Lab 1 frame (now one line in the summary). The two campaign frames are merged. New: sample-ratio check, the conservative-SE figure, peeking and many metrics, and six noncompliance frames.
- `schedule.xlsx` and the syllabus M2 rows now follow the notes' order: transport ends block A and CUPED is in block B.
- New check script `shared/checks/slides02_check.py` (0 mismatches). Case A's release table updated for the new deck.

### Decisions of 8 October, and the cases
- Noncompliance in an RCT (ITT, compliance types, LATE) closes M2; classical IV (outside shifters, 2SLS, weak instruments) stays in Handout H1 with M7, as bonus reading. `schedule.xlsx` (M2B, judgement call 1, M2 bonus reading adds Angrist, Imbens and Rubin 1996), the syllabus, the brief and the README updated.
- M2 notes: new Section 1.9 "Noncompliance: the ITT and the LATE" with Assumptions 1.11-1.12 (exclusion, monotonicity) and Results 1.13-1.16 (two effects of assignment, type shares, the LATE theorem, one-sided noncompliance), ported from H1 and stated for a randomised offer. Section 1.2, the judgement answer, Section 3 (new extension pointing to H1) and the reading list (Imbens and Rubin ch. 23-24; Angrist, Imbens and Rubin 1996) updated; one new goal. H1 gains a pointer to M2 Section 1.9.
- M2 notes Step 6, corrected: it said 40% of offered customers redeemed a ¥10 discount, which would cost ¥4.00 per offer, not the stated ¥1.50. Redemption is now 15% (0.15 x ¥10 = ¥1.50), and the step shows that the LATE (¥12.27) against ¥10 per user is the ITT against ¥1.50 per offer, rescaled. `notes02_check.py` updated.
- A3 is due Friday of Week 5, so nothing is due the weekend before Exam II.
- Reading-and-critique exercises are dropped for now: removed from the syllabus and the brief; v2 critique frames are to be deleted as decks are rebuilt.
- Case A: new Part M2-R6, "Who saw the coupon?" (one-sided noncompliance on the Q2 test: ITT 0.10, first stage 0.80, LATE 0.125, compliers' untreated rate 0.45; openers-only 0.075 and as-treated 0.208 shown wrong; net per seen coupon -¥2.00, consistent with M1). The till discount is stated so that M1's cost model holds.
- Case B: Meeting 9 rewritten for generative AI on Meridian (simulator, estimator and pipeline testbeds with a backtest, synthetic guests, LLM-coded reviews with PPI, text embeddings as controls, memo). The old IV parts are kept as Bonus B1–B4; the full-test ladder and the IV memo were dropped.
- Case C: Meeting 11 rewritten for synthetic control only (flagship, three donors, design freeze and placebos, SC vs DiD, memo using M10's estimate). The old staggered-adoption parts are kept as Bonus B1–B3.
- New check script `shared/checks/case_check.py` for the rewritten case parts; `run_all.sh` runs it.

### Meeting 1 (slides)
- Rebuilt on the lecture's own case (Lin's coupon programme at the coffee chain, case A releases R1 to R5), aligned with notes v4.1 in estimands, assumptions, notation, Result statements (1.1 to 1.13, same numbers and titles) and topic order. The notes' FitLife example is not reproduced; the summary frame points to it.
- 44 frames: title, block A (notes 1.1 to 1.3) 21, block boundary, block B (notes 1.4 to 1.6) 20, summary.
- New in block B, on the coffee-chain case: graph frames (chain, fork, collider; blocked paths; backdoor paths with segment and app opens; graph surgery), a Q3 win-back campaign as the Simpson reversal (pooled -0.22, within +0.05 and +0.20; standardised ATE 0.125, ATT 0.17), and a collider question on `app_opens_q2`.
- Removed: Today's Plan, the Floyd frames (two sentences kept on the SUTVA frame), the prediction-approach frame (one sentence kept), Verifying with the Two Segments, the workshop frame (block C is now Lab 0). Merged the two type-count frames into one.
- Notation now follows `shared/notation.tex` (ATE, ATT, ATU, $\tau_i$, $\Pr$); box colours follow the notes.
- New check script `shared/checks/slides01_check.py` covers every number on the slides; `run_all.sh` now also runs `slides*_check.py`.

## v4.1 (2026-10-07): items brought back from the old decks, plus calibration and decision-focused learning

### Meeting 5 (notes05)
- New: "Recalibrating a score" with Result "Isotonic calibration" (block averages of transformed or DR outcomes; order preserved; proof).
- Worked example Step 5: one sentence on what isotonic calibration would have done.
- New computation exercise: pool-adjacent-violators on six bins, threshold before and after.
- Goals and reading list updated (van der Laan et al., ICML 2023).

### Meeting 6 (notes06), 7 -> 10 pages
- New subsection "Group constraints and the price of fairness": Result (group-specific thresholds, multiplier, dV/dgamma), four-fifths rule, illustration 3:1 -> 1.25:1, price about 585 (555/445 customers), eta about 6,667.
- New subsection "When the mean is not enough: capacity": Result (nonlinear payoff needs each arm's distribution, not the joint), two kitchens (same CATE, opposite decisions), Result (critical fractile) with pinball loss, z_alpha versus kappa, CQTE remark.
  Correction to the old deck: the fractile sets a capacity; the binary promote decision needs E[pi(Y(1))] and E[pi(Y(0))], which experiments identify. The old deck's "quantile of the effect distribution" is not identified and is not needed.
- "Learning the policy directly" rewritten as "From predict-then-optimise to policy learning": three routes, decision-focused learning as policy learning over the optimiser-induced class, DR scores as labels. New Result "Policy learning is weighted classification" (proof); Step 5 reinterpreted with it.
- Two new exercises (capacity computation; fairness plus conservative rule judgement).
- Section 3: fairness stub replaced by "Decision-focused learning in practice" and "Distributional effects". Reading: Elmachtoub-Grigas 2022, Zhao et al. 2012, Kasy-Abebe 2021.
- Goals and pitfall box updated. Section reference to "What the sum assumes" now uses \ref.

### Meeting 9 (notes09), 7 -> 8 pages
- One sentence after "Regret counts only misclassified units" linking it to Meeting 6.
- New extension: three routes on one testbed (optional lab or assignment).

### Notation sheet
- Added F_d(y|x), Gamma_i, c_u, c_o, kappa. Margins tightened to stay on one page.

### Combined PDFs
- all: 110 -> 115 pages; keys rebuilt.
