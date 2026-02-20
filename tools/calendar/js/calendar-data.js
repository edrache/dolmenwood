// Dolmenwood Calendar Data
// Days of the week: Colly, Chime, Hayme, Moot, Frisk, Eggfast, Sunning
// Each month: 4 weeks × 7 days = 28 regular days + Wysendays (special days at end)

const WEEKDAYS = ['Colly','Chime','Hayme','Moot','Frisk','Eggfast','Sunning'];

// Seasons: which months belong to which season (for weather rolling)
// winter: 1,2,3 | spring: 4,5,6 | summer: 7,8,9 | autumn: 10,11,12
const MONTH_SEASON = {
  1:'winter', 2:'winter', 3:'winter',
  4:'spring', 5:'spring', 6:'spring',
  7:'summer', 8:'summer', 9:'summer',
  10:'autumn', 11:'autumn', 12:'autumn'
};

// Moon phases per month: { day: 'new'|'full' }
// New moon ~day 4-5, Full moon ~day 18-19 (based on calendar)
const MOON_PHASES = {
  1:  { 4:'new',  19:'full' },
  2:  { 4:'new',  18:'full' },
  3:  { 5:'new',  20:'full' },
  4:  { 4:'new',  19:'full' },
  5:  { 5:'new',  19:'full' },
  6:  { 5:'new',  20:'full' },
  7:  { 4:'new',  19:'full' },
  8:  { 3:'new',  17:'full' },
  9:  { 3:'new',  18:'full' },
  10: { 4:'new',  19:'full' },
  11: { 4:'new',  19:'full' },
  12: { 5:'new',  19:'full' },
};

