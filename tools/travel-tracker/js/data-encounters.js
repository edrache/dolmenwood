// ── ENCOUNTER TYPE TABLE (1d8) ──
// Source: Dolmenwood Campaign Book – Encounter Type table
// Columns: [Road/Track day, Wild day, Night (fire), Night (no fire)]
const ENC_TYPE_TABLE = [
  null,
  ["Animal",   "Animal",   "Monster", "Animal"],   // 1
  ["Monster",  "Monster",  "Monster", "Animal"],   // 2
  ["Mortal",   "Mortal",   "Mortal",  "Monster"],  // 3
  ["Mortal",   "Sentient", "Mortal",  "Monster"],  // 4
  ["Sentient", "Sentient", "Sentient","Regional"], // 5
  ["Sentient", "Regional", "Sentient","Regional"], // 6
  ["Regional", "Regional", "Regional","Regional"], // 7
  ["Regional", "Regional", "Regional","Regional"], // 8
];

// ── COMMON ENCOUNTER TABLES (d20) ──
// Source: Dolmenwood Campaign Book – Common Encounters
const ENC_COMMON = {
  Animal: [null,
    "Bat, Giant* (1d10)","Bear* (1d4)","Boar* (1d6)","Burrowing Beetle* (2d4)",
    "Carrion Worm* (1d3)","Centipede, Giant* (1d8)","False Unicorn (3d4)",
    "Fire Beetle, Giant* (2d6)","Fly, Giant* (2d6)","Insect Swarm* (1d3)",
    "Rapacious Beetle* (2d4)","Rat, Giant—Snail, Giant—Mutant (1d3)",
    "Red Deer (3d10)","Shaggy Mammoth* (2d8)","Snake—Adder* (1d8)",
    "Stirge* (2d6)","Toad, Giant* (1d4)","Weasel, Giant* (1d6)",
    "Wolf* (3d6)","Yegril* (3d8)"
  ],
  Monster: [null,
    "Ant, Giant* (3d4)","Centaur—Bestial (1)","Cockatrice (1d4)","Ghoul (2d4)",
    "Griffon* (2d8)","Headless Rider (1d4)","Mogglewump (1)","Mugwudge (1d4)",
    "Ogre (1d6)","Owlbear* (1d4)","Root Thing (1d4)","Spinning Spider, Giant—Mutant (1d3)",
    "Stirge* (2d6)","Treowere (1d8)","Werewolf (1d6)","Wolf, Dire* (2d4)",
    "Wyrm—Black Bile (1)","Wyrm—Blood (1)","Wyrm—Yellow Bile (1)","Yickerwill (1d6)"
  ],
  Mortal: [null,
    "Adventuring Party (2d6)","Breggle—Shorthorn (3d10)","Crookhorn (3d10)","Drune—Cottager (1d4)",
    "Fighter† (2d6)","Fortune-Teller† (1d3)","Friar† (1d6)","Hunter† (3d6)",
    "Knight† (2d6)","Lost Soul† (1d4)","Magician† (1d4)","Merchant† (1d20)",
    "Pedlar† (1d4)","Pilgrim† (4d8)","Priest† (1d6)","Thief (Bandit)† (3d10)",
    "Thief (Bandit)† (3d10)","Troll (1d3)","Villager† (2d10)","Witch Owl (1d6)"
  ],
  Sentient: [null,
    "Barrowbogey (2d6)","Breggle—Shorthorn (3d10)","Cleric† (1d20)","Deorling—Stag (1d6)",
    "Elf—Courtier or Knight (1d4)","Elf—Wanderer (1d6)","Goblin (2d6)","Goblin (2d6)",
    "Mossling (2d8)","Nutcap (2d6)","Redcap (2d6)","Scarecrow (1d4)",
    "Scrabey (1d6)","Shape-Stealer (1d6)","Sprite (3d6)","Talking Animal (1d4)",
    "Treowere (1d8)","Troll (1d3)","Wodewose (1d6)","Woodgrue (3d6)"
  ]
};

