#!/usr/bin/env python3
"""
roll.py – Dice roller and random table picker for RPG GM Assistant.
Usage:
    python roll.py 3d6
    python roll.py 2d8+4
    python roll.py --table personality
    python roll.py --table dolmenwood_encounter --context forest --levels 1-3
"""

import argparse
import random
import re
import json
import sys
from pathlib import Path

# ─── Built-in Tables ──────────────────────────────────────────────────────────

TABLES = {
    "personality_demeanor": [
        "Gruff and suspicious",
        "Jovial and generous",
        "Nervous and evasive",
        "Calculating and patient",
        "Melancholic and distant",
        "Fanatical and intense",
        "Cheerful and oblivious",
        "Bitter and resentful",
        "Proud and condescending",
        "Humble and self-deprecating",
        "Paranoid and watchful",
        "Serene and unflappable",
    ],
    "personality_quirk": [
        "Repeats the last word they say, word",
        "Speaks entirely in old proverbs",
        "Over-explains obvious things",
        "Whispers even in empty rooms",
        "Touches their face when lying",
        "Laughs at inappropriate moments",
        "Refers to themselves in third person",
        "Finishes others' sentences, wrongly",
        "Never makes eye contact",
        "Asks questions but doesn't wait for answers",
        "Constantly fidgets with a trinket",
        "Addresses everyone by wrong name",
    ],
    "personality_motivation": [
        "Survival at any cost",
        "Accumulating wealth",
        "Fulfilling a duty or oath",
        "Seeking revenge",
        "Satisfying curiosity",
        "Religious devotion",
        "Protecting someone specific",
        "Proving themselves to someone",
        "Finding a lost thing",
        "Escaping their past",
        "Building something lasting",
        "Pure, uncomplicated hedonism",
    ],
    "personality_secret": [
        "Knows the location of something dangerous",
        "Is not who they claim to be",
        "Owes a life-debt to a powerful figure",
        "Has done something unforgivable",
        "Is being blackmailed",
        "Secretly works for a different faction",
        "Has a hidden family",
        "Is dying and doesn't want anyone to know",
        "Stole something from the party's allies",
        "Witnessed something they can't speak of",
        "Has powers they're hiding",
        "Is in love with someone inappropriate",
    ],
    "npc_role": [
        "Innkeeper with too many opinions",
        "Traveling merchant hiding cargo",
        "Disgraced former knight",
        "Hedge witch looking for apprentice",
        "Pilgrim on a questionable mission",
        "Bounty hunter, wrong target",
        "Escaped servant of a noble",
        "Wandering friar of dubious order",
        "Stranded foreign sailor",
        "Local guide who's never left town",
        "Retired adventurer with a warning",
        "Child with an unusual secret",
    ],
    "dolmenwood_encounter_forest": [
        "1d4 Goatmen scouts, watching from trees",
        "Wandering Drune cultist (roll reaction)",
        "Pack of 2d4 hungry wolves, led by an unnaturally large one",
        "Fairy ring – stepping in teleports to random forest hex",
        "1d6 Woodgrues, gleefully malicious",
        "Lost pilgrim on the wrong road",
        "Ancient standing stone with fresh offerings",
        "1d3 Mossmungers grazing, startle easily",
        "Traveling Brackenwold merchant with strange wares",
        "Hollow tree with something inside",
        "1d4 Crabmen emerging from stream",
        "A Dryad watching, curious (reaction roll)",
    ],
    "dolmenwood_encounter_road": [
        "1d6 bandits posing as merchants",
        "Knight of Brackenwold, tax collecting",
        "Friar of St. Brigid, genuinely helpful",
        "Merchant caravan, one cart's cargo is screaming",
        "2d4 soldiers looking for a deserter",
        "Travelling fair – performers with unsettling acts",
        "Lone rider, dead, still in saddle (horse knows the way home)",
        "Tollbooth manned by a very tall 'human'",
        "1d4 pilgrims fleeing a 'terrible beast'",
        "Roadside shrine with recent bloody offering",
        "Broken cart, owner nowhere to be found",
        "A child, alone, not afraid, going somewhere specific",
    ],
    "dolmenwood_rumor": [
        "The old mill is haunted – but only at harvest time",
        "A noble's daughter vanished near the Hollow Hills",
        "The Drune are looking for something the party has",
        "An ancient map is hidden in the church crypt",
        "Someone is paying triple value for Fairy silver",
        "A well in the next village gives visions",
        "The local lord owes the Fairy Court a debt",
        "A witch offers wishes – she always collects",
        "Something is eating the livestock, working east to west",
        "There is a path that only appears at midnight",
        "A band of knights vanished in the deep wood last winter",
        "The old king's treasury was never found",
    ],
    "starting_equipment_fighter": [
        "Sword, shield, leather armor, 3d6 gp",
        "Two-handed sword, chainmail, 1d6 gp",
        "Spear, shield, leather armor, bow, quiver (20 arrows), 2d6 gp",
        "Battle axe, leather armor, 3 oil flasks, 2d6 gp",
        "Sword, crossbow, 30 bolts, leather armor, 2d6 gp",
        "Pole arm, chainmail, 1d6 gp",
    ],
    "starting_equipment_thief": [
        "Short sword, leather armor, thieves' tools, 3d6 gp",
        "Dagger ×2, leather armor, 50' rope, 3d6 gp",
        "Short sword, sling, 20 stones, leather armor, 2d6 gp",
        "Crossbow, 20 bolts, leather armor, thieves' tools, 2d6 gp",
    ],
    "starting_equipment_magic_user": [
        "Staff, dagger, spellbook, 2d6 gp",
        "Dagger ×2, spellbook, scroll (random level 1 spell), 3d6 gp",
        "Staff, spellbook, 6 torches, 1d6 gp",
    ],
    "starting_equipment_cleric": [
        "Mace, shield, chainmail, holy symbol, 2d6 gp",
        "War hammer, chainmail, holy symbol, 3d6 gp",
        "Mace, leather armor, holy symbol, 3 flasks holy water, 2d6 gp",
    ],
}


