# Dolmenwood GM Assistant

An AI-powered Game Master assistant for running **Dolmenwood** campaigns using the **Old-School Essentials (OSE)** ruleset. Designed to work with Claude Code, Gemini, and other AI agents via a shared instruction set.

---

## What's in This Project

### Core Agent Instructions

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Instructions for Claude Code |
| `AGENTS.md` | System-agnostic agent instructions (mirrored) |
| `GEMINI.md` | Instructions for Gemini (mirrored) |

All three files contain the same GM assistant directives. The agent reads the relevant file depending on the AI environment.

---

### `directives/` – Standard Operating Procedures

Natural-language SOPs that tell the AI *what to do* for each task type:

- `npc_generation.md` – How to generate NPCs (quick or full stat block)
- `character_generation.md` – Full PC/NPC generation for Dolmenwood
- `live_session.md` – Live session mode (fast responses, note-taking, rulings)
- `session_prep.md` – Pre-session preparation workflow
- `session_notes.md` – Post-session summary and note capture
- `encounter_building.md` – Encounter design and random encounter tables

---

### `execution/` – Python Scripts

Deterministic execution scripts the AI orchestrates:

| Script | Description |
|--------|-------------|
| `roll.py` | Dice roller and random table picker |
| `generate_npc.py` | Quick NPC generator (system-agnostic) |
| `dolmenwood_chargen.py` | Full PC/NPC generator using Dolmenwood rules |

---

### `tools/` – Standalone Web Tools

#### `tools/travel-tracker/`

A self-contained HTML/JS app for running the **Dolmenwood overland travel procedure**:
- Click hexes on the map to track movement
- Automated weather rolls, lost checks, random encounter checks
- Travel Point (TP) tracking per OSE/Dolmenwood rules
- Works offline in any browser — no server required

---

### `campaign/dolmenwood/` – Campaign Vault (Obsidian-compatible)

The live campaign data, structured as an Obsidian vault:

```
campaign/dolmenwood/
  CAMPAIGN.md        ← single source of truth (PCs, factions, recent events)
  players/           ← PC sheets (GM version + player-facing version)
  sessions/          ← session summaries (YYYY-MM-DD.md)
  npcs/              ← NPC files
  factions/          ← faction tracker
  locations/         ← location notes
  encounters/        ← encounter files
```

---

### `Maps/` – Map Assets

| Folder | Contents |
|--------|---------|
| `Maps/Referee/` | Full hex map with GM information, VTT-ready versions |
| `Maps/Players/` | Player-safe maps (blank hex grid, player's version) |

---

### `PDF/` – Source PDFs

- `Dolmenwood_Calendar.pdf` – In-world calendar (15 pages)
- `Dolmenwood_Creating_a_character.pdf` – Character creation rules

---

### `players/` – Player-Facing Skills & Resources

Skills and translations organized by AI platform (`skills-anthropics`, `skills-openai`, `skills-custom`), plus localized translations.

---

## Quick Start

### 1. Configuration

```bash
cp .env.example .env
# Fill in NotebookLM notebook IDs
```

### 2. NotebookLM Setup

1. Go to [notebooklm.google.com](https://notebooklm.google.com)
2. Create three notebooks:
   - `Dolmenwood Rules` – upload rulebook PDFs
   - `Dolmenwood Lore` – upload setting material
   - `Dolmenwood Sessions` – session summaries will sync here
3. Copy each notebook ID from the URL into `.env`

### 3. Session Prep

Tell the agent:
> "Prepare session 3. Players ended the last session at the inn in Prigwort. I want them to encounter the Drune this session."

### 4. Live Session

Tell the agent: `session start`

Then use shortcuts:
- `note: [text]` – add a note
- `npc: gate guard` – quick NPC
- `rule: how does morale work?` – rules lookup
- `roll: 2d6+3` – dice roll
- `session end` – close the session

---

## CLI Commands

```bash
# Dice rolling
python execution/roll.py 3d6
python execution/roll.py --ability-scores
python execution/roll.py --table dolmenwood_encounter_forest

# NPC generation
python execution/generate_npc.py --role "guard" --importance minor --quick
python execution/generate_npc.py --role "Drune priest" --importance major --save

# Session notes
python execution/session_note.py start --campaign dolmenwood --session 1
python execution/session_note.py note "Players entered the forest"
python execution/session_note.py end --campaign dolmenwood --session 1
python execution/session_note.py finalize --campaign dolmenwood --session 1
```

---

## Architecture

The system uses a 3-layer architecture:

1. **Directives** (`directives/`) – What to do (natural language SOPs)
2. **Orchestration** (the AI agent) – Reads directives, calls scripts, handles errors
3. **Execution** (`execution/`) – Deterministic Python scripts that do the actual work

The AI never processes data manually when a script exists for the job.

---

## New Campaign

```bash
cp -r campaign/dolmenwood campaign/new_campaign
# Edit campaign/new_campaign/CAMPAIGN.md
# Update ACTIVE_CAMPAIGN in .env
# Create new NotebookLM notebooks
```

---

## Language Convention

- Session notes and player-facing materials → **Polish**
- Rules, mechanics, stat blocks → **English**
- Agent responses follow the GM's language
