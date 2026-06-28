from flask import Flask, render_template_string, request
from flask_socketio import SocketIO
import threading, random, time, json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bangkokmap2024'
socketio = SocketIO(app, cors_allowed_origins="*")

DISTRICTS = [
    "Phra Nakhon", "Dusit", "Nong Chok", "Bang Rak", "Bang Khen",
    "Bang Kapi", "Samphanthawong", "Bangkok Yai", "Bangkok Noi", "Bang Khun Thian",
    "Bang Phlat", "Bang Sue", "Bang Kho Laem", "Bang Na", "Bang Bon",
    "Bang Pak", "Phasi Charoen", "Yannawa", "Sathon", "Silom",
    "Khlong Toei", "Huai Khwang", "Din Daeng", "Ratchathewi", "Phaya Thai",
    "Watthana", "Pathum Wan", "Pom Prap Sattru Phai", "Pracha Thipat", "Min Buri",
    "Lak Si", "Sai Mai", "Chatuchak", "Don Mueang", "Lat Phrao",
    "Wang Thonglang", "Saphan Sung", "Khlong Sam Wa", "Thawi Watthana", "Thung Khru",
    "Rat Burana", "Romklao", "Khlong Toei", "Suan Luang", "Chom Thong",
    "Bukkhalo", "Bang Bon", "Taling Chan", "Thonburi", "Phra Pradaeng",
    "Nong Khaem", "Bang Khae", "Phra Khanong", "Punnawithi", "Yan Nawa"
]

THAI_NAMES = {
    "Phra Nakhon": "พระนคร", "Dusit": "ดุสิต", "Nong Chok": "หนองจอก",
    "Bang Rak": "บางรัก", "Bang Khen": "บางเขน", "Bang Kapi": "บางกะปิ",
    "Samphanthawong": "สัมพันธวงศ์", "Bangkok Yai": "กรุงเทพยai", "Bangkok Noi": "บางกอกน้อย",
    "Bang Khun Thian": "บางขุนเทียน", "Bang Phlat": "บางพลัด", "Bang Sue": "บางซื่อ",
    "Bang Kho Laem": "บางโคล่ม", "Bang Na": "บางนา", "Bang Bon": "บางบอน",
    "Bang Pak": "บางปะกง", "Phasi Charoen": "พาสีชาร์จ", "Yannawa": "ยานนาวา",
    "Sathon": "สาทร", "Silom": "สีลม", "Khlong Toei": "คลองเตย",
    "Huai Khwang": "ห้วยขวาง", "Din Daeng": "ดินแดง", "Ratchathewi": "ราชเทวี",
    "Phaya Thai": "พญาไท", "Watthana": "วัฒนา", "Pathum Wan": "ปทุมวัน",
    "Pom Prap Sattru Phai": "ป้อมปราบศัตรูพ่าย", "Pracha Thipat": "ประชาธิปัตย์",
    "Min Buri": "มีนบุรี", "Lak Si": "หลักสี่", "Sai Mai": "สายไหม",
    "Chatuchak": "จตุจักร", "Don Mueang": "ดอนเมืองหล", "Lat Phrao": "ลาดพร้าว",
    "Wang Thonglang": "วังทองหลาง", "Saphan Sung": "สะพานสูง", "Khlong Sam Wa": "คลองสามวา",
    "Thawi Watthana": "ธาวี วัฒนา", "Thung Khru": "ทุ่งครุ", "Rat Burana": "ราษฎร์บูรณะ",
    "Romklao": "รมเกล้า", "Suan Luang": "สวนหลวง", "Chom Thong": "จอมทอง",
    "Bukkhalo": "บึงกาฬ", "Taling Chan": "ตลิ่งชัน", "Thonburi": "ธนบุรี",
    "Phra Pradaeng": "พระประแดง", "Nong Khaem": "หนองแขม", "Bang Khae": "บางแค",
    "Phra Khanong": "พระโขนง", "Punnawithi": "พุทธมณฑล", "Yan Nawa": "ยานนาวา"
}

