// Dolmenwood Encounter Tables
// Sourced from travel-tracker data + Dolmenwood rulebook

// Encounter type determination (1d8)
// Columns: [road/track day, wilderness day, night+fire, night no fire]
const ENC_TYPE_TABLE = [
  null,
  ['Animal',   'Animal',   'Monster',  'Animal'],
  ['Monster',  'Monster',  'Monster',  'Animal'],
  ['Mortal',   'Mortal',   'Mortal',   'Monster'],
  ['Mortal',   'Sentient', 'Mortal',   'Monster'],
  ['Sentient', 'Sentient', 'Sentient', 'Regional'],
  ['Sentient', 'Regional', 'Sentient', 'Regional'],
  ['Regional', 'Regional', 'Regional', 'Regional'],
  ['Regional', 'Regional', 'Regional', 'Regional'],
];

// Common encounter tables (1d20)
const ENC_COMMON = {
  Animal: [
    null,
    'Bat, Giant (1d10)', 'Bear (1d4)', 'Boar (1d6)', 'Boar, Giant (1d4)',
    'Cat, Wild (1d4)', 'Cockatrice (1d6)', 'Deer (2d6)', 'Fox (1d6)',
    'Frog, Giant (1d6)', 'Horse, Wild (1d6)', 'Owl, Giant (1d4)',
    'Rat, Giant (3d6)', 'Snake, Giant (1d3)', 'Spider, Giant (1d3)',
    'Toad, Giant (1d6)', 'Weasel, Giant (1d4)', 'Wolf (2d6)',
    'Wolverine, Giant (1d4)', 'Wyrm, Wood (1d3)', 'Yegril (3d8)',
  ],
  Monster: [
    null,
    'Banshee (1)', 'Basilisk (1d3)', 'Black Pudding (1)', 'Chimera (1)',
    'Dragon (1)', 'Gelatinous Cube (1)', 'Ghoul (1d6)', 'Harpy (1d6)',
    'Hell Hound (2d4)', 'Hobgoblin (2d6)', 'Hydra (1)', 'Imp (1d4)',
    'Manticore (1)', 'Medusa (1)', 'Minotaur (1d6)', 'Ogre (1d6)',
    'Owlbear (1d4)', 'Troll (1d4)', 'Wight (1d6)', 'Wraith (1d4)',
  ],
  Mortal: [
    null,
    'Bandit (2d4)', 'Bandit (2d4)', 'Brigand (1d6)', 'Charcoal Burner (1d4)',
    'Drune cultist (1d4)', 'Forester (1d4)', 'Hermit (1)', 'Hunter (1d4)',
    'Merchant (1d4+guards)', 'Mercenary (2d6)', 'Minstrel (1d3)',
    'Noble & retinue (1)', 'Peasant (2d6)', 'Pilgrim (2d4)', 'Poacher (1d4)',
    'Refugee (2d4)', 'Soldier, patrol (1d6)', 'Tax collector (1d3+guards)',
    'Tinker (1)', 'Witch (1)',
  ],
  Sentient: [
    null,
    'Breggle, Longhorn (1d6)', 'Breggle, Shorthorn (2d6)', 'Dryad (1d4)',
    'Elf (1d6)', 'Fairy (2d4)', 'Grimalkin (1d3)', 'Hollow (1)',
    'Moss Dwarf (1d6)', 'Moss Dwarf Elder (1)', 'Murkling (2d6)',
    'Pook (1d4)', 'Satyr (1d6)', 'Spriggan (1d4)', 'Stick-man (1d6)',
    'Talking Animal—Badger (1)', 'Talking Animal—Fox (1)',
    'Talking Animal—Raven (1d3)', 'Talking Animal—Stag (1)',
    'Woldwight (1d4)', 'Wood Gnome (2d4)',
  ],
};