const MONTHS = [
  {
    num: 1, name: 'Grimvold', subtitle: 'The Onset of Winter',
    season: 'winter',
    color: '#2a3a5c',
    feasts: {
      1:  'Feast of St Vinicus',
      4:  'Feast of St Albert',
      5:  'Feast of St Offrid',
      9:  'Feast of St Choad',
      17: 'Feast of St Clyde',
      19: 'Winter Solstice · Feast of St Elsa',
      21: 'Feast of St Baldric',
      27: 'Feast of St Cantius',
    },
    wysendays: [
      { day: 29, name: 'Hanglemas', feast: 'Feast of St Joane' },
      { day: 30, name: "Dyboll's Day" },
    ],
    notes: '† End of Hitching (if begun, see 30th of Braghold)',
  },
  {
    num: 2, name: 'Lymewald', subtitle: 'Deep Winter',
    season: 'winter',
    color: '#1e2e4a',
    feasts: {
      1:  '† 1-in-10 chance of Vague',
      2:  'Feast of St Waylord',
      3:  'Feast of St Gondyw',
      8:  '† 1-in-10 chance of Vague',
      9:  'Feast of St Calafredus',
      15: '† 1-in-10 chance of Vague · Feast of St Wynne',
      19: 'Feast of St Albrith',
      22: '† 1-in-10 chance of Vague',
      23: 'Feast of St Fredulus',
      28: 'Feast of St Eggort',
    },
    wysendays: [],
    notes: '† 1-in-10 chance of a Vague beginning',
  },
  {
    num: 3, name: 'Haggryme', subtitle: 'The Fading of Winter',
    season: 'winter',
    color: '#2a3a5c',
    feasts: {
      5:  'Feast of St Clister',
      6:  'Feast of St Ponch',
      8:  '† 1-in-10 chance of Vague',
      11: 'Feast of St Flatius',
      12: 'Feast of St Quister',
      13: 'Feast of St Aeynid',
      15: '† 1-in-10 chance of Vague',
      18: 'Feast of St Visyg',
      22: '† 1-in-10 chance of Vague · Feast of St Pannard',
      23: 'Feast of St Simone',
      25: 'Feast of St Sortia',
      27: 'Feast of St Pastery',
      28: 'Feast of St Bethany',
    },
    wysendays: [
      { day: 29, name: "Yarl's Day", feast: 'Feast of St Tumbel' },
      { day: 30, name: 'The Day of Virgins', feast: 'Feast of St Lillibeth' },
    ],
    notes: '† 1-in-10 chance of a Vague beginning',
  },
  {
    num: 4, name: 'Symswald', subtitle: 'The Onset of Spring',
    season: 'spring',
    color: '#2d4a2a',
    feasts: {
      1:  'Feast of St Gwigh',
      2:  'The Feast of Cats',
      3:  'Feast of St Medigor',
      5:  'Feast of St Ingrid',
      7:  'Feast of St Neblit',
      8:  'Feast of St Dullard',
      10: 'Feast of St Whittery',
      12: 'Feast of St Pious',
      14: 'Feast of St Thorm',
      18: 'Feast of St Goodenough',
      20: 'Vernal Equinox',
    },
    wysendays: [
      { day: 29, name: 'Hopfast' },
    ],
    notes: '',
  },
  {
    num: 5, name: 'Harchment', subtitle: 'High Spring',
    season: 'spring',
    color: '#2d4a2a',
    feasts: {
      7:  'Feast of St Craven',
      9:  'Feast of St Rhilma',
      10: 'Feast of St Talambeth',
      16: 'Feast of St Jorrael',
      19: 'Feast of St Hoargrime',
      22: 'Feast of St Abthius',
      24: 'Feast of St Primace',
      26: 'Feast of St Knock',
    },
    wysendays: [
      { day: 29, name: 'Smithing', feast: 'Feast of St Wilbranch' },
    ],
    notes: '',
  },
  {
    num: 6, name: 'Iggwyld', subtitle: 'The Fading of Spring',
    season: 'spring',
    color: '#2d4a2a',
    feasts: {
      1:  '† 1-in-4 chance of Colliggwyld',
      3:  'Feast of St Gripe',
      9:  'Feast of St Puriphon',
      19: 'Feast of St Hildace',
      27: 'Feast of St Maternis',
      30: '‡ End of Colliggwyld · Feast of St Waylaine',
    },
    wysendays: [
      { day: 29, name: 'Shortening' },
      { day: 30, name: "Longshank's Day ‡", feast: 'Feast of St Waylaine' },
    ],
    notes: '† 1-in-4 chance of Colliggwyld beginning · ‡ End of Colliggwyld (if begun, see 1st of Iggwyld)',
  },
  {
    num: 7, name: 'Chysting', subtitle: 'The Onset of Summer',
    season: 'summer',
    color: '#4a3a10',
    feasts: {
      6:  'Feast of St Nuncy',
      10: 'Feast of St Apoplect',
      16: 'Feast of St Cornice',
      18: 'Summer Solstice',
      20: 'Feast of St Dougan',
      27: 'Feast of St Sabian',
      31: 'Feast of St Jubilant',
    },
    wysendays: [
      { day: 29, name: 'Bradging' },
      { day: 30, name: 'Copsewalow' },
      { day: 31, name: 'Chalice', feast: 'Feast of St Jubilant' },
    ],
    notes: '',
  },
  {
    num: 8, name: 'Lillipythe', subtitle: 'High Summer',
    season: 'summer',
    color: '#4a3a10',
    feasts: {
      4:  'Feast of St Foggarty',
      5:  'Feast of St Keye',
      9:  'Feast of St Primula',
      16: 'Feast of St Dillage',
      20: 'Feast of St Torphia',
      25: 'Feast of St Esther',
      27: 'Feast of St Philodeus',
      28: 'Feast of St Lummox',
    },
    wysendays: [
      { day: 29, name: "Old Dobey's Day", feast: 'Feast of St Capernott' },
    ],
    notes: '',
  },
  {
    num: 9, name: 'Haelhold', subtitle: 'The Fading of Summer',
    season: 'summer',
    color: '#4a3a10',
    feasts: {
      1:  '† 1-in-20 chance of Chame',
      2:  '† 1-in-20 chance of Chame',
      3:  '† 1-in-20 chance of Chame',
      4:  '† 1-in-20 chance of Chame',
      5:  '† 1-in-20 chance of Chame · Feast of St Willibart',
      8:  'Feast of St Sanguine',
      10: 'Feast of St Benester',
      15: 'Feast of St Faxis',
      25: 'Feast of St Gretchen',
      28: 'Feast of St Galaunt',
    },
    wysendays: [],
    notes: '† 1-in-20 chance of Chame beginning',
  },
  {
    num: 10, name: 'Reedwryme', subtitle: 'The Onset of Autumn',
    season: 'autumn',
    color: '#4a2a10',
    feasts: {
      1:  'Feast of St Dextre',
      3:  'Feast of St Wick',
      4:  'Feast of St Elephantine',
      8:  'Feast of St Moribund',
      13: 'Feast of St Loame',
      18: 'Feast of St Shank',
      19: 'Autumnal Equinox',
      21: 'Feast of St Hollyhock',
      22: 'Feast of St Egbert',
      25: 'Feast of St Clewyd',
      26: 'Feast of St Howarth',
      27: 'Feast of St Howdych',
    },
    wysendays: [
      { day: 29, name: "Shub's Eve", feast: 'Feast of St Signis' },
      { day: 30, name: 'Druden Day', feast: 'Festival of the Green Man' },
    ],
    notes: '',
  },
  {
    num: 11, name: 'Obthryme', subtitle: 'Deep Autumn',
    season: 'autumn',
    color: '#4a2a10',
    feasts: {
      7:  'Feast of St Horace',
      9:  'Feast of St Hamfast',
      13: 'Feast of St Woad',
      22: 'Feast of St Hodwich',
      24: 'Feast of St Wort',
      27: 'Feast of St Godfrey',
      28: 'Feast of St Dank',
    },
    wysendays: [],
    notes: '',
  },
  {
    num: 12, name: 'Braghold', subtitle: 'The Fading of Autumn',
    season: 'autumn',
    color: '#4a2a10',
    feasts: {
      9:  'Feast of St Poltry',
      10: 'Feast of St Sedge',
      15: 'Feast of St Clyve',
      21: 'Feast of St Gawain',
      25: 'Feast of St Thridgold',
      28: 'Feast of St Therese',
      30: '† 1-in-4 chance of Hitching · The Hunting of the Winter Hart · Feast of St Willoffrith',
    },
    wysendays: [
      { day: 29, name: 'The Day of Doors', feast: 'Feast of St Habicus' },
      { day: 30, name: 'Dolmenday †', feast: 'The Hunting of the Winter Hart · Feast of St Willoffrith' },
    ],
    notes: '† 1-in-4 chance of Hitching beginning',
  },
];

