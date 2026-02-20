// ── TRAVEL PROCEDURE MODULE ──
// Depends on: dice.js, data-weather.js, encounters.js, state (global), log/logR/updateSidebar/refreshOverlay (index.html)

function runTravel() {
  if (!state.currentHex || !state.targetHex) return;

  const ch = state.currentHex;
  const th = state.targetHex;
  const hc = HEXES[ch];
  const ht = HEXES[th] || { t:'Unknown', r:'Unknown', lc:2, ec:2, tp:3, tc:'moderate' };
  const onRoad    = document.getElementById('chk-road').checked;
  const isForced  = document.getElementById('chk-forced').checked;
  const hasHunter = document.getElementById('chk-hunter').checked;
  const hasGuide  = document.getElementById('chk-guide').checked;

  logBlockOpen();
  log(`<span class="log-section">══ TRAVEL: ${ch} → ${th} ══</span>`);
  log(`Terrain: ${ht.t} | Region: ${ht.r} | Road: ${onRoad ? 'Yes' : 'No'}`);
  if (isForced) log(`<span class="log-warn">FORCED MARCH – party will be exhausted</span>`);

  // ── 1. TP COST ──
  let tpCost = onRoad ? 2 : ht.tp;
  if (state.weatherFlags.I) {
    tpCost += 2;
    log(`<span class="log-warn">Weather Impeded: +2 TP cost</span>`);
  }
  logR('roll', `TP cost: ${tpCost} (${state.tpLeft} remaining)`);
  if (tpCost > state.tpLeft) {
    logR('danger', `NOT ENOUGH TP. Need ${tpCost}, have ${state.tpLeft}.`);
    logBlockClose();
    return;
  }
  state.tpLeft -= tpCost;
  log(`TP after travel: <strong>${state.tpLeft}</strong>`);

  // ── 2. GETTING LOST ──
  log(`<span class="log-section">── LOST CHECK ──</span>`);
  let lostChance = onRoad ? 0 : ht.lc;
  if (!onRoad && state.weatherFlags.V) {
    lostChance = Math.min(6, lostChance + 1);
    log(`<span class="log-warn">Poor visibility: lost chance +1 → ${lostChance}-in-6</span>`);
  }

  let isLost = false;
  if (lostChance === 0) {
    logR('ok', 'Road/track: no lost check needed');
  } else {
    const { hit, roll } = rollXd6chance(lostChance);
    logR('roll', `Lost 1d6 = ${roll} (need ≤${lostChance} to get lost)`);
    if (hit) {
      isLost = true;
      logR('danger', 'PARTY IS LOST');

      // Navigation check
      if (hasGuide) {
        const { hit: found, roll: navRoll } = rollXd6chance(4);
        logR('roll', `Guide navigation 1d6 = ${navRoll} (need ≤4)`);
        if (found) { isLost = false; logR('ok', 'Guide finds the path – not lost'); }
        else log(`<span class="log-warn">Guide fails to navigate</span>`);
      } else if (hasHunter) {
        const { hit: found, roll: navRoll } = rollXd6chance(3);
        logR('roll', `Hunter navigation 1d6 = ${navRoll} (need ≤3)`);
        if (found) { isLost = false; logR('ok', 'Hunter finds the path – not lost'); }
        else log(`<span class="log-warn">Hunter fails to navigate</span>`);
      }

      if (isLost) {
        const { total: lt, rolls: lr } = roll3d6();
        const consequence = LOST_TABLE[lt] || 'Unknown consequence';
        logR('roll', `Consequence 3d6 [${lr.join('+')}] = ${lt}`);
        logR('danger', `→ ${consequence}`);
      }
    } else {
      logR('ok', 'Party stays on course');
    }
  }

  // ── 3. ENCOUNTER CHECK ──
  const timeCtx = state.isNight
    ? (state.hasFire ? 'night, fire' : 'night, no fire')
    : (onRoad ? 'day, road' : 'day, wild');
  log(`<span class="log-section">── ENCOUNTER CHECK (${timeCtx}) ──</span>`);
  const { hit: encHit, roll: encRoll } = rollXd6chance(ht.ec);
  logR('roll', `Encounter 1d6 = ${encRoll} (need ≤${ht.ec})`);
  if (encHit) {
    const typeRoll = roll1d8();
    let colIdx, timeLabel;
    if (!state.isNight) {
      colIdx    = onRoad ? 0 : 1;
      timeLabel = onRoad ? 'Road, day' : 'Wild, day';
    } else {
      colIdx    = state.hasFire ? 2 : 3;
      timeLabel = state.hasFire ? 'Night, fire' : 'Night, no fire';
    }
    const encTypeRow = ENC_TYPE_TABLE[typeRoll];
    const encType    = encTypeRow ? encTypeRow[colIdx] : 'Regional';
    logR('danger', `ENCOUNTER! 1d8 = ${typeRoll} → ${encType} (${timeLabel})`);

    // Creature
    rollCreatureLog(encType, ht.r, 'Creature');

    // Surprise
    const surpRoll = d(6);
    logR('roll', `Surprise 1d6 = ${surpRoll} (party surprised on 1-2)`);
    if (surpRoll <= 2) logR('danger', 'Party is SURPRISED');
    else logR('ok', 'No surprise');

    // Distance
    const distD1 = d(6); const distD2 = d(6);
    const distMult = state.weatherFlags.V ? 15 : 30;
    const dist = (distD1 + distD2) * distMult;
    const distM = Math.round(dist * 0.3048);
    logR('roll', `Distance 2d6×${distMult}ft = ${distD1}+${distD2}=${distD1+distD2} → ${dist}ft (${distM}m)`);

    // Reaction
    const { total: rt, rolls: rr } = roll2d6();
    logR('roll', `Reaction 2d6 [${rr.join('+')}] = ${rt} → ${reactionText(rt)}`);

    // Activity
    const actRoll = roll1d20();
    const actText = activityText(actRoll);
    logR('roll', `Activity 1d20 = ${actRoll} → ${actText}`);
    if (actText.includes('?')) {
      log(`<span class="log-warn">? — rolling second creature:</span>`);
      rollCreatureLog(encType, ht.r, 'Second creature');
    }
  } else {
    logR('ok', 'No encounter');
  }

  // ── 4. MOVE ──
  if (!isLost) {
    state.currentHex = th;
    state.targetHex  = null;
    state.clickPhase = 2;
    logR('ok', `Party arrives at ${th}`);
    refreshOverlay();
  } else {
    state.targetHex = null;
    log(`<span class="log-warn">Party position uncertain – update manually</span>`);
  }

  // ── 5. FORCED MARCH NOTE ──
  if (isForced) {
    log(`<span class="log-warn">Exhausted: −1 to Attack and Damage until full rest</span>`);
  }

  logBlockClose();
  updateSidebar();
}
