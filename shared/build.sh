#!/bin/bash
# Build the course documents. Run from anywhere in the repository:
#   bash shared/build.sh                  everything: notation sheet, syllabus, every meeting, then the combined PDFs in pdf/
#   bash shared/build.sh m03              every document of one meeting (notes, handouts, slides)
#   bash shared/build.sh m03/notes        one document (also m03/slides, m03/handout-H2-neural-estimators)
#   bash shared/build.sh syllabus         the syllabus (also: notation)
#   bash shared/build.sh setup            install TeX Live, poppler and the Python packages (fresh Linux environment)
# Engine: tectonic if it is installed, otherwise pdflatex. Override with ENGINE=pdflatex or ENGINE=tectonic.
# Documents that contain \answer (notes and handouts) also build an answer key, <name>-key.pdf.
# Output goes to a build/ folder next to each source. Each document prints one line: ok, or what went wrong
# (LaTeX errors, undefined references, overfull boxes).
ROOT=$(cd "$(dirname "$0")/.." && pwd)
if [ -z "$ENGINE" ]; then command -v tectonic >/dev/null && ENGINE=tectonic || ENGINE=pdflatex; fi
STATUS=0

setup() {  # for a cloud environment's setup script, these two lines can be pasted as they are
  apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
    texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-pictures poppler-utils
  pip install -q -r "$ROOT/requirements.txt"
}

# compile DIR NAME [key]: one pass of the chosen engine, writing DIR/build/NAME.pdf (or NAME-key.pdf)
compile() {
  local dir=$1 name=$2 job=$2 src
  [ "$3" = key ] && job=$name-key
  mkdir -p "$dir/build"
  if [ "$3" = key ]; then src="\\def\\KEY{}\\input{$name}"; else src="$name.tex"; fi
  if [ "$ENGINE" = tectonic ]; then
    [ "$3" = key ] && { printf '%s\n' "$src" > "$dir/build/$job.tex"; src="build/$job.tex"; }
    (cd "$dir" && tectonic --keep-logs --chatter minimal -Z search-path="$PWD" --outdir build "$src") > "$dir/build/$job.console" 2>&1
  else
    for pass in 1 2 3; do
      (cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build -jobname "$job" "$src") \
        > "$dir/build/$job.console" 2>&1 || break
      grep -q "Rerun to get" "$dir/build/$job.log" || [ $pass = 1 ] || break
    done
  fi
  report "$dir" "$job"
}

report() {
  local log=$1/build/$2.log pdf=${1#"$ROOT"/}/build/$2.pdf problems
  [ -f "$log" ] || log=$1/build/$2.console
  problems=$(grep -E "^!|^error:" "$log" | sort -u | head -5)   # errors first; reference warnings only if none
  [ -z "$problems" ] && problems=$(grep -E "Reference .* undefined|Citation .* undefined" "$log" | sort -u | head -5)
  local overfull; overfull=$(grep -c "^Overfull" "$log")
  if [ -n "$problems" ] || [ ! -f "$1/build/$2.pdf" ]; then
    echo "FAIL $pdf"; [ -n "$problems" ] && echo "$problems" | sed 's/^/     /'; STATUS=1
  elif [ "$overfull" -gt 0 ]; then echo "ok   $pdf  ($overfull overfull box(es); see the .log)"
  else echo "ok   $pdf"; fi
}

doc() {  # doc DIR NAME: the document, plus its answer key when it has answers
  compile "$1" "$2"
  grep -q '\\answer' "$1/$2.tex" && compile "$1" "$2" key
}

meeting() {
  local d=$ROOT/meetings/$1
  [ -d "$d" ] || { echo "no such meeting: $1"; exit 1; }
  cp "$ROOT/shared/coursenotes.sty" "$d/"   # keep the style copy in sync
  if [ -n "$2" ]; then doc "$d" "$2"; return; fi
  for f in notes $(cd "$d" && ls handout-*.tex 2>/dev/null | sed 's/\.tex$//') slides; do doc "$d" "$f"; done
}

all() {
  doc "$ROOT/shared" notation
  doc "$ROOT/syllabus" syllabus
  for d in "$ROOT"/meetings/m*/; do meeting "$(basename "$d")"; done
  if command -v pdfunite >/dev/null; then
    local all=("$ROOT/shared/build/notation.pdf") keys=("$ROOT/shared/build/notation.pdf") d f
    for d in "$ROOT"/meetings/m*; do
      for f in notes $(cd "$d" && ls handout-*.tex 2>/dev/null | sed 's/\.tex$//'); do
        all+=("$d/build/$f.pdf"); keys+=("$d/build/$f-key.pdf")
      done
    done
    mkdir -p "$ROOT/pdf"
    pdfunite "${all[@]}" "$ROOT/pdf/notes-all.pdf" && pdfunite "${keys[@]}" "$ROOT/pdf/notes-keys.pdf" \
      && cp "$ROOT/shared/build/notation.pdf" "$ROOT/pdf/notation.pdf" && echo "combined PDFs in pdf/"
  else
    echo "pdfunite not found: skipped the combined PDFs in pdf/"
  fi
}

echo "engine: $ENGINE"
case "${1:-all}" in
  all) all ;;
  setup) setup ;;
  syllabus) doc "$ROOT/syllabus" syllabus ;;
  notation) doc "$ROOT/shared" notation ;;
  m[0-9][0-9]) meeting "$1" ;;
  m[0-9][0-9]/*) f=${1#*/}; meeting "${1%%/*}" "${f%.tex}" ;;
  *) sed -n '2,11p' "$0"; exit 1 ;;
esac
exit $STATUS
