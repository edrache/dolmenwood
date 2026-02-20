// ── DICE UTILITIES ──
// Pure random functions, no DOM dependencies.

function d(n) { return Math.floor(Math.random() * n) + 1; }

function rollNd6(n) {
  const rolls = [];
  for (let i = 0; i < n; i++) rolls.push(d(6));
  return { total: rolls.reduce((a, b) => a + b, 0), rolls };
}

function roll2d6() { return rollNd6(2); }
function roll3d6() { return rollNd6(3); }
function roll1d8()  { return d(8); }
function roll1d20() { return d(20); }

// Returns { hit: bool, roll: number }
// "x-in-6 chance" — succeeds if 1d6 ≤ x
function rollXd6chance(x) {
  const r = d(6);
  return { hit: r <= x, roll: r };
}
