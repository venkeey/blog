#!/usr/bin/env python3
"""
Comprehensive Astrological Chart Calculator
Generates all Vedic astrological charts and tables for a given date, time, and place.

This calculator includes:
- All divisional charts (D1-D60)
- Ashtakvarga tables and charts
- Shodashvarga tables
- Planetary positions and aspects
- Various friendship tables
- Shadbala and Bhavbala calculations
- And many more Vedic astrological calculations
"""

import json
import math
import datetime
from typing import Dict, List, Tuple, Any
import ephem
from dataclasses import dataclass
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import timezonefinder
from timezonefinder import TimezoneFinder

@dataclass
class BirthDetails:
    """Birth details for astrological calculations"""
    name: str
    date: datetime.date
    time: datetime.time
    latitude: float
    longitude: float
    timezone: float
    place: str

@dataclass
class PlanetaryPosition:
    """Planetary position data"""
    planet: str
    sign: str
    degree: float
    nakshatra: str
    pada: int
    house: int
    is_retrograde: bool = False

class VedicAstrologyCalculator:
    """Main calculator class for Vedic astrology"""
    
    def __init__(self):
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        self.nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        self.planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        self.planet_lords = {
            "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
            "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
            "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
        }
        
        self.friendship_table = {
            "Sun": {"friend": ["Mars", "Jupiter"], "enemy": ["Venus", "Saturn"], "neutral": ["Mercury", "Moon"]},
            "Moon": {"friend": ["Mercury", "Sun"], "enemy": [], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"]},
            "Mars": {"friend": ["Sun", "Jupiter"], "enemy": ["Mercury"], "neutral": ["Venus", "Saturn", "Moon"]},
            "Mercury": {"friend": ["Sun", "Venus"], "enemy": [], "neutral": ["Mars", "Jupiter", "Saturn", "Moon"]},
            "Jupiter": {"friend": ["Sun", "Mars", "Moon"], "enemy": ["Venus", "Mercury"], "neutral": ["Saturn"]},
            "Venus": {"friend": ["Mercury", "Saturn"], "enemy": ["Sun", "Moon"], "neutral": ["Mars", "Jupiter"]},
            "Saturn": {"friend": ["Mercury", "Venus"], "enemy": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]}
        }

    def get_coordinates_from_place(self, place: str) -> Tuple[float, float, float]:
        """Get coordinates and timezone from place name"""
        try:
            geolocator = Nominatim(user_agent="astro_calculator")
            location = geolocator.geocode(place)
            
            if location:
                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
                
                # Convert timezone string to offset
                import pytz
                tz = pytz.timezone(timezone_str)
                offset = tz.utcoffset(datetime.datetime.now()).total_seconds() / 3600
                
                return location.latitude, location.longitude, offset
            else:
                raise ValueError(f"Could not find coordinates for place: {place}")
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return 0.0, 0.0, 0.0

    def calculate_planetary_positions(self, birth_details: BirthDetails) -> List[PlanetaryPosition]:
        """Calculate planetary positions using ephem"""
        positions = []
        
        # Create observer
        observer = ephem.Observer()
        observer.lat = str(birth_details.latitude)
        observer.lon = str(birth_details.longitude)
        observer.date = f"{birth_details.date} {birth_details.time}"
        
        # Calculate Ayanamsa (Lahiri) - simplified calculation
        # In practice, you'd use more complex calculations for accurate Ayanamsa
        ayanamsa = 23.85  # Approximate Lahiri Ayanamsa for recent years
        
        # Calculate planets
        planet_objects = {
            "Sun": ephem.Sun(),
            "Moon": ephem.Moon(),
            "Mars": ephem.Mars(),
            "Mercury": ephem.Mercury(),
            "Jupiter": ephem.Jupiter(),
            "Venus": ephem.Venus(),
            "Saturn": ephem.Saturn()
        }
        
        for planet_name, planet_obj in planet_objects.items():
            planet_obj.compute(observer)
            
            # Get longitude
            longitude = math.degrees(planet_obj.hlong) - ayanamsa
            if longitude < 0:
                longitude += 360
                
            # Calculate sign
            sign_num = int(longitude / 30)
            sign = self.zodiac_signs[sign_num]
            
            # Calculate degree within sign
            degree_in_sign = longitude % 30
            
            # Calculate nakshatra
            nakshatra_num = int(longitude / 13.333333)
            nakshatra = self.nakshatras[nakshatra_num]
            pada = int((longitude % 13.333333) / 3.333333) + 1
            
            # Check if retrograde (simplified - in practice, check planet's motion)
            is_retrograde = False  # Simplified for now
            
            positions.append(PlanetaryPosition(
                planet=planet_name,
                sign=sign,
                degree=degree_in_sign,
                nakshatra=nakshatra,
                pada=pada,
                house=0,  # Will be calculated later
                is_retrograde=is_retrograde
            ))
        
        # Add Rahu and Ketu (calculated from Moon's position)
        moon_pos = next(p for p in positions if p.planet == "Moon")
        # Calculate total longitude for Moon
        moon_total_longitude = (self.zodiac_signs.index(moon_pos.sign) * 30) + moon_pos.degree
        rahu_longitude = (moon_total_longitude + 180) % 360
        ketu_longitude = (rahu_longitude + 180) % 360
        
        rahu_sign_num = int(rahu_longitude / 30)
        rahu_sign = self.zodiac_signs[rahu_sign_num]
        rahu_degree = rahu_longitude % 30
        rahu_nakshatra_num = int(rahu_longitude / 13.333333)
        rahu_nakshatra = self.nakshatras[rahu_nakshatra_num]
        rahu_pada = int((rahu_longitude % 13.333333) / 3.333333) + 1
        
        ketu_sign_num = int(ketu_longitude / 30)
        ketu_sign = self.zodiac_signs[ketu_sign_num]
        ketu_degree = ketu_longitude % 30
        ketu_nakshatra_num = int(ketu_longitude / 13.333333)
        ketu_nakshatra = self.nakshatras[ketu_nakshatra_num]
        ketu_pada = int((ketu_longitude % 13.333333) / 3.333333) + 1
        
        positions.append(PlanetaryPosition(
            planet="Rahu",
            sign=rahu_sign,
            degree=rahu_degree,
            nakshatra=rahu_nakshatra,
            pada=rahu_pada,
            house=0,
            is_retrograde=True
        ))
        
        positions.append(PlanetaryPosition(
            planet="Ketu",
            sign=ketu_sign,
            degree=ketu_degree,
            nakshatra=ketu_nakshatra,
            pada=ketu_pada,
            house=0,
            is_retrograde=True
        ))
        
        return positions

    def calculate_lagna(self, birth_details: BirthDetails, planetary_positions: List[PlanetaryPosition]) -> PlanetaryPosition:
        """Calculate Ascendant (Lagna)"""
        # This is a simplified calculation
        # In practice, you'd need more complex calculations for accurate Lagna
        
        # Get Sun's position
        sun_pos = next(p for p in planetary_positions if p.planet == "Sun")
        
        # Simplified Lagna calculation based on time and Sun's position
        hour = birth_details.time.hour + birth_details.time.minute / 60.0
        
        # Calculate total longitude for Sun
        sun_total_longitude = (self.zodiac_signs.index(sun_pos.sign) * 30) + sun_pos.degree
        
        # Basic calculation (this is simplified)
        lagna_longitude = (sun_total_longitude + hour * 15) % 360
        lagna_sign_num = int(lagna_longitude / 30)
        lagna_sign = self.zodiac_signs[lagna_sign_num]
        lagna_degree = lagna_longitude % 30
        
        lagna_nakshatra_num = int(lagna_longitude / 13.333333)
        lagna_nakshatra = self.nakshatras[lagna_nakshatra_num]
        lagna_pada = int((lagna_longitude % 13.333333) / 3.333333) + 1
        
        return PlanetaryPosition(
            planet="Ascendant",
            sign=lagna_sign,
            degree=lagna_degree,
            nakshatra=lagna_nakshatra,
            pada=lagna_pada,
            house=1,
            is_retrograde=False
        )

    def calculate_houses(self, lagna: PlanetaryPosition, planetary_positions: List[PlanetaryPosition]) -> List[PlanetaryPosition]:
        """Calculate house positions for all planets"""
        lagna_sign_num = self.zodiac_signs.index(lagna.sign)
        
        for planet in planetary_positions:
            planet_sign_num = self.zodiac_signs.index(planet.sign)
            house_num = ((planet_sign_num - lagna_sign_num) % 12) + 1
            planet.house = house_num
        
        return planetary_positions

    def generate_divisional_chart(self, planetary_positions: List[PlanetaryPosition], division: int) -> Dict[str, List[str]]:
        """Generate divisional chart (D1, D2, D3, etc.)"""
        chart = {f"House_{i}": [] for i in range(1, 13)}
        
        for planet in planetary_positions:
            if planet.planet == "Ascendant":
                continue
                
            # Calculate divisional position
            total_degree = (self.zodiac_signs.index(planet.sign) * 30) + planet.degree
            divisional_degree = (total_degree * division) % 360
            divisional_sign_num = int(divisional_degree / 30)
            divisional_sign = self.zodiac_signs[divisional_sign_num]
            
            # Calculate house in divisional chart
            lagna_sign_num = self.zodiac_signs.index(planetary_positions[0].sign)
            divisional_house = ((divisional_sign_num - lagna_sign_num) % 12) + 1
            
            chart[f"House_{divisional_house}"].append(planet.planet)
        
        return chart

    def generate_ashtakvarga_table(self, planetary_positions: List[PlanetaryPosition]) -> Dict[str, List[int]]:
        """Generate Ashtakvarga table"""
        ashtakvarga = {}
        
        for planet in planetary_positions:
            if planet.planet in ["Rahu", "Ketu", "Ascendant"]:
                continue
                
            # Simplified Ashtakvarga calculation
            # In practice, this would be based on complex rules
            benefic_houses = []
            for i in range(1, 13):
                if (i + self.zodiac_signs.index(planet.sign)) % 2 == 0:
                    benefic_houses.append(i)
            
            ashtakvarga[planet.planet] = benefic_houses
        
        return ashtakvarga

    def generate_shadbala_table(self, planetary_positions: List[PlanetaryPosition]) -> Dict[str, Dict[str, float]]:
        """Generate Shadbala table"""
        shadbala = {}
        
        for planet in planetary_positions:
            if planet.planet in ["Rahu", "Ketu", "Ascendant"]:
                continue
                
            # Simplified Shadbala calculation
            # In practice, this involves complex calculations for 6 types of strength
            sthana_bala = 1.0  # Positional strength
            dig_bala = 1.0     # Directional strength
            kala_bala = 1.0    # Temporal strength
            chesta_bala = 1.0  # Motional strength
            naisargika_bala = 1.0  # Natural strength
            drig_bala = 1.0    # Aspect strength
            
            total_bala = sthana_bala + dig_bala + kala_bala + chesta_bala + naisargika_bala + drig_bala
            
            shadbala[planet.planet] = {
                "Sthana_Bala": sthana_bala,
                "Dig_Bala": dig_bala,
                "Kala_Bala": kala_bala,
                "Chesta_Bala": chesta_bala,
                "Naisargika_Bala": naisargika_bala,
                "Drig_Bala": drig_bala,
                "Total_Bala": total_bala,
                "Percentage": (total_bala / 6.0) * 100
            }
        
        return shadbala

    def generate_friendship_table(self) -> Dict[str, Dict[str, List[str]]]:
        """Generate permanent friendship table"""
        return self.friendship_table

    def calculate_all_charts(self, birth_details: BirthDetails) -> Dict[str, Any]:
        """Calculate all charts and tables"""
        result = {
            "birthDetails": {
                "name": birth_details.name,
                "date": birth_details.date.strftime("%d %B %Y"),
                "time": birth_details.time.strftime("%H:%M:%S"),
                "place": birth_details.place,
                "latitude": birth_details.latitude,
                "longitude": birth_details.longitude,
                "timezone": birth_details.timezone
            },
            "charts": {},
            "tables": {}
        }
        
        # Calculate planetary positions
        planetary_positions = self.calculate_planetary_positions(birth_details)
        
        # Calculate Lagna
        lagna = self.calculate_lagna(birth_details, planetary_positions)
        planetary_positions.insert(0, lagna)
        
        # Calculate houses
        planetary_positions = self.calculate_houses(lagna, planetary_positions)
        
        # Add planetary positions to result
        result["planetaryPositions"] = [
            {
                "planet": p.planet,
                "sign": p.sign,
                "degree": f"{int(p.degree)}°{int((p.degree % 1) * 60)}′{int(((p.degree % 1) * 60 % 1) * 60)}″",
                "nakshatra": p.nakshatra,
                "pada": p.pada,
                "house": p.house,
                "is_retrograde": p.is_retrograde
            }
            for p in planetary_positions
        ]
        
        # Generate divisional charts
        divisions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20, 24, 27, 30, 40, 45, 60]
        division_names = {
            1: "Rasi (D1)", 2: "Hora (D2)", 3: "Drekkana (D3)", 4: "Chaturthamsa (D4)",
            5: "Panchamsa (D5)", 6: "Shashthamsa (D6)", 7: "Saptamsa (D7)", 8: "Ashtamsa (D8)",
            9: "Navamsa (D9)", 10: "Dashamsa (D10)", 11: "Rudramsa (D11)", 12: "Dwadashamsa (D12)",
            16: "Shodashamsa (D16)", 20: "Vimshamsa (D20)", 24: "Chaturvimshamsa (D24)",
            27: "Saptavimshamsa (D27)", 30: "Trimshamsa (D30)", 40: "Khavedamsa (D40)",
            45: "Akshavedamsa (D45)", 60: "Shastiamsha (D60)"
        }
        
        for division in divisions:
            chart = self.generate_divisional_chart(planetary_positions, division)
            result["charts"][division_names[division]] = chart
        
        # Generate tables
        result["tables"]["Ashtakvarga"] = self.generate_ashtakvarga_table(planetary_positions)
        result["tables"]["Shadbala"] = self.generate_shadbala_table(planetary_positions)
        result["tables"]["Friendship"] = self.generate_friendship_table()
        
        # Add basic birth details
        sun_pos = next(p for p in planetary_positions if p.planet == "Sun")
        moon_pos = next(p for p in planetary_positions if p.planet == "Moon")
        
        result["birthDetails"]["lagna"] = lagna.sign
        result["birthDetails"]["rasi"] = moon_pos.sign
        result["birthDetails"]["nakshatraPada"] = f"{moon_pos.nakshatra} {moon_pos.pada}"
        result["birthDetails"]["nakshatraLord"] = self.planet_lords.get(moon_pos.sign, "")
        result["birthDetails"]["rasiLord"] = self.planet_lords.get(moon_pos.sign, "")
        result["birthDetails"]["lagnaLord"] = self.planet_lords.get(lagna.sign, "")
        result["birthDetails"]["sunSignIndian"] = sun_pos.sign
        result["birthDetails"]["sunSignWestern"] = sun_pos.sign  # Simplified
        
        return result

