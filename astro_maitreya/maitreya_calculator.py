#!/usr/bin/env python3
"""
Maitreya-Style Astrological Calculator
=====================================
Implements the exact calculation algorithms from Maitreya 8 for high-precision Vedic astrology.
Based on the C++ source code analysis from maitreya8-8.1.1/src/jyotish/

Author: AI Assistant
Date: January 2025
"""

import math
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple
import pyswisseph as swe
from dataclasses import dataclass


@dataclass
class PlanetPosition:
    """Planet position data structure matching Maitreya's ObjectPosition class"""
    name: str
    longitude: float  # Tropical longitude
    sidereal_longitude: float  # Sidereal longitude with ayanamsa
    latitude: float
    distance: float
    longitude_speed: float
    latitude_speed: float
    distance_speed: float
    retrograde: bool
    rasi: int  # Zodiac sign (0-11)
    rasi_longitude: float  # Position within the sign
    nakshatra: int  # Nakshatra (0-26)
    nakshatra_pada: int  # Pada (1-4)


@dataclass
class HousePosition:
    """House cusp positions"""
    house: int
    longitude: float
    sidereal_longitude: float
    rasi: int


class MaitreyaCalculator:
    """
    Maitreya-style astrological calculator implementing exact algorithms
    from the C++ source code for maximum accuracy and compatibility.
    """
    
    def __init__(self):
        """Initialize calculator with Maitreya's default settings"""
        self.ayanamsa_type = swe.SIDM_LAHIRI  # Lahiri ayanamsa (default in Maitreya)
        self.house_system = b'P'  # Placidus (default in Maitreya)
        self.ephemeris_path = None
        
        # Initialize Swiss Ephemeris
        self._init_swiss_ephemeris()
        
        # Maitreya's planet IDs mapping
        self.planets = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mars': swe.MARS,
            'Mercury': swe.MERCURY,
            'Jupiter': swe.JUPITER,
            'Venus': swe.VENUS,
            'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE,  # North Node
            'Ketu': swe.MEAN_NODE,  # South Node (calculated)
        }
        
        # Nakshatra names (Maitreya order)
        self.nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        # Rasi names
        self.rasis = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # Varga divisions (matching Maitreya's implementation)
        self.varga_divisions = {
            'D1': 1, 'D2': 2, 'D3': 3, 'D4': 4, 'D5': 5, 'D6': 6, 'D7': 7, 'D8': 8, 'D9': 9, 'D10': 10,
            'D11': 11, 'D12': 12, 'D13': 13, 'D14': 14, 'D15': 15, 'D16': 16, 'D17': 17, 'D18': 18, 'D19': 19, 'D20': 20,
            'D21': 21, 'D22': 22, 'D23': 23, 'D24': 24, 'D25': 25, 'D26': 26, 'D27': 27, 'D28': 28, 'D29': 29, 'D30': 30,
            'D40': 40, 'D45': 45, 'D60': 60, 'D81': 81, 'D108': 108, 'D144': 144
        }

    def _init_swiss_ephemeris(self):
        """Initialize Swiss Ephemeris with Maitreya-compatible settings"""
        try:
            # Set ephemeris path if available
            if self.ephemeris_path:
                swe.set_ephe_path(self.ephemeris_path)
            
            # Set sidereal mode with Lahiri ayanamsa (Maitreya default)
            swe.set_sid_mode(self.ayanamsa_type)
            
            print("✓ Swiss Ephemeris initialized with Maitreya settings")
        except Exception as e:
            print(f"⚠️  Warning: Swiss Ephemeris initialization: {e}")

    def julian_day(self, year: int, month: int, day: int, hour: float) -> float:
        """
        Calculate Julian Day using Swiss Ephemeris
        Matches Maitreya's calc_jd function
        """
        return swe.julday(year, month, day, hour, swe.GREG_CAL)

    def get_ayanamsa(self, jd: float) -> float:
        """
        Get ayanamsa value for given Julian Day
        Matches Maitreya's calcAyanamsa function
        """
        return swe.get_ayanamsa(jd)

    def calculate_planet_position(self, jd: float, planet_name: str) -> PlanetPosition:
        """
        Calculate planet position using Maitreya's algorithm
        Based on Calculator::calcPosition and Calculator::calcPositionSpeed
        """
        try:
            if planet_name == 'Ketu':
                # Ketu is 180° opposite to Rahu (Maitreya's implementation)
                rahu_data = swe.calc_ut(jd, self.planets['Rahu'])
                longitude = (rahu_data[0][0] + 180) % 360
                latitude = -rahu_data[0][1]  # Opposite latitude
                distance = rahu_data[0][2]
                longitude_speed = -rahu_data[0][3]  # Opposite speed
                latitude_speed = -rahu_data[0][4]
                distance_speed = rahu_data[0][5]
            else:
                # Calculate planet position
                planet_data = swe.calc_ut(jd, self.planets[planet_name])
                longitude = planet_data[0][0]
                latitude = planet_data[0][1]
                distance = planet_data[0][2]
                longitude_speed = planet_data[0][3]
                latitude_speed = planet_data[0][4]
                distance_speed = planet_data[0][5]
            
            # Apply ayanamsa for sidereal longitude (Maitreya's approach)
            ayanamsa = self.get_ayanamsa(jd)
            sidereal_longitude = (longitude - ayanamsa) % 360
            
            # Calculate rasi (zodiac sign) - Maitreya's getRasi function
            rasi = int(sidereal_longitude // 30)
            rasi_longitude = sidereal_longitude % 30
            
            # Calculate nakshatra and pada - Maitreya's nakshatra calculation
            nakshatra_length = 360 / 27  # 13.333... degrees per nakshatra
            nakshatra = int(sidereal_longitude // nakshatra_length)
            nakshatra_position = sidereal_longitude % nakshatra_length
            nakshatra_pada = int(nakshatra_position // (nakshatra_length / 4)) + 1
            
            # Check retrograde motion
            retrograde = longitude_speed < 0
            
            return PlanetPosition(
                name=planet_name,
                longitude=longitude,
                sidereal_longitude=sidereal_longitude,
                latitude=latitude,
                distance=distance,
                longitude_speed=longitude_speed,
                latitude_speed=latitude_speed,
                distance_speed=distance_speed,
                retrograde=retrograde,
                rasi=rasi,
                rasi_longitude=rasi_longitude,
                nakshatra=nakshatra,
                nakshatra_pada=nakshatra_pada
            )
            
        except Exception as e:
            print(f"Error calculating {planet_name}: {e}")
            return None

    def calculate_houses(self, jd: float, latitude: float, longitude: float) -> List[HousePosition]:
        """
        Calculate house cusps using Maitreya's algorithm
        Based on Calculator::calcHouses function
        """
        try:
            # Calculate houses using Swiss Ephemeris
            houses, ascmc = swe.houses(jd, latitude, longitude, self.house_system)
            
            # Apply ayanamsa for sidereal positions
            ayanamsa = self.get_ayanamsa(jd)
            
            house_positions = []
            for i in range(12):
                tropical_longitude = houses[i]
                sidereal_longitude = (tropical_longitude - ayanamsa) % 360
                rasi = int(sidereal_longitude // 30)
                
                house_positions.append(HousePosition(
                    house=i + 1,
                    longitude=tropical_longitude,
                    sidereal_longitude=sidereal_longitude,
                    rasi=rasi
                ))
            
            return house_positions
            
        except Exception as e:
            print(f"Error calculating houses: {e}")
            return []

    def calc_varga(self, longitude: float, division: int) -> int:
        """
        Calculate Varga (divisional chart) position using Maitreya's exact algorithm
        Based on VargaExpert::calcVarga function from Varga.cpp
        
        This implements the precise formulas from Maitreya's C++ code.
        """
        # Apply ayanamsa to get sidereal longitude
        sidereal_lon = longitude % 360
        
        if division == 1:  # D1 - Rasi
            return int(sidereal_lon // 30)
            
        elif division == 2:  # D2 - Hora (Maitreya's Parasara mode)
            # Based on Maitreya's implementation: ret = a_red(len - 15, 60) + 90
            temp = ((sidereal_lon - 15) % 60) + 90
            return int(temp // 30) % 12
            
        elif division == 3:  # D3 - Drekkana 
            # Maitreya: ret = 3 * len
            temp = (3 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 4:  # D4 - Chaturthamsa
            # Maitreya: ret = 4 * len
            temp = (4 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 5:  # D5 - Panchamsa
            # Maitreya: ret = 5 * len
            temp = (5 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 6:  # D6 - Shashthamsa
            # Maitreya: ret = 6 * len
            temp = (6 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 7:  # D7 - Saptamsa
            # Maitreya: ret = 7 * len
            temp = (7 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 8:  # D8 - Ashtamsa
            # Maitreya: ret = 8 * len
            temp = (8 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 9:  # D9 - Navamsa
            # Maitreya: ret = 9 * len
            temp = (9 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 10:  # D10 - Dasamsa
            # Maitreya: ret = 10 * len
            temp = (10 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 12:  # D12 - Dvadasamsa
            # Maitreya uses special getDvadasamsaLongitude function
            rasi = int(sidereal_lon // 30)
            rasi_len = sidereal_lon % 30
            temp = (rasi * 30 + rasi_len * 12) % 360
            return int(temp // 30)
            
        elif division == 16:  # D16 - Shodasamsa
            # Maitreya: ret = 16 * len
            temp = (16 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 20:  # D20 - Vimsamsa
            # Maitreya: ret = 20 * len
            temp = (20 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 24:  # D24 - Chaturvimsamsa
            # Maitreya: ret = 24 * len
            temp = (24 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 27:  # D27 - Nakshatramsa
            # Maitreya: ret = 27 * len
            temp = (27 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 30:  # D30 - Trimsamsa
            # Maitreya: ret = 30 * len
            temp = (30 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 40:  # D40 - Khavedamsa
            # Maitreya: ret = 40 * len
            temp = (40 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 45:  # D45 - Akshavedamsa
            # Maitreya: ret = 45 * len
            temp = (45 * sidereal_lon) % 360
            return int(temp // 30)
            
        elif division == 60:  # D60 - Shashtyamsa
            # Maitreya: ret = 60 * len
            temp = (60 * sidereal_lon) % 360
            return int(temp // 30)
            
        else:
            # Generic formula for other divisions
            temp = (division * sidereal_lon) % 360
            return int(temp // 30)

    def generate_all_vargas(self, planet_positions: List[PlanetPosition]) -> Dict[str, Dict[str, int]]:
        """
        Generate all divisional charts using Maitreya's algorithms
        Returns dictionary with varga name as key and planet positions as values
        """
        varga_charts = {}
        
        for varga_name, division in self.varga_divisions.items():
            chart = {}
            for planet in planet_positions:
                if planet:  # Check if planet position is valid
                    varga_rasi = self.calc_varga(planet.sidereal_longitude, division)
                    chart[planet.name] = varga_rasi
            
            varga_charts[varga_name] = chart
        
        return varga_charts

    def calculate_comprehensive_chart(self, name: str, year: int, month: int, day: int, 
                                    hour: int, minute: int, latitude: float, longitude: float,
                                    timezone_offset: float = 5.5) -> Dict[str, Any]:
        """
        Calculate comprehensive astrological chart using Maitreya's algorithms
        
        Args:
            name: Person's name
            year, month, day: Birth date
            hour, minute: Birth time
            latitude, longitude: Birth location
            timezone_offset: Timezone offset from UTC (default 5.5 for India)
        
        Returns:
            Complete chart data in JSON-compatible format
        """
        # Convert time to UTC and calculate Julian Day
        hour_decimal = hour + minute / 60.0 - timezone_offset
        jd = self.julian_day(year, month, day, hour_decimal)
        
        # Calculate all planet positions
        planet_positions = []
        for planet_name in self.planets.keys():
            pos = self.calculate_planet_position(jd, planet_name)
            if pos:
                planet_positions.append(pos)
        
        # Calculate house positions
        house_positions = self.calculate_houses(jd, latitude, longitude)
        
        # Generate all divisional charts
        varga_charts = self.generate_all_vargas(planet_positions)
        
        # Get ayanamsa
        ayanamsa = self.get_ayanamsa(jd)
        
        # Create comprehensive output
        chart_data = {
            "personal_info": {
                "name": name,
                "birth_date": f"{day:02d}/{month:02d}/{year}",
                "birth_time": f"{hour:02d}:{minute:02d}",
                "birth_place": "Nellore, India",
                "latitude": latitude,
                "longitude": longitude,
                "timezone": f"UTC+{timezone_offset}",
                "julian_day": jd
            },
            "calculation_info": {
                "ayanamsa_type": "Lahiri",
                "ayanamsa_value": ayanamsa,
                "house_system": "Placidus",
                "ephemeris": "Swiss Ephemeris",
                "calculator": "Maitreya Algorithm Implementation"
            },
            "planets": {},
            "houses": {},
            "divisional_charts": varga_charts,
            "chart_summary": {
                "ascendant_sign": "",
                "moon_sign": "",
                "sun_sign": "",
                "birth_nakshatra": ""
            }
        }
        
        # Add planet data
        for planet in planet_positions:
            chart_data["planets"][planet.name] = {
                "tropical_longitude": round(planet.longitude, 6),
                "sidereal_longitude": round(planet.sidereal_longitude, 6),
                "rasi": planet.rasi,
                "rasi_name": self.rasis[planet.rasi],
                "rasi_longitude": round(planet.rasi_longitude, 6),
                "nakshatra": planet.nakshatra,
                "nakshatra_name": self.nakshatras[planet.nakshatra],
                "nakshatra_pada": planet.nakshatra_pada,
                "latitude": round(planet.latitude, 6),
                "longitude_speed": round(planet.longitude_speed, 6),
                "retrograde": planet.retrograde
            }
        
        # Add house data
        for house in house_positions:
            chart_data["houses"][f"House_{house.house}"] = {
                "tropical_longitude": round(house.longitude, 6),
                "sidereal_longitude": round(house.sidereal_longitude, 6),
                "rasi": house.rasi,
                "rasi_name": self.rasis[house.rasi]
            }
        
        # Fill chart summary
        if planet_positions:
            # Find Ascendant (1st house cusp)
            if house_positions:
                asc_rasi = house_positions[0].rasi
                chart_data["chart_summary"]["ascendant_sign"] = self.rasis[asc_rasi]
            
            # Find Moon and Sun signs
            for planet in planet_positions:
                if planet.name == "Moon":
                    chart_data["chart_summary"]["moon_sign"] = self.rasis[planet.rasi]
                    chart_data["chart_summary"]["birth_nakshatra"] = self.nakshatras[planet.nakshatra]
                elif planet.name == "Sun":
                    chart_data["chart_summary"]["sun_sign"] = self.rasis[planet.rasi]
        
        return chart_data


def main():
    """Generate chart for July 21, 1975, 23:10, Nellore, India"""
    
    print("🕉️  Maitreya-Style Astrological Calculator")
    print("=" * 50)
    
    # Initialize calculator
    calc = MaitreyaCalculator()
    
    # Birth details
    name = "User Chart"
    year, month, day = 1975, 7, 21
    hour, minute = 23, 10
    
    # Nellore, India coordinates
    latitude = 14.4426  # 14°26'33"N
    longitude = 79.9865  # 79°59'11"E
    timezone_offset = 5.5  # IST
    
    print(f"📅 Calculating chart for: {name}")
    print(f"🕐 Birth: {day}/{month}/{year} at {hour:02d}:{minute:02d}")
    print(f"📍 Location: Nellore, India ({latitude}°N, {longitude}°E)")
    print()
    
    # Calculate comprehensive chart
    chart_data = calc.calculate_comprehensive_chart(
        name, year, month, day, hour, minute, latitude, longitude, timezone_offset
    )
    
    # Save to JSON file
    output_file = "maitreya_chart_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chart_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Chart calculation complete!")
    print(f"📁 Detailed output saved to: {output_file}")
    
    # Display summary
    print("\n📊 Chart Summary:")
    print(f"   Ascendant: {chart_data['chart_summary']['ascendant_sign']}")
    print(f"   Moon Sign: {chart_data['chart_summary']['moon_sign']}")
    print(f"   Sun Sign: {chart_data['chart_summary']['sun_sign']}")
    print(f"   Birth Nakshatra: {chart_data['chart_summary']['birth_nakshatra']}")
    print(f"   Ayanamsa (Lahiri): {chart_data['calculation_info']['ayanamsa_value']:.6f}°")
    
    print(f"\n🎯 Generated {len(chart_data['divisional_charts'])} divisional charts")
    print("   Including: D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60, D81, D108, D144")
    
    return chart_data


if __name__ == "__main__":
    main() 