# --- Major Bangkok roads (approximate waypoints) used both to draw the road
# network on the map and as "tracks" that mock GPS agents travel along ---
ROADS = {
    "Sukhumvit Rd": [
        [13.7440, 100.5340], [13.7367, 100.5606], [13.7300, 100.5780],
        [13.7100, 100.6050], [13.6950, 100.6300], [13.6700, 100.6700]
    ],
    "Silom Rd": [
        [13.7287, 100.5345], [13.7245, 100.5290], [13.7200, 100.5230],
        [13.7235, 100.5180]
    ],
    "Rama IV Rd": [
        [13.7440, 100.5130], [13.7300, 100.5300], [13.7200, 100.5430],
        [13.7050, 100.5600], [13.6950, 100.5750], [13.6920, 100.5800]
    ],
    "Phetchaburi Rd": [
        [13.7530, 100.4980], [13.7540, 100.5300], [13.7555, 100.5600],
        [13.7570, 100.5850], [13.7600, 100.6100]
    ],
    "Ratchadaphisek Rd": [
        [13.7700, 100.5300], [13.7780, 100.5650], [13.7900, 100.5780],
        [13.8050, 100.5750], [13.8200, 100.5700]
    ],
    "Vibhavadi Rangsit Rd": [
        [13.7900, 100.5500], [13.8200, 100.5550], [13.8500, 100.5600],
        [13.8800, 100.5650], [13.9100, 100.6050]
    ],
    "Phahonyothin Rd": [
        [13.7980, 100.5560], [13.8200, 100.5610], [13.8450, 100.5650],
        [13.8700, 100.6000], [13.9000, 100.6200]
    ],
    "Charoen Krung Rd": [
        [13.7470, 100.5010], [13.7350, 100.5100], [13.7220, 100.5160],
        [13.7050, 100.5120], [13.6920, 100.5080]
    ],
    "Lat Phrao Rd": [
        [13.7950, 100.5700], [13.8050, 100.5950], [13.8150, 100.6200],
        [13.8200, 100.6450]
    ],
    "Rama IX Rd": [
        [13.7560, 100.5700], [13.7600, 100.5900], [13.7650, 100.6150],
        [13.7700, 100.6400]
    ],
    "Sathon Rd": [
        [13.7220, 100.5210], [13.7180, 100.5260], [13.7150, 100.5310],
        [13.7090, 100.5380]
    ],
    "Bangna-Trad Rd": [
        [13.6700, 100.6050], [13.6650, 100.6350], [13.6600, 100.6700],
        [13.6550, 100.7050]
    ],
    "Chan Rd / Thonburi": [
        [13.7050, 100.5050], [13.6950, 100.4950], [13.6800, 100.4850],
        [13.6600, 100.4800]
    ],
    "Kanchanaphisek Rd (West)": [
        [13.7900, 100.3400], [13.7500, 100.3500], [13.7100, 100.3650],
        [13.6700, 100.3800], [13.6300, 100.4000]
    ],
    "Ramkhamhaeng Rd": [
        [13.7550, 100.6100], [13.7650, 100.6400], [13.7750, 100.6700],
        [13.7850, 100.7000]
    ],
}

# Mock "live GPS" agents — each travels back and forth along one of the
# roads above, so the map shows little dots moving on real streets.
GPS_AGENTS = []
def _init_gps_agents(n=180):
    GPS_AGENTS.clear()
    road_names = list(ROADS.keys())
    for i in range(n):
        road = random.choice(road_names)
        pts = ROADS[road]
        GPS_AGENTS.append({
            "id": i,
            "road": road,
            "seg": random.randint(0, len(pts) - 2),
            "t": random.random(),
            "dir": random.choice([1, -1]),
            "speed": random.uniform(0.01, 0.035),
        })
_init_gps_agents()

def _lerp(a, b, t):
    return a + (b - a) * t

def step_gps_agents():
    """Advance every mock GPS agent a little along its road and return positions."""
    out = []
    for ag in GPS_AGENTS:
        pts = ROADS[ag["road"]]
        ag["t"] += ag["speed"] * ag["dir"]
        if ag["t"] >= 1.0:
            ag["t"] = 0.0
            ag["seg"] += ag["dir"]
        elif ag["t"] <= 0.0:
            ag["t"] = 1.0
            ag["seg"] += ag["dir"]
        if ag["seg"] >= len(pts) - 1:
            ag["seg"] = len(pts) - 2
            ag["dir"] = -1
        elif ag["seg"] <= 0:
            ag["seg"] = 0
            ag["dir"] = 1
        p0, p1 = pts[ag["seg"]], pts[ag["seg"] + 1]
        lat = _lerp(p0[0], p1[0], ag["t"])
        lng = _lerp(p0[1], p1[1], ag["t"])
        out.append({"id": ag["id"], "lat": round(lat, 6), "lng": round(lng, 6)})
    return out

def mock_gps_feed():
    """Background thread: pushes simulated live GPS pings every second."""
    while True:
        time.sleep(1.0)
        socketio.emit('gps_tick', {"agents": step_gps_agents()})

# Initial seed — scaled to 10M total population
populations = {d: 0 for d in DISTRICTS}
populations["Pathum Wan"] = 450000  # CBD peak
populations["Huai Khwang"] = 380000
populations["Ratchathewi"] = 320000
populations["Bang Rak"] = 290000
populations["Khlong Toei"] = 270000
populations["Samphanthawong"] = 250000
populations["Chatuchak"] = 240000
populations["Phaya Thai"] = 220000
populations["Sathon"] = 200000

