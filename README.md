# 🗺️ Bangkok Live Population & GPS Map (10M Edition)

Real-time Flask + Socket.IO app showing **all 50 Bangkok districts**, locked to a **Bangkok-only map view**, with realistic **10 million person population** patterns, a **visible road network**, and **mock live GPS dots** moving along the streets. Includes a **live clock** ⏰ and **time slider** ⏱️ to see population flows throughout the day.

## ✨ New in This Version

### 📍 **Bangkok-Only Map**
- Map is locked to a Bangkok bounding box (`maxBounds`) — you can't pan/zoom out into the rest of Thailand or the region
- District GeoJSON is filtered to only the 50 official Bangkok khet (เขต) — no stray provinces rendered

### 🛣️ **Visible Road Network**
- Dark basemap tiles that render streets, not just blank polygons
- ~15 major roads drawn as glowing overlay lines, including Sukhumvit, Silom, Rama IV, Phetchaburi, Ratchadaphisek, Vibhavadi Rangsit, Phahonyothin, Charoen Krung, Lat Phrao, Rama IX, Sathon, Bangna-Trad, Kanchanaphisek, and Ramkhamhaeng
- Hover a road line to see its name

### 🟢 **Mock Live GPS Tracking**
- A background simulation generates ~180 "people" as GPS agents
- Each agent travels back and forth along a real road, with its own speed and direction
- Positions are pushed to the browser every second over WebSocket (`gps_tick` event)
- Rendered as small green dots that visibly move along the streets in real time — a simple, self-contained stand-in for a real GPS feed

### 🕐 **Live Clock**
- Shows current time in header, updates every second, 24-hour format

### ⏰ **Time Slider**
- Slide through 5am → 11pm to see realistic population for any time
- Districts peak at different hours (BTS rush, lunch rush, evening rush, nightlife, etc.)

### 💯 **10 Million Population**
- Realistic Bangkok total (~10M people), scaled by district importance
- Peak hours show 1.5M+ in the CBD
- Color intensity matches actual crowd levels

## 🎮 How to Use

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run it
```bash
python bangkok_map_app.py
```

### Open browser
```
http://localhost:5000
```

---

## 📊 Three Tabs

### 📡 **Live Feed Tab**
- Real-time events streaming in (district, people count, action)
- Auto-scrolls newest events to the top

### ⏰ **Time Tab**
- **Slider**: drag from 5am to 11pm
- **Time Display**: shows current slider hour
- **Context**: explains what's happening at that time
- **Randomize Button**: 🎲 generate data for the selected time

### 🏆 **Rankings Tab**
- Top 15 most crowded districts
- Visual bars showing density, updates live as population changes

---

## ⏰ Time Patterns (Realistic Bangkok)

| Hour | What's Happening | Busy Districts | Population |
|---|---|---|---|
| 🌅 **5am** | Joggers, monks, temples | Phra Nakhon | 150k total |
| 🚌 **7am** | **BTS/MRT PACKED** | Pathum Wan, Ratchathewi | **1.2M** 🔴 |
| ☀️ **10am** | Office hours | Most CBD areas | 800k |
| 🍽️ **12pm** | **LUNCH RUSH** | Malls, restaurants | **1.4M** 🔴 |
| ☕ **2pm** | Afternoon shopping | Mixed areas | 700k |
| 🚗 **5pm** | **EVENING RUSH** | All transit hubs | **1.5M** 🔴 |
| 🎭 **7pm** | Restaurants/bars | Entertainment areas | 900k |
| 🌙 **9pm** | Night venues | Bang Rak, Khlong Toei | 650k |
| 🌃 **11pm** | Very quiet | Residential | 300k |

---

## 🗺️ Key Districts

### 🔴 **Peak During Rushes (1.2M–1.5M)**
- **Pathum Wan** (ปทุมวัน) — Siam, CentralWorld, CBD mega-mall
- **Ratchathewi** (ราชเทวี) — Victory Monument, BTS hub
- **Huai Khwang** (ห้วยขวาง) — Business area
- **Bang Rak** (บางรัก) — Silom (nightlife + CBD)

### 🟠 **Busy During Work (400k–800k)**
- **Khlong Toei** (คลองเตย) — Sukhumvit, shopping
- **Chatuchak** (จตุจักร) — Massive weekend market
- **Samphanthawong** (สัมพันธวงศ์) — Chinatown

### 🟡 **Moderate (100k–400k)**
- **Dusit**, **Lak Si**, **Bang Na**, **Thung Khru**

### 🔵 **Always Quiet (5k–50k)**
- **Outer residential** — Nong Khaem, Bang Khae, Phra Pradaeng

---

## 💡 How to Test It

1. **Open the app** → http://localhost:5000
2. **Watch the green dots** drift along the road lines — that's the mock live GPS feed
3. **Go to ⏰ Time tab**, drag slider to 7:00 (morning rush), click **"🎲 Randomize This Time"**
4. **Watch the map turn RED** — CBD districts explode with people 🔥
5. **Drag to 23:00** (late night), randomize again → map turns blue, everything quiet
6. Try panning/zooming — the view stays locked to Bangkok

---

## 🔧 Technical Details

### Stack
- Flask + Flask-SocketIO
- Leaflet.js maps with a road-rendering dark basemap
- Bangkok-filtered GeoJSON district boundaries
- Background thread simulating ~180 GPS agents along real road polylines
- Dark theme (GitHub-style)

### Live GPS Simulation
- 15 major Bangkok roads defined as waypoint polylines
- Each agent is assigned a road, a position along it, a speed, and a direction
- A server-side loop advances every agent each second and emits positions over WebSocket
- This is **simulated** movement, not real device tracking — a realistic stand-in for wiring up an actual GPS/telemetry feed later

### Population Scaling
- **Total**: ~10M people in Bangkok metro
- **Morning rush**: 1.2–1.5M in transit/work
- **Late night**: 300k mostly sleeping
- **Peak hours**: CBD concentrates 1M+ people

---

## 🚀 Deploy (Optional)

To run it online (Render, Railway, Fly.io):

```bash
git push  # to GitHub
```

Then deploy your repo on Render:
- Build: `pip install -r requirements.txt`
- Start: `gunicorn bangkok_map_app:app`

You get a live URL like `https://bangkok-map.onrender.com` 🌐

---

## ⚠️ Known Limits

- Map tiles and GeoJSON boundaries load from external sources (internet required)
- WebSocket works in Chrome/Firefox/Safari
- GPS positions and population are simulated, not real live tracking
- Population randomizes based on time-of-day patterns

---

**Enjoy exploring Bangkok's 10M people — now street by street!** 🚇🏙️🌃

Built with ❤️ for Bangkok urban data enthusiasts
