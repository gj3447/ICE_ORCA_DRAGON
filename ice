#!/usr/bin/env sh
set -eu

ICE_REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ ! -x "$ICE_REPO_ROOT/node_modules/.bin/tsx" ]; then
  echo "ice: Node dependencies are missing; run: npm ci" >&2
  exit 2
fi

exec "$ICE_REPO_ROOT/node_modules/.bin/tsx" "$ICE_REPO_ROOT/src/cli.ts" "$@"
