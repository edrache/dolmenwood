// Shared calendar state – persisted in localStorage
// Key: 'dolmenwood_calendar_state'

const STATE_KEY = 'dolmenwood_calendar_state';

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

function loadState() {
  try {
    const raw = localStorage.getItem(STATE_KEY);
    if (raw) {
      return Object.assign({}, DEFAULT_STATE, JSON.parse(raw));
    }
  } catch (e) { /* ignore */ }
  return Object.assign({}, DEFAULT_STATE);
}

function saveState(state) {
  try {
    localStorage.setItem(STATE_KEY, JSON.stringify(state));
  } catch (e) { /* ignore */ }
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
