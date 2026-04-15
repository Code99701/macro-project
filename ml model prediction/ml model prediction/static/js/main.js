let pieChartObj = null;
let analyzerChartObj = null;

const teamColors = {
    'Chennai Super Kings': { p: '#facc15', s: '#eab308', t: '#fde047' },       
    'Mumbai Indians': { p: '#3b82f6', s: '#1d4ed8', t: '#60a5fa' },            
    'Royal Challengers Bangalore': { p: '#ef4444', s: '#b91c1c', t: '#f87171' }, 
    'Kolkata Knight Riders': { p: '#a855f7', s: '#7e22ce', t: '#c084fc' },     
    'Sunrisers Hyderabad': { p: '#f97316', s: '#c2410c', t: '#fb923c' },       
    'Rajasthan Royals': { p: '#ec4899', s: '#be185d', t: '#f472b6' },          
    'Delhi Capitals': { p: '#0ea5e9', s: '#0369a1', t: '#38bdf8' },            
    'Kings XI Punjab': { p: '#dc2626', s: '#991b1b', t: '#ef4444' }            
};

document.addEventListener('DOMContentLoaded', () => {
    if(window.VanillaTilt) {
        VanillaTilt.init(document.querySelectorAll(".tilt-panel"), { max: 5, speed: 400, glare: true, "max-glare": 0.2 });
    }

    const form = document.getElementById('predictForm');
    const submitBtn = document.getElementById('submitBtn');
    const battingSelect = document.getElementById('batting_team');
    const overSlider = document.getElementById('overs');
    const matchSelect = document.getElementById('matchSelect');
    
    battingSelect.addEventListener('change', (e) => {
        const t = e.target.value;
        if(teamColors[t]) {
            document.documentElement.style.setProperty('--theme-primary', teamColors[t].p);
            document.documentElement.style.setProperty('--theme-secondary', teamColors[t].s);
            document.documentElement.style.setProperty('--theme-tertiary', teamColors[t].t);
        }
    });

    overSlider.addEventListener('input', (e) => {
        document.getElementById('overVal').innerText = parseFloat(e.target.value).toFixed(1);
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = getFormData();
        if(formData.batting_team === formData.bowling_team) {
            showToast("Batting and Bowling teams cannot be the same!", "error"); return;
        }
        submitBtn.classList.add('btn-loading'); submitBtn.disabled = true;

        try {
            // Mock API response since we are running locally without backend
            const winProb = Math.floor(Math.random() * 100);
            const timeline = [];
            for(let i=1; i<=20; i++) {
                timeline.push({
                    over: i.toString(),
                    runs: Math.floor(Math.random() * 15),
                    wickets: Math.floor(Math.random() * 2),
                    win_prob: Math.min(100, Math.max(0, winProb + (Math.random() * 20 - 10))),
                    loss_prob: 100 - Math.min(100, Math.max(0, winProb + (Math.random() * 20 - 10)))
                });
            }
            
            const result = {
                success: true,
                batting_team: formData.batting_team,
                bowling_team: formData.bowling_team,
                win_probability: winProb,
                loss_probability: 100 - winProb,
                timeline: timeline
            };

            setTimeout(() => {
                updateResultsUI(result);
                
                // Render the synthesized timeline chart
                document.getElementById('analyzerSection').style.display = 'block';
                document.getElementById('analyzerTitle').innerText = `${formData.batting_team} Chase Target - ${formData.target}`;
                renderAnalyzerChart(result);

                fetchHistory(); // Updates global db
                if(result.win_probability >= 90 || result.win_probability <= 10) triggerConfetti();
                showToast("Prediction Engine Analysis Complete!", "success");
                
                submitBtn.classList.remove('btn-loading'); submitBtn.disabled = false;
            }, 800); // Simulate network delay
        } catch (error) {
            console.error(error); showToast("Failed to run prediction simulation.", "error");
            submitBtn.classList.remove('btn-loading'); submitBtn.disabled = false;
        }
    });

    fetchHistory();
});

function getFormData() {
    return {
        batting_team: document.getElementById('batting_team').value, bowling_team: document.getElementById('bowling_team').value,
        city: document.getElementById('city').value,
        target: parseInt(document.getElementById('target').value) || 0, score: parseInt(document.getElementById('score').value) || 0,
        overs: parseFloat(document.getElementById('overs').value) || 0, wickets: parseInt(document.getElementById('wickets').value) || 0
    };
}

function updateResultsUI(result) {
    document.getElementById('resBattingTeam').textContent = result.batting_team;
    document.getElementById('resBowlingTeam').textContent = result.bowling_team;
    animateValue("resBattingProb", 0, result.win_probability, 1000);
    animateValue("resBowlingProb", 0, result.loss_probability, 1000);
    document.getElementById('progressBar').style.width = `${result.win_probability}%`;
    const rPanel = document.getElementById('resultsPanel');
    rPanel.style.display = 'block';
    if(window.VanillaTilt) { rPanel.vanillaTilt.destroy(); VanillaTilt.init(rPanel); }
}

