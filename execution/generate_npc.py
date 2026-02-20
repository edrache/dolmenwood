#!/usr/bin/env python3
"""
generate_npc.py – Generate NPC stat blocks and personalities.
Usage:
    python generate_npc.py --role "innkeeper" --importance minor
    python generate_npc.py --role "Drune cultist" --importance major --level 3
    python generate_npc.py --quick              # random minor NPC, no frills
"""

import argparse
import random
import json
import re
from pathlib import Path
from datetime import datetime

CAMPAIGN_DIR = Path(__file__).parent.parent / "campaign"

# ─── OSE Stat Tables ──────────────────────────────────────────────────────────

MORALE_BY_TYPE = {
    "common folk": 6, "townsperson": 6, "merchant": 7, "soldier": 8,
    "guard": 9, "veteran": 10, "cultist": 10, "fanatic": 12,
    "bandit": 8, "thug": 7, "assassin": 9, "knight": 11,
    "drune": 10, "default": 8,
}

HD_BY_IMPORTANCE = {
    "minor": (1, 1), "major": (2, 4), "boss": (5, 8)
}

ALIGNMENT_OPTIONS = ["Lawful", "Neutral", "Chaotic"]

# ─── Random Tables ────────────────────────────────────────────────────────────

DEMEANORS = [
    "Gruff and suspicious", "Jovial and generous", "Nervous and evasive",
    "Calculating and patient", "Melancholic and distant", "Fanatical and intense",
    "Proud and condescending", "Bitter and resentful", "Cheerful and oblivious",
    "Serene and unflappable"
]

QUIRKS = [
    "Repeats the last word they say", "Speaks in old proverbs",
    "Over-explains obvious things", "Whispers even in empty rooms",
    "Laughs at inappropriate moments", "Never makes eye contact",
    "Touches face when lying", "Finishes others' sentences, incorrectly",
    "Constantly fidgets with a ring or coin", "Addresses everyone by wrong name"
]

MOTIVATIONS = [
    "Survival at any cost", "Accumulating wealth", "Fulfilling an oath",
    "Seeking revenge", "Satisfying curiosity", "Religious devotion",
    "Protecting someone specific", "Proving themselves", "Escaping their past",
    "Building something lasting"
]

SECRETS = [
    "Knows the location of something dangerous",
    "Is not who they claim to be",
    "Owes a life-debt to a powerful figure",
    "Has done something unforgivable and fears discovery",
    "Is being blackmailed by an unknown party",
    "Secretly works for a rival faction",
    "Has hidden family they protect obsessively",
    "Is dying and tells no one",
    "Witnessed something unspeakable in the deep woods",
    "Stole something that doesn't belong to them"
]

APPEARANCES = [
    "Weathered face, eyes that miss nothing, perpetually muddy boots",
    "Surprisingly well-dressed for where they are, nervous hands",
    "Old scar from jaw to ear, matter-of-fact about it",
    "Extremely tall, stooped from years of low doorways",
    "Ink-stained fingers, mutters while thinking",
    "Moves silently, even in a crowd",
    "Enormous beard, surprisingly gentle voice",
    "Missing two fingers on the left hand",
    "Striking eyes, an unusual color",
    "Looks younger than their age; something is off about that"
]


# ─── Stat Generation ──────────────────────────────────────────────────────────

def roll(expression: str) -> int:
    """Simple dice roller for internal use."""
    match = re.match(r'^(\d*)d(\d+)([+-]\d+)?$', expression.lower())
    if not match:
        return int(expression)
    n = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    mod = int(match.group(3)) if match.group(3) else 0
    return sum(random.randint(1, sides) for _ in range(n)) + mod


def osef_modifier(score: int) -> str:
    table = {3: -3, 4: -2, 5: -2, 6: -1, 7: -1, 8: -1,
             9: 0, 10: 0, 11: 0, 12: 0,
             13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 3}
    m = table.get(score, 0)
    return f"+{m}" if m >= 0 else str(m)


