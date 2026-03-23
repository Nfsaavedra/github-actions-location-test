#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 N" >&2
  echo "  Dispatch the workflow in dispatch-location.yml N times on the repo default branch." >&2
  echo "  Each run starts only after the previous run has finished." >&2
  exit 1
}

[[ "${1:-}" =~ ^[1-9][0-9]*$ ]] || usage

readonly N="$1"
readonly WORKFLOW="dispatch-location.yml"

if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "error: run this from inside the git clone of the repository" >&2
  exit 1
fi

cd "$(git rev-parse --show-toplevel)"

if ! command -v gh &>/dev/null; then
  echo "error: install the GitHub CLI: https://cli.github.com" >&2
  exit 1
fi

ref=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || echo main)

for ((i = 1; i <= N; i++)); do
  echo "=== Dispatch $i of $N ==="
  last_id=$(gh run list --workflow="$WORKFLOW" --limit 1 --json databaseId -q '.[0].databaseId' 2>/dev/null || true)
  if [[ "$last_id" == "null" ]]; then
    last_id=""
  fi

  gh workflow run "$WORKFLOW" --ref "$ref"

  run_id=""
  for ((attempt = 1; attempt <= 90; attempt++)); do
    sleep 2
    current=$(gh run list --workflow="$WORKFLOW" --limit 1 --json databaseId -q '.[0].databaseId' 2>/dev/null || true)
    if [[ "$current" == "null" ]]; then
      current=""
    fi
    if [[ -n "$current" && "$current" != "$last_id" ]]; then
      run_id=$current
      break
    fi
  done

  if [[ -z "$run_id" ]]; then
    echo "error: timed out waiting for a new workflow run after dispatch" >&2
    exit 1
  fi

  echo "Waiting for run $run_id ..."
  gh run watch "$run_id"
done

echo "Finished $N run(s)."