# Time-based population patterns (scaled to 10M)
TIME_PATTERNS = {
    "🌅 05:00 (Early Morning)": {
        "description": "Joggers, monks, early workers • Very quiet",
        "BUSY": {"Phra Nakhon": (80000, 150000), "Chatuchak": (50000, 100000)},
        "MEDIUM": {"Pathum Wan": (150000, 250000), "Bang Rak": (80000, 120000)},
        "QUIET": {d: (5000, 20000) for d in DISTRICTS if d not in ["Phra Nakhon","Chatuchak","Pathum Wan","Bang Rak"]}
    },
    "🚌 07:00 (Morning Rush)": {
        "description": "BTS/MRT packed, office rush • VERY CROWDED",
        "BUSY": {"Pathum Wan": (800000, 1200000), "Ratchathewi": (600000, 900000), "Huai Khwang": (550000, 800000), "Phaya Thai": (500000, 750000)},
        "MEDIUM": {"Bang Rak": (350000, 500000), "Khlong Toei": (300000, 450000), "Sathon": (250000, 350000)},
        "QUIET": {d: (20000, 80000) for d in DISTRICTS if d not in ["Pathum Wan","Ratchathewi","Huai Khwang","Phaya Thai","Bang Rak","Khlong Toei","Sathon"]}
    },
    "☀️ 10:00 (Mid Morning)": {
        "description": "Offices busy, malls opening • Moderately crowded",
        "BUSY": {"Pathum Wan": (700000, 1000000), "Chatuchak": (450000, 700000), "Ratchathewi": (400000, 600000)},
        "MEDIUM": {"Huai Khwang": (350000, 500000), "Bang Rak": (300000, 400000), "Khlong Toei": (250000, 350000)},
        "QUIET": {d: (30000, 100000) for d in DISTRICTS if d not in ["Pathum Wan","Chatuchak","Ratchathewi","Huai Khwang","Bang Rak","Khlong Toei"]}
    },
    "🍽️ 12:00 (Lunch Time)": {
        "description": "Restaurants packed, malls peak • EXTREMELY CROWDED",
        "BUSY": {"Pathum Wan": (1000000, 1400000), "Bang Rak": (700000, 1000000), "Sathon": (600000, 850000), "Khlong Toei": (580000, 800000), "Ratchathewi": (500000, 700000)},
        "MEDIUM": {"Huai Khwang": (400000, 600000), "Chatuchak": (350000, 550000), "Phaya Thai": (300000, 450000)},
        "QUIET": {d: (50000, 150000) for d in DISTRICTS if d not in ["Pathum Wan","Bang Rak","Sathon","Khlong Toei","Ratchathewi","Huai Khwang","Chatuchak","Phaya Thai"]}
    },
    "☕ 14:00 (Afternoon)": {
        "description": "Shopping centers, schools • Moderately crowded",
        "BUSY": {"Pathum Wan": (750000, 1100000), "Chatuchak": (400000, 650000), "Bang Rak": (400000, 600000)},
        "MEDIUM": {"Khlong Toei": (300000, 450000), "Ratchathewi": (250000, 400000), "Sathon": (250000, 350000)},
        "QUIET": {d: (40000, 120000) for d in DISTRICTS if d not in ["Pathum Wan","Chatuchak","Bang Rak","Khlong Toei","Ratchathewi","Sathon"]}
    },
    "🚗 17:00 (Evening Rush)": {
        "description": "Heavy traffic, BTS overflowing, malls packed • CHAOS",
        "BUSY": {"Pathum Wan": (1100000, 1500000), "Ratchathewi": (800000, 1100000), "Huai Khwang": (700000, 950000), "Bang Rak": (800000, 1100000), "Khlong Toei": (750000, 1000000), "Chatuchak": (600000, 850000)},
        "MEDIUM": {"Sathon": (450000, 650000), "Phaya Thai": (400000, 600000), "Din Daeng": (300000, 450000)},
        "QUIET": {d: (80000, 250000) for d in DISTRICTS if d not in ["Pathum Wan","Ratchathewi","Huai Khwang","Bang Rak","Khlong Toei","Chatuchak","Sathon","Phaya Thai","Din Daeng"]}
    },
    "🎭 19:00 (Evening)": {
        "description": "Restaurants/bars busy, late shopping • Very crowded",
        "BUSY": {"Pathum Wan": (900000, 1300000), "Bang Rak": (700000, 1000000), "Chatuchak": (500000, 800000), "Khlong Toei": (600000, 850000)},
        "MEDIUM": {"Sathon": (400000, 600000), "Huai Khwang": (350000, 500000), "Phaya Thai": (300000, 450000)},
        "QUIET": {d: (60000, 200000) for d in DISTRICTS if d not in ["Pathum Wan","Bang Rak","Chatuchak","Khlong Toei","Sathon","Huai Khwang","Phaya Thai"]}
    },
    "🌙 21:00 (Night)": {
        "description": "Entertainment peak, some dispersal • Moderately crowded",
        "BUSY": {"Pathum Wan": (650000, 950000), "Bang Rak": (550000, 800000), "Chatuchak": (350000, 550000), "Khlong Toei": (450000, 650000)},
        "MEDIUM": {"Sathon": (300000, 450000), "Huai Khwang": (250000, 400000), "Ratchathewi": (200000, 350000)},
        "QUIET": {d: (40000, 150000) for d in DISTRICTS if d not in ["Pathum Wan","Bang Rak","Chatuchak","Khlong Toei","Sathon","Huai Khwang","Ratchathewi"]}
    },
    "🌃 23:00 (Late Night)": {
        "description": "Very quiet, night venues only • Mostly sleeping",
        "BUSY": {"Bang Rak": (200000, 400000), "Khlong Toei": (150000, 300000), "Chatuchak": (80000, 200000)},
        "MEDIUM": {"Pathum Wan": (120000, 280000), "Ratchathewi": (80000, 180000)},
        "QUIET": {d: (5000, 50000) for d in DISTRICTS if d not in ["Bang Rak","Khlong Toei","Chatuchak","Pathum Wan","Ratchathewi"]}
    },
}

