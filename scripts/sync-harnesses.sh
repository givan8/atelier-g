#!/usr/bin/env bash
# Project the canonical skill library into harness-specific directories.
#
# skills/  is written by hand.  Everything this script writes is generated and
# committed — see docs/adr/0003-generated-harness-directories.md.
#
# Adding a harness means adding one function here, not forking the library.
#
# Usage:
#   ./scripts/sync-harnesses.sh          # regenerate
#   ./scripts/sync-harnesses.sh --check  # fail if output would change (CI)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

banner_text() {
  printf '<!-- GENERATED FROM %s — DO NOT EDIT. Run ./scripts/sync-harnesses.sh -->' "$1"
}

# Insert the banner *after* the frontmatter block. A harness parses frontmatter
# only when it is the first thing in the file, so the banner cannot lead.
insert_banner_after_frontmatter() {
  awk -v banner="$1" '
    BEGIN { fences = 0; done = 0 }
    {
      print
      if ($0 == "---") { fences++ }
      if (fences == 2 && !done) { print ""; print banner; done = 1 }
    }
  '
}

# ---------------------------------------------------------------- Claude Code
sync_claude() {
  local out=".claude/skills"
  rm -rf "$out"
  mkdir -p "$out"

  for dir in skills/*/; do
    local name
    name="$(basename "$dir")"
    [[ -f "$dir/SKILL.md" ]] || continue

    mkdir -p "$out/$name"
    # Links to repo root (../../x) sit one level deeper in the projection.
    # Links to a sibling skill (../other/) still resolve, since the projection
    # keeps the same sibling layout — leave those alone.
    sed 's|](\.\./\.\./|](../../../|g' "$dir/SKILL.md" |
      insert_banner_after_frontmatter "$(banner_text "skills/$name/SKILL.md")" \
      > "$out/$name/SKILL.md"

    # Copy any supporting files the skill links to.
    find "$dir" -mindepth 1 -not -name SKILL.md -print0 2>/dev/null |
      while IFS= read -r -d '' extra; do
        cp -r "$extra" "$out/$name/"
      done
  done

  echo "  .claude/skills/  <- $(find skills -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ') skills"
}

# Slash commands are harness-specific affordances, not library content.
sync_claude_commands() {
  local out=".claude/commands"
  mkdir -p "$out"

  emit() { # name, skill, one-line purpose
    {
      printf -- '---\ndescription: %s\n---\n\n' "$3"
      banner_text "scripts/sync-harnesses.sh"
      printf '\n\n'
      printf 'Read `skills/%s/SKILL.md` and follow it for the task described below.\n\n' "$2"
      printf 'Task: $ARGUMENTS\n\n'
      printf 'Before acting, confirm you have read `docs/house-rules.md`.\n'
    } > "$out/$1.md"
  }

  emit plan        plan-feature     "Scope a request into an executable plan"
  emit build       implement-change "Implement an agreed plan against the codebase"
  emit test        write-tests      "Add or repair test coverage"
  emit review      review-code      "Review a diff against the house standard"
  emit ship        ship-pr          "Turn finished work into a reviewable PR"
  emit triage      triage-issue     "Decide what to do with an inbound issue"
  emit adr         write-adr        "Record an architecture decision"
  emit new-project scaffold-project "Stand up a new repository from a template"

  echo "  .claude/commands/  <- 8 commands"
}

if [[ $CHECK -eq 1 ]]; then
  if ! git diff --quiet -- .claude 2>/dev/null; then
    echo "working tree is dirty under .claude/ — commit or stash first" >&2
    exit 2
  fi
fi

echo "syncing from skills/ …"
sync_claude
sync_claude_commands

if [[ $CHECK -eq 1 ]]; then
  if ! git diff --quiet -- .claude; then
    echo >&2
    echo "generated output is out of date or was hand-edited." >&2
    echo "run ./scripts/sync-harnesses.sh and commit the result." >&2
    git --no-pager diff --stat -- .claude >&2
    exit 1
  fi
  echo "generated output is up to date"
fi

echo "done"
