// ── WEATHER MODULE ──
// Depends on: dice.js, data-weather.js, state (global), log/logR (from index.html)

function runWeather() {
  const season = document.getElementById('inp-season').value;
  const { total, rolls } = roll2d6();
  const table = WEATHER[season];
  const result = table[total];

  state.weatherFlags = {
    I: result.includes('(I') || result.includes(',I'),
    V: result.includes('V)') || result.includes('V,') || result.includes('(V'),
    W: result.includes('W)') || result.includes('W,') || result.includes('(W')
  };
  state.weatherText = result;

  recalcTP();

  const flags = Object.entries(state.weatherFlags)
    .filter(([, v]) => v)
    .map(([k]) => `<span class="weather-flag flag-${k}">${k}</span>`)
    .join('');

  document.getElementById('disp-weather').innerHTML =
    `<span class="log-roll">${result}</span> ${flags}`;

  log(`<span class="log-section">── WEATHER ──</span>`);
  log(`<span class="log-roll">2d6 [${rolls.join('+')}] = ${total}</span> → ${result}${flags}`);
  if (state.weatherFlags.I) log(`<span class="log-warn">Travel Impeded: −2 TP today</span>`);
  if (state.weatherFlags.V) log(`<span class="log-warn">Poor Visibility: encounter distance halved (30ft→15ft / 9m→5m), Lost chance +1-in-6</span>`);
  if (state.weatherFlags.W) log(`<span class="log-warn">Wet: campfire difficult</span>`);

  updateSidebar();
}

function recalcTP() {
  const speed = parseInt(document.getElementById('inp-speed').value) || 40;
  let tp = Math.floor(speed / 5);
  if (document.getElementById('chk-forced').checked) tp = Math.floor(tp * 1.5);
  if (state.weatherFlags.I) tp = Math.max(0, tp - 2);
  state.tpMax = tp;
  state.tpLeft = tp;
}

function resetTP() {
  // Advance calendar day if sync is enabled (async, fires and forgets display update)
  if (typeof advanceCalendarDay === 'function') advanceCalendarDay();
  recalcTP();
  log(`<span class="log-info">New day – TP reset to ${state.tpMax}</span>`);
  updateTPBar();
  updateSidebar();
}
