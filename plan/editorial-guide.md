# Editorial guide

Rules for revising the course materials of SHBI-GB 7342, Applied Causal Inference for Business. Every edit must
comply. `AGENTS.md` sets the working rules (git, checks, builds); this guide sets the editorial standard.

The standard: every document reads as finished, human-authored teaching material that a reader outside the class can
pick up and follow.

---

## 0. Scope and definitions

### Documents

Self-containment and definition rules apply at the level of a **document**:

| Artifact | One document is | Source |
|---|---|---|
| Slides | One deck per meeting (Blocks A and B; one block in the exam meetings, 5 and 11) | `meetings/mNN/slides.tex` |
| Technical notes | One set of notes per meeting | `meetings/mNN/notes.tex` |
| Handouts | Each handout | `meetings/mNN/handout-HN-topic.tex` |
| Cases | The student version of each case | `cases/*/student.md` |
| Labs | One lab per meeting, with its supplied resources (data, starter code) | `labs/` (when built) |
| Assignments and exams | Each one, with its supplied resources | `assignments/` (when built) |
| Syllabus | The syllabus, including its weekly schedule | `syllabus/syllabus.tex` |
| Notation sheet | The notation sheet | `shared/notation.tex` |

### Student-facing and excluded paths

Rules and automated checks apply to the student-facing paths only:

```
STUDENT_FACING = meetings/*/slides.tex  meetings/*/notes.tex  meetings/*/handout-*.tex
                 cases/*/student.md  syllabus/syllabus.tex  shared/notation.tex
                 labs/  assignments/                                    (once they exist)
EXCLUDED       = cases/*/instructor.md  plan/  reviews/  shared/checks/  shared/*.sty  shared/*.sh
                 AGENTS.md  CLAUDE.md  README.md  */build/  pdf/
```

Text that `shared/coursenotes.sty` prints on student documents (page headers, title lines) is student-facing, even
though the style file itself is excluded.

**Instructor-only content inside student-facing sources** is exempt from the student-facing rules and checks:

- `\answer{...}` blocks in the notes and handouts (they print only in the answer key);
- `% [RELEASE ...]` comments in the slides, which mark where case parts are handed out;
- other source comments that maintain the file (what it is, which check script verifies its numbers). Comments
  never hold commented-out drafts or change history.

`cases/*/instructor.md` and `plan/schedule.xlsx` are instructor documents. Sections 2 and 3 (writing, spelling) apply
to them; Sections 4 and 5 (self-containment, labels) do not, since they must name frames, parts and plans.

Generated files (PDFs, notebook outputs) are checked through their sources.

### Types of pass

- **Spelling pass:** the one-time conversion to US spelling and serial commas (Section 3). Mechanical; runs first, as
  its own pull request, before any other editing.
- **Editorial pass:** wording, structure, labels, residue, cross-references, citations, formatting. Must not change
  technical content (Section 6).
- **Technical pass:** formulas, code behavior, numerical outputs, dependencies, figures. Scoped separately.

Each pull request states which type of pass it is.

## 1. Remove production history; keep attribution

The materials show no trace of how they were produced: drafts, prior versions, tools, or editing decisions. Scholarly
citations, dataset sources, and required attributions are not production history and are kept (Section 7).

Remove:

- Provenance notes about drafting: "(from the spreadsheet)", "(per the syllabus)", "(based on the earlier draft)",
  "(as requested)".
