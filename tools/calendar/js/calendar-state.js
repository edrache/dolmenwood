// Shared calendar state – persisted via server API (localStorage as fallback)
// Server API: GET/POST /api/state
// localStorage key: 'dolmenwood_calendar_state'

const STATE_KEY = 'dolmenwood_calendar_state';
// API runs via Cytrus reverse proxy with Let's Encrypt (HTTPS → Flask :3000)
const API_URL = 'https://calendar-api.cytr.us/api/state';

const DEFAULT_STATE = {
  month: 1,
  day: 1,
  year: 1,
  // Daily weather (set by referee, shown to players)
  weatherText: '',
  weatherFlags: { I: false, V: false, W: false },
  // Notes visible to players
  publicNote: '',
  // Campaign year label
  yearLabel: '',
};

// --- localStorage helpers (always kept in sync as fallback) ---

function _localLoad() {
  try {
    const raw = localStorage.getItem(STATE_KEY);
    if (raw) return Object.assign({}, DEFAULT_STATE, JSON.parse(raw));
  } catch (e) { /* ignore */ }
  return Object.assign({}, DEFAULT_STATE);
}

function _localSave(state) {
  try {
    localStorage.setItem(STATE_KEY, JSON.stringify(state));
  } catch (e) { /* ignore */ }
}

// --- Synchronous fallback API (used by pages that haven't migrated to async) ---

function loadState() {
  return _localLoad();
}

function saveState(state) {
  _localSave(state);
}

// --- Async server API ---

// Fetch state from server; falls back to localStorage on error.
// Returns Promise<{ state, fromServer: bool }>
async function fetchState() {
  try {
    const res = await fetch(API_URL, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const state = Object.assign({}, DEFAULT_STATE, data);
    state.weatherFlags = Object.assign({}, DEFAULT_STATE.weatherFlags, state.weatherFlags);
    _localSave(state); // keep localStorage in sync
    return { state, fromServer: true };
  } catch (e) {
    return { state: _localLoad(), fromServer: false };
  }
}

// Push state to server; always saves to localStorage too.
// Returns Promise<{ ok: bool, fromServer: bool }>
async function pushState(state, refereeToken) {
  _localSave(state);
  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Referee-Token': refereeToken || '',
      },
      body: JSON.stringify(state),
    });
    if (res.status === 403) return { ok: false, fromServer: true, error: 'Zły token' };
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return { ok: true, fromServer: true };
  } catch (e) {
    return { ok: false, fromServer: false, error: e.message };
  }
}

function advanceDay(state) {
  const newState = Object.assign({}, state);
  const len = getMonthLength(state.month);
  if (state.day < len) {
    newState.day = state.day + 1;
  } else if (state.month < 12) {
    newState.month = state.month + 1;
    newState.day = 1;
  } else {
    newState.month = 1;
    newState.day = 1;
    newState.year = state.year + 1;
  }
  // Clear daily weather when day advances
  newState.weatherText = '';
  newState.weatherFlags = { I: false, V: false, W: false };
  return newState;
}

function retreatDay(state) {
  const newState = Object.assign({}, state);
  if (state.day > 1) {
    newState.day = state.day - 1;
  } else if (state.month > 1) {
    newState.month = state.month - 1;
    newState.day = getMonthLength(newState.month);
  } else {
    newState.month = 12;
    newState.day = getMonthLength(12);
    newState.year = Math.max(1, state.year - 1);
  }
  newState.weatherText = '';
  newState.weatherFlags = { I: false, V: false, W: false };
  return newState;
}