// ── REGIONAL ENCOUNTER TABLES (d20) ──
// Source: Dolmenwood Campaign Book – Regional Encounters
// Key = region name (matches HEXES[id].r, or partial match)
const ENC_REGIONAL = {
  "Aldweald": [null,
    "Antler Wraith (2d4)","Breggle—Shorthorn (3d10)","Centaur—Sylvan (2d6)","Deorling—Doe (4d4)",
    "Elf—Wanderer (1d6)","Fly, Giant* (2d6)","Fairy Horse (1)","Gelatinous Hulk (1d4)",
    "Gloam (1)","Goblin (2d6)","Grimalkin (1d12)","Madtom (1d12)",
    "Mugwudge (1d4)","Pedlar† (1d4)","Redcap (2d6)","Sprite (3d6)",
    "Thief (Pirate)† (3d10)","Wild Hunt (see p355)","Witch (1d6)","Woodgrue (3d6)"
  ],
  "Aquatic": [null,
    "Adventuring Party","Angler† (2d4)","Boggin (1d6)","Catfish, Giant* (1d2)",
    "Eel—Wanderer (1d6)","Fly, Giant* (2d6)","Insect Swarm* (1d3)","Kelpie (1)",
    "Killer Bee* (2d6)","Knight, Giant* (1d4)","Merchant† (1d20)","Merfolk (1d4)",
    "Pedlar† (1d4)","Pike, Giant* (1d4)","Stirge* (2d6)","Thief (Pirate)† (3d10)",
    "Unicorn—Blessed (1d6)","Toad, Giant* (1d4)","Water Termite, Giant* (1d3)","Wyrm—Phlegm (1)"
  ],
  "Dwelmfurgh": [null,
    "Antler Wraith (2d4)","Basilisk (1d6)","Brambling (1d4)","Centipede, Giant* (1d8)",
    "Deorling—Doe (4d4)","Drune—Audrune (1)","Drune—Braithmaid (1d4)","Drune—Cottager (2d6)",
    "Drune—Drunewife (1)","Lost Soul† (1d4)","Madtom (1d12)","Shadow (1d8)",
    "Skeleton (3d6)","Spinning Spider, Giant* (1d3)","Thief (Bandit)† (3d10)","Wicker Giant (1)",
    "Wight (1d6)","Witch (1d6)","Wyrm—Yellow Bile (1)","Woodgrue (3d6)"
  ],
  "Fever Marsh": [null,
    "Bat, Vampire* (1d10)","Black Tentacles (1d4)","Bog Salamander (1d3)","Centaur—Bestial (1)",
    "Fly, Giant* (2d6)","Fly, Giant* (2d6)","Galosher (2d6)","Gelatinous Hulk (1d4)",
    "Harridan (1d3)","Insect Swarm* (1d3)","Leech, Giant* (1d4)","Madtom (1d12)",
    "Marsh Lantern (1d12)","Mugwudge (1d4)","Redcap (2d6)","Shadow (1d8)",
    "Toad, Giant* (1d4)","Troll (1d3)","Wyrm—Phlegm (1)","Wyrm—Phlegm (1)"
  ],
  "Hag's Addle": [null,
    "Banshee (1)","Bat, Vampire* (1d10)","Black Tentacles (1d4)","Bog Corpse (2d4)",
    "Bog Salamander (1d3)","Boggy Forest (2d6)","Cleric† (1d20)","Drune—Braithmaid (1d4)",
    "Ghoul (2d4)","Leech, Giant* (1d4)","Marsh Lantern (1d12)","Mugwudge (1d4)",
    "Shadow (1d8)","Swamp Spider, Giant* (1d3)","Swamp Sloth* (1d6)","The Hag (see p82)",
    "Toad, Giant* (1d4)","Troll (1d4)","Unicorn—Corrupt (1d6)","Wronguncle (1)"
  ],
  "High Wold": [null,
    "Barrowbogey (2d6)","Breggle—Longhorn (2d4)","Breggle—Shorthorn (3d10)","Breggle—Shorthorn (3d10)",
    "Criert (1d6)","Criert (1d6)","Drune—Braithmaid (1d4)","Elf—Knight (1d4)",
    "Goblin (2d6)","Grimalkin (1d4)","Merchant† (1d20)","Priest† (1d6)",
    "Shadow (1d8)","Swamp Spider, Giant* (1d3)","Treowere (1d8)","Scrabey (1d6)",
    "Thief (Bandit)† (3d10)","Redslob (1d4)","Witch Owl (1d6)","Woodgrue (3d6)"
  ],
  "Mulchgrove": [null,
    "Bat, Vampire* (1d10)","Bog Corpse (2d4)","Bog Salamander (1d3)","Braincork (1d8)",
    "Criert (1d6)","Gelatinous Hulk (1d4)","Lost Soul† (1d4)","Mossling (2d8)",
    "Mossling (2d8)","Mossling (4d8)","Mould Oracle (1d3)","Ochre Slime-Hulk (1)",
    "Onyx Blob (1)","Pook Morel (2d10)","Pook Morel (2d10)","Redslob (1d4)",
    "Redslob (1d4)","Unicorn—Corrupt (1d6)","Wodewose (1d6)","Wronguncle (1)"
  ],
  "Nagwood": [null,
    "Atanuwf (see p45)","Bat, Vampire* (1d10)","Bog Corpse (2d4)","Centaur—Bestial (1)",
    "Crookhorn (3d10)","Crookhorn (3d10)","Crookhorn (3d10)","Crookhorn (6d10)",
    "Harridan (1d3)","Harridan (1d3)","Manticore (1d4)","Ochre Slime-Hulk (1)",
    "Ogre (1d6)","Ogre (1d6)","Owlbear* (1d4)","Redslob (1d4)",
    "Snail, Giant—Mutant (1d3)","Spinning Spider, Giant (1d4)","Treowere (Chaotic) (1d8)","Wyrm—Black Bile (1)"
  ],
  "Northern Scratch": [null,
    "Banshee (1)","Crookhorn (3d10)","Black Tentacles (1d4)","Deorling—Doe (4d4)",
    "Bog Corpse (2d4)","Fly, Giant* (2d6)","Fomorian (1d3)","Gloam (1)",
    "Gloam (1)","Harridan (1d4)","Leech, Giant* (1d4)","Madtom (1d12)",
    "Marsh Lantern (1d12)","Shadow (1d8)","Spectre (1d4)","Scarecrow (1d4)",
    "Shadow (1d8)","Spectre (1d4)","Wight (1d6)","Witch Owl (1d6)"
  ],
  "Table Downs": [null,
    "Banshee (1)","Crookhorn (3d10)","Deorling—Doe (4d4)","Elf—Wanderer (1d6)",
    "Fighter† (2d6)","Friar† (1d6)","Gloam (1)","Ghoul (1d4)",
    "Gloam (1)","Headless Rider (1d4)","Killer Bee* (2d6)","Lost Soul† (1d4)",
    "Mossling (2d8)","Merchant† (1d20)","Pook Morel (2d10)","Scrabey (1d6)",
    "Skeleton (3d6)","Wight (1d6)","Villager† (2d10)","Woodgrue (3d6)"
  ],
  "Tithelands": [null,
    "Breggle—Shorthorn (3d10)","Cobbin (1d4)","Cobbin (1d4)","Cobbin (1d4)",
    "Crookhorn (3d10)","Crookhorn (3d10)","Gloam (1)","Goblin (2d6)",
    "Goblin (2d6)","Grimalkin (1d4)","Knight† (2d6)","Merchant† (1d20)",
    "Mossling (2d8)","Ogre (1d6)","Owlbear* (1d4)","Scrabey (1d6)",
    "Sprite (3d6)","Sprite (3d6)","Troll (1d3)","Woodgrue (3d6)"
  ],
  "Valley of Wise Beasts": [null,
    "Cobbin (1d4)","Cobbin (1d4)","Cobbin (1d4)","Cobbin (3d8)",
    "Crookhorn (3d10)","Goblin (2d6)","Goblin (2d6)","Grimalkin (1d4)",
    "Grimalkin (1d4)","Knight† (2d6)","Lost Soul† (1d4)","Mossling (2d8)",
    "Merchant† (1d20)","Ogre (1d6)","Owlbear* (1d4)","Scrabey (1d6)",
    "Deorling—Stag (1d6)","Grimalkin (1d4)","Unicorn—Corrupt (1d6)","Woodgrue (3d6)"
  ]
};
