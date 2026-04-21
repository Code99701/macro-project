// ============================================================
// DATA
// ============================================================
const TEAMS = [
  'Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders',
  'Royal Challengers Bangalore', 'Kings XI Punjab', 'Rajasthan Royals',
  'Delhi Daredevils', 'Sunrisers Hyderabad', 'Deccan Chargers',
  'Gujarat Lions', 'Pune Warriors', 'Rising Pune Supergiant',
  'Delhi Capitals', 'Kochi Tuskers Kerala', 'Rising Pune Supergiants'
];

const CITIES = [
  'Abu Dhabi', 'Ahmedabad', 'Bangalore', 'Bengaluru', 'Bloemfontein',
  'Cape Town', 'Centurion', 'Chandigarh', 'Chennai', 'Cuttack', 'Delhi',
  'Dharamsala', 'Durban', 'East London', 'Hyderabad', 'Indore', 'Jaipur',
  'Johannesburg', 'Kanpur', 'Kimberley', 'Kochi', 'Kolkata', 'Mohali',
  'Mumbai', 'Nagpur', 'Port Elizabeth', 'Pune', 'Raipur', 'Rajkot',
  'Ranchi', 'Sharjah', 'Visakhapatnam'
];

const TEAM_STATS = {
  'Chennai Super Kings': { wins: 100, matches: 164, titles: 3, winPct: 61.0 },
  'Mumbai Indians': { wins: 109, matches: 187, titles: 4, winPct: 58.3 },
  'Kolkata Knight Riders': { wins: 92, matches: 178, titles: 2, winPct: 51.7 },
  'Royal Challengers Bangalore': { wins: 84, matches: 180, titles: 0, winPct: 46.7 },
  'Kings XI Punjab': { wins: 82, matches: 176, titles: 0, winPct: 46.6 },
  'Rajasthan Royals': { wins: 75, matches: 147, titles: 1, winPct: 51.0 },
  'Delhi Daredevils': { wins: 67, matches: 161, titles: 0, winPct: 41.6 },
  'Sunrisers Hyderabad': { wins: 58, matches: 108, titles: 1, winPct: 53.7 },
  'Deccan Chargers': { wins: 29, matches: 75, titles: 1, winPct: 38.7 },
  'Gujarat Lions': { wins: 13, matches: 30, titles: 0, winPct: 43.3 },
  'Pune Warriors': { wins: 12, matches: 46, titles: 0, winPct: 26.1 },
  'Rising Pune Supergiant': { wins: 10, matches: 16, titles: 0, winPct: 62.5 },
  'Delhi Capitals': { wins: 10, matches: 16, titles: 0, winPct: 62.5 },
  'Kochi Tuskers Kerala': { wins: 6, matches: 14, titles: 0, winPct: 42.9 },
  'Rising Pune Supergiants': { wins: 5, matches: 14, titles: 0, winPct: 35.7 }
};

const TOP_BATSMEN = [
  { name: 'V Kohli', runs: 5434, balls: 4211, sr: 129.0, fours: 482, sixes: 191, color: '#FF6384' },
  { name: 'SK Raina', runs: 5415, balls: 4044, sr: 133.9, fours: 495, sixes: 195, color: '#FF9F40' },
  { name: 'RG Sharma', runs: 4914, balls: 3816, sr: 128.8, fours: 431, sixes: 194, color: '#FFCD56' },
  { name: 'DA Warner', runs: 4741, balls: 3398, sr: 139.5, fours: 459, sixes: 181, color: '#4BC0C0' },
  { name: 'S Dhawan', runs: 4632, balls: 3776, sr: 122.7, fours: 526, sixes: 96, color: '#9966FF' },
  { name: 'CH Gayle', runs: 4560, balls: 3131, sr: 145.6, fours: 376, sixes: 327, color: '#FF6384' },
  { name: 'MS Dhoni', runs: 4477, balls: 3318, sr: 134.9, fours: 297, sixes: 207, color: '#36A2EB' },
  { name: 'RV Uthappa', runs: 4446, balls: 3492, sr: 127.3, fours: 436, sixes: 156, color: '#4BC0C0' },
  { name: 'AB de Villiers', runs: 4428, balls: 2977, sr: 148.7, fours: 357, sixes: 214, color: '#9966FF' },
  { name: 'G Gambhir', runs: 4223, balls: 3524, sr: 119.8, fours: 492, sixes: 59, color: '#FF9F40' }
];

const TOP_BOWLERS = [
  { name: 'SL Malinga', wickets: 170, eco: 7.08, color: '#FF6384' },
  { name: 'A Mishra', wickets: 156, eco: 7.28, color: '#FF9F40' },
  { name: 'Harbhajan Singh', wickets: 150, eco: 7.04, color: '#FFCD56' },
  { name: 'PP Chawla', wickets: 149, eco: 7.89, color: '#4BC0C0' },
  { name: 'DJ Bravo', wickets: 147, eco: 8.26, color: '#9966FF' },
  { name: 'B Kumar', wickets: 133, eco: 7.23, color: '#FF6384' },
  { name: 'R Ashwin', wickets: 125, eco: 6.75, color: '#36A2EB' },
  { name: 'SP Narine', wickets: 122, eco: 6.78, color: '#4BC0C0' },
  { name: 'UT Yadav', wickets: 119, eco: 8.38, color: '#9966FF' },
  { name: 'RA Jadeja', wickets: 108, eco: 7.61, color: '#FF9F40' }
];