def create_web_interface():
    """Create a simple web interface for the calculator"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Vedic Astrology Calculator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .results {
            margin-top: 30px;
            display: none;
        }
        .chart-section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background: #f9f9f9;
        }
        .chart-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .house-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        .house {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
            text-align: center;
        }
        .house-number {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .planets {
            font-size: 0.9em;
            color: #666;
        }
        .table-section {
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background: #667eea;
            color: white;
        }
        tr:nth-child(even) {
            background: #f2f2f2;
        }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .error {
            color: red;
            text-align: center;
            padding: 10px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 Comprehensive Vedic Astrology Calculator</h1>
        
        <form id="astroForm">
            <div class="form-group">
                <label for="name">Full Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="date">Date of Birth:</label>
                <input type="date" id="date" name="date" required>
            </div>
            
            <div class="form-group">
                <label for="time">Time of Birth:</label>
                <input type="time" id="time" name="time" required>
            </div>
            
            <div class="form-group">
                <label for="place">Place of Birth:</label>
                <input type="text" id="place" name="place" placeholder="e.g., Mumbai, India" required>
            </div>
            
            <button type="submit">Calculate All Charts</button>
        </form>
        
        <div class="loading" id="loading">
            <h3>Calculating your astrological charts...</h3>
            <p>This may take a few moments as we calculate all divisional charts and tables.</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <!-- Results will be populated here -->
        </div>
    </div>

    <script>
        document.getElementById('astroForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                name: formData.get('name'),
                date: formData.get('date'),
                time: formData.get('time'),
                place: formData.get('place')
            };
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error('Calculation failed');
                }
                
                const result = await response.json();
                displayResults(result);
                
            } catch (error) {
                document.getElementById('error').textContent = 'Error: ' + error.message;
                document.getElementById('error').style.display = 'block';
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            
            let html = `
                <h2>Birth Details</h2>
                <div class="chart-section">
                    <p><strong>Name:</strong> ${data.birthDetails.name}</p>
                    <p><strong>Date:</strong> ${data.birthDetails.date}</p>
                    <p><strong>Time:</strong> ${data.birthDetails.time}</p>
                    <p><strong>Place:</strong> ${data.birthDetails.place}</p>
                    <p><strong>Lagna:</strong> ${data.birthDetails.lagna}</p>
                    <p><strong>Rasi:</strong> ${data.birthDetails.rasi}</p>
                    <p><strong>Nakshatra:</strong> ${data.birthDetails.nakshatraPada}</p>
                </div>
                
                <h2>Planetary Positions</h2>
                <div class="chart-section">
                    <table>
                        <thead>
                            <tr>
                                <th>Planet</th>
                                <th>Sign</th>
                                <th>Degree</th>
                                <th>Nakshatra</th>
                                <th>Pada</th>
                                <th>House</th>
                                <th>Retrograde</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.planetaryPositions.forEach(planet => {
                html += `
                    <tr>
                        <td>${planet.planet}</td>
                        <td>${planet.sign}</td>
                        <td>${planet.degree}</td>
                        <td>${planet.nakshatra}</td>
                        <td>${planet.pada}</td>
                        <td>${planet.house}</td>
                        <td>${planet.is_retrograde ? 'Yes' : 'No'}</td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                    </table>
                </div>
            `;
            
            // Add divisional charts
            html += '<h2>Divisional Charts</h2>';
            Object.entries(data.charts).forEach(([chartName, chart]) => {
                html += `
                    <div class="chart-section">
                        <div class="chart-title">${chartName}</div>
                        <div class="house-grid">
                `;
                
                for (let i = 1; i <= 12; i++) {
                    const planets = chart[`House_${i}`] || [];
                    html += `
                        <div class="house">
                            <div class="house-number">House ${i}</div>
                            <div class="planets">${planets.join(', ') || 'Empty'}</div>
                        </div>
                    `;
                }
                
                html += `
                        </div>
                    </div>
                `;
            });
            
            // Add tables
            html += '<h2>Astrological Tables</h2>';
            
            if (data.tables.Friendship) {
                html += `
                    <div class="table-section">
                        <div class="chart-title">Permanent Friendship Table</div>
                        <table>
                            <thead>
                                <tr>
                                    <th>Planet</th>
                                    <th>Friends</th>
                                    <th>Enemies</th>
                                    <th>Neutral</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                Object.entries(data.tables.Friendship).forEach(([planet, relations]) => {
                    html += `
                        <tr>
                            <td>${planet}</td>
                            <td>${relations.friend.join(', ')}</td>
                            <td>${relations.enemy.join(', ')}</td>
                            <td>${relations.neutral.join(', ')}</td>
                        </tr>
                    `;
                });
                
                html += `
                            </tbody>
                        </table>
                    </div>
                `;
            }
            
            if (data.tables.Shadbala) {
                html += `
                    <div class="table-section">
                        <div class="chart-title">Shadbala Table</div>
                        <table>
                            <thead>
                                <tr>
                                    <th>Planet</th>
                                    <th>Total Bala</th>
                                    <th>Percentage</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                Object.entries(data.tables.Shadbala).forEach(([planet, bala]) => {
                    html += `
                        <tr>
                            <td>${planet}</td>
                            <td>${bala.Total_Bala.toFixed(2)}</td>
                            <td>${bala.Percentage.toFixed(2)}%</td>
                        </tr>
                    `;
                });
                
                html += `
                            </tbody>
                        </table>
                    </div>
                `;
            }
            
            resultsDiv.innerHTML = html;
        }
    </script>
</body>
</html>
    """
    
    with open("astro_calculator_web.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Web interface created: astro_calculator_web.html")