# ─── Dice Rolling ─────────────────────────────────────────────────────────────

def parse_and_roll(expression: str) -> dict:
    """Parse dice expression like '3d6', '2d8+4', 'd20', '4d6dl1' (drop lowest)."""
    expression = expression.strip().lower()
    
    # Handle 4d6 drop lowest
    dl_match = re.match(r'^(\d+)d(\d+)dl(\d+)$', expression)
    if dl_match:
        n, sides, drop = int(dl_match.group(1)), int(dl_match.group(2)), int(dl_match.group(3))
        rolls = [random.randint(1, sides) for _ in range(n)]
        sorted_rolls = sorted(rolls)
        dropped = sorted_rolls[:drop]
        kept = sorted_rolls[drop:]
        total = sum(kept)
        return {
            "expression": expression,
            "rolls": rolls,
            "dropped": dropped,
            "kept": kept,
            "total": total,
            "note": f"Dropped lowest {drop}: {dropped}"
        }
    
    # Handle standard XdY+Z
    match = re.match(r'^(\d*)d(\d+)([+-]\d+)?$', expression)
    if not match:
        return {"error": f"Cannot parse dice expression: '{expression}'"}
    
    n_str, sides_str, mod_str = match.groups()
    n = int(n_str) if n_str else 1
    sides = int(sides_str)
    mod = int(mod_str) if mod_str else 0
    
    if n < 1 or n > 100:
        return {"error": "Number of dice must be between 1 and 100"}
    if sides < 2 or sides > 1000:
        return {"error": "Sides must be between 2 and 1000"}
    
    rolls = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + mod
    
    result = {
        "expression": expression,
        "rolls": rolls,
        "total": total,
    }
    if mod:
        result["modifier"] = mod
        result["subtotal"] = sum(rolls)
    
    return result


def roll_ability_scores(method: str = "3d6") -> dict:
    """Roll 6 ability scores. Methods: 3d6, 3d6_drop, 4d6_drop"""
    stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    results = {}
    
    for stat in stats:
        if method == "4d6_drop":
            roll_result = parse_and_roll("4d6dl1")
            results[stat] = roll_result["total"]
        elif method == "3d6_drop":
            rolls = sorted([random.randint(1, 6) for _ in range(3)])
            results[stat] = sum(rolls[1:])  # drop lowest
        else:  # 3d6 straight
            results[stat] = parse_and_roll("3d6")["total"]
    
    return results


def modifier(score: int) -> str:
    """OSE ability score modifier."""
    table = {
        3: -3, 4: -2, 5: -2, 6: -1, 7: -1, 8: -1,
        9: 0, 10: 0, 11: 0, 12: 0,
        13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 3
    }
    mod = table.get(score, 0)
    return f"+{mod}" if mod >= 0 else str(mod)


# ─── Table Rolling ────────────────────────────────────────────────────────────