const SEASON_WINNERS = {
  'IPL-2008': 'Rajasthan Royals', 'IPL-2009': 'Deccan Chargers',
  'IPL-2010': 'Chennai Super Kings', 'IPL-2011': 'Chennai Super Kings',
  'IPL-2012': 'Kolkata Knight Riders', 'IPL-2013': 'Mumbai Indians',
  'IPL-2014': 'Kolkata Knight Riders', 'IPL-2015': 'Mumbai Indians',
  'IPL-2016': 'Sunrisers Hyderabad', 'IPL-2017': 'Mumbai Indians',
  'IPL-2018': 'Chennai Super Kings', 'IPL-2019': 'Mumbai Indians'
};

const H2H = {
  'Mumbai Indians': { 'Chennai Super Kings': 16, 'Kolkata Knight Riders': 14, 'Royal Challengers Bangalore': 14, 'Kings XI Punjab': 14, 'Rajasthan Royals': 14, 'Delhi Daredevils': 14, 'Sunrisers Hyderabad': 7 },
  'Chennai Super Kings': { 'Mumbai Indians': 12, 'Kolkata Knight Riders': 15, 'Royal Challengers Bangalore': 14, 'Kings XI Punjab': 15, 'Rajasthan Royals': 12, 'Delhi Daredevils': 14, 'Sunrisers Hyderabad': 3 },
  'Kolkata Knight Riders': { 'Mumbai Indians': 14, 'Chennai Super Kings': 11, 'Royal Challengers Bangalore': 14, 'Kings XI Punjab': 13, 'Rajasthan Royals': 11, 'Delhi Daredevils': 14, 'Sunrisers Hyderabad': 7 },
  'Royal Challengers Bangalore': { 'Mumbai Indians': 9, 'Chennai Super Kings': 8, 'Kolkata Knight Riders': 10, 'Kings XI Punjab': 12, 'Rajasthan Royals': 8, 'Delhi Daredevils': 14, 'Sunrisers Hyderabad': 6 },
  'Kings XI Punjab': { 'Mumbai Indians': 10, 'Chennai Super Kings': 9, 'Kolkata Knight Riders': 11, 'Royal Challengers Bangalore': 12, 'Rajasthan Royals': 10, 'Delhi Daredevils': 11, 'Sunrisers Hyderabad': 10 },
  'Rajasthan Royals': { 'Mumbai Indians': 8, 'Chennai Super Kings': 10, 'Kolkata Knight Riders': 9, 'Royal Challengers Bangalore': 8, 'Kings XI Punjab': 10, 'Delhi Daredevils': 10, 'Sunrisers Hyderabad': 6 },
  'Delhi Daredevils': { 'Mumbai Indians': 11, 'Chennai Super Kings': 8, 'Kolkata Knight Riders': 10, 'Royal Challengers Bangalore': 14, 'Kings XI Punjab': 11, 'Rajasthan Royals': 10, 'Sunrisers Hyderabad': 8 },
  'Sunrisers Hyderabad': { 'Mumbai Indians': 7, 'Chennai Super Kings': 3, 'Kolkata Knight Riders': 7, 'Royal Challengers Bangalore': 8, 'Kings XI Punjab': 10, 'Rajasthan Royals': 6, 'Delhi Daredevils': 8 }
};

const VENUE_STATS = {
  'Eden Gardens': { bat_first_wins: 30, total: 77, pct: 39.0 },
  'Wankhede Stadium': { bat_first_wins: 36, total: 73, pct: 49.3 },
  'M Chinnaswamy Stadium': { bat_first_wins: 30, total: 71, pct: 42.3 },
  'Feroz Shah Kotla': { bat_first_wins: 32, total: 66, pct: 48.5 },
  'Rajiv Gandhi Intl Stadium, Uppal': { bat_first_wins: 22, total: 56, pct: 39.3 },
  'MA Chidambaram Stadium, Chepauk': { bat_first_wins: 31, total: 49, pct: 63.3 },
  'Sawai Mansingh Stadium': { bat_first_wins: 15, total: 47, pct: 31.9 },
  'Punjab CA Stadium, Mohali': { bat_first_wins: 15, total: 35, pct: 42.9 },
  'Maharashtra CA Stadium': { bat_first_wins: 7, total: 21, pct: 33.3 },
  'Dr DY Patil Sports Academy': { bat_first_wins: 7, total: 17, pct: 41.2 }
};

const POM_LEADERS = [
  { name: 'CH Gayle', pom: 21 }, { name: 'AB de Villiers', pom: 20 },
  { name: 'MS Dhoni', pom: 17 }, { name: 'DA Warner', pom: 17 },
  { name: 'RG Sharma', pom: 17 }, { name: 'YK Pathan', pom: 16 },
  { name: 'SR Watson', pom: 15 }, { name: 'SK Raina', pom: 14 },
  { name: 'G Gambhir', pom: 13 }, { name: 'MEK Hussey', pom: 12 }
];

