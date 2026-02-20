// ── ENCOUNTER MODULE ──
// Depends on: dice.js, data-encounters.js, state (global), log/logR (from index.html)

// Roll a creature from the appropriate table and log the result.
// encType: 'Animal'|'Monster'|'Mortal'|'Sentient'|'Regional'
// region: region string from hex data (used for Regional)
// label: prefix shown in log ('Creature', 'Second creature', etc.)
function rollCreatureLog(encType, region, label) {
  const r = roll1d20();
  if (encType === 'Regional') {
    const regionKey = Object.keys(ENC_REGIONAL).find(k => (region || '').includes(k)) || null;
    if (regionKey) {
      const creature = ENC_REGIONAL[regionKey][r] || '—';
      logR('roll', `${label} [Regional: ${regionKey}] 1d20=${r} → ${creature}`);
    } else {
      log(`<span class="log-warn">${label} — no regional table for "${region}".</span>`);
    }
  } else if (ENC_COMMON[encType]) {
    const creature = ENC_COMMON[encType][r] || '—';
    logR('roll', `${label} [${encType}] 1d20=${r} → ${creature}`);
  } else {
    log(`<span class="log-warn">${label} — unknown type: ${encType}.</span>`);
  }
}

function reactionText(roll) {
  if (roll <= 2)  return 'Hostile – attacks immediately';
  if (roll <= 5)  return 'Unfriendly – may attack';
  if (roll <= 8)  return 'Neutral – wary, uncertain';
  if (roll <= 11) return 'Indifferent – not interested';
  return 'Friendly – willing to negotiate';
}

function activityText(roll) {
  // Source: Dolmenwood Campaign Book – Creature Activity (d20)
  const acts = [null,
    'Celebrating',                                     // 1
    'Chasing ? (roll another encounter)',              // 2
    'Constructing',                                    // 3
    'Defecating',                                      // 4
    'Dying / wounded',                                 // 5
    'Fleeing from ? (roll another encounter)',         // 6
    'Hallucinating',                                   // 7
    'Hunting / foraging',                              // 8
    'In combat with ? (roll another encounter)',       // 9
    'Journey / pilgrimage',                            // 10
    'Lost / exploring',                                // 11
    'Marking territory',                               // 12
    'Mating / courting',                               // 13
    'Negotiating with ? (roll another encounter)',     // 14
    'Patrolling / guarding',                           // 15
    'Resting / camping',                               // 16
    'Ritual / magic',                                  // 17
    'Sleeping',                                        // 18
    'Trapped / imprisoned',                            // 19
    'Washing',                                         // 20
  ];
  return acts[roll] || 'Unknown activity';
}