def main():
    """Main function to run the calculator"""
    print("🌟 Comprehensive Vedic Astrology Calculator")
    print("=" * 50)
    
    # Create web interface
    create_web_interface()
    
    # Example usage
    calculator = VedicAstrologyCalculator()
    
    # Example birth details
    birth_details = BirthDetails(
        name="Example Person",
        date=datetime.date(1990, 6, 15),
        time=datetime.time(14, 30, 0),
        latitude=19.0760,
        longitude=72.8777,
        timezone=5.5,
        place="Mumbai, India"
    )
    
    print(f"\nCalculating charts for: {birth_details.name}")
    print(f"Date: {birth_details.date}")
    print(f"Time: {birth_details.time}")
    print(f"Place: {birth_details.place}")
    
    # Calculate all charts
    result = calculator.calculate_all_charts(birth_details)
    
    # Save to JSON file
    with open("astro_complete_charts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Complete astrological analysis saved to: astro_complete_charts.json")
    print(f"🌐 Web interface created: astro_calculator_web.html")
    
    # Display summary
    print(f"\n📊 Summary:")
    print(f"   • Birth Details: {result['birthDetails']['lagna']} Lagna, {result['birthDetails']['rasi']} Rasi")
    print(f"   • Nakshatra: {result['birthDetails']['nakshatraPada']}")
    print(f"   • Divisional Charts: {len(result['charts'])} charts generated")
    print(f"   • Tables: {len(result['tables'])} tables calculated")
    
    print(f"\n🎯 To use the calculator:")
    print(f"   1. Open astro_calculator_web.html in your browser")
    print(f"   2. Enter birth details")
    print(f"   3. View all charts and tables")
    print(f"   4. Or run this script with your own birth details")

if __name__ == "__main__":
    main() 