const SEASON_TEAM_WINS = {
  'IPL-2008': { 'Rajasthan Royals': 8, 'Chennai Super Kings': 6, 'Delhi Daredevils': 6, 'Kolkata Knight Riders': 5, 'Kings XI Punjab': 5, 'Mumbai Indians': 5, 'Royal Challengers Bangalore': 4, 'Deccan Chargers': 2 },
  'IPL-2009': { 'Delhi Daredevils': 10, 'Deccan Chargers': 9, 'Rajasthan Royals': 8, 'Bangalore': 6, 'KolkataKnightRiders': 5, 'Chennai Super Kings': 5, 'Mumbai Indians': 4, 'Kings XI Punjab': 2 },
  'IPL-2010': { 'Mumbai Indians': 11, 'Chennai Super Kings': 10, 'Royal Challengers Bangalore': 9, 'Kolkata Knight Riders': 7, 'Delhi Daredevils': 7, 'Kings XI Punjab': 6, 'Rajasthan Royals': 4, 'Deccan Chargers': 4 },
  'IPL-2011': { 'Royal Challengers Bangalore': 12, 'Chennai Super Kings': 11, 'Mumbai Indians': 9, 'Kolkata Knight Riders': 8, 'Rajasthan Royals': 7, 'Delhi Daredevils': 7, 'Kings XI Punjab': 4, 'Deccan Chargers': 4 },
  'IPL-2012': { 'Kolkata Knight Riders': 12, 'Delhi Daredevils': 12, 'Chennai Super Kings': 11, 'Mumbai Indians': 11, 'Rajasthan Royals': 8, 'Kings XI Punjab': 7, 'Royal Challengers Bangalore': 7, 'Deccan Chargers': 2, 'Pune Warriors': 2 },
  'IPL-2013': { 'Mumbai Indians': 11, 'Chennai Super Kings': 10, 'Rajasthan Royals': 9, 'Kolkata Knight Riders': 8, 'Sunrisers Hyderabad': 7, 'Delhi Daredevils': 7, 'Royal Challengers Bangalore': 6, 'Kings XI Punjab': 5, 'Pune Warriors': 1 },
  'IPL-2014': { 'Kings XI Punjab': 11, 'Kolkata Knight Riders': 11, 'Chennai Super Kings': 9, 'Mumbai Indians': 7, 'Rajasthan Royals': 7, 'Royal Challengers Bangalore': 7, 'Delhi Daredevils': 5, 'Sunrisers Hyderabad': 5 },
  'IPL-2015': { 'Mumbai Indians': 12, 'Chennai Super Kings': 11, 'Royal Challengers Bangalore': 9, 'Rajasthan Royals': 9, 'Kolkata Knight Riders': 7, 'Sunrisers Hyderabad': 7, 'Delhi Daredevils': 5, 'Kings XI Punjab': 2 },
  'IPL-2016': { 'Sunrisers Hyderabad': 11, 'Royal Challengers Bangalore': 11, 'Gujarat Lions': 9, 'Mumbai Indians': 8, 'Kolkata Knight Riders': 7, 'Kings XI Punjab': 7, 'Delhi Daredevils': 5, 'Rising Pune Supergiants': 5 },
  'IPL-2017': { 'Mumbai Indians': 10, 'Rising Pune Supergiant': 9, 'Sunrisers Hyderabad': 8, 'Kolkata Knight Riders': 8, 'Delhi Daredevils': 7, 'Kings XI Punjab': 7, 'Royal Challengers Bangalore': 5, 'Gujarat Lions': 4 },
  'IPL-2018': { 'Sunrisers Hyderabad': 9, 'Chennai Super Kings': 9, 'Kolkata Knight Riders': 8, 'Rajasthan Royals': 7, 'Kings XI Punjab': 7, 'Mumbai Indians': 6, 'Royal Challengers Bangalore': 6, 'Delhi Daredevils': 5 },
  'IPL-2019': { 'Mumbai Indians': 11, 'Chennai Super Kings': 10, 'Delhi Capitals': 9, 'Sunrisers Hyderabad': 6, 'Kolkata Knight Riders': 6, 'Kings XI Punjab': 6, 'Rajasthan Royals': 5, 'Royal Challengers Bangalore': 5 }
};

const ACTIVE_TEAMS_H2H = ['Mumbai Indians', 'Chennai Super Kings', 'Kolkata Knight Riders', 'Royal Challengers Bangalore', 'Kings XI Punjab', 'Rajasthan Royals', 'Delhi Daredevils', 'Sunrisers Hyderabad'];

// ============================================================
// INIT
// ============================================================
function init() {
  populateDropdowns();
  buildTeamsTable();
  buildPlayerLists();
  buildSeasonGrid();
  buildVenueList();
  buildH2HMatrix();
  buildH2HDropdowns();
  renderCharts();
}

