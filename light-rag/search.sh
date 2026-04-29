#!/bin/bash
# light-rag search wrapper for OpenClaw
# Usage: search.sh "query" [top_k]
# Output: JSON to stdout

set -euo pipefail

cd /root/.openclaw/workspace/light-rag
source venv/bin/activate

QUERY="${1:-}"
TOP_K="${2:-5}"

if [ -z "$QUERY" ]; then
  echo '{"error":"missing query"}'
  exit 1
fi

PYTHONPATH=. python -m src.cli --config config/config.memory-test.yaml search "$QUERY" --top-k "$TOP_K"
