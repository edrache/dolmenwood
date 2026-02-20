// ── WEATHER TABLES (2d6) ──
// Source: Dolmenwood Campaign Book
// Flags: I = Impeded travel (−2 TP), V = Visibility halved, W = Wet (campfire difficult)
const WEATHER = {
  spring: {
    2:"Cold, gentle snow (W)",3:"Chilly, damp (W)",4:"Windy, cloudy",5:"Brisk, clear",
    6:"Clement, cheery",7:"Warm, sunny",8:"Bright, fresh",9:"Blustery, drizzle (W)",
    10:"Pouring rain (V,W)",11:"Gloomy, cool",12:"Chill mist (V)"
  },
  summer: {
    2:"Cool winds",3:"Low cloud, mist (V)",4:"Warm, gentle rain (W)",5:"Brooding thunder",
    6:"Balmy, clear",7:"Hot, humid",8:"Overcast, muggy",9:"Sweltering, still",
    10:"Baking, dry",11:"Warm wind",12:"Thunderstorm (V,W)"
  },
  autumn: {
    2:"Torrential rain (V,W)",3:"Rolling fog (V)",4:"Driving rain (V,W)",5:"Bracing wind",
    6:"Balmy, clement",7:"Clear, chilly",8:"Drizzle, damp (W)",9:"Cloudy, misty (V)",
    10:"Brooding clouds",11:"Frosty, chill",12:"Icy, gentle snow (W)"
  },
  winter: {
    2:"Deep freeze, hoarfrost",3:"Snowstorm (I,V,W)",4:"Relentless wind",5:"Bitter, silent",
    6:"Frigid, icy",7:"Clear, cold",8:"Freezing rain (V,W)",9:"Cold wind, gloomy",
    10:"Frigid mist (V)",11:"Icy, steady snow (V,W)",12:"Relentless blizzard (I,V,W)"
  },
  hitching: {
    2:"Torrential rain (V,W)",3:"Clear, fresh dew (W)",4:"Sleepy, purple mist (V)",
    5:"Interminable drizzle (W)",6:"Balmy mist (V)",7:"Thick fog, hot (V)",
    8:"Misty, seeping damp (V,W)",9:"Hazy fog, dripping (V,W)",10:"Sticky dew drips (W)",
    11:"Gloomy, shadows drip",12:"Befuddling green fog (V)"
  },
  vague: {
    2:"Hoarfrost, freezing fog (V)",3:"Steady snow, icy mist (V,W)",4:"Low mist, writhing soil",
    5:"Sickly, yellow mist (V)",6:"Thick, rolling fog (V)",7:"Freezing fog (V)",
    8:"Chill mist, winds wail (V)",9:"Icy mist, eerie howling (V)",10:"Violet mist rises (V)",
    11:"Blizzard, earth tremors (I,V,W)",12:"Blizzard, dense fog (I,V,W)"
  }
};

// ── LOST CONSEQUENCES (3d6) ──
// Source: Dolmenwood Campaign Book
const LOST_TABLE = {
  3:"Lost in time – 1d4+1 days pass",
  4:"Fairy Road – party stumbles onto a random fairy road",
  5:"Circles – end the day in the starting hex",
  6:"Deviation 90° LEFT",
  7:"Deviation 90° LEFT",
  8:"Deviation 45° LEFT",
  9:"Deviation 45° LEFT",
  10:"Uncertain paths – all TP costs doubled today",
  11:"Uncertain paths – all TP costs doubled today",
  12:"Deviation 45° RIGHT",
  13:"Deviation 45° RIGHT",
  14:"Deviation 90° RIGHT",
  15:"Deviation 90° RIGHT",
  16:"Circles – end the day in the starting hex",
  17:"Nodal Stone – knocked unconscious, wake near random nodal stone",
  18:"Bewildering Fog – emerge in random hex ≥2 hexes away"
};