function populateDropdowns() {
  const addOptions = (sel, arr) => {
    arr.forEach(v => { const o = new Option(v, v); sel.add(o); });
  };
  addOptions(document.getElementById('bat-team'), TEAMS);
  addOptions(document.getElementById('bowl-team'), TEAMS);
  addOptions(document.getElementById('host-city'), CITIES);

  // Quick stats
  const qs = document.getElementById('quick-stats');
  const top5 = Object.entries(TEAM_STATS).sort((a, b) => b[1].winPct - a[1].winPct).slice(0, 6);
  qs.innerHTML = top5.map(([name, s]) => `
<div style="background: var(--navy2); border-radius: 10px; padding: 10px;">
  <div style="font-family: 'Rajdhani'; font-size: 11px; font-weight: 700; color: var(--text3); letter-spacing: 1px; margin-bottom: 3px;">
    ${name.replace(' Super Kings', '').replace(' Indians', '').replace(' Knight Riders', '').replace(' Challengers Bangalore', '').replace(' Punjab', '').replace(' Royals', '').replace(' Daredevils', '').replace(' Hyderabad', '')}
  </div>
  <div style="font-family: 'Bebas Neue'; font-size: 24px; color: ${s.winPct > 55 ? 'var(--gold)' : 'var(--text)'};">${s.winPct}%</div>
  <div style="font-size: 10px; color: var(--text3);">${s.wins}W / ${s.matches}M</div>
</div>
  `).join('');
}

// ============================================================
// TEAMS TABLE
// ============================================================
function buildTeamsTable() {
  const sorted = Object.entries(TEAM_STATS).sort((a, b) => b[1].winPct - a[1].winPct);
  const tbody = document.getElementById('teams-tbody');
  tbody.innerHTML = sorted.map(([name, s], i) => {
    const lost = s.matches - s.wins;
    const titleBadge = s.titles > 0 ? `<span class="badge badge-gold">🏆 ${s.titles}×</span>` : '';
    const rankColor = i === 0 ? 'var(--gold)' : i === 1 ? '#B0B8D4' : i === 2 ? '#CD7F32' : '';
    return `<tr>
  <td class="rank" style="${rankColor ? `color:${rankColor}` : ''}"> ${i + 1}</td>
  <td class="team-name">${name}</td>
  <td style="color: var(--text2);">${s.matches}</td>
  <td style="color: var(--green); font-weight: 500;">${s.wins}</td>
  <td style="color: var(--red);">${lost}</td>
  <td style="font-family: 'Bebas Neue'; font-size: 17px; color:${s.winPct > 55 ? 'var(--gold)' : s.winPct > 50 ? 'var(--green)' : 'var(--text)'};">${s.winPct}%</td>
  <td class="win-bar-wrap">
    <div class="win-bar-bg"><div class="win-bar-fill" style="width:${s.winPct}%;"></div></div>
  </td>
  <td>${titleBadge}</td>
</tr>`;
  }).join('');
}

// ============================================================
// PLAYER LISTS
// ============================================================
const AVATAR_COLORS = ['#3A6FF8', '#E63946', '#2DC653', '#F5C842', '#9B5DE5', '#F15BB5', '#00BBF9', '#F5834A', '#4CC9F0', '#7209B7'];

function buildPlayerLists() {
  const batList = document.getElementById('batsmen-list');
  batList.innerHTML = TOP_BATSMEN.map((p, i) => `
<div class="player-row">
  <span class="player-rank${i < 3 ? ' top3' : ''}">${i + 1}</span>
  <div class="player-avatar" style="background:${AVATAR_COLORS[i]}22; color:${AVATAR_COLORS[i]};">
    ${p.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
  </div>
  <div class="player-info">
    <div class="player-name">${p.name}</div>
    <div class="player-detail">SR: ${p.sr} · 4s: ${p.fours} · 6s: ${p.sixes}</div>
  </div>
  <div>
    <div class="player-stat" style="color:${AVATAR_COLORS[i]};">${p.runs.toLocaleString()}</div>
    <div class="player-stat-sub">Runs</div>
  </div>
</div>
  `).join('');

  const bowlList = document.getElementById('bowlers-list');
  bowlList.innerHTML = TOP_BOWLERS.map((p, i) => `
<div class="player-row">
  <span class="player-rank${i < 3 ? ' top3' : ''}">${i + 1}</span>
  <div class="player-avatar" style="background:${AVATAR_COLORS[i]}22; color:${AVATAR_COLORS[i]};">
    ${p.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
  </div>
  <div class="player-info">
    <div class="player-name">${p.name}</div>
    <div class="player-detail">Economy: ${p.eco}</div>
  </div>
  <div>
    <div class="player-stat" style="color:${AVATAR_COLORS[i]};">${p.wickets}</div>
    <div class="player-stat-sub">Wickets</div>
  </div>
</div>
  `).join('');
}

// ============================================================
// SEASON GRID
// ============================================================
function buildSeasonGrid() {
  const grid = document.getElementById('season-grid');
  const titleCounts = {};
  Object.values(SEASON_WINNERS).forEach(t => { titleCounts[t] = (titleCounts[t] || 0) + 1; });

  grid.innerHTML = Object.entries(SEASON_WINNERS).map(([s, winner]) => {
    const year = s.replace('IPL-', '');
    return `<div class="season-card">
  <div class="season-trophy">🏆</div>
  <div class="season-year">${year}</div>
  <div class="season-winner">${winner}</div>
  <div class="season-count">${titleCounts[winner]}× champions</div>
</div>`;
  }).join('');
}

