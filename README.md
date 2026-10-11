# SHBI-GB 7342 Applied Causal Inference for Business: core materials

This repository holds the working core of the course: current sources, the scripts that verify every number, and the
documents that record the decisions. Each document has one file name; its history lives in git, not in versioned
copies. Rules for AI assistants are in `AGENTS.md`. The pre-git material is in `../_archive-2026-10-07.zip`, outside the
repository.

**Start here.** This file says what is current, how to build and check, and what is open. `plan/revision-plan.md` gives
the purpose of the fall 2026 revision, how generative AI enters the course, and the work remaining. `plan/FLAGS.md`
lists every decision waiting on the instructor.

## Layout

```
meetings/m01 ... m11/   notes.tex (technical notes), slides.tex (lecture slides), handout-*.tex,
                        coursenotes.sty (a synced copy, so each folder compiles on its own), figure files
shared/                 coursenotes.sty (master copy), notation.tex, build.sh, build_all.sh, cloud-setup.sh,
                        checks/ (number checks, run_all.sh, editorial_scan.py)
syllabus/               syllabus.tex (follows plan/schedule.xlsx)
cases/                  lecture cases A to C, student and instructor versions
plan/                   schedule.xlsx (source of truth for the calendar, labs, assignments and deadlines),
                        revision-plan.md, editorial-guide.md, FLAGS.md, CHANGELOG.md,
                        old-decks/ (the instructor's earlier decks: reference and voice model only, never built)
reviews/                review reports (pass 1, 2026-10-07)
pdf/                    combined notes, answer keys and notation sheet (generated; not tracked by git)
```

## Status

| Material | State |
|---|---|
| Technical notes, M1–M11 | v4.1 plus the M2 noncompliance section (8 Oct) and the editorial pass (9 Oct). Pass 1 review (arithmetic, wording) done; pass 2 (independent proof check) not yet |
| Handouts H1–H6 | Same state as the notes. Self-contained: each restates what it uses from a meeting instead of citing its numbers |
| Lecture slides, M1–M11 | Rebuilt to the notes and the schedule (8 Oct), editorial pass done (9 Oct); under the instructor's review. Every number checked by `slidesNN_check.py` |
| Syllabus | Matches `schedule.xlsx`. Undecided items are marked `\tbd` and listed in `plan/FLAGS.md` |
| Cases A–C | Aligned with the rebuilt decks; numbers in the rewritten parts checked by `case_check.py` |
| Labs 1–11, assignments A1–A4, autograder | Specified in `schedule.xlsx`; not built |
| Releases | No git tags yet. The spelling and editorial passes are in stacked pull requests #6 to #10 (merge in order) |

## Course structure (from the spreadsheet)

Meetings on Tuesdays and Thursdays, 20 October to 1 December 2026 (no meeting on 26 November, Thanksgiving). Each
meeting has two 50-minute lecture blocks (A, B) and a 60-minute block C, which holds Lab N for Meeting N.

| M | Topic | Handout | Notes |
|---|---|---|---|
| 1 | Causal basics | | |
| 2 | Experiments (closing with noncompliance and the LATE) | H1 Interference | |
| 3 | Conditional effects | H2 Neural estimators | |
| 4 | Causal trees and forests | | |
| 5 | Evaluating targeting policies | | Exam I (M1–M4) |
| 6 | Allocation and policy learning | H3 Sequential decisions | |
| 7 | Observational data | H4 Instrumental variables | Proposal presentations |
| 8 | Double machine learning | H5 Regression discontinuity | |
| 9 | Generative AI in causal analysis | | |
| 10 | Panel data and DiD | H6 Staggered adoption | |
| 11 | Synthetic control (SDID, matrix completion in Section 3) | | Exam II (M5–M10) |
| 12 | Final presentations | | |

Four assignments; Labs 1–11, ten graded and Lab 7 optional; bonus reading is optional. Lecture cases (`cases/`): Houtan
Coffee, a coffee chain (Case A, M1–M7); Qiantan Hotels, a hotel group (Case B, M8–M9); and Sanlin Home, a home-goods
retail chain (Case C, M10–M11). The notes' worked examples deliberately use other businesses: Yangsi Fitness (fitness
chain) in M1, M3, M7, M10, H5 and H6; Pujiang Delivery (food delivery) everywhere else. All businesses, people and case
data are fictional; the names come from places near the Qiantan campus.

## Conventions

