#!/bin/bash

set -euo pipefail
studio_root="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "$studio_root/pc" "$@"
