---
name: update-revisions
description: Update the nerd.nu Creative and PvE map revision information from the wiki. Trigger this when the user asks to update revision info, refresh map revision data, or run the revision update script.
---

# Update Revisions Skill

Use this skill to update the nerd.nu map revision date arrays in the project template. The AI handles the scraping and template updating process directly using its built-in tools.

## Instructions

1. Use `read_url_content` to fetch the content of the following wiki pages:
   - PvE: `https://wiki.nerd.nu/wiki/PvE`
   - Creative: `https://wiki.nerd.nu/wiki/Creative`
2. Parse the HTML tables containing revision histories:
   - For PvE, extract: Revision Number, Start Date, End Date, and Comments.
   - For Creative, extract: Rev, Start Date, End Date, and Comments.
3. Clean and normalize the dates:
   - If an end date is `-`, `(current)`, or empty, set it to `null`.
   - For Creative Rev 7, if the start date is empty, normalize it to `"2010-09-01"`.
   - For Creative Rev 6, normalize the start date `"2010-07"` to `"2010-07-01"` and end date to `"2010-08-31"`.
   - For Creative Rev 5, normalize the end date to `"2010-06-30"`.
4. Identify the active Minecraft version in the comments (e.g. "Minecraft 1.20.4").
5. Update the javascript arrays `pveRevisions` and `creativeRevisions` inside [nerd_map_lookup.html](core/templates/core/nerd_map_lookup.html) with the updated arrays in JSON format.

## Crucial Execution Rules

- **Do NOT use background tasks or run scripts in the background.** All file reads, writes, and web requests must be completed synchronously.
- **Verify the template file [nerd_map_lookup.html](core/templates/core/nerd_map_lookup.html) is fully updated** before completing your response. Do not exit until the file has been successfully written.