def roll_on_table(table_name: str, tables_dir: Path = None) -> dict:
    """Roll on a named table. Checks built-in tables, then campaign tables dir."""
    
    # Check built-in tables
    if table_name in TABLES:
        table = TABLES[table_name]
        idx = random.randint(0, len(table) - 1)
        return {
            "table": table_name,
            "roll": idx + 1,
            "total_entries": len(table),
            "result": table[idx],
            "source": "built-in"
        }
    
    # Check campaign tables directory
    if tables_dir:
        table_file = tables_dir / f"{table_name}.json"
        if table_file.exists():
            with open(table_file) as f:
                table = json.load(f)
            entries = table.get("entries", table)
            if isinstance(entries, list):
                idx = random.randint(0, len(entries) - 1)
                return {
                    "table": table_name,
                    "roll": idx + 1,
                    "total_entries": len(entries),
                    "result": entries[idx],
                    "source": str(table_file)
                }
    
    # List available tables if not found
    available = list(TABLES.keys())
    if tables_dir:
        available += [f.stem for f in tables_dir.glob("*.json")]
    
    return {
        "error": f"Table '{table_name}' not found.",
        "available_tables": sorted(available)
    }


def roll_personality() -> dict:
    """Roll a complete personality: demeanor, quirk, motivation, secret."""
    return {
        "demeanor": roll_on_table("personality_demeanor")["result"],
        "quirk": roll_on_table("personality_quirk")["result"],
        "motivation": roll_on_table("personality_motivation")["result"],
        "secret": roll_on_table("personality_secret")["result"],
    }


# ─── CLI ──────────────────────────────────────────────────────────────────────

def format_roll_result(result: dict) -> str:
    if "error" in result:
        return f"ERROR: {result['error']}"
    
    parts = [f"🎲 {result['expression'].upper()}"]
    
    if len(result.get("rolls", [])) > 1:
        parts.append(f"  Rolls: {result['rolls']}")
    
    if "dropped" in result:
        parts.append(f"  Dropped: {result['dropped']}")
    if "modifier" in result:
        parts.append(f"  Subtotal: {result['subtotal']} + {result['modifier']}")
    
    parts.append(f"  ═══ Result: {result['total']} ═══")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="RPG dice roller and table picker")
    parser.add_argument("expression", nargs="?", help="Dice expression (e.g. 3d6, 2d8+4)")
    parser.add_argument("--table", "-t", help="Roll on a named table")
    parser.add_argument("--ability-scores", "-a", action="store_true", help="Roll 6 ability scores")
    parser.add_argument("--method", default="3d6", choices=["3d6", "3d6_drop", "4d6_drop"],
                        help="Ability score rolling method")
    parser.add_argument("--personality", "-p", action="store_true", help="Roll a full personality")
    parser.add_argument("--list-tables", action="store_true", help="List all available tables")
    parser.add_argument("--campaign", default="dolmenwood", help="Campaign name (for table lookup)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Set up campaign tables path
    script_dir = Path(__file__).parent.parent
    tables_dir = script_dir / "campaign" / args.campaign / "encounters" / "tables"
    
    # List tables
    if args.list_tables:
        print("Built-in tables:")
        for name in sorted(TABLES.keys()):
            print(f"  {name} ({len(TABLES[name])} entries)")
        if tables_dir.exists():
            print(f"\nCampaign tables ({args.campaign}):")
            for f in sorted(tables_dir.glob("*.json")):
                print(f"  {f.stem}")
        sys.exit(0)
    
    # Roll personality
    if args.personality:
        result = roll_personality()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("🎭 Personality Roll:")
            for key, val in result.items():
                print(f"  {key.capitalize()}: {val}")
        sys.exit(0)
    
    # Roll ability scores
    if args.ability_scores:
        scores = roll_ability_scores(args.method)
        if args.json:
            print(json.dumps(scores, indent=2))
        else:
            print(f"📊 Ability Scores ({args.method}):")
            for stat, score in scores.items():
                print(f"  {stat}: {score:2d} ({modifier(score)})")
        sys.exit(0)
    
    # Roll on table
    if args.table:
        result = roll_on_table(args.table, tables_dir)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if "error" in result:
                print(f"ERROR: {result['error']}")
                if "available_tables" in result:
                    print("Available tables:", ", ".join(result["available_tables"]))
            else:
                print(f"📋 Table: {result['table']} (d{result['total_entries']})")
                print(f"  Roll: {result['roll']}")
                print(f"  ═══ Result: {result['result']} ═══")
        sys.exit(0)
    
    # Roll dice expression
    if args.expression:
        result = parse_and_roll(args.expression)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_roll_result(result))
        sys.exit(0)
    
    parser.print_help()


if __name__ == "__main__":
    main()
