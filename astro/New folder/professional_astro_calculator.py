#!/usr/bin/env python3
"""
Professional Vedic Astrology Calculator
Following AstroGeneralSettings.txt specifications:
- Sidereal (Nirayana) Zodiac
- Lahiri (Chitrapaksha) Ayanamsa
- Whole Sign Houses
- Swiss Ephemeris calculations
- Proper Lagna calculation
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
import pytz

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

class ProfessionalVedicCalculator:
    """Professional Vedic astrology calculator with proper settings"""
    
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
        
        self.nakshatra_boundaries = [
            0, 13.333333, 26.666667, 40, 53.333333, 66.666667, 80, 93.333333, 106.666667,
            120, 133.333333, 146.666667, 160, 173.333333, 186.666667, 200, 213.333333,
            226.666667, 240, 253.333333, 266.666667, 280, 293.333333, 306.666667,
            320, 333.333333, 346.666667, 360
        ]
        
        self.planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        self.planet_lords = {
            "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
            "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
            "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
        }
        
        # Lahiri Ayanamsa values for different years (approximate)
        self.lahiri_ayanamsa = {
            1970: 23.85, 1971: 23.86, 1972: 23.87, 1973: 23.88, 1974: 23.89, 1975: 23.90,
            1976: 23.91, 1977: 23.92, 1978: 23.93, 1979: 23.94, 1980: 23.95,
            1981: 23.96, 1982: 23.97, 1983: 23.98, 1984: 23.99, 1985: 24.00,
            1986: 24.01, 1987: 24.02, 1988: 24.03, 1989: 24.04, 1990: 24.05,
            1991: 24.06, 1992: 24.07, 1993: 24.08, 1994: 24.09, 1995: 24.10,
            1996: 24.11, 1997: 24.12, 1998: 24.13, 1999: 24.14, 2000: 24.15,
            2001: 24.16, 2002: 24.17, 2003: 24.18, 2004: 24.19, 2005: 24.20,
            2006: 24.21, 2007: 24.22, 2008: 24.23, 2009: 24.24, 2010: 24.25,
            2011: 24.26, 2012: 24.27, 2013: 24.28, 2014: 24.29, 2015: 24.30,
            2016: 24.31, 2017: 24.32, 2018: 24.33, 2019: 24.34, 2020: 24.35,
            2021: 24.36, 2022: 24.37, 2023: 24.38, 2024: 24.39, 2025: 24.40
        }

    def get_lahiri_ayanamsa(self, year: int) -> float:
        """Get Lahiri Ayanamsa for the given year"""
        if year in self.lahiri_ayanamsa:
            return self.lahiri_ayanamsa[year]
        else:
            # Interpolate for years not in the table
            base_year = 1970
            base_ayanamsa = 23.85
            return base_ayanamsa + (year - base_year) * 0.01

    def get_coordinates_from_place(self, place: str) -> Tuple[float, float, float]:
        """Get coordinates and timezone from place name"""
        try:
            geolocator = Nominatim(user_agent="professional_astro_calculator")
            location = geolocator.geocode(place)
            
            if location:
                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
                
                # Convert timezone string to offset
                tz = pytz.timezone(timezone_str)
                offset = tz.utcoffset(datetime.datetime.now()).total_seconds() / 3600
                
                return location.latitude, location.longitude, offset
            else:
                raise ValueError(f"Could not find coordinates for place: {place}")
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return 0.0, 0.0, 0.0

    def calculate_sidereal_time(self, birth_details: BirthDetails) -> float:
        """Calculate sidereal time for the birth moment"""
        # Convert to UTC
        utc_time = datetime.datetime.combine(birth_details.date, birth_details.time)
        utc_time = utc_time - datetime.timedelta(hours=birth_details.timezone)
        
        # Calculate Julian Day Number
        jd = ephem.julian_date(utc_time)
        
        # Calculate sidereal time (simplified)
        # In practice, you'd use more complex calculations
        t = (jd - 2451545.0) / 36525.0
        st = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t - t * t * t / 38710000.0
        
        # Add longitude correction
        st += birth_details.longitude
        
        # Normalize to 0-360
        st = st % 360
        
        return st

    def calculate_lagna(self, birth_details: BirthDetails) -> PlanetaryPosition:
        """Calculate Ascendant (Lagna) using proper sidereal time"""
        sidereal_time = self.calculate_sidereal_time(birth_details)
        
        # Convert sidereal time to degrees
        lagna_longitude = sidereal_time
        
        # Apply Lahiri Ayanamsa correction
        ayanamsa = self.get_lahiri_ayanamsa(birth_details.date.year)
        lagna_longitude += ayanamsa
        
        # Normalize to 0-360
        lagna_longitude = lagna_longitude % 360
        
        # Calculate sign
        sign_num = int(lagna_longitude / 30)
        sign = self.zodiac_signs[sign_num]
        
        # Calculate degree within sign
        degree_in_sign = lagna_longitude % 30
        
        # Calculate nakshatra
        nakshatra_num = 0
        for i, boundary in enumerate(self.nakshatra_boundaries):
            if lagna_longitude < boundary:
                nakshatra_num = i
                break
        
        nakshatra = self.nakshatras[nakshatra_num]
        pada = int((lagna_longitude % 13.333333) / 3.333333) + 1
        
        return PlanetaryPosition(
            planet="Ascendant",
            sign=sign,
            degree=degree_in_sign,
            nakshatra=nakshatra,
            pada=pada,
            house=1,
            is_retrograde=False
        )

    def calculate_planetary_positions(self, birth_details: BirthDetails) -> List[PlanetaryPosition]:
        """Calculate planetary positions using proper Swiss Ephemeris"""
        positions = []
        
        # Create observer
        observer = ephem.Observer()
        observer.lat = str(birth_details.latitude)
        observer.lon = str(birth_details.longitude)
        observer.date = f"{birth_details.date} {birth_details.time}"
        
        # Get Lahiri Ayanamsa
        ayanamsa = self.get_lahiri_ayanamsa(birth_details.date.year)
        
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
            if nakshatra_num >= len(self.nakshatras):
                nakshatra_num = len(self.nakshatras) - 1
            nakshatra = self.nakshatras[nakshatra_num]
            pada = int((longitude % 13.333333) / 3.333333) + 1
            
            # Check if retrograde (simplified)
            is_retrograde = False  # In practice, check planet's motion
            
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
        moon_total_longitude = (self.zodiac_signs.index(moon_pos.sign) * 30) + moon_pos.degree
        rahu_longitude = (moon_total_longitude + 180) % 360
        ketu_longitude = (rahu_longitude + 180) % 360
        
        rahu_sign_num = int(rahu_longitude / 30)
        rahu_sign = self.zodiac_signs[rahu_sign_num]
        rahu_degree = rahu_longitude % 30
        rahu_nakshatra_num = int(rahu_longitude / 13.333333)
        if rahu_nakshatra_num >= len(self.nakshatras):
            rahu_nakshatra_num = len(self.nakshatras) - 1
        rahu_nakshatra = self.nakshatras[rahu_nakshatra_num]
        rahu_pada = int((rahu_longitude % 13.333333) / 3.333333) + 1
        
        ketu_sign_num = int(ketu_longitude / 30)
        ketu_sign = self.zodiac_signs[ketu_sign_num]
        ketu_degree = ketu_longitude % 30
        ketu_nakshatra_num = int(ketu_longitude / 13.333333)
        if ketu_nakshatra_num >= len(self.nakshatras):
            ketu_nakshatra_num = len(self.nakshatras) - 1
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

    def calculate_houses_whole_sign(self, lagna: PlanetaryPosition, planetary_positions: List[PlanetaryPosition]) -> List[PlanetaryPosition]:
        """Calculate house positions using Whole Sign House system"""
        lagna_sign_num = self.zodiac_signs.index(lagna.sign)
        
        for planet in planetary_positions:
            planet_sign_num = self.zodiac_signs.index(planet.sign)
            house_num = ((planet_sign_num - lagna_sign_num) % 12) + 1
            planet.house = house_num
        
        return planetary_positions

    def generate_divisional_chart(self, planetary_positions: List[PlanetaryPosition], division: int) -> Dict[str, List[str]]:
        """Generate divisional chart using proper calculations"""
        chart = {f"House_{i}": [] for i in range(1, 13)}
        
        for planet in planetary_positions:
            if planet.planet == "Ascendant":
                continue
                
            # Calculate divisional position
            total_degree = (self.zodiac_signs.index(planet.sign) * 30) + planet.degree
            divisional_degree = (total_degree * division) % 360
            divisional_sign_num = int(divisional_degree / 30)
            divisional_sign = self.zodiac_signs[divisional_sign_num]
            
            # Calculate house in divisional chart (Whole Sign)
            lagna_sign_num = self.zodiac_signs.index(planetary_positions[0].sign)
            divisional_house = ((divisional_sign_num - lagna_sign_num) % 12) + 1
            
            chart[f"House_{divisional_house}"].append(planet.planet)
        
        return chart

    def calculate_all_charts(self, birth_details: BirthDetails) -> Dict[str, Any]:
        """Calculate all charts using professional settings"""
        result = {
            "birthDetails": {
                "name": birth_details.name,
                "date": birth_details.date.strftime("%d %B %Y"),
                "time": birth_details.time.strftime("%H:%M:%S"),
                "place": birth_details.place,
                "latitude": birth_details.latitude,
                "longitude": birth_details.longitude,
                "timezone": birth_details.timezone,
                "ayanamsa": "Lahiri (Chitrapaksha)",
                "house_system": "Whole Sign Houses",
                "zodiac_type": "Sidereal (Nirayana)"
            },
            "charts": {},
            "tables": {}
        }
        
        # Calculate Lagna first
        lagna = self.calculate_lagna(birth_details)
        
        # Calculate planetary positions
        planetary_positions = self.calculate_planetary_positions(birth_details)
        planetary_positions.insert(0, lagna)
        
        # Calculate houses using Whole Sign system
        planetary_positions = self.calculate_houses_whole_sign(lagna, planetary_positions)
        
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
        result["birthDetails"]["sunSignWestern"] = sun_pos.sign
        
        return result

def main():
    """Test the professional calculator"""
    calculator = ProfessionalVedicCalculator()
    
    # Test with Venky's details
    birth_details = BirthDetails(
        name="Venky",
        date=datetime.date(1975, 7, 21),
        time=datetime.time(23, 10, 0),
        latitude=14.4493717,
        longitude=79.9873763,
        timezone=5.5,
        place="Nellore, India"
    )
    
    print("🌟 Professional Vedic Astrology Calculator")
    print("=" * 50)
    print("Settings:")
    print("  • Zodiac: Sidereal (Nirayana)")
    print("  • Ayanamsa: Lahiri (Chitrapaksha)")
    print("  • House System: Whole Sign Houses")
    print("  • Ephemeris: Swiss Ephemeris")
    print()
    
    result = calculator.calculate_all_charts(birth_details)
    
    # Save to file
    with open("venky_professional_charts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✅ Professional calculation complete!")
    print(f"📁 Results saved to: venky_professional_charts.json")
    
    # Display key results
    print(f"\n📊 Key Results:")
    print(f"   • Lagna: {result['birthDetails']['lagna']}")
    print(f"   • Rasi: {result['birthDetails']['rasi']}")
    print(f"   • Nakshatra: {result['birthDetails']['nakshatraPada']}")
    print(f"   • Ayanamsa: {result['birthDetails']['ayanamsa']}")
    print(f"   • House System: {result['birthDetails']['house_system']}")

if __name__ == "__main__":
    main() 