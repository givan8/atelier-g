#!/usr/bin/env bash
# Create a new project from a template, carrying the house standard with it.
#
#   ./scripts/new-project.sh billing-webhooks --template service-ts
#   ./scripts/new-project.sh ingest --template service-py --dest ~/code
#
# See skills/scaffold-project/SKILL.md for what to do after this runs.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

NAME=""
TEMPLATE=""
DEST="$(pwd)"

usage() {
  cat <<EOF
usage: new-project.sh NAME --template TEMPLATE [--dest DIR]

  NAME        lowercase-hyphenated, named for what it does
  --template  one of: $(ls -1 "$ROOT/templates" | grep -v '^_' | tr '\n' ' ')
  --dest      where to create it (default: current directory)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --template) TEMPLATE="${2:-}"; shift 2 ;;
    --dest)     DEST="${2:-}"; shift 2 ;;
    -h|--help)  usage; exit 0 ;;
    -*)         echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    *)          NAME="$1"; shift ;;
  esac
done

[[ -n "$NAME" ]] || { echo "error: NAME is required" >&2; usage >&2; exit 2; }
[[ -n "$TEMPLATE" ]] || { echo "error: --template is required" >&2; usage >&2; exit 2; }

if [[ ! "$NAME" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]; then
  echo "error: NAME must be lowercase-hyphenated (got '$NAME')" >&2
  exit 2
fi

SRC="$ROOT/templates/$TEMPLATE"
[[ -d "$SRC" ]] || { echo "error: no template '$TEMPLATE' in templates/" >&2; exit 2; }

TARGET="$DEST/$NAME"
[[ -e "$TARGET" ]] && { echo "error: $TARGET already exists" >&2; exit 1; }

mkdir -p "$TARGET"
cp -r "$SRC/." "$TARGET/"
cp -r "$ROOT/templates/_shared/." "$TARGET/"
mkdir -p "$TARGET/docs/adr"
mv "$TARGET/adr-template.md" "$TARGET/docs/adr/TEMPLATE.md" 2>/dev/null || true

# Substitute placeholders.
YEAR="$(date +%Y)"
find "$TARGET" -type f -not -path '*/.git/*' \
  \( -name '*.md' -o -name '*.json' -o -name '*.toml' -o -name '*.yml' -o -name '*.yaml' \
     -o -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.txt' -o -name '*.cfg' \) \
  -exec sed -i.bak \
    -e "s|{{PROJECT_NAME}}|$NAME|g" \
    -e "s|{{TEMPLATE}}|$TEMPLATE|g" \
    -e "s|{{YEAR}}|$YEAR|g" {} \;
find "$TARGET" -name '*.bak' -delete

git -C "$TARGET" init --quiet
git -C "$TARGET" add -A
git -C "$TARGET" commit --quiet -m "chore: scaffold $NAME from template $TEMPLATE"

cat <<EOF

created $TARGET  (template: $TEMPLATE)

next, per skills/scaffold-project/SKILL.md:
  1. install and run the tests from a clean clone — prove it works
  2. write docs/adr/0001-*.md: why this project exists
  3. add CODEOWNERS
  4. replace the README placeholders with what is actually true
  5. push, and confirm CI is green on the first commit

do not build features on a scaffold whose CI has never passed.
EOF