events = []

def randomize_by_time(time_period):
    """Randomize population based on selected time period."""
    global populations
    pattern = TIME_PATTERNS.get(time_period, {})
    populations = {d: 0 for d in DISTRICTS}
    
    for district, (lo, hi) in pattern.get("BUSY", {}).items():
        if district in populations:
            populations[district] = random.randint(lo, hi)
    
    for district, (lo, hi) in pattern.get("MEDIUM", {}).items():
        if district in populations:
            populations[district] = random.randint(lo, hi)
    
    for district_dict in [pattern.get("QUIET", {})]:
        for district, (lo, hi) in district_dict.items():
            if district in populations:
                populations[district] = random.randint(lo, hi)
    
    socketio.emit('populations_reset', {'populations': populations})

def mock_live_feed():
    """Simulates real-time people moving between provinces."""
    BUSY = ["Pathum Wan","Ratchathewi","Huai Khwang","Bang Rak","Khlong Toei","Samphanthawong","Chatuchak","Phaya Thai"]
    QUIET = [d for d in DISTRICTS if d not in BUSY]

    actions = [
        ("📱 Check-in", 100, 800),
        ("🚌 Group arrived", 1000, 8000),
        ("🎉 Event started", 5000, 30000),
        ("🚶 People leaving", -500, -4000),
        ("🏖️ Tourists arrived", 2000, 15000),
        ("🏠 Residents returned", 500, 3000),
        ("🚗 Traffic surge", 3000, 20000),
    ]

    while True:
        time.sleep(random.uniform(1.5, 3.5))

        if random.random() < 0.65:
            district = random.choice(BUSY)
        else:
            district = random.choice(QUIET)

        action_label, mn, mx = random.choice(actions)
        delta = random.randint(min(mn,mx), max(mn,mx))

        populations[district] = max(0, populations[district] + delta)

        if random.random() < 0.02:
            district = random.choice(DISTRICTS)
            populations[district] += random.randint(5000, 20000)
            action_label = "🔥 MAJOR EVENT"

        socketio.emit('population_update', {
            "district": district,
            "count": populations[district],
            "delta": delta,
            "action": action_label,
            "thai": THAI_NAMES.get(district, "")
        })

@app.route('/')
def index():
    time_options = json.dumps(list(TIME_PATTERNS.keys()), ensure_ascii=False)
    return render_template_string(HTML,
        thai_names=json.dumps(THAI_NAMES, ensure_ascii=False),
        init_populations=json.dumps(populations, ensure_ascii=False),
        time_options=time_options,
        roads_json=json.dumps(ROADS, ensure_ascii=False),
        district_names_json=json.dumps(DISTRICTS, ensure_ascii=False)
    )

@app.route('/api/randomize', methods=['POST'])
def randomize_endpoint():
    data = request.json
    time_period = data.get('time_period')
    if time_period in TIME_PATTERNS:
        randomize_by_time(time_period)
        return {'ok': True, 'message': f'Randomized to {time_period}', 'populations': populations}
    return {'ok': False, 'error': 'Invalid time period'}, 400

