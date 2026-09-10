#!/usr/bin/env bash
# The reorder agent. Module 1, slide 9: "an agent reorders stock ... Nobody looks."
# Claude Code, with one job (reorder_agent_prompt.md) and two commands (agent_tools.py).
# It runs on the trainer's Claude subscription. No API key.
#
# From jaffle_shop/:
#   ./reorder_agent.sh 2026-06-02
# The room watches each command it runs. /exit ends the session.
cd "$(dirname "$0")"
source .venv/bin/activate   # the agent's commands need the sandbox's Python
DAY="${1:-2026-06-02}"
claude \
  --model opus \
  --system-prompt "$(cat reorder_agent_prompt.md)" \
  --tools Bash \
  --allowedTools "Bash(python agent_tools.py read:*)" "Bash(python agent_tools.py order:*)" \
  --permission-mode dontAsk \
  --strict-mcp-config \
  "Good morning. It is $DAY, 09:00. Place today's order."
