// Dolmenwood Weather Tables (2d6)
// Flags: I=Impeded travel, V=Visibility halved, W=Wet (campfire difficult)

const WEATHER = {
  winter: {
    2:  { text: 'Deep freeze, hoarfrost',           I:false, V:false, W:false },
    3:  { text: 'Bitter cold, ice',                 I:false, V:false, W:false },
    4:  { text: 'Overcast, freezing',               I:false, V:false, W:false },
    5:  { text: 'Cold, grey skies',                 I:false, V:false, W:false },
    6:  { text: 'Cold, clear',                      I:false, V:false, W:false },
    7:  { text: 'Crisp, bright winter sun',         I:false, V:false, W:false },
    8:  { text: 'Overcast, chill',                  I:false, V:false, W:false },
    9:  { text: 'Blustering wind, flurries',        I:false, V:false, W:false },
    10: { text: 'Heavy snowfall (I,V)',              I:true,  V:true,  W:false },
    11: { text: 'Freezing fog (V)',                  I:false, V:true,  W:false },
    12: { text: 'Relentless blizzard (I,V,W)',       I:true,  V:true,  W:true  },
  },
  spring: {
    2:  { text: 'Cold, gentle snow (W)',             I:false, V:false, W:true  },
    3:  { text: 'Chilly, damp (W)',                  I:false, V:false, W:true  },
    4:  { text: 'Windy, cloudy',                     I:false, V:false, W:false },
    5:  { text: 'Brisk, clear',                      I:false, V:false, W:false },
    6:  { text: 'Clement, cheery',                   I:false, V:false, W:false },
    7:  { text: 'Warm, sunny',                       I:false, V:false, W:false },
    8:  { text: 'Bright, fresh',                     I:false, V:false, W:false },
    9:  { text: 'Blustery, drizzle (W)',              I:false, V:false, W:true  },
    10: { text: 'Pouring rain (V,W)',                 I:false, V:true,  W:true  },
    11: { text: 'Gloomy, cool',                      I:false, V:false, W:false },
    12: { text: 'Chill mist (V)',                    I:false, V:true,  W:false },
  },
  summer: {
    2:  { text: 'Cool winds',                        I:false, V:false, W:false },
    3:  { text: 'Overcast, pleasant',                I:false, V:false, W:false },
    4:  { text: 'Warm, breezy',                      I:false, V:false, W:false },
    5:  { text: 'Hot, sunny',                        I:false, V:false, W:false },
    6:  { text: 'Glorious sunshine',                 I:false, V:false, W:false },
    7:  { text: 'Hot, humid',                        I:false, V:false, W:false },
    8:  { text: 'Stifling heat',                     I:false, V:false, W:false },
    9:  { text: 'Sudden shower (W)',                 I:false, V:false, W:true  },
    10: { text: 'Heavy rain (V,W)',                  I:false, V:true,  W:true  },
    11: { text: 'Oppressive, overcast',              I:false, V:false, W:false },
    12: { text: 'Thunderstorm (V,W)',                I:false, V:true,  W:true  },
  },
  autumn: {
    2:  { text: 'Torrential rain (V,W)',             I:false, V:true,  W:true  },
    3:  { text: 'Cold rain (W)',                     I:false, V:false, W:true  },
    4:  { text: 'Grey, drizzly (W)',                 I:false, V:false, W:true  },
    5:  { text: 'Overcast, cold',                    I:false, V:false, W:false },
    6:  { text: 'Chill, clear',                      I:false, V:false, W:false },
    7:  { text: 'Crisp autumn day',                  I:false, V:false, W:false },
    8:  { text: 'Blustery, leaves falling',          I:false, V:false, W:false },
    9:  { text: 'Heavy overcast',                    I:false, V:false, W:false },
    10: { text: 'Thick fog (V)',                     I:false, V:true,  W:false },
    11: { text: 'Sleet (I,W)',                       I:true,  V:false, W:true  },
    12: { text: 'Icy, gentle snow (W)',              I:false, V:false, W:true  },
  },
  hitching: {
    2:  { text: 'Eerie stillness',                   I:false, V:false, W:false },
    3:  { text: 'Unnatural cold',                    I:false, V:false, W:false },
    4:  { text: 'Strange winds from nowhere',        I:false, V:false, W:false },
    5:  { text: 'Pale, colourless sky',              I:false, V:false, W:false },
    6:  { text: 'The air smells of iron',            I:false, V:false, W:false },
    7:  { text: 'Unsettling quiet',                  I:false, V:false, W:false },
    8:  { text: 'Distant sounds, no source',         I:false, V:false, W:false },
    9:  { text: 'Thin, persistent mist (V)',         I:false, V:true,  W:false },
    10: { text: 'Frost without cold',                I:false, V:false, W:false },
    11: { text: 'Total, oppressive fog (V)',         I:false, V:true,  W:false },
    12: { text: 'Reality flickers (V)',              I:false, V:true,  W:false },
  },
  vague: {
    2:  { text: 'Colours too bright, eyes ache',    I:false, V:false, W:false },
    3:  { text: 'Rain falls upward briefly',         I:false, V:false, W:false },
    4:  { text: 'Flowers bloom and die in hours',   I:false, V:false, W:false },
    5:  { text: 'Shadows point the wrong way',      I:false, V:false, W:false },
    6:  { text: 'Everything tastes of honey',       I:false, V:false, W:false },
    7:  { text: 'Time feels stretched',             I:false, V:false, W:false },
    8:  { text: 'Dusk lasts for hours',             I:false, V:false, W:false },
    9:  { text: 'Music heard in the wind',          I:false, V:false, W:false },
    10: { text: 'The moon rises twice (V)',         I:false, V:true,  W:false },
    11: { text: 'Faerie lights at the tree-line',   I:false, V:false, W:false },
    12: { text: 'A gate opens somewhere nearby (I)',I:true,  V:false, W:false },
  },
};

function rollWeather(season) {
  const d1 = Math.ceil(Math.random() * 6);
  const d2 = Math.ceil(Math.random() * 6);
  const total = d1 + d2;
  const table = WEATHER[season] || WEATHER.autumn;
  const result = table[total];
  return { d1, d2, total, ...result };
}