- Change-log language: "now covers", "has been moved to", "updated to include", "new:", "revised", "(v1.0)".
  Course-internal statements that are legitimate ("as we saw in Meeting 1") are not change-log language, and neither
  is case content that happens to use the words (a "draft memo" in a case task, a vendor's "version 2").
- Parenthetical summaries attached to titles or table cells that describe content instead of naming it.
  "Experiments (closing with noncompliance and the LATE)" becomes "Experiments". If the detail matters, give it its
  own column or line.
- Editorial narration about the document itself: "This section explains...", "Below we outline...", "Note: this
  table summarizes...".
- Leftovers: TODO, XXX, "[insert]", lorem ipsum, commented-out drafts in source files.
- Version numbers and dates on title lines (Section 8).
- Empty table columns. A column empty in every row is deleted. A cell that is legitimately empty uses a marker defined
  once in the table note (for example, "n/a: not applicable").
- Internal paths, file names, and tool references in rendered text: `meetings/m03/slides.tex`, "the repo", "the
  spreadsheet".

**Placeholders for open decisions** (`\tbd{...}` in the syllabus) are never deleted. They block release, and each is
resolved with the instructor or logged in `plan/FLAGS.md`.

Example. Before:

> Course structure (from the spreadsheet)
>
> | M | Topic | Handout | Notes |
> |---|---|---|---|
> | 2 | Experiments (closing with noncompliance and the LATE) | H1 Interference | |

After:

> Course structure
>
> | Meeting | Topic | Handout |
> |---|---|---|
> | 2 | Experiments | H1: Interference |

## 2. Writing traits to remove

These are defaults. The exceptions listed are the only exceptions; do not extend them by analogy.

- **No em-dashes.** House style, no exceptions. Rewrite with a comma, colon, parentheses, or two sentences. In LaTeX
  sources an em-dash is written `---`; elsewhere it is the character itself.
- **En-dashes** (`--` in LaTeX, the character elsewhere) are used only for:
  - numeric and date ranges (pp. 12–18, 2019–2024, July–December);
  - joint names (Frisch–Waugh–Lovell, Anderson–Rubin);
  - paired terms (before–after).

  Everywhere else, use a hyphen.
- **Stock phrasing is not used:** "delve", "dive into", "let's explore", "it's worth noting", "it is important to
  note", "crucial", "pivotal", "realm", "leverage" (as a verb for "use"), "unlock", "seamless", "harness" (as a verb),
  "in today's data-driven world", "game-changer", "key takeaway(s)", "at its core", "a testament to". "Landscape" only
  in its literal or technical sense (a loss landscape).
- **No "not just X, but Y"** constructions, and no reflexive groups of three adjectives ("fast, flexible, and
  powerful").
- **Rhetorical questions:** allowed only if the next sentence answers the question with a specific claim. Never as
  the first sentence of a section or slide. A question-form slide title is allowed if the frame answers it.
- **Summaries:** allowed only after a derivation or a multi-step argument, and must add consolidation (the result in
  one line, or the conditions under which it holds). No closing sentence that restates the paragraph above it.
  Slide exceptions: each deck's closing Summary frame and the "End of Block A" frame.
- **Bold:**
  - In technical notes, handouts, cases, and the syllabus: defined terms at first definition, genuine warnings, and
    step labels in lab and assignment instructions. Not for emphasis in running prose.
  - On slides: defined terms at first use, plus at most one key phrase per frame.
  - Structural bold is not emphasis and is always allowed: table headers, box and block titles, the next block's title
    on the "End of Block A" frame, and spine labels such as **Estimand.**
- **Bullets vs prose:** bullets for genuinely parallel items (assumptions, steps, options). Arguments are written as
  prose. Technical notes are primarily connected prose.
- **No stacked hedges** ("may potentially", "could possibly suggest").
- **Do not substitute other devices for banned ones.** In running prose:
  - at most one colon per paragraph (colons in math, in tables, in labels such as "Definition 1.1:", and in the
    lead-in label of a list item do not count);
  - no dramatic fragments ("Not because X. Because Y.");
  - no stock framing openers: "The key insight is", "Here's the thing", "This matters because", "In short", "Put
    simply", "The bottom line".
- **Headings** name the content. No "Title: Clever Subtitle" patterns.
- **Technical vocabulary stays:** "robust standard errors", "significant" in the statistical sense, "leverage" as a
  regression diagnostic, "agent harness" and "test harness" as nouns.

## 3. Spelling and mechanics: US English

- US spelling throughout: randomization, randomize, optimize, analyze, modeling, modeled, labeled, behavior, center,
  program, practice (verb and noun), judgment, defense, license (noun and verb), fulfill, enroll, gray, while (not
  whilst), among (not amongst).
- Watch especially for: -ise/-isation → -ize/-ization; -yse → -yze; -our → -or; -tre → -ter; doubled l before a
  suffix (modelled, labelled, travelled, cancelled) → single l.
- Exceptions: direct quotations; titles of published works in reference lists; proper names; code identifiers and
  arguments that must match a library's API; and identifiers that never print (LaTeX labels, macro names, file names).
- Serial (Oxford) comma.
- Double quotation marks (``...'' in LaTeX; straight double quotes in the Markdown cases); single quotes only inside
  double quotes.
- Numbers: spell out one through nine in prose; numerals for 10 and above, and always for measurements, percentages,
  statistics, money, and anything with a unit. Percentages use "%" with numerals everywhere (12%, not 12 percent).
  Numerals are always used in labels (Meeting 3, Lab 3, Week 2, Part M3-R2), in or next to math, in tables, and with
  symbols.
- "e.g.," and "i.e.," take a following comma.
- Capitalization of titles and headings:
  - slide frame titles: Title Case;
  - technical notes, handouts, cases, and the syllabus (document titles, section and subsection headings, case part
    headings): sentence case.

  Consistency within each artifact type is what matters.

## 4. Self-containment

Each document (Section 0) contains the definitions, assumptions, and explanations needed to understand its own
substantive content. A reader holding only that document never needs a document of another type to follow it.

### Across artifact types: not allowed

A document never refers to a document of a different artifact type. Slides do not cite technical notes, cases, labs,
or handouts. Technical notes do not cite slides, cases, or labs. Handouts do not cite technical notes or slides.
Cases do not cite slides, technical notes, labs, or handouts. And so on.

Remove, for example: "see the notes for the proof", "as shown in the slides", "the case discusses", "we will practice
this in the lab", "refer to Handout H2", "Lab 3 opener" (in a case heading), "by Result 1.15 of Meeting 2" (in a
handout).

**One exception, for navigation:** the annotated reading list of a set of technical notes may list a handout as an
entry. The body text never depends on it.

### Within the same artifact type: allowed

Documents of the same type may call back to earlier meetings. Slides for Meeting 10 may refer to Meeting 1 ("Recall
the selection-bias decomposition from Meeting 1"), and so may the technical notes. Rules:

- Name the concept and the meeting ("the LATE theorem from Meeting 2"). Do not cite result, equation, section, slide,
  or page numbers from another meeting.
- Callbacks go backward only. Do not promise content in a later meeting by number; a brief preview by concept
  ("later in the course we relax this assumption") is fine. The one exception is the course-map frame in the Meeting 1
  deck, which lists the later meetings by number.
- If following the current argument requires the earlier result, restate it in one or two sentences instead of only
  pointing to it.

A case spans several meetings. Its parts may refer to its own earlier parts and to the meetings they belong to.

### Labs, assignments, and exams: navigation allowed

A lab, assignment, or exam may refer to the resources supplied with it ("Load `rides.csv`, provided with this lab").
Such references never substitute for an explanation of the method.

### Syllabus and schedule

These organize the course and may list every component (meetings, labs, handouts, cases, assignments) by name with a
short description. They must not depend on the content of those components.

### Filling gaps

When removing a cross-reference leaves a gap, fill it by restating content **that already exists elsewhere in the
approved materials**, in one or two sentences. Do not write new content or examples, and do not replace a reference
with a vaguer one ("as discussed elsewhere"). For example, Handouts H4 and H5 restate the Meeting 2 results they use
(the LATE theorem and its assumptions) instead of citing them by number.

Each document defines its own notation and abbreviations at first use, even if another document already defines them.
Duplication of short definitions across documents is expected.

The notation sheet is a standalone reference. No document other than the syllabus refers to it.

## 5. Notation, terminology, and labels

### Notation

- The notation reference is `shared/notation.tex` (the notation sheet). It gains a usage column: for each symbol,
  where it is used.
- Log conflicts (the same object written differently, or the same symbol used for different objects) in
  `plan/FLAGS.md`. Do not choose between conflicting notations.
- Explicitly declared local exceptions are allowed when a model needs different notation (for example, time-indexed
  treatment in dynamic regimes). The exception is stated where it is introduced and recorded in the notation sheet.
- State the estimand before the estimator.

### Terminology

Keep a glossary at `shared/glossary.md` with four columns: concept, preferred term, accepted synonyms, distinctions to
preserve. For example, heterogeneous treatment effects (the phenomenon) and the CATE (a specific estimand) are related
but not interchangeable, and that distinction must survive editing. Replace a term only when the glossary lists it as
a synonym of the preferred term.

### Labels

| Component | Label |
|---|---|
| Meeting | "Meeting 3" |
| Lecture block | "Block A", "Block B"; the lab slot is "Block C" |
| Lab | "Lab 3" (Lab N goes with Meeting N; no letter) |
| Handout | "Handout H2" |
| Case part | "Part M3-R2" (Meeting 3, second release), with the scheme defined once at the top of each case |

Do not use "M3" outside case part IDs, or "Session 3", "Class 3", or "Lecture 3A". Course weeks ("Week 2") appear only
in the syllabus and the schedule. Weeks as units of data (week 4 of a store panel) are content, not labels.

## 6. Technical content and reproducibility

### In a spelling or editorial pass

- Do not change formulas, technical claims, assumptions, code behavior, numerical outputs, or dependencies.
- After any edit that touches a printed number (including spelling one out), rerun `bash shared/checks/run_all.sh`.
  The check scripts hold the printed strings, so a reformatted number can silently stop being checked.
- Verify reproducibility where feasible (code runs, outputs match, figures regenerate) and log failures in
  `plan/FLAGS.md`. Do not fix them.
- If a technical statement looks wrong, log it with the location and reason.

### In a technical pass

Fix logged issues to these standards:

- Every number in the documents is verified by its script in `shared/checks/` (`AGENTS.md`).
- Code runs as written from a clean environment, with random seeds set and package versions pinned in
  `requirements.txt`.
- Outputs shown in documents match what the code produces.
- Figures regenerate from scripts in the repository, with labeled axes and units, legible at projection size, and
  readable in grayscale and by color-blind readers (no meaning carried by red versus green alone).

## 7. Sources, data, and confidentiality

- **Citation style:** Chicago Manual of Style, author-date system, used consistently across all documents. Complete
  entries (authors, year, title, venue, DOI or URL where available).
- **Where references go:**
  - Each slide deck has a References frame, placed immediately before the closing Summary frame.
  - Technical notes and handouts use their annotated reading list as the reference list, with entries in Chicago
    author-date form; annotations are allowed.
  - The syllabus uses its bonus-reading table.
- Every in-text citation appears in the reference list of the same document. A references frame lists only works
  cited in that deck; an annotated reading list may also hold uncited further reading.
- Every dataset has a source line and its license or terms of use.
- Every borrowed figure, table, or quotation is cited. Images are original, licensed, or public domain, with
  attribution where required.
- No confidential or proprietary data, internal metrics, brand elements, or identifiable details from companies or
  industry partners. Use public, simulated, or anonymized and aggregated data cleared for teaching. Log anything
  uncertain in `plan/FLAGS.md`.
- No references to internal communications, unpublished partner reports, or private conversations.

## 8. Format and presentation

- Each document opens with its title. No version numbers, edit or build dates (`\date{\today}`), draft labels, or
  author notes on the title line or in page headers.
- **Slides:** one idea per frame. Avoid dense paragraphs; short prose only for a definition, quotation, or case setup.
  Each deck runs title, road map, Block A, the "End of Block A" frame, Block B, References, Summary (exam meetings
  have one lecture block and no boundary frame). Figures readable from the back of a room.
- **Technical notes:** full sentences and paragraphs, numbered sections, equations numbered only if referenced within
  the same document.
- **Tables:** every column has a header; units in headers; consistent alignment; empty cells handled as in Section 1.
- All links resolve. No links to private drives or repositories in student-facing documents unless students have
  access.
- Accessibility: alt text for images in HTML and Markdown outputs, sufficient color contrast, no information conveyed
  by color alone.
- **The build completes with no errors, no undefined references or citations, and no overfull boxes** (`bash
  shared/build.sh mNN`, `mNN/notes`, `syllabus` and so on; with pdflatex or tectonic). Underfull-box
  and font warnings are not tracked.

## 9. Voice

- Write for an intelligent reader outside the class: a manager or analyst with quantitative training.
- Direct and concrete. Prefer a specific business example to an abstract claim.
- The current prose (the technical notes, handouts, cases, and rebuilt decks) was largely machine-drafted and is not
  the voice reference. The voice reference is `plan/old-decks/lecture01.tex` to `lecture09.tex`, the instructor's own
  tested decks. Move prose toward it: plain declarative sentences, varied length, concrete business examples, direct
  address. For technical notes, follow the decks' word choice and directness in full paragraphs. Do not rewrite
  sentences that already read this way.
- The old decks set voice only. Where their spelling, punctuation, or formatting conflicts with this guide (they use
  em-dashes and British spelling), the guide wins. `plan/old-decks/` stays excluded from the scan.
- Voice changes are made in editorial passes, never in the spelling pass, and never change technical content.

## 10. Process

- **Order of work:** the spelling pass first (one mechanical pull request: US spelling and serial commas, nothing
  else); then editorial passes; technical passes as needed.
- **Branches:** one branch per pass (for example, `edit/residue-and-labels`, `edit/meeting-05`,
  `tech/lab-reproducibility`), or the session's assigned `claude/...` branch. One pull request per batch.
- Follow `AGENTS.md`: run `git status` first, commit each coherent change with its reason, never rewrite history.
- Make routine wording decisions directly. That is the job.
- Log to `plan/FLAGS.md` only:
  - unresolved substantive ambiguity (meaning unclear, or a fix could change meaning);
  - conflicts between materials (notation, terminology, facts);
  - issues outside the current pass's scope (technical problems found in an editorial pass, possible confidentiality
    or licensing issues);
  - open decisions behind `\tbd` placeholders.

  Format: `- [ ] path/to/file:line | section | issue | options`
- **Never summarize changes inside the course materials.** Each pull request description carries counts per rule (for
  example, "em-dashes removed: 41; cross-references removed: 17, of which 9 replaced with restated definitions") and
  the scan results (Section 11). Substantive content changes are also recorded in `plan/CHANGELOG.md`, as `AGENTS.md`
  requires; the changelog is not course material.

## 11. Automated checks

Run from the repository root:

```bash
python3 shared/checks/editorial_scan.py             # every match, then counts per rule
python3 shared/checks/editorial_scan.py --summary   # counts only
python3 shared/checks/editorial_scan.py meetings/m03/slides.tex   # one file
bash shared/checks/run_all.sh                       # numbers (AGENTS.md)
```

The scan covers the student-facing paths of Section 0. It removes `\answer{...}` blocks and LaTeX comments (including
`% [RELEASE ...]` markers) before matching, keeping line numbers. Include its counts in the pull request description.

**The requirement is zero unresolved violations, not zero pattern matches.** Each match is either fixed, judged a
legitimate use (listed in the pull request description with a reason), or logged in `plan/FLAGS.md`.

### Failures (fix or flag)

| Check | What it matches |
|---|---|
| Em-dash | `---` in LaTeX; the em-dash character elsewhere |
| Placeholder | `\tbd{`, TODO, TBD, XXX, `[insert`, lorem ipsum. A `\tbd` is logged, never deleted |
| Citation | An in-text citation ("Wager and Athey (2018)", "(Rubin, 2008)") whose author and year are not in the same document's reference list |
| Build (Section 8) | Errors, undefined references or citations, overfull boxes |
| Numbers | Any mismatch reported by `run_all.sh` |

### Review candidates (inspect each match)

| Check | What it matches |
|---|---|
| En-dash between words | `--` (LaTeX) or the en-dash character between letters; allowed only for joint names and paired terms |
| British spelling | -ise/-isation, -yse, -our, -tre forms, doubled l (modelled, labelled), programme, whilst, amongst, per cent, judgement, defence, licence, and others; a stoplist removes US words with the same endings (raise, exercise, analysis, otherwise) |
| Serial comma | "X, Y and Z" lists without the final comma |
| Stock phrasing | The Section 2 list; "agent harness" and "test harness" are exempt |
| Production history and title residue | Change-log phrases, "draft", "version N", `\today`, narration about the document |
| Labels | "M3" outside case part IDs, "Session 3", "Class 3", "Lecture 3A", "Lab 3C", "Block 3" |
| Cross-artifact references | Per artifact type: slides naming notes, handouts, labs, case parts, worksheets or assignments; technical notes naming slides, labs, case parts or handouts in the body; handouts citing another meeting's Results or Sections; cases naming slides, notes, handouts, labs or frames |
| Forward references | "Meeting N" with N later than the document's own meeting, except in the Meeting 1 course-map frame |
| Question titles | Slide titles ending in "?": the frame must answer the question |
| Bold on slides | Frames with more than two `\textbf`: defined terms plus at most one key phrase. Structural bold is ignored (table headers, box and block titles, spine labels, TikZ node labels, the next block's title on the "End of Block A" frame) |
| Substitute devices | Paragraphs with more than one colon (math, tables, labels and list lead-ins excluded); dramatic fragments ("Not because X. Because Y."); stock framing openers |
| Cross-meeting numbers | "Result", "Assumption", "Section" or "equation" numbers cited next to another meeting |