// ============================================================
// VENUE LIST
// ============================================================
function buildVenueList() {
  const list = document.getElementById('venue-list');
  list.innerHTML = Object.entries(VENUE_STATS).map(([name, s]) => {
    const pctClass = s.pct > 55 ? 'danger' : s.pct < 40 ? 'good' : '';
    return `<div class="venue-row">
  <div class="venue-name">${name}</div>
  <div style="font-size: 10px; color: var(--text3); white-space: nowrap;">${s.total} matches</div>
  <div class="venue-bar-wrap">
    <div class="win-bar-bg"><div class="win-bar-fill" style="width:${s.pct}%; background: linear-gradient(90deg, #4F8EF7, #9B5DE5);"></div></div>
  </div>
  <div class="venue-pct ${pctClass}">${s.pct}%</div>
</div>`;
  }).join('');
}

// ============================================================
// H2H MATRIX
// ============================================================
function buildH2HMatrix() {
  const table = document.getElementById('h2h-matrix');
  const teams = ACTIVE_TEAMS_H2H;
  const abbr = t => t.replace(' Super Kings', 'CSK').replace('Mumbai Indians', 'MI').replace('Kolkata Knight Riders', 'KKR').replace('Royal Challengers Bangalore', 'RCB').replace('Kings XI Punjab', 'KXIP').replace('Rajasthan Royals', 'RR').replace('Delhi Daredevils', 'DD').replace('Sunrisers Hyderabad', 'SRH');

  let html = '<thead><tr><th>TEAM</th>';
  teams.forEach(t => { html += `<th>${abbr(t)}</th>`; });
  html += '</tr></thead><tbody>';

  teams.forEach(t1 => {
    html += `<tr><td>${abbr(t1)}</td>`;
    teams.forEach(t2 => {
      if (t1 === t2) { html += '<td class="self">-</td>'; return; }
      const w = (H2H[t1] && H2H[t1][t2]) || 0;
      const cls = w >= 14 ? 'high' : w >= 10 ? 'mid' : 'low';
      html += `<td class="${cls}">${w}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody>';
  table.innerHTML = html;
}

function buildH2HDropdowns() {
  const active = ACTIVE_TEAMS_H2H;
  ['h2h-team1', 'h2h-team2'].forEach(id => {
    const sel = document.getElementById(id);
    active.forEach(t => sel.add(new Option(t, t)));
  });
}

function updateH2H() {
  const t1 = document.getElementById('h2h-team1').value;
  const t2 = document.getElementById('h2h-team2').value;
  if (!t1 || !t2 || t1 === t2) { document.getElementById('h2h-result').style.display = 'none'; return; }

  const w1 = (H2H[t1] && H2H[t1][t2]) || 0;
  const w2 = (H2H[t2] && H2H[t2][t1]) || 0;
  const total = w1 + w2;

  document.getElementById('h2h-w1').textContent = w1;
  document.getElementById('h2h-w2').textContent = w2;
  document.getElementById('h2h-n1').textContent = t1;
  document.getElementById('h2h-n2').textContent = t2;
  document.getElementById('h2h-total').textContent = total + ' matches';
  document.getElementById('h2h-result').style.display = 'grid';
  document.getElementById('h2h-bar-section').style.display = 'block';

  if (total > 0) {
    document.getElementById('h2h-bar1').style.width = (w1 / total * 100) + '%';
    document.getElementById('h2h-bar2').style.width = (w2 / total * 100) + '%';
  }
}

function showInputError(msg) {
  const box = document.getElementById('input-error');
  const el = document.getElementById('err-msg');

  const lines = msg.split('\n');
  let html = '';
  lines.forEach((line, i) => {
    const trimmed = line.trim();
    if (trimmed.startsWith('•')) {
      html += `<div class="err-bullet-row">` +
        `<span class="err-bullet-dot">▸</span>` +
        `<span class="err-bullet-text">${trimmed.slice(1).trim()}</span></div>`;
    } else if (trimmed) {
      html += (i > 0 ? '<br>' : '') + trimmed;
    }
  });
  el.innerHTML = html;

  box.classList.remove('visible');
  void box.offsetWidth;
  box.classList.add('visible');
  box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function clearInputError() {
  document.getElementById('input-error').classList.remove('visible');
}

function validateCricketInputs(balls, score, wickets, target) {
  const overs = Math.floor(balls / 6) + '.' + (balls % 6);

  // ── Zero-ball edge cases ─────────────────────────────────────────────
  if (balls === 0 && score > 0)
    return `Score of ${score} is impossible — no balls have been bowled yet. Score must be 0 at the start of the innings.`;

  if (balls === 0 && wickets > 0)
    return `${wickets} wicket(s) cannot fall before a single ball is bowled. No deliveries means no dismissals.`;

  if (balls > 0) {
    // ── Tier 1: Absolute maximum (ignores wickets) ────────────────────
    const absoluteMax = balls * 6;

    if (score > absoluteMax) {
      if (wickets > 0) {
        const scoring = Math.max(0, balls - wickets);
        const adjMax = scoring * 6;
        return `Score of ${score} in ${overs} overs (${balls} ball(s)) is physically impossible.\n` +
          `  • Absolute maximum (6 per ball): ${absoluteMax} runs\n` +
          `  • With ${wickets} wicket(s), ${wickets} ball(s) used for dismissals → only ${scoring} scoring ball(s) left\n` +
          `  • Wicket-adjusted maximum: ${adjMax} runs (${scoring} × 6)\n` +
          `Your score exceeds both limits. Please recheck.`;
      }
      return `Score of ${score} in ${overs} overs (${balls} ball(s)) is impossible. ` +
        `Maximum achievable is ${absoluteMax} runs (${balls} × 6). Please recheck the score.`;
    }

    // ── Tier 2: Wicket-adjusted maximum ───────────────────────────────
    // Each wicket consumes one delivery with 0 scoring runs (standard dismissals).
    // Scoring balls = total balls − wicket balls.
    // Max score = scoring_balls × 6.
    if (wickets > 0 && wickets <= balls) {
      const scoringBalls = balls - wickets;
      const wicketAdjMax = scoringBalls * 6;

      if (scoringBalls === 0 && score > 0) {
        return `Score of ${score} is impossible: all ${balls} ball(s) resulted in a wicket, ` +
          `leaving 0 balls to score from. Expected score should be 0.`;
      }

      if (score > wicketAdjMax) {
        return `Score of ${score} is not possible with ${wickets} wicket(s) in ${balls} ball(s).\n` +
          `  • ${wickets} ball(s) consumed by dismissal(s) → ${scoringBalls} scoring ball(s) remaining\n` +
          `  • Maximum possible score: ${wicketAdjMax} runs (${scoringBalls} × 6)\n` +
          `Adjust the score to ${wicketAdjMax} or less, or reduce the number of wickets.`;
      }
    }

    // ── Wickets vs balls ─────────────────────────────────────────────
    if (wickets > balls)
      return `${wickets} wickets in ${balls} ball(s) is not possible. ` +
        `At most 1 wicket can fall per ball — maximum here is ${Math.min(balls, 10)}.`;
  }

  // ── Score vs target ──────────────────────────────────────────────────
  if (score >= target)
    return `Current score (${score}) equals or exceeds target (${target}). ` +
      `If the target is already reached, the match is over — it's not ongoing.`;

  // ── Target range ─────────────────────────────────────────────────────
  if (target < 2)
    return `Target of ${target} is too low for a T20 match. Minimum valid target is 2 runs.`;

  if (target > 350)
    return `Target of ${target} is unrealistically high. The IPL/T20 record is ~278 — please double-check.`;

  // ── All-out ───────────────────────────────────────────────────────────
  if (wickets === 10 && balls < 120)
    return `All 10 wickets are out — the innings is complete. ` +
      `The batting team is all out; no further scoring is possible.`;

  // ── Full 20 overs done, target not met ───────────────────────────────
  if (balls >= 120 && score < target)
    return `All 20 overs have been bowled and the target (${target}) has not been reached. ` +
      `The bowling team has already won.`;

  return null;
}

function updateOversSlider(input) {
  const balls = parseInt(input.value);
  document.getElementById('overs-val').textContent = Math.floor(balls / 6) + '.' + (balls % 6);
  input.style.setProperty('--pct', (balls / 120 * 100).toFixed(1) + '%');
}

async function predict() {
  clearInputError();

  const batTeam = document.getElementById('bat-team').value;
  const bowlTeam = document.getElementById('bowl-team').value;
  const city = document.getElementById('host-city').value;
  const target = parseFloat(document.getElementById('target').value);
  const score = parseFloat(document.getElementById('current-score').value);
  const wickets = parseFloat(document.getElementById('wickets').value);
  const oversRaw = parseInt(document.getElementById('overs-slider').value);
  const overs = oversRaw / 6.0;

  if (!batTeam || !bowlTeam) {
    shakeInput('bat-team'); shakeInput('bowl-team');
    showInputError('Please select both a batting team and a bowling team.');
    return;
  }
  if (batTeam === bowlTeam) {
    showInputError('Batting and bowling teams must be different. A team cannot play against itself.');
    return;
  }
  if (!target || target <= 0) {
    shakeInput('target');
    showInputError('Please enter a valid target score (must be a positive number).');
    return;
  }
  if (isNaN(score) || score < 0) {
    shakeInput('current-score');
    showInputError('Current score cannot be negative or empty.');
    return;
  }
  if (isNaN(wickets) || wickets < 0 || wickets > 10) {
    shakeInput('wickets');
    showInputError('Wickets out must be a number between 0 and 10.');
    return;
  }

  const cricketError = validateCricketInputs(oversRaw, score, wickets, target);
  if (cricketError) {
    showInputError(cricketError);
    return;
  }

  const btn = document.querySelector('.btn-predict');
  const orgText = btn.textContent;
  btn.textContent = 'ANALYZING...';
  btn.style.pointerEvents = 'none';

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        batting_team: batTeam, bowling_team: bowlTeam,
        city: city || 'Mumbai', target, score, overs, wickets
      })
    });
    if (!res.ok) throw new Error('Server returned ' + res.status);
    const data = await res.json();
    if (!data.success) {
      showInputError('Prediction error: ' + data.error);
      return;
    }

    const runsNeeded = target - score;
    const ballsLeft = 120 - oversRaw;
    const rrr = ballsLeft > 0 ? (runsNeeded / (ballsLeft / 6)) : 999;
    const crr = overs > 0 ? (score / overs) : 0;
    showResult(data.win_probability, data.loss_probability, batTeam, bowlTeam,
      rrr, crr, runsNeeded, ballsLeft, data.ground_size || '', data.avg_boundary_m || 0);
  } catch (err) {
    console.error(err);
    showInputError('Cannot reach the prediction server. Make sure flask_app.py is running.');
  } finally {
    btn.textContent = orgText;
    btn.style.pointerEvents = 'auto';
  }
}

