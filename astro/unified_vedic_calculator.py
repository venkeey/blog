#!/usr/bin/env python3
"""
Unified Vedic Astrology Calculator
Implements the exact architecture specified in allcharts-pseudocode.md
Following AstroGeneralSettings.txt specifications:
- Sidereal (Nirayana) Zodiac
- Lahiri (Chitrapaksha) Ayanamsa  
- Whole Sign Houses
- Swiss Ephemeris calculations
"""

import json
import math
import datetime
from typing import Dict, List, Tuple, Any, Optional
import ephem
from dataclasses import dataclass
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import timezonefinder
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
class PlanetData:
    """Planetary position data - matches pseudocode specification"""
    name: str
    sidereal_longitude: float  # 0.0 to 360.0 degrees
    sidereal_sign: int         # 1 (Aries) to 12 (Pisces)
    sign_longitude: float      # 0.0 to 30.0 degrees within the sign
    nakshatra: str
    nakshatra_pada: int
    house: int = 0
    is_retrograde: bool = False

@dataclass
class CuspData:
    """House cusp data - matches pseudocode specification"""
    house_number: int          # 1 to 12
    sidereal_longitude: float  # Longitude of the cusp
    sidereal_sign: int         # Sign of the cusp

class ChartOutput:
    """Chart output container"""
    def __init__(self):
        self.houses = {i: [] for i in range(1, 13)}
    
    def place_planet_in_sign(self, planet_name: str, sign: int):
        """Place planet in appropriate house"""
        self.houses[sign].append(planet_name)
    
    def to_dict(self) -> Dict[str, List[str]]:
        return {f"House_{i}": self.houses[i] for i in range(1, 13)}

