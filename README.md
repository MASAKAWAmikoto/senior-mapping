# 🗺️ Bangkok Live Population Heatmap (10M Edition)

Real-time Flask + Socket.IO app showing **all 50 Bangkok districts** with realistic **10 million person population** patterns. Includes **live clock** ⏰ and **time slider** ⏱️ to see population flows throughout the day.

## ✨ New Features

### 🕐 **Live Clock**
- Shows current time in header
- Updates every second
- Thai time format (24-hour)

### ⏰ **Time Slider (NEW!)**
- Slide through 5am → 11pm
- See realistic population for any time
- **Districts peak at different hours**:
  - **5am**: Temples, joggers → Phra Nakhon busy
  - **7am**: BTS/MRT CHAOS → Pathum Wan explodes (1.2M people)
  - **12pm**: Lunch peak → Restaurants/malls overflowing
  - **5pm**: Evening rush → Traffic jams everywhere
  - **9pm**: Night venues → Bang Rak (nightlife district) peaks
  - **11pm**: Everything closes → Very quiet

### 📍 **All 50 Districts**
Including **Bang Khae** (บางแค) and **Samphanthawong** (สัมพันธวงศ์) now properly displayed!

### 💯 **10 Million Population**
- Realistic Bangkok total (~10M people)
- Scaled by district importance
- Peak hours show 1.5M+ in CBD
- Color intensity matches actual crowd levels

## 🎮 How to Use

### Stop Old Version
```bash
Ctrl + C  (in the terminal running the app)
```

### Replace File
Download the new `bangkok_map_app.py` and copy to your folder

### Run It
```bash
python bangkok_map_app.py
```

### Open Browser
```
http://localhost:5000
```

---

## 📊 Three Tabs

### 📡 **Live Feed Tab**
- Real-time events streaming in
- Shows district, people count, action
- Auto-scrolls newest events at top

### ⏰ **Time Tab (NEW!)**
- **Slider**: Drag from 5am to 11pm
- **Time Display**: Shows current slider hour
- **Context**: Explains what's happening at that time
- **Randomize Button**: 🎲 Generate data for selected time

### 🏆 **Rankings Tab**
- Top 15 most crowded districts
- Visual bars showing density
- Updates live as population changes

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

### 🔴 **Peak During Rushes (1.2M-1.5M)**
- **Pathum Wan** (ปทุมวัน) — Siam, CentralWorld, CBD mega-mall
- **Ratchathewi** (ราชเทวี) — Victory Monument, BTS hub
- **Huai Khwang** (ห้วยขวาง) — Business area
- **Bang Rak** (บางรัก) — Silom (nightlife + CBD)

### 🟠 **Busy During Work (400k-800k)**
- **Khlong Toei** (คลองเตย) — Sukhumvit, shopping
- **Chatuchak** (จตุจักร) — Massive weekend market
- **Samphanthawong** (สัมพันธวงศ์) — Chinatown

### 🟡 **Moderate (100k-400k)**
- **Dusit**, **Lak Si**, **Bang Na**, **Thung Khru**

### 🔵 **Always Quiet (5k-50k)**
- **Outer residential** — Nong Khaem, Bang Khae, Phra Pradaeng

---

## 💡 How to Test It

1. **Open the app** → http://localhost:5000
2. **Go to ⏰ Time tab**
3. **Drag slider to 7:00** (morning rush)
4. **Click "🎲 Randomize This Time"**
5. **Watch map turn RED** — CBD districts explode with people! 🔥
6. **Drag to 23:00** (late night)
7. **Randomize again** → Map turns BLUE, everything quiet

---

## 🔧 Technical Details

### Stack
- Flask + Flask-SocketIO
- Leaflet.js maps
- Real Bangkok GeoJSON data
- Dark theme (GitHub-style)

### Real Data
- 50 Bangkok districts (all current)
- GeoJSON boundaries from official sources
- Population patterns based on actual Bangkok rush hour data
- Time-based simulation realistic to Thailand traffic

### Population Scaling
- **Total**: ~10M people in Bangkok metro
- **Morning rush**: 1.2-1.5M in transit/work
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

- Map loads from GeoJSON (internet required)
- WebSocket works in Chrome/Firefox/Safari
- Simulated data (not real live tracking)
- Population randomizes based on time patterns

---

**Enjoy exploring Bangkok's 10M people!** 🚇🏙️🌃

Built with ❤️ for Bangkok urban data enthusiasts