HTML = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>🗺️ Bangkok Live Population 10M</title>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://cdn.socket.io/4.7.4/socket.io.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Sarabun',sans-serif;background:#0d1117;color:#e6edf3;height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{background:linear-gradient(90deg,#161b22,#1f2937);border-bottom:1px solid #30363d;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
header h1{font-size:1rem;font-weight:700;background:linear-gradient(90deg,#58a6ff,#ff6b6b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.header-right{display:flex;gap:16px;align-items:center}
.clock{font-size:1.3rem;font-weight:700;color:#3fb950;font-family:monospace;min-width:80px}
.live-badge{display:flex;align-items:center;gap:6px;font-size:0.72rem;color:#3fb950;font-weight:600}
.pulse{width:8px;height:8px;border-radius:50%;background:#3fb950;animation:pulse 1.2s infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.4;transform:scale(1.4)}}
.legend{display:flex;align-items:center;gap:8px;font-size:0.65rem;color:#8b949e}
.legend-bar{width:100px;height:8px;border-radius:4px;background:linear-gradient(90deg,#1565c0,#80deea,#fff9c4,#ff9800,#e53935,#b71c1c);border:1px solid #30363d}
.main{display:flex;flex:1;overflow:hidden}
#map{flex:1;background:#0d1117}
.panel{width:320px;background:#161b22;border-left:1px solid #30363d;display:flex;flex-direction:column;overflow:hidden}
.panel-tabs{display:flex;border-bottom:1px solid #30363d}
.tab{flex:1;padding:10px;text-align:center;font-size:0.75rem;font-weight:600;cursor:pointer;color:#8b949e;border-bottom:2px solid transparent}
.tab.active{color:#58a6ff;border-bottom-color:#58a6ff;background:#1f2937}
.tab-content{display:none;flex:1;flex-direction:column;overflow:hidden}
.tab-content.active{display:flex}
.controls{padding:12px;border-bottom:1px solid #30363d;background:#1f2937}
.control-group{margin-bottom:10px}
.control-group label{font-size:0.68rem;color:#8b949e;text-transform:uppercase;margin-bottom:4px;display:block}
.control-group input[type=range]{width:100%;accent-color:#58a6ff;cursor:pointer}
.time-labels{display:flex;justify-content:space-between;font-size:0.6rem;color:#484f58;margin-top:2px}
.btn-randomize{width:100%;padding:8px;background:#f97316;color:#fff;border:none;border-radius:6px;font-weight:600;font-family:'Sarabun',sans-serif;font-size:0.78rem;cursor:pointer}
.btn-randomize:hover{background:#ea580c}
.feed-list{flex:1;overflow-y:auto;padding:6px}
.feed-item{padding:8px 10px;border-radius:6px;margin-bottom:4px;border-left:3px solid;background:#0d1117;animation:slideIn 0.3s ease;font-size:0.74rem}
@keyframes slideIn{from{opacity:0;transform:translateX(10px)}to{opacity:1;transform:translateX(0)}}
.feed-item.pos{border-left-color:#3fb950}.feed-item.neg{border-left-color:#f85149}.feed-item.surge{border-left-color:#ff9800;background:#1a1500}
.feed-action{color:#8b949e;margin-bottom:2px}
.feed-province{font-weight:700;color:#e6edf3}
.feed-delta{font-weight:700;font-size:0.8rem}
.feed-delta.pos{color:#3fb950}.feed-delta.neg{color:#f85149}
.rank-list{flex:1;overflow-y:auto;padding:6px}
.rank-item{padding:7px 10px;border-radius:6px;margin-bottom:3px;cursor:pointer;border:1px solid transparent;transition:all 0.15s;font-size:0.75rem}
.rank-item:hover{background:#21262d;border-color:#30363d}
.rank-item-row{display:flex;gap:8px;align-items:center}
.rank-num{font-weight:700;color:#484f58;font-size:0.68rem;min-width:20px}
.rank-bar-wrap{height:6px;background:#21262d;border-radius:3px;overflow:hidden;flex:1}
.rank-bar{height:100%;border-radius:3px;transition:width 0.5s ease}
.rank-count{font-weight:700;min-width:50px;text-align:right;font-size:0.73rem}
.stats-bar{padding:8px 12px;border-top:1px solid #30363d;background:#161b22;font-size:0.68rem;color:#8b949e;display:flex;gap:12px;flex-shrink:0}
.stat{display:flex;flex-direction:column}.stat-val{font-size:0.9rem;font-weight:700;color:#e6edf3}
.leaflet-container{background:#0d1117!important}
.tooltip-custom{background:rgba(13,17,23,0.95)!important;border:1px solid #30363d!important;border-radius:8px!important;color:#e6edf3!important;padding:8px 12px!important;font-family:'Sarabun',sans-serif!important;font-size:0.78rem!important}
.feed-list::-webkit-scrollbar,.rank-list::-webkit-scrollbar{width:4px}
.feed-list::-webkit-scrollbar-thumb,.rank-list::-webkit-scrollbar-thumb{background:#30363d;border-radius:2px}
</style>
</head>
<body>
<header>
  <h1>🗺️ Bangkok Live Population (10M people)</h1>
  <div class="header-right">
    <div class="clock" id="clock">00:00</div>
    <div class="legend">
      <span>Empty</span>
      <div class="legend-bar"></div>
      <span>Crowded</span>
      <span style="margin-left:10px;color:#39ff88">●</span><span>Live GPS</span>
    </div>
    <div class="live-badge"><div class="pulse"></div>LIVE</div>
  </div>
</header>
<div class="main">
  <div id="map"></div>
  <div class="panel">
    <div class="panel-tabs">
      <div class="tab active" onclick="switchTab('feed',this)">📡 Feed</div>
      <div class="tab" onclick="switchTab('time',this)">⏰ Time</div>
      <div class="tab" onclick="switchTab('ranks',this)">🏆 Top</div>
    </div>

    <!-- FEED TAB -->
    <div class="tab-content active" id="tab-feed">
      <div class="feed-list" id="feed-list"></div>
    </div>

    <!-- TIME TAB -->
    <div class="tab-content" id="tab-time">
      <div class="controls">
        <div class="control-group">
          <label>⏰ Time Slider (24h)</label>
          <input type="range" id="time-slider" min="5" max="23" value="12" oninput="onTimeSlide()"/>
          <div class="time-labels">
            <span>05:00</span><span id="time-display">12:00</span><span>23:00</span>
          </div>
        </div>
        <button class="btn-randomize" onclick="randomizeBySlider()">🎲 Randomize This Time</button>
        <div style="margin-top:8px;padding:8px;background:#0d1117;border-radius:6px;font-size:0.68rem;color:#8b949e;line-height:1.4">
          <strong>Time Context:</strong><br/>
          <span id="time-context">Select time to see realistic Bangkok patterns</span>
        </div>
      </div>
    </div>

    <!-- RANKINGS TAB -->
    <div class="tab-content" id="tab-ranks">
      <div class="rank-list" id="rank-list"></div>
    </div>

    <div class="stats-bar">
      <div class="stat"><span class="stat-val" id="total-pop">0</span><span>Total People</span></div>
      <div class="stat"><span class="stat-val" id="active-districts">0</span><span>Active</span></div>
      <div class="stat"><span class="stat-val" id="events-min">0</span><span>Events/min</span></div>
    </div>
  </div>
</div>

<script>
const THAI_NAMES = {{ thai_names | safe }};
const initPops = {{ init_populations | safe }};
const TIME_PATTERNS_LIST = {{ time_options | safe }};
const ROADS = {{ roads_json | safe }};
const BKK_DISTRICT_NAMES = {{ district_names_json | safe }};
const BKK_BOUNDS = [[13.49, 100.32], [13.96, 100.94]]; // tight Bangkok-only bbox

let populations = {...initPops};
let map, geojsonLayer, layerMap = {};
let gpsLayer, gpsMarkers = {};
let selectedDistrict = null;
let eventCount = 0, eventsLastMin = 0;
const allDistricts = Object.keys(THAI_NAMES).sort();

// SocketIO - CREATE FIRST
const socket = io();

socket.on('populations_reset', data => {
  populations = data.populations;
  Object.keys(populations).forEach(d => refreshLayer(d));
  renderRankings();
  updateStats();
});

socket.on('population_update', data => {
  populations[data.district] = data.count;
  eventCount++;
  refreshLayer(data.district);
  addFeedItem(data);
  renderRankings();
  updateStats();
});

socket.on('gps_tick', data => {
  updateGpsAgents(data.agents);
});

// Live Clock
function updateClock() {
  const now = new Date();
  const h = String(now.getHours()).padStart(2,'0');
  const m = String(now.getMinutes()).padStart(2,'0');
  document.getElementById('clock').textContent = h + ':' + m;
}
setInterval(updateClock, 1000);
updateClock();

// Time Slider
function onTimeSlide() {
  const hour = parseInt(document.getElementById('time-slider').value);
  document.getElementById('time-display').textContent = String(hour).padStart(2,'0') + ':00';
  updateTimeContext(hour);
}

function updateTimeContext(hour) {
  const contexts = {
    5: "🌅 Early commuters, joggers • Very quiet",
    7: "🚌 BTS/MRT packed • CROWDED",
    10: "☀️ Office hours, malls open • Moderate",
    12: "🍽️ Lunch rush peak • EXTREMELY CROWDED",
    14: "☕ Afternoon shopping • Moderate",
    17: "🚗 Evening rush hour • CHAOS",
    19: "🎭 Restaurants/bars busy • Very crowded",
    21: "🌙 Night venues peak • Crowded",
    23: "🌃 Late night • Very quiet"
  };
  document.getElementById('time-context').textContent = contexts[hour] || "Regular time";
}

function randomizeBySlider() {
  const hour = parseInt(document.getElementById('time-slider').value);
  const timeLabel = String(hour).padStart(2,'0') + ":00";
  
  // Find closest time pattern
  const hours = [5,7,10,12,14,17,19,21,23];
  const closest = hours.reduce((p,c) => Math.abs(c-hour) < Math.abs(p-hour) ? c : p);
  const timeKey = TIME_PATTERNS_LIST.find(t => t.includes(String(closest).padStart(2,'0') + ':00'));
  
  if (!timeKey) { alert('No pattern for this time'); return; }
  
  fetch('/api/randomize', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({time_period: timeKey})
  })
  .then(r => r.json())
  .then(data => {
    if (data.ok) {
      populations = data.populations;
      Object.keys(populations).forEach(d => refreshLayer(d));
      renderRankings();
      updateStats();
    }
  });
}

function getColor(pop) {
  if (pop === 0) return {fill:'#1565c0', opacity:0.12};
  if (pop < 100000) return {fill:'#1976d2', opacity:0.3};
  if (pop < 300000) return {fill:'#42a5f5', opacity:0.45};
  if (pop < 600000) return {fill:'#80deea', opacity:0.52};
  if (pop < 800000) return {fill:'#fff9c4', opacity:0.58};
  if (pop < 1000000) return {fill:'#ffcc02', opacity:0.63};
  if (pop < 1200000) return {fill:'#ff9800', opacity:0.68};
  if (pop < 1400000) return {fill:'#ef5350', opacity:0.75};
  return {fill:'#b71c1c', opacity:0.92};
}

function styleFeature(f) {
  const c = getColor(populations[f.properties.name] || 0);
  return {fillColor:c.fill, fillOpacity:c.opacity, color:'#58a6ff', weight:1.2, opacity:0.7};
}

function drawRoads() {
  Object.entries(ROADS).forEach(([name, pts]) => {
    L.polyline(pts, {
      color: '#ffd54f',
      weight: 2,
      opacity: 0.55,
      dashArray: '1,0'
    }).addTo(map).bindTooltip(name, {sticky:true, className:'tooltip-custom'});
  });
}

function initGpsLayer() {
  gpsLayer = L.layerGroup().addTo(map);
}

function updateGpsAgents(agents) {
  if (!gpsLayer) return;
  agents.forEach(a => {
    let m = gpsMarkers[a.id];
    if (!m) {
      m = L.circleMarker([a.lat, a.lng], {
        radius: 3, color: '#39ff88', fillColor: '#39ff88',
        fillOpacity: 0.95, weight: 1, opacity: 0.9, renderer: gpsRenderer
      }).addTo(gpsLayer);
      gpsMarkers[a.id] = m;
    } else {
      m.setLatLng([a.lat, a.lng]);
    }
  });
}

let gpsRenderer;

function initMap() {
  map = L.map('map', {
    center: [13.735, 100.55],
    zoom: 11,
    minZoom: 10,
    maxZoom: 17,
    zoomControl: true,
    attributionControl: false,
    maxBounds: BKK_BOUNDS,
    maxBoundsViscosity: 1.0
  });

  // Road-visible dark basemap (CartoDB dark_all renders the street network)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19,
    bounds: BKK_BOUNDS
  }).addTo(map);

  gpsRenderer = L.canvas({padding: 0.5});
  drawRoads();
  initGpsLayer();

  // Fetch country-level GeoJSON but KEEP ONLY Bangkok's districts so the
  // rest of Thailand never renders.
  fetch('https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json')
    .then(r => r.json())
    .then(data => {
      const bkkOnly = {
        type: 'FeatureCollection',
        features: (data.features || []).filter(f => {
          const n = f.properties.name || f.properties.NAME || '';
          return BKK_DISTRICT_NAMES.includes(n);
        })
      };

      if (bkkOnly.features.length === 0) {
        throw new Error('No Bangkok features matched — using fallback markers');
      }

      geojsonLayer = L.geoJSON(bkkOnly, {
        style: styleFeature,
        onEachFeature: (feature, layer) => {
          let name = feature.properties.name || feature.properties.NAME || 'Unknown';
          layerMap[name] = layer;
          layer.on({
            mouseover(e) {
              layer.setStyle({weight:2.5, color:'#ffffff', opacity:1});
              layer.bringToFront();
              const pop = populations[name] || 0;
              const pct = ((pop / 10000000) * 100).toFixed(1);
              layer.bindTooltip(
                `<strong>${name}</strong><br/>${THAI_NAMES[name]||''}<br/>👥 ${(pop/1000).toFixed(0)}k people (${pct}%)`,
                {className:'tooltip-custom', sticky:true, direction:'top'}
              ).openTooltip(e.latlng);
            },
            mouseout(e) { geojsonLayer.resetStyle(layer); layer.closeTooltip(); }
          });
        }
      }).addTo(map);

      map.setMaxBounds(BKK_BOUNDS);
      map.setView([13.735, 100.55], 11);

      renderRankings();
      updateStats();
    })
    .catch(err => {
      console.log('GeoJSON load error, using fallback:', err);
      // Fallback: marker circles for the well-known central districts
      allDistricts.forEach(name => {
        const coords = {
          "Phra Nakhon": [13.7563, 100.5018],
          "Dusit": [13.8071, 100.5237],
          "Bang Rak": [13.7214, 100.5304],
          "Pathum Wan": [13.7465, 100.5372],
          "Ratchathewi": [13.7600, 100.5414],
          "Huai Khwang": [13.7904, 100.5678],
          "Chatuchak": [13.8061, 100.5603],
          "Samphanthawong": [13.7313, 100.5125],
          "Khlong Toei": [13.6734, 100.5816],
          "Bang Khae": [13.6412, 100.3846]
        };
        if (coords[name]) {
          const circle = L.circleMarker(coords[name], {
            radius: 15,
            fillColor: '#1565c0',
            color: '#58a6ff',
            weight: 1,
            opacity: 0.8,
            fillOpacity: 0.5
          }).addTo(map);
          layerMap[name] = circle;
          circle.on('mouseover', function() { 
            circle.setStyle({weight:2, radius:20});
            const pop = populations[name]||0;
            circle.bindTooltip(`${name}<br/>👥 ${(pop/1000).toFixed(0)}k`).openTooltip();
          });
          circle.on('mouseout', () => circle.setStyle({weight:1, radius:15}));
        }
      });
      map.setView([13.735, 100.55], 11);
      renderRankings();
      updateStats();
    });
}

function refreshLayer(name) {
  const layer = layerMap[name];
  if (!layer) return;
  const c = getColor(populations[name] || 0);
  layer.setStyle({fillColor:c.fill, fillOpacity:c.opacity, color:'#58a6ff', weight:1.2, opacity:0.7});
}

function addFeedItem(data) {
  const list = document.getElementById('feed-list');
  const isNeg = data.delta < 0;
  const cls = Math.abs(data.delta) >= 5000 ? 'surge' : isNeg ? 'neg' : 'pos';
  const delta = isNeg ? '' : '+';
  
  const item = document.createElement('div');
  item.className = `feed-item ${cls}`;
  item.innerHTML = `
    <div class="feed-action">${data.action}</div>
    <div style="display:flex;justify-content:space-between">
      <div><div class="feed-province">${data.district}</div><div style="font-size:0.65rem;color:#8b949e">${data.thai}</div></div>
      <div><div class="feed-delta ${cls.includes('neg') ? 'neg' : 'pos'}">${delta}${(data.delta/1000).toFixed(1)}k</div><div style="font-size:0.65rem;color:#8b949e">${(data.count/1000).toFixed(0)}k total</div></div>
    </div>`;
  list.insertBefore(item, list.firstChild);
  while (list.children.length > 30) list.removeChild(list.lastChild);
}

function renderRankings() {
  const sorted = Object.entries(populations).sort((a,b) => b[1]-a[1]).slice(0,15);
  const max = sorted[0]?.[1] || 1;
  const list = document.getElementById('rank-list');
  list.innerHTML = sorted.map(([name, pop], i) => {
    const pct = Math.round(pop/max*100);
    const c = getColor(pop);
    return `<div class="rank-item">
      <div class="rank-item-row">
        <div class="rank-num">${i+1}</div>
        <div style="flex:1"><div style="font-weight:600;color:#e6edf3">${name}</div><div style="font-size:0.63rem;color:#8b949e">${THAI_NAMES[name]||''}</div></div>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:${pct}%;background:${c.fill}"></div></div>
        <div class="rank-count" style="color:${c.fill}">${(pop/1000).toFixed(0)}k</div>
      </div>
    </div>`;
  }).join('');
}

function updateStats() {
  const vals = Object.values(populations);
  const total = vals.reduce((a,b)=>a+b,0);
  const active = vals.filter(v=>v>0).length;
  const pct = ((total/10000000)*100).toFixed(1);
  document.getElementById('total-pop').textContent = (total/1000000).toFixed(1)+'M';
  document.getElementById('active-districts').textContent = active;
  document.getElementById('events-min').textContent = eventsLastMin;
}

function switchTab(name, el) {
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}

onTimeSlide();
setInterval(()=>{ eventsLastMin=eventCount; eventCount=0; updateStats(); }, 60000);
setInterval(updateStats, 3000);
initMap();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    t = threading.Thread(target=mock_live_feed, daemon=True)
    t.start()
    t2 = threading.Thread(target=mock_gps_feed, daemon=True)
    t2.start()
    print("\n🗺️  Bangkok Live Population (10M) running!")
    print("👉  Open: http://localhost:5000\n")
    socketio.run(app, debug=False, port=5000, allow_unsafe_werkzeug=True)
