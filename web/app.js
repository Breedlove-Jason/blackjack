const $ = id => document.getElementById(id);
const suits = {H: ['♥', 'hearts'], D: ['♦', 'diamonds'], C: ['♣', 'clubs'], S: ['♠', 'spades']};
let game, loading = false;
function cards(id, hand) {
  $(id).replaceChildren(...hand.map(card => {
    const el = document.createElement('div');
    el.className = 'card'; el.setAttribute('role', 'img');
    if (!card) { el.classList.add('back'); el.textContent = '♠'; el.setAttribute('aria-label', 'Face-down card'); return el; }
    const [rank, suit] = card;
    if (suit === 'H' || suit === 'D') el.classList.add('red');
    el.setAttribute('aria-label', `${rank} of ${suits[suit][1]}`);
    el.append(document.createTextNode(rank));
    const pip = document.createElement('span'); pip.textContent = suits[suit][0];
    const corner = document.createElement('small'); corner.textContent = rank;
    el.append(pip, corner); return el;
  }));
}
function sync() {
  const s = JSON.parse(game.snapshot());
  if (s.phase !== 'ready') { cards('player-cards', s.player); cards('dealer-cards', s.dealer); }
  $('player-total').textContent = s.phase === 'ready' ? '—' : `${s.player_total}${s.player_total > 21 ? ' · BUST' : ''}`;
  $('dealer-total').textContent = s.phase === 'ready' ? '—' : s.dealer_total === null ? 'One card hidden' : `${s.dealer_total}${s.dealer_total > 21 ? ' · BUST' : ''}`;
  $('round').textContent = s.rounds ? `Hand ${String(s.rounds).padStart(2, '0')}` : 'Take your seat';
  $('wins').textContent = s.scores.win; $('losses').textContent = s.scores.loss; $('pushes').textContent = s.scores.push;
  $('status').textContent = s.message;
  $('hit').disabled = $('stand').disabled = s.phase !== 'playing';
  $('deal').disabled = s.phase === 'playing';
  $('deal').textContent = s.phase === 'ready' ? 'Deal me in ↗' : 'Next hand ↗';
}
function act(action) {
  if (!game) return load();
  game[action](); sync();
  if ($('deal').disabled) $('hit').focus({preventScroll:true}); else $('deal').focus({preventScroll:true});
}
for (const action of ['deal', 'hit', 'stand']) $(action).addEventListener('click', () => act(action));
async function load() {
  if (loading) return;
  loading = true; $('deal').disabled = true; $('deal').textContent = 'Loading…';
  $('status').textContent = 'Loading Python. Your first visit may take a moment.';
  try {
    const {loadPyodide} = await import('https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs');
    const py = await loadPyodide();
    const response = await fetch('engine.py');
    if (!response.ok) throw new Error('Unable to load game rules');
    py.runPython(await response.text());
    py.runPython('game = Game()'); game = py.globals.get('game'); sync();
  } catch (error) {
    console.error(error); $('status').textContent = 'The table could not load. Check your connection and retry.';
    $('deal').textContent = 'Retry'; $('deal').disabled = false;
  } finally { loading = false; }
}
load();
