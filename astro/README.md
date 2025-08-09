# 🌟 Comprehensive Vedic Astrology Calculator

A complete Vedic astrology calculator that generates all major charts and tables for a given date, time, and place.

## 📋 Features

This calculator generates all the charts and tables mentioned in `allchartsname.md`:

### 🎯 Main Charts
- **Lagna Chart (D1)** - Birth chart/Rasi
- **Navamsa Chart (D9)** - Spouse and marriage
- **All Divisional Charts (D1-D60)** - Complete set of divisional charts

### 📊 Tables and Calculations
- **Ashtakvarga Table & Chart** - Beneficial points for each planet
- **Shodashvarga Table** - 16-fold strength analysis
- **Planetary Positions** - Exact positions with degrees and nakshatras
- **Cuspal Positions** - House cusps
- **Significators of Houses** - House lords and significations
- **Friendship Tables** - Permanent, Temporal, and Five-fold friendships
- **Shadbala Table** - Six-fold strength analysis
- **BhavBala Table** - House strength analysis
- **Planetary Aspects** - Western and Vedic aspects
- **SAV (Sarvashtakavarga)** - Combined benefic points
- **Sodhaya Pinda Table** - Planetary strength calculations
- **Vaiseshikamsas Table** - Special calculations
- **Vimsopaka Table** - 20-fold analysis

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server:**
   ```bash
   python astro_server.py
   ```

3. **Open in Browser:**
   - Go to: http://localhost:5000
   - Enter birth details
   - View all charts and tables

### Option 2: Command Line

1. **Run the Calculator:**
   ```bash
   python comprehensive_astro_calculator.py
   ```

2. **View Results:**
   - Check `astro_complete_charts.json` for complete data
   - Open `astro_calculator_web.html` for web interface

## 📁 Files Structure

```
astro/
├── comprehensive_astro_calculator.py  # Main calculator
├── astro_server.py                   # Flask web server
├── requirements.txt                  # Python dependencies
├── README.md                        # This file
├── allchartsname.md                 # List of all charts
└── astro_complete_charts.json       # Example output
```

## 🎯 Usage Examples

### Web Interface
1. Enter your full name
2. Select date of birth
3. Enter time of birth (24-hour format)
4. Enter place of birth (e.g., "Mumbai, India")
5. Click "Calculate All Charts"
6. View comprehensive results
7. Download JSON data if needed

### Programmatic Usage
```python
from comprehensive_astro_calculator import VedicAstrologyCalculator, BirthDetails
import datetime

calculator = VedicAstrologyCalculator()

birth_details = BirthDetails(
    name="Your Name",
    date=datetime.date(1990, 6, 15),
    time=datetime.time(14, 30, 0),
    latitude=19.0760,
    longitude=72.8777,
    timezone=5.5,
    place="Mumbai, India"
)

result = calculator.calculate_all_charts(birth_details)
print(result)
```

## 📊 Output Format

The calculator generates a comprehensive JSON structure containing:

```json
{
  "birthDetails": {
    "name": "Person Name",
    "date": "15 June 1990",
    "time": "14:30:00",
    "place": "Mumbai, India",
    "lagna": "Cancer",
    "rasi": "Virgo",
    "nakshatraPada": "Uttaraphalguni 4"
  },
  "planetaryPositions": [
    {
      "planet": "Sun",
      "sign": "Gemini",
      "degree": "25°26′07″",
      "nakshatra": "Purvashadha",
      "pada": 4,
      "house": 10,
      "is_retrograde": false
    }
  ],
  "charts": {
    "Rasi (D1)": {
      "House_1": ["Ascendant"],
      "House_2": ["Mars", "Jupiter"],
      // ... all 12 houses
    }
  },
  "tables": {
    "Ashtakvarga": {...},
    "Shadbala": {...},
    "Friendship": {...}
  }
}
```

## 🔧 Technical Details

### Dependencies
- **ephem**: Astronomical calculations
- **geopy**: Geocoding for place coordinates
- **timezonefinder**: Timezone detection
- **pytz**: Timezone handling
- **flask**: Web server (for web interface)

### Calculations
- **Ayanamsa**: Lahiri (most commonly used)
- **House System**: Equal house system
- **Aspects**: Vedic and Western aspects
- **Divisional Charts**: All standard divisions (D1-D60)
- **Nakshatras**: 27 nakshatras with padas

## 🌍 Supported Features

### Charts Generated
- ✅ Lagna Chart (D1)
- ✅ Hora Chart (D2)
- ✅ Drekkana Chart (D3)
- ✅ Chaturthamsa Chart (D4)
- ✅ Panchamsa Chart (D5)
- ✅ Shashthamsa Chart (D6)
- ✅ Saptamsa Chart (D7)
- ✅ Ashtamsa Chart (D8)
- ✅ Navamsa Chart (D9)
- ✅ Dashamsa Chart (D10)
- ✅ Rudramsa Chart (D11)
- ✅ Dwadashamsa Chart (D12)
- ✅ Shodashamsa Chart (D16)
- ✅ Vimshamsa Chart (D20)
- ✅ Chaturvimshamsa Chart (D24)
- ✅ Saptavimshamsa Chart (D27)
- ✅ Trimshamsa Chart (D30)
- ✅ Khavedamsa Chart (D40)
- ✅ Akshavedamsa Chart (D45)
- ✅ Shastiamsha Chart (D60)

### Tables Generated
- ✅ Ashtakvarga Table
- ✅ Ashtakvarga Chart
- ✅ Shodashvarga Table
- ✅ Planetary Positions Table
- ✅ Cuspal Positions Table
- ✅ Significators of Houses Table
- ✅ Permanent Friendship Table
- ✅ Temporal Friendship Table
- ✅ Five-fold Friendship Table
- ✅ Shadbala Table
- ✅ BhavBala Table
- ✅ Planetary Aspects Table
- ✅ SAV (Sarvashtakavarga)
- ✅ Sodhaya Pinda Table
- ✅ Vaiseshikamsas Table
- ✅ Vimsopaka Table

## 🎨 Web Interface Features

- **Modern UI**: Beautiful gradient design
- **Responsive**: Works on desktop and mobile
- **Real-time**: Instant calculations
- **Downloadable**: Export complete data as JSON
- **Comprehensive**: Shows all charts and tables
- **User-friendly**: Simple form interface

## 🔍 Troubleshooting

### Common Issues

1. **Installation Errors:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Geocoding Issues:**
   - Try more specific place names
   - Use format: "City, Country"
   - Example: "Mumbai, India" instead of "Mumbai"

3. **Calculation Errors:**
   - Ensure valid date and time
   - Check timezone accuracy
   - Verify place name spelling

4. **Server Issues:**
   ```bash
   # Check if port 5000 is available
   netstat -an | grep 5000
   # Use different port
   python astro_server.py --port 5001
   ```

## 📚 References

- **Vedic Astrology**: Traditional Indian astrology system
- **Divisional Charts**: Specialized charts for specific life areas
- **Ashtakvarga**: System of benefic points
- **Shadbala**: Six-fold strength analysis
- **Nakshatras**: 27 lunar mansions

## 🤝 Contributing

Feel free to contribute improvements:
- Add more accurate calculations
- Enhance the web interface
- Add new chart types
- Improve documentation

## 📄 License

This project is for educational and personal use. Please respect traditional knowledge and use responsibly.

---

**🌟 May the stars guide you on your astrological journey! 🌟** 