- **Notes and handouts** have three sections:
  - Section 1, the general result: numbered Results with short proofs (every identification result gets one; estimation
    results get a one-line reason and a reference); examinable.
  - Section 2, a worked example on the notes' own business, with a computation and a judgement exercise; examinable.
  - Section 3, extensions and an annotated reading list; not examined.
- Each note opens with the decision box and a goals box. Results and Assumptions share one counter per document.
- Handouts are not examined. One PDF per meeting, plus its handout if it has one. Answer keys build from the same
  source (`\def\KEY{}`).
- **Slides and notes** share estimands, assumptions, notation, Result statements (same number, title and wording) and
  topic order, but not the example: each lecture keeps its own case, with numbers checked by its own script.
- Notation follows `shared/notation.tex`. Net value is always $v(x)$; adoption-date potential outcomes are $Y_{it}(g)$.
- Writing, labels, self-containment and citations follow `plan/editorial-guide.md`.

## How to build

From a meeting folder, `bash ../../shared/build.sh notes` writes `build/notes.pdf` and `build/notes-key.pdf`; handouts
build the same way (`bash ../../shared/build.sh handout-H1-interference`), and slides with
`bash ../../shared/build.sh slides nokey`. From the repository root, `bash shared/build_all.sh` syncs the style copies,
rebuilds every document and key, and writes the combined PDFs to `pdf/`. Edit the style only in `shared/coursenotes.sty`.
`shared/cloud-setup.sh` installs LaTeX and the Python packages (`requirements.txt`) in a fresh environment.

## How to check

`bash shared/checks/run_all.sh` reruns one check script per document (notes, handouts, slides, rewritten case parts)
and prints only failures. It needs Python 3 with numpy, scipy and scikit-learn. After editing a number, update its
check script, then rerun.

`python3 shared/checks/editorial_scan.py [files]` runs the editorial checks of `plan/editorial-guide.md`.

Simulation scripts behind worked examples:
- `m08_sim.py`: M8 DML;
- `m08_fig.py`: M8 figure data, written into `meetings/m08/`;
- `m09_sim.py`: M9 simulators, slow, more than 5 minutes;
- `m11_sim.py`: M11 synthetic control;
- `h5_sim.py`: H5 regression discontinuity, writes `meetings/m08/h5_bins.csv`;
- `h6_check.py`: H6 staggered adoption.

## Decisions on record

- Simulators and LLM-generated variables get a full meeting (M9), after DML. A learned simulator is both a data
  generator and the testbed for a whole predict-then-optimize pipeline.
- Proofs are light, for key results; identification theorems always get one.
- Six handouts, numbered in meeting order (8 Oct): H1 interference (M2), H2 neural estimators (M3), H3 sequential
  decisions (M6), H4 instrumental variables (M7), H5 regression discontinuity (M8), H6 staggered adoption (M10). Synthetic
  DiD and matrix completion stay in M11, Section 3.
- Noncompliance in an RCT (ITT, compliance types, LATE) closes M2, lecture and notes (8 Oct). Classical IV (outside
  shifters, 2SLS, weak instruments) stays in Handout H4 with M7, as bonus reading.
- Reading-and-critique exercises are dropped for now (8 Oct).
- Ported from the old causal-module decks (October 2026): newsvendor and capacity, M6; fairness as a priced constraint,
  M6; causal (isotonic) calibration, M5; the predict-then-optimize / decision-focused / policy-learning spectrum, M6
  and M9.
- Deferred: a pricing handout, "From elasticity to price" (pricing from $\hat\theta(x)$, coupon menus, capacity).
  Material is in the old L9 deck.
- Editorial standard (9 Oct): `plan/editorial-guide.md`, with US English, Chicago author-date references, and slides,
  notes and handouts that never point to one another.

## Open items

1. Merge pull requests #6 to #10 (spelling and editorial passes), in order.
2. Settle the decisions in `plan/FLAGS.md`: the syllabus `\tbd` items, and the
   technical points found in the editorial pass.
3. Technical pass on the flagged statements (for example the M10 event-study standard errors and the M11 notation
   clashes), then pass 2: independent check of every numbered Result; pass 3: a student read, one meeting ahead.
4. Review the rebuilt slides (all eleven decks).
5. Build Labs 1–11, assignments A1–A4, the autograder and locked RCT set (see `plan/revision-plan.md`, Section 3).
6. Seed the M8 simulation so its numbers are exactly reproducible (text uses $-0.575$; runs give $-0.574$ to $-0.578$).
7. Optional: the pricing handout; the M9 "three routes" lab (described in M9 Section 3).
