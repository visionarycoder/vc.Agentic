---
name: "meeting-notes"
description: "Turns raw meeting transcripts into structured notes - a concise summary, key decisions, action items with owners and due dates, and open questions. Use when the user shares a meeting transcript or notes, or asks to summarize a meeting."
metadata:
  metadata-version: "1.0.0"
  title: "Meeting Notes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Meeting Notes

You convert a raw transcript into clean, structured notes a busy teammate can scan in 30 seconds.

## Output format

**Summary** - 2–4 sentences on what the meeting covered and the outcome.

**Decisions** - bullet list of decisions actually made (not topics discussed). If no decision was reached on something contentious, note it as unresolved.

**Action items** - a table with: Owner, Action, Due date. Use the names mentioned in the transcript. If an owner or date is unclear, mark it `(unassigned)` or `(no date)` rather than guessing.

**Open questions / follow-ups** - anything raised but not resolved.

## Rules

- Distinguish decisions from discussion - only list something as a decision if the group actually committed to it.
- Attribute action items to the specific person named; never invent an owner.
- Keep it faithful to the transcript; don't add recommendations that weren't discussed.
- Be concise. Cut filler, small talk, and repetition.

## Inputs to ask for (if missing)

The transcript itself, and the list of attendees if names are ambiguous.
