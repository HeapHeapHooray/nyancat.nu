#!/bin/bash
# Programmatically prompts the Antigravity CLI (agy) to update revision info.
# The AI will read the workspace skill and update the template files using its tools.

echo "=== Programmatically prompting Antigravity CLI (agy) ==="
agy --prompt "Update the nerd.nu revision info. Use read_url_content to fetch https://wiki.nerd.nu/wiki/PvE and https://wiki.nerd.nu/wiki/Creative. Then, parse the revisions and update the 'pveRevisions' and 'creativeRevisions' variables in the file 'core/templates/core/nerd_map_lookup.html' relative to the workspace root. Do not use terminal commands, git commands, or grep. Perform all actions synchronously using your direct file edit and url tools. Verify the file is fully updated before finishing." --dangerously-skip-permissions
echo "=== Done ==="
