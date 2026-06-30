#!/bin/bash
# Claude Code PreToolUse hook
# Intercepts git commit commands. If source documentation files are staged
# but the vault has no corresponding staged updates, blocks the commit and
# asks Claude to sync the vault first.

input=$(cat)

# Extract the bash command from the hook input JSON
command=$(python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('command', ''))
except Exception:
    print('')
" <<< "$input")

# Only act on git commit commands
if ! echo "$command" | grep -qE "git\s+commit"; then
  exit 0
fi

VAULT="vault/school-timeline-vault"

# Collect staged source documentation files
staged_sources=()
while IFS= read -r file; do
  case "$file" in
    bugs/*.md|docs/*.md|features/*.md|tasks/*.md|README.md)
      staged_sources+=("$file")
      ;;
  esac
done < <(git diff --cached --name-only 2>/dev/null)

# No source docs staged — nothing to do
if [ ${#staged_sources[@]} -eq 0 ]; then
  exit 0
fi

# If vault files are also staged, the sync was already done — allow commit
vault_staged=$(git diff --cached --name-only 2>/dev/null | grep -c "^$VAULT/" || true)
if [ "$vault_staged" -gt 0 ]; then
  exit 0
fi

# Build the list string for the message
files_list=""
for f in "${staged_sources[@]}"; do
  files_list="$files_list  - $f\n"
done

python3 - <<PYEOF
import json

files = """$files_list"""
vault = "$VAULT"

context = (
    "Source documentation files were staged for commit but the Obsidian vault has no staged updates.\n\n"
    "Changed source files:\n"
    + files +
    "\nPlease:\n"
    "1. Read each changed source file\n"
    "2. Update the corresponding note in " + vault + "/ using proper Obsidian formatting "
    "(frontmatter, wikilinks, callouts)\n"
    "3. Stage the updated vault notes (git add)\n"
    "4. Retry the commit"
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Obsidian vault sync required before commit",
        "additionalContext": context
    }
}))
PYEOF