// Regional encounter tables by hex region (1d20)
const ENC_REGIONAL = {
  'Aldweald': [
    null,
    'Antler Wraith (2d4)', 'Breggle—Shorthorn (3d10)', 'Dryad (1d6)',
    'Elf (1d4)', 'Feral Woodgrue (1d6)', 'Hollow (1d3)',
    'Leshy (1d4)', 'Moss Dwarf (2d6)', 'Murkling (3d6)',
    'Pook (1d6)', 'Quickwood (1)', 'Satyr (2d4)',
    'Spriggan (1d6)', 'Stick-man (2d6)', 'Treant (1)',
    'Unicorn (1)', 'Woldwight (1d6)', 'Wood Gnome (2d6)',
    'Woodgrue (3d6)', 'Wraith, Antler (1)',
  ],
  'Brackenwold': [
    null,
    'Bat, Giant (2d6)', 'Black Pudding (1)', 'Breggle—Shorthorn (2d6)',
    'Crocodile, Giant (1d3)', 'Frog, Giant (2d6)', 'Ghoul (2d4)',
    'Giant Leech (1d6)', 'Harpy (1d4)', 'Hollow (1d3)',
    'Hydra (1)', 'Lizard, Giant (1d6)', 'Merrow (1d4)',
    'Murkling (2d6)', 'Pook (1d4)', 'Rat, Giant (4d6)',
    'Slug, Giant (1d3)', 'Snake, Giant (1d4)', 'Toad, Giant (2d4)',
    'Will-o-Wisp (1d3)', 'Zombie (2d6)',
  ],
  'Wychwood': [
    null,
    'Breggle—Longhorn (1d6)', 'Demon, Wood (1)', 'Dryad (1d3)',
    'Elf (1d4)', 'Gnoll (2d6)', 'Hag (1)', 'Harpy (1d4)',
    'Hollow (1d3)', 'Imp (1d6)', 'Manticore (1)',
    'Medusa (1)', 'Night-gaunt (1d4)', 'Ogre (1d4)',
    'Pook (1d6)', 'Shadow (1d4)', 'Spectre (1d3)',
    'Stick-man (1d6)', 'Troll (1d3)', 'Wight (2d4)',
    'Woodgrue, Feral (2d6)',
  ],
  'Nagwood': [
    null,
    'Elf (1d6)', 'Fairy (2d6)', 'Gnome, Wood (2d6)',
    'Grimalkin (1d4)', 'Hollow (1d3)', 'Leprechaun (1d3)',
    'Moss Dwarf (1d6)', 'Murkling (2d6)', 'Night-gaunt (1d3)',
    'Nixie (2d6)', 'Pixie (2d6)', 'Pook (1d6)',
    'Quickwood (1)', 'Satyr (1d6)', 'Sprite (3d6)',
    'Stick-man (1d4)', 'Treant (1)', 'Unicorn (1)',
    'Will-o-Wisp (1d3)', 'Woodgrue (2d6)',
  ],
};

const REGIONS = Object.keys(ENC_REGIONAL);

// Reaction table (2d6)
const REACTION_TABLE = {
  2:  { text: 'Hostile — attacks immediately', hostile: true },
  3:  { text: 'Hostile — attacks immediately', hostile: true },
  4:  { text: 'Unfriendly — may attack',       hostile: false },
  5:  { text: 'Unfriendly — may attack',       hostile: false },
  6:  { text: 'Neutral — uncertain',           hostile: false },
  7:  { text: 'Neutral — uncertain',           hostile: false },
  8:  { text: 'Neutral — uncertain',           hostile: false },
  9:  { text: 'Indifferent — not interested',  hostile: false },
  10: { text: 'Indifferent — not interested',  hostile: false },
  11: { text: 'Friendly — open to talk',       hostile: false },
  12: { text: 'Friendly — open to talk',       hostile: false },
};

// Activity table (1d20)
const ACTIVITY_TABLE = [
  null,
  'Foraging / feeding', 'Sleeping / resting', 'Moving purposefully',
  'Playing / at ease', 'Guarding territory', 'Hunting another creature',
  'Fleeing something', 'Investigating a smell / sound', 'Wounded, wary',
  'At a lair entrance', 'Carrying prey', 'Meeting / gathering',
  'Performing a ritual', 'Setting an ambush', 'Searching for something',
  'Lost / confused', 'Fighting each other', 'Resting after a meal',
  'Scouting the area', 'Summoned / bound (may trigger 2nd encounter)',
];

function rollEncounter(context, region) {
  // context: 'road', 'wild', 'night_fire', 'night_no_fire'
  const colMap = { road: 0, wild: 1, night_fire: 2, night_no_fire: 3 };
  const col = colMap[context] ?? 1;

  const typeRoll = Math.ceil(Math.random() * 8);
  const encType = ENC_TYPE_TABLE[typeRoll][col];

  let creatureRoll = Math.ceil(Math.random() * 20);
  let creature;
  if (encType === 'Regional') {
    const regionKey = REGIONS.find(r => (region || '').includes(r)) || REGIONS[0];
    creature = ENC_REGIONAL[regionKey][creatureRoll];
  } else {
    creature = ENC_COMMON[encType][creatureRoll];
  }

  const surpriseRoll = Math.ceil(Math.random() * 6);
  const partySurprised = surpriseRoll <= 2;

  const distD1 = Math.ceil(Math.random() * 6);
  const distD2 = Math.ceil(Math.random() * 6);

  const reactionD1 = Math.ceil(Math.random() * 6);
  const reactionD2 = Math.ceil(Math.random() * 6);
  const reactionTotal = reactionD1 + reactionD2;
  const reaction = REACTION_TABLE[reactionTotal];

  const activityRoll = Math.ceil(Math.random() * 20);
  const activity = ACTIVITY_TABLE[activityRoll];

  return {
    typeRoll, encType, creatureRoll, creature,
    surpriseRoll, partySurprised,
    distD1, distD2, distFt: (distD1 + distD2) * 30,
    reactionD1, reactionD2, reactionTotal, reaction,
    activityRoll, activity,
  };
}