def generate_ose_stats(hd_range: tuple, role: str = "") -> dict:
    """Generate OSE-compatible NPC stats."""
    hd_min, hd_max = hd_range
    hd = random.randint(hd_min, hd_max)
    hp = roll(f"{hd}d6")
    
    # AC based on rough role inference
    role_lower = role.lower()
    if any(w in role_lower for w in ["knight", "soldier", "guard", "warrior"]):
        ac_desc, ac_asc = random.choice([(5, 14), (4, 15), (3, 16)])  # chainmail or plate range
    elif any(w in role_lower for w in ["thief", "assassin", "rogue", "scout"]):
        ac_desc, ac_asc = 7, 12  # leather
    elif any(w in role_lower for w in ["mage", "wizard", "witch", "drune"]):
        ac_desc, ac_asc = 9, 10  # no armor
    else:
        ac_desc, ac_asc = random.choice([(9, 10), (8, 11), (7, 12)])  # unarmored to leather
    
    # Morale
    morale = 8
    for key in MORALE_BY_TYPE:
        if key in role_lower:
            morale = MORALE_BY_TYPE[key]
            break
    
    # Attack bonus (roughly HD/2, min +0)
    atk_bonus = max(0, hd // 2)
    
    # Saving throws (use fighter progression as rough default)
    save_base = max(16 - hd, 8)
    saves = {
        "death_poison": save_base,
        "wands": save_base + 1,
        "paralysis_stone": save_base + 1,
        "breath": save_base + 2,
        "spells": save_base + 2,
    }
    
    return {
        "hd": hd,
        "hp": hp,
        "ac_descending": ac_desc,
        "ac_ascending": ac_asc,
        "morale": morale,
        "attack_bonus": atk_bonus,
        "saves": saves,
        "xp": hd * 10 + (hd * 5 if hd > 3 else 0),  # rough OSE XP
    }


# ─── NPC Generation ───────────────────────────────────────────────────────────

def generate_npc(role: str, importance: str = "minor", level: int = None,
                 faction: str = None, concept: str = None, gm_secret: str = None) -> dict:
    """Generate a complete NPC."""
    
    # Name generation (simple placeholder system)
    first_names = ["Aldric", "Bramwell", "Cressida", "Dorrin", "Elspeth",
                   "Finnegan", "Gritha", "Holt", "Ingrid", "Jaspeth",
                   "Kaela", "Lorn", "Marta", "Nold", "Oswin", "Petra",
                   "Querin", "Rook", "Sybil", "Thatch", "Ursula", "Varn",
                   "Wilda", "Xander", "Ysolde", "Zurn"]
    last_names = ["Ashwood", "Brackenmoor", "Coldwell", "Dunmore", "Fernhollow",
                  "Grimthorn", "Holloway", "Ironkeep", "Jarrow", "Kettlemist",
                  "Longmarsh", "Mossbrook", "Nightfen", "Oldwick", "Pinehurst",
                  "Quicksilver", "Ravenwood", "Silverstream", "Thorngate", "Underhill"]
    
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # Stats
    hd_range = HD_BY_IMPORTANCE.get(importance, (1, 1))
    stats = generate_ose_stats(hd_range, role)
    
    # Personality
    personality = {
        "demeanor": random.choice(DEMEANORS),
        "quirk": random.choice(QUIRKS),
        "motivation": random.choice(MOTIVATIONS),
        "secret": gm_secret or random.choice(SECRETS),
        "appearance": random.choice(APPEARANCES),
    }
    
    # Alignment
    alignment = random.choices(ALIGNMENT_OPTIONS, weights=[3, 5, 2])[0]
    
    return {
        "name": name,
        "role": role,
        "importance": importance,
        "faction": faction,
        "concept": concept,
        "alignment": alignment,
        "stats": stats,
        "personality": personality,
    }


# ─── Output Formatting ────────────────────────────────────────────────────────

def format_quick(npc: dict) -> str:
    """Quick NPC block for live session use."""
    s = npc["stats"]
    p = npc["personality"]
    
    lines = [
        f"**{npc['name']}** – {npc['role']}",
        f"Looks: {p['appearance']}",
        f"Manner: {p['demeanor']}. {p['quirk']}.",
        f"Wants: {p['motivation']}",
        f"Knows: {p['secret']}",
        f"Stats: AC {s['ac_ascending']} (desc {s['ac_descending']})  HD {s['hd']}  HP {s['hp']}  Morale {s['morale']}",
    ]
    if npc.get("faction"):
        lines.insert(1, f"Faction: {npc['faction']}")
    
    return "\n".join(lines)


def format_full_markdown(npc: dict, include_gm_notes: bool = True) -> str:
    """Full Obsidian-ready Markdown NPC file."""
    s = npc["stats"]
    p = npc["personality"]
    date = datetime.now().strftime("%Y-%m-%d")
    slug = npc['name'].lower().replace(' ', '_')
    
    saves = s['saves']
    
    doc = f"""---
tags: [npc, {npc['importance']}, {npc.get('faction', 'no-faction').lower().replace(' ', '-')}]
name: {npc['name']}
role: {npc['role']}
importance: {npc['importance']}
faction: {npc.get('faction', 'None')}
alignment: {npc['alignment']}
status: alive
created: {date}
---

# {npc['name']}
**Role:** {npc['role']}
**Importance:** {npc['importance']} | **Alignment:** {npc['alignment']}
{"**Faction:** " + npc['faction'] if npc.get('faction') else ""}

---

## Stat Block

| Stat | Value |
|------|-------|
| **HD** | {s['hd']} |
| **HP** | {s['hp']} |
| **AC (Ascending)** | {s['ac_ascending']} |
| **AC (Descending)** | {s['ac_descending']} |
| **Attack Bonus** | +{s['attack_bonus']} |
| **Morale** | {s['morale']} |
| **XP** | {s['xp']} |

**Saving Throws**

| Death/Poison | Wands | Paralysis/Stone | Breath | Spells |
|-------------|-------|----------------|--------|--------|
| {saves['death_poison']} | {saves['wands']} | {saves['paralysis_stone']} | {saves['breath']} | {saves['spells']} |

---

## Personality

**Appearance:** {p['appearance']}

**Demeanor:** {p['demeanor']}

**Speech quirk:** {p['quirk']}

**Motivation:** {p['motivation']}

---

## Equipment

*[Fill in – weapons, armor, notable items]*

---

## Background

*[Fill in – how they came to be here, relevant history]*

---

## Connections

- **Faction:** {npc.get('faction', 'None')}
- **Knows:** *[Link to related NPCs]*
- **Location:** *[Where they're usually found]*
"""
    
    if include_gm_notes:
        doc += f"""
---

## GM Notes (remove for player handout)

> **Secret:** {p['secret']}
>
> **Plot hook:** *[How this NPC connects to the campaign's threads]*
>
> **If threatened:** *[What do they do? Fight, flee, bargain?]*
"""
    
    return doc


def save_npc(npc: dict, campaign: str):
    """Save NPC to campaign vault."""
    npc_dir = CAMPAIGN_DIR / campaign / "npcs"
    npc_dir.mkdir(parents=True, exist_ok=True)
    
    slug = npc['name'].lower().replace(' ', '_')
    
    # GM version
    gm_path = npc_dir / f"{slug}_gm.md"
    gm_path.write_text(format_full_markdown(npc, include_gm_notes=True), encoding="utf-8")
    
    # Player version
    player_path = npc_dir / f"{slug}_player.md"
    player_path.write_text(format_full_markdown(npc, include_gm_notes=False), encoding="utf-8")
    
    return gm_path, player_path


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="NPC generator for OSE/Dolmenwood")
    parser.add_argument("--role", "-r", default="townsperson", help="NPC role/occupation")
    parser.add_argument("--importance", "-i", default="minor",
                        choices=["minor", "major", "boss"])
    parser.add_argument("--faction", "-f", help="Faction affiliation")
    parser.add_argument("--concept", help="Flavour concept")
    parser.add_argument("--secret", help="GM secret override")
    parser.add_argument("--quick", "-q", action="store_true", help="Quick output only (live session)")
    parser.add_argument("--save", "-s", action="store_true", help="Save to campaign vault")
    parser.add_argument("--campaign", default="dolmenwood")
    
    args = parser.parse_args()
    
    npc = generate_npc(
        role=args.role,
        importance=args.importance,
        faction=args.faction,
        concept=args.concept,
        gm_secret=args.secret,
    )
    
    if args.quick:
        print(format_quick(npc))
    else:
        print(format_full_markdown(npc))
    
    if args.save:
        gm_path, player_path = save_npc(npc, args.campaign)
        print(f"\n✓ Saved: {gm_path}")
        print(f"✓ Saved: {player_path}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
