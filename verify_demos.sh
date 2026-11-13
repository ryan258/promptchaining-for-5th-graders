#!/usr/bin/env bash
# Run only deterministic local fixtures.
set -euo pipefail
studio_root="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$studio_root"
if [[ -x "$studio_root/.venv/bin/python" ]]; then
  studio_python="$studio_root/.venv/bin/python"
elif [[ -x "$studio_root/venv/bin/python" ]]; then
  studio_python="$studio_root/venv/bin/python"
elif [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
  studio_python="$VIRTUAL_ENV/bin/python"
else
  printf '%s\n' 'Set up the local Python environment first. See docs/SETUP-AND-MODELS.md.' >&2
  exit 1
fi
exec "$studio_python" -m demos.offline_smoke "$@"