async function fetchHistory() {
    try {
        // Mock data for analytics
        const data = {
            success: true,
            history: [
                { batting_team: 'Chennai Super Kings', bowling_team: 'Mumbai Indians', city: 'Mumbai', target: 180, score: 100, wickets: 3, overs: 12, win_probability: 45, loss_probability: 55 },
                { batting_team: 'Royal Challengers Bangalore', bowling_team: 'Delhi Capitals', city: 'Bangalore', target: 200, score: 180, wickets: 2, overs: 18, win_probability: 80, loss_probability: 20 }
            ],
            avg_win: 48,
            avg_loss: 52,
            top_teams: [
                { team: 'Chennai Super Kings', count: 120 },
                { team: 'Mumbai Indians', count: 110 },
                { team: 'Royal Challengers Bangalore', count: 95 }
            ]
        };

        const list = document.getElementById('historyList');
        list.innerHTML = '';
        data.history.forEach(item => {
            const h = document.createElement('div'); h.className = 'history-item';
            h.innerHTML = `
                <div><div class="hist-matchup">${item.batting_team} vs ${item.bowling_team}</div>
                <div class="hist-details">${item.city} | T:${item.target} | ${item.score}/${item.wickets} in ${item.overs}v</div></div>
                <div class="hist-result"><span class="hist-bat">${item.win_probability}%</span> - <span class="hist-bowl">${item.loss_probability}%</span></div>
            `;
            list.appendChild(h);
        });

        document.getElementById('avgWinProb').innerText = data.avg_win + "%";
        document.getElementById('avgLossProb').innerText = data.avg_loss + "%";
        renderPieChart(data.top_teams);
    } catch (e) { console.error(e); }
}



// ========================
// EXACT REPLICATION OF MATPLOTLIB JUPYTER GRAPH
// ========================
function renderAnalyzerChart(data) {
    const ctx = document.getElementById('analyzerChart').getContext('2d');
    if(analyzerChartObj) analyzerChartObj.destroy();

    const labels = data.timeline.map(t => t.over);
    const runs = data.timeline.map(t => t.runs);
    const wickets = data.timeline.map(t => t.wickets);
    const winProbs = data.timeline.map(t => t.win_prob);
    const lossProbs = data.timeline.map(t => t.loss_prob);

    analyzerChartObj = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Win Prob (Batting)',
                    data: winProbs,
                    type: 'line',
                    borderColor: 'red', // Exact as requested
                    borderWidth: 4,
                    tension: 0.1,
                    yAxisID: 'y-prob',
                    pointRadius: 2,
                    pointBackgroundColor: 'red'
                },
                {
                    label: 'Win Prob (Bowling)',
                    data: lossProbs,
                    type: 'line',
                    borderColor: '#00a65a', // Exact Green from notebook
                    borderWidth: 4,
                    tension: 0.1,
                    yAxisID: 'y-prob',
                    pointRadius: 2,
                    pointBackgroundColor: '#00a65a'
                },
                {
                    label: 'Wickets',
                    data: wickets,
                    type: 'line',
                    borderColor: 'yellow', // Exact Yellow
                    borderWidth: 3,
                    tension: 0.1,
                    yAxisID: 'y-runs',
                    pointRadius: 3,
                    pointBackgroundColor: 'yellow'
                },
                {
                    label: 'Runs Scored',
                    data: runs,
                    backgroundColor: '#1f77b4', // Classic Matplotlib blue
                    barPercentage: 0.8,
                    yAxisID: 'y-runs'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#ffffff' },
                    title: { display: false }
                },
                'y-prob': {
                    type: 'linear', position: 'left', min: 0, max: 100,
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { color: '#ffffff', stepSize: 20 },
                    title: { display: false }
                },
                'y-runs': {
                    type: 'linear', position: 'right', min: 0, max: 35,
                    grid: { drawOnChartArea: false }, 
                    ticks: { color: '#ffffff', stepSize: 5 },
                    title: { display: false }
                }
            },
            plugins: {
                legend: { display: false }, // Hiding legend to exactly match the look of the notebook graph
                tooltip: { backgroundColor: 'rgba(15, 23, 42, 0.9)', titleColor: '#fff', bodyColor: '#cbd5e1' }
            }
        }
    });
}

function renderPieChart(topTeamsArray) {
    const ctx = document.getElementById('pieChart').getContext('2d');
    if(pieChartObj) pieChartObj.destroy();
    if(!topTeamsArray || topTeamsArray.length === 0) return;
    pieChartObj = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: topTeamsArray.map(t => t.team),
            datasets: [{
                data: topTeamsArray.map(t => t.count), backgroundColor: ['#3b82f6', '#ec4899', '#facc15', '#a855f7', '#0ea5e9'], borderWidth: 0
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: '#fff', font: {family: 'Outfit'} } } } }
    });
}

// ========================
// UTILS
// ========================

window.switchTab = function(tabId) {
    document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tabId).style.display = 'grid';
    event.target.classList.add('active');
}

function showToast(msg, type="success") {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`; toast.innerText = msg;
    container.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 50);
    setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 400); }, 4000);
}

function animateValue(id, start, end, duration) {
    if (start === end) return;
    const obj = document.getElementById(id); let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start) + "%";
        if (progress < 1) window.requestAnimationFrame(step);
    }; window.requestAnimationFrame(step);
}

function triggerConfetti() {
    const canvas = document.getElementById('particleCanvas'); const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    const particles = [];
    for(let i=0; i<100; i++) {
        particles.push({ x: canvas.width/2, y: canvas.height/2, vx: (Math.random() - 0.5) * 15, vy: (Math.random() - 0.5) * 15, size: Math.random() * 5 + 2, color: `hsl(${Math.random()*360}, 100%, 50%)`, life: 1 });
    }
    function renderParticles() {
        ctx.clearRect(0,0, canvas.width, canvas.height); let alive = false;
        particles.forEach(p => {
            if(p.life > 0) {
                alive = true; p.x += p.vx; p.y += p.vy; p.vy += 0.2; p.life -= 0.01;
                ctx.globalAlpha = p.life; ctx.fillStyle = p.color; ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
            }
        });
        if(alive) requestAnimationFrame(renderParticles); else ctx.clearRect(0,0, canvas.width, canvas.height);
    } renderParticles();
}