function shakeInput(id) {
  const el = document.getElementById(id);
  el.style.borderColor = 'var(--red)';
  setTimeout(() => { el.style.borderColor = ''; }, 1500);
}

function showResult(batProb, bowlProb, batTeam, bowlTeam, rrr, crr, runsNeeded, ballsLeft) {
  const panel = document.getElementById('result-panel');
  panel.style.display = 'block';
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  // Update text
  document.getElementById('bat-prob').textContent = batProb + '%';
  document.getElementById('bowl-prob').textContent = bowlProb + '%';
  document.getElementById('bat-team-display').textContent = batTeam;
  document.getElementById('bowl-team-display').textContent = bowlTeam;

  document.getElementById('gauge-pct-text').textContent = batProb + '%';
  document.getElementById('gauge-winner-text').textContent = batProb > 50 ? (batTeam.split(' ').pop() + ' favored').toUpperCase() : (bowlTeam.split(' ').pop() + ' favored').toUpperCase();

  // Stats
  const rrrEl = document.getElementById('rs-rrr');
  const crrEl = document.getElementById('rs-crr');
  rrrEl.textContent = rrr > 99 ? 'N/A' : rrr.toFixed(2);
  crrEl.textContent = crr.toFixed(2);
  document.getElementById('rs-runs').textContent = Math.max(0, Math.round(runsNeeded));
  document.getElementById('rs-balls').textContent = Math.max(0, Math.round(ballsLeft));

  rrrEl.className = 'rs-value ' + (rrr < 7 ? 'good' : rrr < 10 ? 'warn' : 'danger');
  crrEl.className = 'rs-value ' + (crr > rrr ? 'good' : crr > rrr * 0.85 ? 'warn' : 'danger');

  // Animate gauge
  const totalLen = 377;
  const offset = totalLen - (batProb / 100) * totalLen;
  document.getElementById('gauge-fill').style.strokeDashoffset = offset;

  // Needle: -90 deg = 0%, +90 deg = 100%
  const angle = -90 + (batProb / 100) * 180;
  document.getElementById('gauge-needle').style.transform = `rotate(${angle}deg)`;

  // Insight text
  const insight = document.getElementById('prediction-insight');
  let msg = '';
  if (batProb >= 75) msg = `<strong style="color: var(--green);">Strong position for ${batTeam}.</strong> The Required Run Rate is manageable with plenty of wickets in hand. Barring a dramatic collapse, ${batTeam} should wrap this up comfortably.`;
  else if (batProb >= 55) msg = `<strong style="color: var(--gold);">${batTeam} hold the edge</strong>, but this match is far from over. The required rate is under pressure — a couple of quick wickets could swing momentum to ${bowlTeam} rapidly.`;
  else if (batProb >= 45) msg = `<strong style="color: var(--gold);">Too close to call.</strong> The match is evenly poised. Momentum, experience, and the next 2–3 overs will be absolutely decisive. Both teams have a realistic chance here.`;
  else if (batProb >= 25) msg = `<strong style="color: var(--red);">${bowlTeam} are in the driving seat.</strong> The Required Run Rate is climbing steeply and wickets are tumbling. ${batTeam} will need something extraordinary — big hitting and a bit of luck — to pull this off.`;
  else msg = `<strong style="color: var(--red);">Near-impossible task for ${batTeam}.</strong> The mathematics are brutal — the required rate is astronomical with limited resources remaining. Barring a miracle knock, ${bowlTeam} look set for a convincing win.`;

  insight.innerHTML = msg;
}

