# Directive: NPC Generation

> Updated: initial version

## Purpose
Generate complete NPCs usable at the table: stat block, personality, secrets, faction ties. Works for both improvised NPCs (quick, during session) and prepared NPCs (full, before session).

## Inputs
- `role` – what the NPC does (e.g., "innkeeper", "Drune cultist scout", "wandering merchant")
- `importance` – `minor | major | boss`
- `system` – defaults to active campaign system (currently: Dolmenwood / OSE-adjacent)
- `faction` – optional, links NPC to a faction file
- `context` – optional, e.g., "party just entered town, needs info about missing child"

## Output Types

### Quick NPC (live session, minor)
Single block, fits in 30 seconds of reading:
```
Name: [Name]
Role: [Role]
Looks: [1 sentence]
Voice/manner: [1 sentence]
Wants: [1 thing]
Knows: [1 secret or useful fact]
Stats: AC [X] HD [X] HP [X] Morale [X]
```

### Full NPC (session prep, major/boss)
Full Markdown file saved to `campaign/{name}/npcs/{slug}.md`. Use `templates/npc.md`.

## Process

1. Check `campaign/{name}/npcs/` – does a similar NPC already exist? Reuse or adapt.
2. For rules-accurate stat blocks, query NotebookLM: `search_rules.py --query "OSE [creature type] stats"`
3. Roll personality using tables if no context given (use `roll.py --table personality`)
4. For major NPCs: assign at least 1 secret, 1 want, 1 fear
5. For boss NPCs: add special abilities, lair description, morale threshold behavior
6. Save to vault, update `CAMPAIGN.md` NPC list

## Stat Block Format (Dolmenwood / OSE)

```
**[Name]** ([Role])
AC [X] (ascending: [Y])  HP [X]d[X] ([avg])
Move [X]'  Morale [X]  Alignment [X]
Attacks: [attack] [+X] ([damage])
Saves: D[X] W[X] P[X] B[X] S[X]
Special: [abilities]
Treasure: [type]
XP: [X]
```

## Personality Generation (if not specified)
Roll or pick from each:
- **Demeanor:** gruff / jovial / nervous / calculating / melancholic / fanatical
- **Speech quirk:** repeats last word / speaks in proverbs / over-explains / whispers
- **Motivation:** survival / greed / duty / revenge / curiosity / devotion
- **Secret:** knows something dangerous / is not who they claim / owes a debt / has done something terrible

## Player-Facing Output
When generating a PC or NPC for players: strip all GM secrets. Output clean Markdown, no `<!-- hidden -->` blocks.

## Edge Cases
- Unknown creature type → use closest analog, flag for GM review
- NPC appears in multiple factions → create cross-links in both faction files
- NPC dies during session → update file with `status: deceased`, keep in vault for history

## Learnings
*Update this section as you encounter edge cases.*
