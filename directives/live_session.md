# Directive: Live Session

> Updated: initial version
> **CRITICAL:** During live session, responses must be SHORT and FAST. No preamble. No "Great question!". Just the answer.

## Purpose
Provide real-time support during a running session: rules lookups, NPC improvisation, random rolls, quick rulings, note capture.

## Entering Live Session Mode

GM signals with: `"session start"`, `"we're playing"`, `"sesja start"`, or similar.

On session start:
1. Confirm active campaign is loaded
2. Open `.tmp/session_live.md` (create if missing) with header:
   ```
   # Session Live Notes – [Date]
   ## Present: [players if known]
   ---
   ```
3. Switch to fast-response mode (see below)
4. Remind GM: "Live mode active. Say 'note:' to log something, 'roll:' for dice, 'npc:' for improvised NPC."

## Fast-Response Mode Rules

- **Rules questions** → Answer in ≤3 sentences. If uncertain, say "Checking NotebookLM..." then give answer.
- **NPC improvisation** → Give Quick NPC block (see `npc_generation.md`) immediately
- **Dice rolls** → Just give the result + brief context
- **"What does X know?"** → Give 1–3 bullet points max
- **Lore questions** → 2 sentences max, then "want more detail?"
- **Rulings** → Give a ruling, explain in 1 sentence, offer alternative if ambiguous

## Live Commands (GM shortcuts)

| Command | Action |
|---------|--------|
| `note: [text]` | Append to `session_live.md` with timestamp |
| `roll: [XdY+Z]` | Execute dice roll |
| `roll: [table name]` | Roll on named random table |
| `npc: [role/description]` | Generate Quick NPC immediately |
| `morale [creature]` | Look up morale score, tell GM when to roll |
| `rule: [question]` | Fast rules lookup via NotebookLM |
| `faction: [name]` | Quick faction status summary |
| `session end` | Exit live mode, trigger session notes (see `session_notes.md`) |

## Note Logging Format

Auto-append to `.tmp/session_live.md`:
```
[HH:MM] note: [text as given by GM]
[HH:MM] roll: [expression] → [result]
[HH:MM] npc: [name] – [role] appeared
[HH:MM] event: [significant thing that happened]
```

## Improvised NPC Protocol

When GM asks for an NPC mid-session:
1. Check `campaign/npcs/` for anyone fitting the role (10 second scan)
2. If found → load and summarize
3. If not → generate Quick NPC on the spot, log to `.tmp/session_live.md`
4. After session → convert logged NPCs to full files if they matter

## Rules Lookup Protocol

1. Query NotebookLM MCP first (most accurate): `search_rules.py --query "[question]" --notebook dolmenwood_rules`
2. If no result → answer from training knowledge, flag as "from memory, verify"
3. Give the ruling the GM can use right now
4. Note any edge cases in 1 sentence

## Morale Reference (OSE / Dolmenwood)

Roll 2d6 when:
- First casualty on monster side
- Monster reduced to half HP
- Monster's leader killed
- Monster facing obviously superior force

Result ≤ Morale: monsters flee/surrender
Result > Morale: monsters fight on

## Exiting Live Mode

GM signals with: `"session end"`, `"koniec sesji"`, or similar.

On session end:
1. Confirm notes captured in `.tmp/session_live.md`
2. Ask: "Gotowe! Czy chcesz teraz podsumowanie sesji?" (offer to run `session_notes.md` directive)
3. Exit fast-response mode

## Edge Cases
- GM forgets to say "session start" → if messages are short, tactical, and GM is clearly playing, assume live mode
- Multiple NPCs improvised → batch-prompt after session: "These 3 NPCs appeared – want full files?"
- Rules conflict arises → give both interpretations, let GM rule, note their ruling for future

## Learnings
*Update this section as you encounter edge cases.*
