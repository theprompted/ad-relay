#!/bin/bash
# The Ad Relay — Autonomous multi-leg agent loop
# Usage: ./ad-relay.sh [max_legs]
# Each run spawns a fresh Claude instance. That instance runs one leg, hands off, exits.
# The next instance picks up from the baton.

# Note: intentionally no set -e — claude --print exits non-zero, handled with || true

MAX_LEGS=10

while [[ $# -gt 0 ]]; do
  case $1 in
    *)
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        MAX_LEGS="$1"
      fi
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RELAY_FILE="$SCRIPT_DIR/ad-relay.json"
BATON_FILE="$SCRIPT_DIR/baton.txt"

if [ ! -f "$RELAY_FILE" ]; then
  echo "Error: ad-relay.json not found in $SCRIPT_DIR"
  echo "Copy ad-relay.template.json to ad-relay.json and configure it before running."
  exit 1
fi

# Initialize baton if it doesn't exist
if [ ! -f "$BATON_FILE" ]; then
  echo "# Relay Baton" > "$BATON_FILE"
  echo "Started: $(date)" >> "$BATON_FILE"
  echo "---" >> "$BATON_FILE"
fi

echo "Starting The Ad Relay — Max legs: $MAX_LEGS"
echo "Relay config: $RELAY_FILE"
echo ""

for i in $(seq 1 $MAX_LEGS); do
  echo "==============================================================="
  echo "  Leg $i of $MAX_LEGS"
  echo "==============================================================="

  OUTPUT=$(claude --dangerously-skip-permissions --print < "$SCRIPT_DIR/AD-RELAY.md" 2>&1 | tee /dev/stderr) || true

  if echo "$OUTPUT" | grep -q "RELAY_COMPLETE"; then
    echo ""
    echo "Relay complete — all legs handed off."
    echo "Finished at leg $i of $MAX_LEGS"
    exit 0
  fi

  echo "Leg $i handed off. Next leg loading..."
  echo ""
  sleep 2
done

echo ""
echo "Relay reached max legs ($MAX_LEGS) without completing."
echo "Check baton.txt for status."
exit 1