// Total days per month (28 regular + wysendays)
function getMonthLength(monthNum) {
  const m = MONTHS[monthNum - 1];
  const extra = m.wysendays.length;
  return 28 + extra;
}

// Returns { month, day, weekday, isWysenday, feast, moonPhase, season }
function getDayInfo(monthNum, dayNum) {
  const m = MONTHS[monthNum - 1];
  const isWysenday = dayNum > 28;
  let weekday = null;
  let wysenday = null;

  if (isWysenday) {
    wysenday = m.wysendays[dayNum - 29] || null;
  } else {
    weekday = WEEKDAYS[(dayNum - 1) % 7];
  }

  const feast = m.feasts[dayNum] || null;
  const moonPhase = (MOON_PHASES[monthNum] || {})[dayNum] || null;

  return {
    month: m,
    monthNum,
    dayNum,
    weekday,
    isWysenday,
    wysenday,
    feast,
    moonPhase,
    season: m.season,
  };
}

// Convert absolute day number (1 = 1 Grimvold) to { month, day }
function absoluteToDate(abs) {
  let remaining = abs;
  for (let i = 1; i <= 12; i++) {
    const len = getMonthLength(i);
    if (remaining <= len) return { month: i, day: remaining };
    remaining -= len;
  }
  return { month: 12, day: getMonthLength(12) };
}

// Convert { month, day } to absolute day number
function dateToAbsolute(month, day) {
  let abs = 0;
  for (let i = 1; i < month; i++) abs += getMonthLength(i);
  return abs + day;
}

// Total days in a year
function yearLength() {
  let total = 0;
  for (let i = 1; i <= 12; i++) total += getMonthLength(i);
  return total;
}
