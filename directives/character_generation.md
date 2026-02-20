# Directive: Character Generation

> Updated: added dolmenwood_chargen.py

## Purpose
Generate complete player characters or detailed NPCs: full stat blocks, equipment, skills with descriptions, personality, and secrets. Output always comes in two versions — GM (full) and player handout (no secrets).

## Execution Script

**Dolmenwood (current campaign):**
```bash
execution/dolmenwood_chargen.py
```

This script is built directly from the Dolmenwood Player's Book. It handles all 6 kindreds, all 9 classes, correct stat tables, equipment rolls, and skill descriptions.

**System-agnostic quick NPC:**
```bash
execution/generate_npc.py
```

Use for fast improvised NPCs during session prep or live play when a full stat block isn't needed.

---

## Common Commands

```bash
# Random character, no restrictions
python execution/dolmenwood_chargen.py

# Filter by kindred (allow only these)
python execution/dolmenwood_chargen.py --kindred human breggle

# Exclude specific classes
python execution/dolmenwood_chargen.py --exclude-class magician enchanter

# Combine filters
python execution/dolmenwood_chargen.py --kindred human breggle --exclude-class magician

# Fix kindred or class
python execution/dolmenwood_chargen.py --kindred elf --class enchanter

# Generate 3 options for player to choose from
python execution/dolmenwood_chargen.py --count 3 --kindred human breggle --quick

# Save to Obsidian vault (creates _gm.md and _player.md)
python execution/dolmenwood_chargen.py --kindred human breggle --save --campaign dolmenwood

# List all valid kindreds and classes
python execution/dolmenwood_chargen.py --list
```

---

## Inputs

| Parameter | Values | Default |
|-----------|--------|---------|
| `--kindred` | human, breggle, elf, grimalkin, mossling, woodgrue | random |
| `--class` | bard, cleric, enchanter, fighter, friar, hunter, knight, magician, thief | random |
| `--exclude-class` | any class name(s) | none |
| `--count` | integer | 1 |
| `--save` | flag | off |
| `--campaign` | campaign folder name | dolmenwood |
| `--quick` | flag, summary only | off |

---

## Output Files

Saved to `campaign/{campaign}/players/` when `--save` is used:

- `{slug}_gm.md` — full sheet including GM Notes section (secrets, hooks, loyalty)
- `{slug}_player.md` — clean handout, no GM notes

For NPCs (when generating an NPC rather than a PC), save to `campaign/{campaign}/npcs/` manually after generation.

---

## What the Script Generates (Dolmenwood)

From the rulebook tables:

- **Ability scores** — 3d6 in order (STR, INT, WIS, DEX, CON, CHA)
- **HP** — class HD + CON modifier, minimum 1
- **AC** — base + armour from equipment roll
- **Saving throws** — from class advancement table (Level 1)
- **Attack bonus** — from class advancement table (Level 1)
- **Equipment** — rolled from class-specific tables (armour, weapons, class items)
- **Starting gold** — 3d6 × 10 gp
- **Skills** — with targets from rulebook, explained in plain language
- **Class abilities** — full descriptions of all Level 1 abilities
- **Kindred traits** — all racial traits described
- **XP modifier** — based on prime ability score(s), including Human +10% bonus
- **Name** — from kindred name tables in rulebook
- **Background** — from kindred background tables
- **Alignment** — weighted random (clerics/friars: Lawful or Neutral only)
- **Special data** — Magician gets spellbook roll (d6, 3 spells), Knight gets liege

---

## Kindred × Class Restrictions

| Kindred | Cannot be |
|---------|-----------|
| Elf | Cleric, Friar |
| Grimalkin | Cleric, Friar |
| Woodgrue | Cleric, Friar |
| Human | Enchanter (rare, possible with GM approval) |
| Breggle | Cleric, Friar (possible, but rare) |
| Mossling | No hard restrictions |

The script enforces hard restrictions automatically. Soft restrictions (e.g. breggle clerics being rare) are handled by weighting — common classes appear more often in random rolls.

---

## Typical Workflow: Generating PCs Before Session 1

1. Ask players for any preferences (kindred, class, concept)
2. Run once per player with their constraints:
   ```bash
   python execution/dolmenwood_chargen.py --kindred human breggle --exclude-class magician --save
   ```
3. Open `_gm.md` — fill in Personality section and GM Notes (secret, hook)
4. Give player `_player.md` — they fill in Appearance, Demeanour, Wants, Fears
5. Update `campaign/dolmenwood/CAMPAIGN.md` — add PC to players table

---

## Typical Workflow: Generating NPCs

For important NPCs, use `dolmenwood_chargen.py` — richer output:
```bash
python execution/dolmenwood_chargen.py --kindred breggle --class knight --save
```

For minor NPCs improvised at the table, use `generate_npc.py` — faster:
```bash
python execution/generate_npc.py --role "innkeeper" --importance minor --quick
```

---

## Edge Cases

- Player wants specific ability scores → generate normally, let player swap two scores (house rule — ask GM)
- Class not available for chosen kindred → script blocks it and explains why; GM can override with `--class` flag directly
- NPC at high level → generate at Level 1, note in GM Notes that they're more experienced; adjust HP/attack manually
- Multiple characters, one session → use `--count 3 --quick` to generate options, then `--save` the chosen one

## Learnings
*Update this section as you encounter edge cases.*