// ============================================================
// PANEL SWITCHING
// ============================================================
function showPanel(name) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
  event.target.classList.add('active');
}

// ============================================================
// CHARTS
// ============================================================
function renderCharts() {
  // Team win rates (horizontal bar)
  const teamsSorted = Object.entries(TEAM_STATS).sort((a, b) => b[1].winPct - a[1].winPct).slice(0, 10);
  new Chart(document.getElementById('chartTeamWins'), {
    type: 'bar',
    data: {
      labels: teamsSorted.map(([n]) => n.length > 18 ? n.substring(0, 18) + '…' : n),
      datasets: [{
        label: 'Win %',
        data: teamsSorted.map(([, s]) => s.winPct),
        backgroundColor: teamsSorted.map(([, s]) => s.winPct > 55 ? 'rgba(245,200,66,0.75)' : s.winPct > 50 ? 'rgba(45,198,83,0.65)' : 'rgba(79,142,247,0.6)'),
        borderColor: teamsSorted.map(([, s]) => s.winPct > 55 ? '#F5C842' : s.winPct > 50 ? '#2DC653' : '#4F8EF7'),
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#9AA3C4', font: { size: 11 } }, max: 75 },
        y: { grid: { display: false }, ticks: { color: '#F0F2FF', font: { size: 11, family: 'Rajdhani' } } }
      }
    }
  });

  // Toss doughnut
  new Chart(document.getElementById('chartToss'), {
    type: 'doughnut',
    data: {
      labels: ['Toss Winner Wins', 'Toss Winner Loses'],
      datasets: [{
        data: [52.3, 47.7],
        backgroundColor: ['rgba(245,200,66,0.8)', 'rgba(90,98,128,0.4)'],
        borderColor: ['#F5C842', '#2A3050'],
        borderWidth: 2,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed}%` } }
      }
    }
  });

  // Batsmen bar
  new Chart(document.getElementById('chartBatsmen'), {
    type: 'bar',
    data: {
      labels: TOP_BATSMEN.slice(0, 8).map(p => p.name),
      datasets: [{
        label: 'Runs',
        data: TOP_BATSMEN.slice(0, 8).map(p => p.runs),
        backgroundColor: TOP_BATSMEN.slice(0, 8).map(p => p.color + 'BB'),
        borderColor: TOP_BATSMEN.slice(0, 8).map(p => p.color),
        borderWidth: 1,
        borderRadius: 5,
        indexAxis: 'y'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#9AA3C4', font: { size: 11 } } },
        y: { grid: { display: false }, ticks: { color: '#F0F2FF', font: { size: 12, family: 'Rajdhani', weight: '700' } } }
      }
    }
  });

  // Strike rate bubble
  new Chart(document.getElementById('chartSR'), {
    type: 'bubble',
    data: {
      datasets: TOP_BATSMEN.slice(0, 8).map(p => ({
        label: p.name,
        data: [{ x: p.runs, y: p.sr, r: Math.sqrt(p.sixes * 2) + 5 }],
        backgroundColor: p.color + '99',
        borderColor: p.color,
        borderWidth: 2
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => `${ctx.dataset.label}: ${ctx.raw.x} runs, SR ${ctx.raw.y}` } }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#9AA3C4', font: { size: 11 } },
          title: { display: true, text: 'Career Runs', color: '#5A6280', font: { size: 11 } },
          min: 3800, max: 5900
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#9AA3C4', font: { size: 11 } },
          title: { display: true, text: 'Strike Rate', color: '#5A6280', font: { size: 11 } },
          min: 110, max: 160
        }
      }
    }
  });

  // Season stacked bar
  const seasons = Object.keys(SEASON_TEAM_WINS);
  const mainTeams = ['Mumbai Indians', 'Chennai Super Kings', 'Kolkata Knight Riders', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad', 'Rajasthan Royals'];
  const teamColors = { 'Mumbai Indians': '#1B6FF0', 'Chennai Super Kings': '#F5C842', 'Kolkata Knight Riders': '#7B2D8B', 'Royal Challengers Bangalore': '#E63946', 'Sunrisers Hyderabad': '#F5834A', 'Rajasthan Royals': '#2DC653' };

  new Chart(document.getElementById('chartSeasons'), {
    type: 'bar',
    data: {
      labels: seasons.map(s => s.replace('IPL-', '')),
      datasets: mainTeams.map(t => ({
        label: t,
        data: seasons.map(s => SEASON_TEAM_WINS[s][t] || 0),
        backgroundColor: teamColors[t] + 'CC',
        borderColor: teamColors[t],
        borderWidth: 1,
        borderRadius: 2,
        stack: 'wins'
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: { color: '#9AA3C4', font: { size: 11, family: 'Rajdhani' }, boxWidth: 12, boxHeight: 12, padding: 16 }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#9AA3C4', font: { size: 11 } }, stacked: true },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#9AA3C4', font: { size: 11 } }, stacked: true }
      }
    }
  });

  // Venues bar
  const venues = Object.entries(VENUE_STATS);
  new Chart(document.getElementById('chartVenues'), {
    type: 'bar',
    data: {
      labels: venues.map(([n]) => n.length > 20 ? n.substring(0, 20) + '…' : n),
      datasets: [{
        label: 'Bat First Win %',
        data: venues.map(([, v]) => v.pct),
        backgroundColor: venues.map(([, v]) => v.pct > 55 ? 'rgba(230,57,70,0.7)' : v.pct < 40 ? 'rgba(45,198,83,0.7)' : 'rgba(79,142,247,0.7)'),
        borderColor: venues.map(([, v]) => v.pct > 55 ? '#E63946' : v.pct < 40 ? '#2DC653' : '#4F8EF7'),
        borderWidth: 1,
        borderRadius: 5,
        indexAxis: 'y'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#9AA3C4', callback: v => v + '%' }, max: 75 },
        y: { grid: { display: false }, ticks: { color: '#F0F2FF', font: { size: 11, family: 'Rajdhani' } } }
      }
    }
  });

  // POM bar
  new Chart(document.getElementById('chartPOM'), {
    type: 'bar',
    data: {
      labels: POM_LEADERS.map(p => p.name),
      datasets: [{
        label: 'Player of the Match Awards',
        data: POM_LEADERS.map(p => p.pom),
        backgroundColor: POM_LEADERS.map((_, i) => AVATAR_COLORS[i] + 'BB'),
        borderColor: POM_LEADERS.map((_, i) => AVATAR_COLORS[i]),
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#9AA3C4', font: { size: 11, family: 'Rajdhani' }, maxRotation: 35, autoSkip: false } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#9AA3C4' } }
      }
    }
  });

  // Set initial slider gradient
  const slider = document.getElementById('overs-slider');
  slider.style.setProperty('--pct', '50%');
}

// Start
document.addEventListener('DOMContentLoaded', init);