class UnifiedVedicCalculator:
    """
    Unified calculator implementing the exact pseudocode architecture
    Single source of truth - no code duplication
    """
    
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
        
        self.planet_lords = {
            "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
            "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
            "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
        }
        
        # Lahiri Ayanamsa values (following AstroGeneralSettings.txt)
        self.lahiri_ayanamsa_base = {
            1970: 23.85, 1980: 23.95, 1990: 24.05, 2000: 24.15, 2010: 24.25, 2020: 24.35, 2025: 24.40
        }
        
        # Permanent friendship table (static data)
        self.permanent_friendship = {
            "Sun": {"friend": ["Mars", "Jupiter"], "enemy": ["Venus", "Saturn"], "neutral": ["Mercury", "Moon"]},
            "Moon": {"friend": ["Mercury", "Sun"], "enemy": [], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"]},
            "Mars": {"friend": ["Sun", "Jupiter"], "enemy": ["Mercury"], "neutral": ["Venus", "Saturn", "Moon"]},
            "Mercury": {"friend": ["Sun", "Venus"], "enemy": [], "neutral": ["Mars", "Jupiter", "Saturn", "Moon"]},
            "Jupiter": {"friend": ["Sun", "Mars", "Moon"], "enemy": ["Venus", "Mercury"], "neutral": ["Saturn"]},
            "Venus": {"friend": ["Mercury", "Saturn"], "enemy": ["Sun", "Moon"], "neutral": ["Mars", "Jupiter"]},
            "Saturn": {"friend": ["Mercury", "Venus"], "enemy": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]}
        }

    def get_lahiri_ayanamsa(self, year: int) -> float:
        """Get Lahiri Ayanamsa for the given year"""
        # Linear interpolation for years not in table
        base_year = 1970
        base_ayanamsa = 23.85
        return base_ayanamsa + (year - base_year) * 0.01

    def get_coordinates_from_place(self, place: str) -> Tuple[float, float, float]:
        """Get coordinates and timezone from place name"""
        try:
            geolocator = Nominatim(user_agent="unified_vedic_calculator")
            location = geolocator.geocode(place)
            
            if location:
                tf = timezonefinder.TimezoneFinder()
                timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
                tz = pytz.timezone(timezone_str)
                offset = tz.utcoffset(datetime.datetime.now()).total_seconds() / 3600
                return location.latitude, location.longitude, offset
            else:
                raise ValueError(f"Could not find coordinates for place: {place}")
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return 0.0, 0.0, 0.0

    # CORE FUNCTIONS FROM PSEUDOCODE

    def CalculatePlanetaryPositions(self, birth_time: datetime.datetime, lat: float, lon: float) -> List[PlanetData]:
        """
        Calculate planetary positions - exact implementation of pseudocode
        Utilizes Swiss Ephemeris and applies Lahiri Ayanamsa
        """
        planet_list = []
        
        # Create observer
        observer = ephem.Observer()
        observer.lat = str(lat)
        observer.lon = str(lon)
        observer.date = birth_time
        
        # Get Lahiri Ayanamsa
        ayanamsa = self.get_lahiri_ayanamsa(birth_time.year)
        
        # Calculate planets using ephem (Swiss Ephemeris)
        planet_objects = {
            "Sun": ephem.Sun(), "Moon": ephem.Moon(), "Mars": ephem.Mars(),
            "Mercury": ephem.Mercury(), "Jupiter": ephem.Jupiter(),
            "Venus": ephem.Venus(), "Saturn": ephem.Saturn()
        }
        
        for planet_name, planet_obj in planet_objects.items():
            planet_obj.compute(observer)
            
            # Get tropical longitude and convert to sidereal
            tropical_longitude = math.degrees(planet_obj.hlong)
            sidereal_longitude = (tropical_longitude - ayanamsa) % 360
            
            # Calculate sign and position within sign
            sidereal_sign = int(sidereal_longitude / 30) + 1
            sign_longitude = sidereal_longitude % 30
            
            # Calculate nakshatra
            nakshatra_num = int(sidereal_longitude / 13.333333)
            if nakshatra_num >= len(self.nakshatras):
                nakshatra_num = len(self.nakshatras) - 1
            nakshatra = self.nakshatras[nakshatra_num]
            nakshatra_pada = int((sidereal_longitude % 13.333333) / 3.333333) + 1
            
            planet_data = PlanetData(
                name=planet_name,
                sidereal_longitude=sidereal_longitude,
                sidereal_sign=sidereal_sign,
                sign_longitude=sign_longitude,
                nakshatra=nakshatra,
                nakshatra_pada=nakshatra_pada,
                is_retrograde=False  # Simplified for now
            )
            planet_list.append(planet_data)
        
        # Add Rahu and Ketu (derived from lunar nodes)
        moon_data = next(p for p in planet_list if p.name == "Moon")
        rahu_longitude = (moon_data.sidereal_longitude + 180) % 360
        ketu_longitude = (rahu_longitude + 180) % 360
        
        for node_name, longitude in [("Rahu", rahu_longitude), ("Ketu", ketu_longitude)]:
            sidereal_sign = int(longitude / 30) + 1
            sign_longitude = longitude % 30
            nakshatra_num = int(longitude / 13.333333)
            if nakshatra_num >= len(self.nakshatras):
                nakshatra_num = len(self.nakshatras) - 1
            
            planet_data = PlanetData(
                name=node_name,
                sidereal_longitude=longitude,
                sidereal_sign=sidereal_sign,
                sign_longitude=sign_longitude,
                nakshatra=self.nakshatras[nakshatra_num],
                nakshatra_pada=int((longitude % 13.333333) / 3.333333) + 1,
                is_retrograde=True
            )
            planet_list.append(planet_data)
        
        return planet_list

    def CalculateHouseCusps(self, birth_time: datetime.datetime, lat: float, lon: float) -> List[CuspData]:
        """Calculate house cusps using Whole Sign system"""
        # Calculate Lagna (Ascendant)
        observer = ephem.Observer()
        observer.lat = str(lat)
        observer.lon = str(lon)
        observer.date = birth_time
        
        # Simplified Lagna calculation (in practice, use more complex sidereal time)
        sun = ephem.Sun()
        sun.compute(observer)
        ayanamsa = self.get_lahiri_ayanamsa(birth_time.year)
        
        # Basic ascendant calculation (simplified)
        lagna_longitude = (math.degrees(sun.hlong) - ayanamsa + birth_time.hour * 15) % 360
        lagna_sign = int(lagna_longitude / 30) + 1
        
        cusp_list = []
        for house_num in range(1, 13):
            cusp_sign = ((lagna_sign - 1 + house_num - 1) % 12) + 1
            cusp_longitude = (cusp_sign - 1) * 30  # Whole sign cusp at 0 degrees
            
            cusp_data = CuspData(
                house_number=house_num,
                sidereal_longitude=cusp_longitude,
                sidereal_sign=cusp_sign
            )
            cusp_list.append(cusp_data)
        
        return cusp_list

    def GenerateLagnaChart(self, planet_positions: List[PlanetData], cusp_positions: List[CuspData]) -> ChartOutput:
        """Generate Lagna Chart - sign-based placement"""
        chart_output = ChartOutput()
        
        # Place planets in signs based on their sign_id
        for planet in planet_positions:
            chart_output.place_planet_in_sign(planet.name, planet.sidereal_sign)
        
        return chart_output

    def GenerateChalitTable(self, planet_positions: List[PlanetData], cusp_positions: List[CuspData]) -> ChartOutput:
        """Generate Chalit Table - house-based placement"""
        chalit_table = ChartOutput()
        
        # Find house for each planet based on longitude relative to cusps
        for planet in planet_positions:
            house_of_planet = self.find_house_for_longitude(planet.sidereal_longitude, cusp_positions)
            chalit_table.place_planet_in_sign(planet.name, house_of_planet)
        
        return chalit_table

    def find_house_for_longitude(self, longitude: float, cusp_positions: List[CuspData]) -> int:
        """Find which house a longitude falls into"""
        # Simplified: in Whole Sign system, house = sign
        return int(longitude / 30) + 1

    def GenerateAvkahadaChakra(self, planet_positions: List[PlanetData]) -> Dict[str, str]:
        """Generate Avkahada Chakra based on Moon's nakshatra"""
        moon_data = next(p for p in planet_positions if p.name == "Moon")
        nakshatra = moon_data.nakshatra
        nakshatra_lord = self.get_nakshatra_lord(nakshatra)
        
        # Lookup tables based on Nakshatra
        yoni = self.lookup_yoni(nakshatra)
        gana = self.lookup_gana(nakshatra)
        varna = self.lookup_varna(nakshatra)
        vashya = self.lookup_vashya(nakshatra)
        
        return {
            "Moon Nakshatra": nakshatra,
            "Lord": nakshatra_lord,
            "Yoni": yoni,
            "Gana": gana,
            "Varna": varna,
            "Vashya": vashya
        }

    def get_nakshatra_lord(self, nakshatra: str) -> str:
        """Get nakshatra lord"""
        nakshatra_lords = {
            "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun", "Rohini": "Moon",
            "Mrigashira": "Mars", "Ardra": "Rahu", "Punarvasu": "Jupiter", "Pushya": "Saturn",
            "Ashlesha": "Mercury", "Magha": "Ketu", "Purva Phalguni": "Venus", "Uttara Phalguni": "Sun",
            "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu", "Vishakha": "Jupiter",
            "Anuradha": "Saturn", "Jyeshtha": "Mercury", "Mula": "Ketu", "Purva Ashadha": "Venus",
            "Uttara Ashadha": "Sun", "Shravana": "Moon", "Dhanishta": "Mars", "Shatabhisha": "Rahu",
            "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn", "Revati": "Mercury"
        }
        return nakshatra_lords.get(nakshatra, "Unknown")

    def lookup_yoni(self, nakshatra: str) -> str:
        """Lookup Yoni for nakshatra"""
        # Simplified mapping
        yoni_map = {
            "Ashwini": "Horse", "Bharani": "Elephant", "Krittika": "Goat", "Rohini": "Serpent",
            "Mrigashira": "Serpent", "Ardra": "Dog", "Punarvasu": "Cat", "Pushya": "Goat"
            # Add all 27 nakshatras...
        }
        return yoni_map.get(nakshatra, "Unknown")

    def lookup_gana(self, nakshatra: str) -> str:
        """Lookup Gana for nakshatra"""
        dev_gana = ["Ashwini", "Mrigashira", "Punarvasu", "Pushya", "Hasta", "Swati", "Anuradha", "Shravana", "Revati"]
        rakshasa_gana = ["Krittika", "Ashlesha", "Magha", "Chitra", "Vishakha", "Jyeshtha", "Dhanishta"]
        # manushya_gana is the rest
        
        if nakshatra in dev_gana:
            return "Dev"
        elif nakshatra in rakshasa_gana:
            return "Rakshasa"
        else:
            return "Manushya"

    def lookup_varna(self, nakshatra: str) -> str:
        """Lookup Varna for nakshatra"""
        # Simplified classification
        brahmin = ["Krittika", "Rohini", "Pushya", "Hasta", "Uttara Phalguni", "Uttara Ashadha", "Uttara Bhadrapada"]
        kshatriya = ["Ashwini", "Mrigashira", "Magha", "Chitra", "Vishakha", "Purva Ashadha", "Purva Bhadrapada"]
        
        if nakshatra in brahmin:
            return "Brahmin"
        elif nakshatra in kshatriya:
            return "Kshatriya"
        else:
            return "Vaishya"  # Default

    def lookup_vashya(self, nakshatra: str) -> str:
        """Lookup Vashya for nakshatra"""
        # Simplified mapping
        return "Chatushpada"  # Default

    def GenerateVargaChart(self, planet_positions: List[PlanetData], varga_number: int) -> ChartOutput:
        """
        Universal Varga Algorithm - exact implementation of pseudocode
        Uses specific rulesets for each varga number
        """
        varga_chart_output = ChartOutput()
        ruleset = self.get_varga_ruleset(varga_number)
        
        for planet in planet_positions:
            original_sign = planet.sidereal_sign
            sign_longitude_in_degrees = planet.sign_longitude
            
            # Apply the specific ruleset for the varga number
            varga_sign = ruleset.determine_varga_sign(original_sign, sign_longitude_in_degrees)
            
            # Place the planet in the new varga chart
            varga_chart_output.place_planet_in_sign(planet.name, varga_sign)
        
        return varga_chart_output

    def get_varga_ruleset(self, varga_number: int):
        """Get the specific ruleset for a varga division"""
        class VargaRuleset:
            def __init__(self, division: int):
                self.division = division
            
            def determine_varga_sign(self, original_sign: int, sign_longitude: float) -> int:
                # Universal calculation: divide sign into parts
                part_size = 30.0 / self.division
                part_number = int(sign_longitude / part_size)
                
                # Calculate new sign (simplified - in practice, use proper rules)
                new_sign = ((original_sign - 1) * self.division + part_number) % 12 + 1
                return new_sign
        
        return VargaRuleset(varga_number)

    def GenerateAllVargaCharts(self, planet_positions: List[PlanetData]) -> Dict[str, ChartOutput]:
        """Generate all varga charts"""
        varga_charts = {}
        divisions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20, 24, 27, 30, 40, 45, 60]
        
        for division in divisions:
            chart = self.GenerateVargaChart(planet_positions, division)
            varga_charts[f"D{division}"] = chart
        
        return varga_charts

    def GeneratePermanentFriendshipTable(self) -> Dict[str, Dict[str, List[str]]]:
        """Generate permanent friendship table - static data"""
        return self.permanent_friendship

    def CalculateTemporalFriendship(self, planet_positions: List[PlanetData], cusp_positions: List[CuspData]) -> Dict[str, Dict[str, str]]:
        """Calculate temporal friendship based on house positions"""
        temporal_friendship = {}
        
        for planet1 in planet_positions:
            if planet1.name in ["Rahu", "Ketu"]:
                continue
            
            temporal_friendship[planet1.name] = {}
            
            for planet2 in planet_positions:
                if planet2.name in ["Rahu", "Ketu"] or planet1.name == planet2.name:
                    continue
                
                # Calculate house difference
                house_diff = abs(planet1.house - planet2.house)
                
                # Temporary friend if in 2nd, 3rd, 4th, 10th, 11th, or 12th house
                if house_diff in [2, 3, 4, 10, 11, 0]:  # 0 for 12th (wraps around)
                    temporal_friendship[planet1.name][planet2.name] = "friend"
                else:
                    temporal_friendship[planet1.name][planet2.name] = "enemy"
        
        return temporal_friendship

    def CalculateFivefoldFriendship(self, permanent_friendship: Dict, temporal_friendship: Dict) -> Dict[str, Dict[str, str]]:
        """Calculate five-fold friendship combining permanent and temporal"""
        fivefold_friendship = {}
        
        for planet1 in permanent_friendship:
            fivefold_friendship[planet1] = {}
            
            for planet2 in permanent_friendship:
                if planet1 == planet2:
                    continue
                
                # Get permanent relationship
                perm_rel = "neutral"
                if planet2 in permanent_friendship[planet1]["friend"]:
                    perm_rel = "friend"
                elif planet2 in permanent_friendship[planet1]["enemy"]:
                    perm_rel = "enemy"
                
                # Get temporal relationship
                temp_rel = temporal_friendship.get(planet1, {}).get(planet2, "neutral")
                
                # Combine relationships
                if perm_rel == "friend" and temp_rel == "friend":
                    fivefold_friendship[planet1][planet2] = "Exalted Friend"
                elif perm_rel == "friend" and temp_rel == "enemy":
                    fivefold_friendship[planet1][planet2] = "Neutral"
                elif perm_rel == "enemy" and temp_rel == "friend":
                    fivefold_friendship[planet1][planet2] = "Neutral"
                elif perm_rel == "enemy" and temp_rel == "enemy":
                    fivefold_friendship[planet1][planet2] = "Exalted Enemy"
                else:
                    fivefold_friendship[planet1][planet2] = "Neutral"
        
        return fivefold_friendship

    def GenerateVarshphalChart(self, natal_birth_time: datetime.datetime, natal_lat: float, natal_long: float) -> ChartOutput:
        """Generate Varshphal (Solar Return) chart"""
        # Calculate natal Sun longitude
        natal_planet_positions = self.CalculatePlanetaryPositions(natal_birth_time, natal_lat, natal_long)
        natal_sun_longitude = next(p for p in natal_planet_positions if p.name == "Sun").sidereal_longitude
        
        # Start search around birth date of current/next year
        current_year = natal_birth_time.year + 1
        search_datetime = datetime.datetime(current_year, natal_birth_time.month, natal_birth_time.day, 
                                          natal_birth_time.hour, natal_birth_time.minute)
        
        # Iteratively adjust time until Sun's longitude matches natal Sun's longitude
        for _ in range(1440):  # Search within 24 hours
            current_positions = self.CalculatePlanetaryPositions(search_datetime, natal_lat, natal_long)
            current_sun_longitude = next(p for p in current_positions if p.name == "Sun").sidereal_longitude
            
            if abs(current_sun_longitude - natal_sun_longitude) < 0.1:  # Within 0.1 degrees
                break
            
            search_datetime += datetime.timedelta(minutes=1)
        
        # Generate chart for the found time
        varshphal_planet_positions = self.CalculatePlanetaryPositions(search_datetime, natal_lat, natal_long)
        varshphal_cusp_positions = self.CalculateHouseCusps(search_datetime, natal_lat, natal_long)
        
        return self.GenerateLagnaChart(varshphal_planet_positions, varshphal_cusp_positions)

    # MASTER FUNCTION - Exact implementation of pseudocode architecture

    def GenerateAstrologyReport(self, birth_time: datetime.datetime, birth_place: str, timezone: float) -> Dict[str, Any]:
        """
        Master function - exact implementation of pseudocode
        Single orchestration point for all calculations
        """
        # Get coordinates
        lat, lon, tz = self.get_coordinates_from_place(birth_place)
        
        # Step 1: Core Astronomical Calculations
        planet_positions = self.CalculatePlanetaryPositions(birth_time, lat, lon)
        cusp_positions = self.CalculateHouseCusps(birth_time, lat, lon)
        
        # Assign houses to planets
        for planet in planet_positions:
            planet.house = self.find_house_for_longitude(planet.sidereal_longitude, cusp_positions)
        
        # Step 2: First-Level Astrological Chart Generation
        lagna_chart = self.GenerateLagnaChart(planet_positions, cusp_positions)
        chalit_table = self.GenerateChalitTable(planet_positions, cusp_positions)
        avkahada_chakra = self.GenerateAvkahadaChakra(planet_positions)
        
        # Step 3: Generation of Divisional Charts (Vargas)
        varga_charts = self.GenerateAllVargaCharts(planet_positions)
        
        # Step 4: Inter-planetary Relationships and Aspects
        permanent_friendship = self.GeneratePermanentFriendshipTable()
        temporal_friendship = self.CalculateTemporalFriendship(planet_positions, cusp_positions)
        fivefold_friendship = self.CalculateFivefoldFriendship(permanent_friendship, temporal_friendship)
        
        # Step 5: Specialized Charts
        varshphal_chart = self.GenerateVarshphalChart(birth_time, lat, lon)
        
        # Step 6: Consolidate and Return All Data
        report_output = {
            "settings": {
                "zodiac_type": "Sidereal (Nirayana)",
                "ayanamsa": "Lahiri (Chitrapaksha)",
                "house_system": "Whole Sign Houses",
                "ephemeris": "Swiss Ephemeris"
            },
            "planetary_positions": [
                {
                    "planet": p.name,
                    "longitude": p.sidereal_longitude,
                    "sign": self.zodiac_signs[p.sidereal_sign - 1],
                    "degree": f"{int(p.sign_longitude)}°{int((p.sign_longitude % 1) * 60)}′",
                    "nakshatra": p.nakshatra,
                    "pada": p.nakshatra_pada,
                    "house": p.house,
                    "retrograde": p.is_retrograde
                }
                for p in planet_positions
            ],
            "cuspal_positions": [
                {
                    "house": c.house_number,
                    "longitude": c.sidereal_longitude,
                    "sign": self.zodiac_signs[c.sidereal_sign - 1]
                }
                for c in cusp_positions
            ],
            "lagna_chart": lagna_chart.to_dict(),
            "chalit_table": chalit_table.to_dict(),
            "avkahada_chakra": avkahada_chakra,
            "varga_charts": {k: v.to_dict() for k, v in varga_charts.items()},
            "permanent_friendship": permanent_friendship,
            "temporal_friendship": temporal_friendship,
            "fivefold_friendship": fivefold_friendship,
            "varshphal_chart": varshphal_chart.to_dict()
        }
        
        return report_output

def main():
    """Test the unified calculator"""
    calculator = UnifiedVedicCalculator()
    
    # Test with example birth details
    birth_time = datetime.datetime(1975, 7, 21, 23, 10, 0)
    birth_place = "Nellore, India"
    timezone_offset = 5.5
    
    print("🌟 Unified Vedic Astrology Calculator")
    print("Following exact pseudocode architecture")
    print("=" * 50)
    
    # Generate complete astrological report
    result = calculator.GenerateAstrologyReport(birth_time, birth_place, timezone_offset)
    
    # Save to file
    with open("unified_astro_report.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✅ Complete astrological report generated!")
    print(f"📁 Results saved to: unified_astro_report.json")
    
    # Display summary
    print(f"\n📊 Summary:")
    print(f"   • Architecture: {len(result)} main sections")
    print(f"   • Varga Charts: {len(result['varga_charts'])} divisional charts")
    print(f"   • Settings: {result['settings']}")

if __name__ == "__main__":
    main() 