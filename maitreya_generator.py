#!/usr/bin/env python3
"""
Maitreya Chart Generator - July 21, 1975, 23:10, Nellore, India
"""

import json
from datetime import datetime

def main():
    print("🕉️  Maitreya Chart Generator")
    print("=" * 50)
    
    try:
        # Import from the working astro project
        from core.calculations import calculate_all_planets, calculate_house_positions
        from utils.time_utils import datetime_to_julian_day
        
        print("✅ Astro modules imported successfully")
        
        # Birth details
        birth_datetime = datetime(1975, 7, 21, 23, 10)
        latitude, longitude = 14.4426, 79.9865
        timezone_offset = 5.5
        
        print(f"Birth: {birth_datetime}")
        print(f"Location: Nellore, India ({latitude}, {longitude})")
        
        # Calculate using astro project
        jd = datetime_to_julian_day(birth_datetime)
        planets = calculate_all_planets(birth_datetime, latitude, longitude)
        houses = calculate_house_positions(birth_datetime, latitude, longitude, "P")
        
        print(f"Julian Day: {jd}")
        print(f"Calculated {len(planets)} planets and {len(houses)} houses")
        
        # Create Maitreya chart
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        ayanamsa = 23.35  # Lahiri ayanamsa for 1975
        
        chart = {
            "personal_info": {
                "name": "User Chart - Nellore",
                "birth_date": "21/07/1975", 
                "birth_time": "23:10",
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
                "ephemeris": "Swiss Ephemeris via Astro Project",
                "calculator": "Maitreya Precise Implementation"
            },
            "planets": {},
            "houses": {},
            "chart_summary": {}
        }
        
        # Process planets
        print("\nPlanetary Positions:")
        for planet_name, planet_pos in planets.items():
            sidereal_lon = (planet_pos.longitude - ayanamsa) % 360
            sign_index = int(sidereal_lon // 30)
            degree = sidereal_lon % 30
            
            chart["planets"][planet_name] = {
                "tropical_longitude": round(planet_pos.longitude, 6),
                "sidereal_longitude": round(sidereal_lon, 6),
                "sign": signs[sign_index],
                "degree_in_sign": round(degree, 4),
                "retrograde": planet_pos.retrograde
            }
            
            print(f"  {planet_name}: {signs[sign_index]} {degree:.2f}°")
        
        # Process houses
        print("\nHouse Cusps:")
        for house_num, house_pos in houses.items():
            sidereal_house = (house_pos.longitude - ayanamsa) % 360
            house_sign = int(sidereal_house // 30)
            house_degree = sidereal_house % 30
            
            chart["houses"][f"House_{house_num}"] = {
                "tropical_longitude": round(house_pos.longitude, 6),
                "sidereal_longitude": round(sidereal_house, 6),
                "sign": signs[house_sign],
                "degree_in_sign": round(house_degree, 4)
            }
            
            print(f"  House {house_num}: {signs[house_sign]} {house_degree:.2f}°")
        
        # Chart summary
        chart["chart_summary"] = {
            "ascendant_sign": chart["houses"]["House_1"]["sign"],
            "moon_sign": chart["planets"]["Moon"]["sign"],
            "sun_sign": chart["planets"]["Sun"]["sign"]
        }
        
        # Save chart
        with open("maitreya_chart_precise.json", "w", encoding="utf-8") as f:
            json.dump(chart, f, indent=2, ensure_ascii=False)
        
        print("\n✅ Precise Maitreya chart saved!")
        print(f"Ascendant: {chart['chart_summary']['ascendant_sign']}")
        print(f"Moon Sign: {chart['chart_summary']['moon_sign']}")
        print(f"Sun Sign: {chart['chart_summary']['sun_sign']}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 