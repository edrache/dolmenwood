# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [0.3.1] – 2026-02-21

### Added
- **`tools/travel-tracker/` – Calendar sync integration**
  - New "Campaign Day" card in the sidebar displaying current campaign date and season (loaded from calendar state on startup — server API with localStorage fallback)
  - "Sync with Calendar" toggle: when enabled, keeps the Season selector in sync with the active calendar month, and syncs weather flags (I/V/W) if weather was set in the calendar
  - "Reset TP (New Day)" now automatically advances the calendar day (written to localStorage) when sync is enabled; status shown inline
  - Imports `tools/calendar/js/calendar-data.js` and `calendar-state.js` for shared data model — no duplication

---

## [0.3.0] – 2026-02-20

### Added
- **`tools/calendar/`** – Dolmenwood in-world calendar web app (two-page, folk aesthetic)
  - `index.html`: player-facing calendar view
    - Current day banner with weekday name, month, season, moon phase, feast day
    - Full 12-month calendar grid with Wysendays, saint's feasts, moon phases marked
    - "Forthcoming Days of Note" panel listing next 8 events with countdown
    - Auto-polls `localStorage` every 10s to reflect Referee updates in near real-time
  - `referee.html`: Referee's private control panel
    - Day navigation (previous/next) and manual date picker with year label
    - Weather roller: 2d6 against season table (Winter/Spring/Summer/Autumn/Hitching/Vague)
    - Weather flags: I (Impeded travel), V (Visibility halved), W (Wet/campfire difficult)
    - Custom weather entry with flag checkboxes; one-click "set as today's weather"
    - Encounter check (1d6 ≤ 2) and full encounter roller:
      type (1d8), creature (1d20), surprise, distance (2d6 × 30 ft), reaction (2d6), activity (1d20)
    - Encounter contexts: Wilderness Day, Road Day, Night+Fire, Night No Fire
    - Regional encounter tables: Aldweald, Brackenwold, Wychwood, Nagwood
    - Quick dice buttons: d4, d6, d8, d10, d12, d20, d100, 2d6
    - Public note field (rendered on player view)
    - Session log with timestamps and day labels; persisted in `localStorage`
  - `js/calendar-data.js`: all 12 months with feasts, Wysendays, moon phases, season mapping
  - `js/calendar-state.js`: shared state model, `localStorage` persistence, day advance/retreat
  - `js/weather-data.js`: 2d6 weather tables for all 6 season variants + `rollWeather()`
  - `js/encounters-data.js`: encounter type table, common tables (Animal/Monster/Mortal/Sentient), 4 regional tables, reaction & activity tables + `rollEncounter()`
  - `css/folk.css`: folk/illuminated-manuscript stylesheet (Cinzel + Crimson Text, parchment palette)

---

## [0.2.0] – 2026-01-XX

### Changed
- **`tools/travel-tracker/`** – Refactored monolithic `index.html` into separate JS modules:
  - `js/data-hexes.js`, `js/data-weather.js`, `js/data-encounters.js`
  - `js/dice.js`, `js/weather.js`, `js/encounters.js`, `js/travel.js`

---

## [0.1.0] – 2025-XX-XX

### Added
- Initial project structure: `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` agent instructions
- `directives/`: SOPs for NPC generation, character generation, session prep, session notes, encounter building, live session mode
- `execution/`: `roll.py`, `generate_npc.py`, `dolmenwood_chargen.py`, `session_note.py`, `search_rules.py`
- `templates/`: Obsidian markdown templates (NPC, session, faction, location, encounter, player character)
- `tools/travel-tracker/`: overland travel procedure app (hex map, weather, encounters, TP tracking)
- `campaign/dolmenwood/`: campaign vault scaffold (CAMPAIGN.md, players, sessions, NPCs, factions, locations, encounters)
- `Maps/`: Referee and player-facing map assets
- `PDF/`: Dolmenwood Calendar, character creation rules
