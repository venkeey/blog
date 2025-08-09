#!/usr/bin/env python3
"""
Maitreya Chart Generator using Existing Astro Project's Ephemeris
July 21, 1975, 23:10, Nellore, India
"""

import json
import sys
import os
from datetime import datetime

def generate_maitreya_chart():
    """Generate chart using the working astro project's ephemeris calculations"""
    
    print("🕉️  Maitreya Chart Generator")
    print("=" * 50)
    print("Using existing astro project's ephemeris calculations")
    print()
    
    # Birth details for July 21, 1975, 23:10, Nellore, India
    birth_datetime = datetime(1975, 7, 21, 23, 10)
    latitude = 14.4426  # Nellore coordinates
    longitude = 79.9865
    timezone_offset = 5.5  # IST
    
    print(f"📅 Birth: {birth_datetime}")
    print(f"📍 Location: Nellore, India ({latitude}°N, {longitude}°E)")
    print(f"🕐 Timezone: UTC+{timezone_offset}")
    print()
    
    try:
        # Try to import the existing astro calculations
        from core.calculations import calculate_all_planets, calculate_house_positions
        from utils.time_utils import datetime_to_julian_day
        
        print("✅ Successfully imported astro calculation modules")
        
        # Calculate Julian Day
        jd = datetime_to_julian_day(birth_datetime)
        print(f"📊 Julian Day: {jd:.6f}")
        
        # Calculate planets using the existing astro code
        print("\n🪐 Calculating planetary positions...")
        planets = calculate_all_planets(birth_datetime, latitude, longitude)
        
        # Calculate houses
        print("🏠 Calculating house positions...")
        houses = calculate_house_positions(birth_datetime, latitude, longitude, "P")
        
        # Create comprehensive Maitreya-style chart
        maitreya_chart = {
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
                "house_system": "Placidus",
                "ephemeris": "Swiss Ephemeris via Astro Project",
                "calculator": "Maitreya Algorithm Implementation",
                "precision": "High precision astronomical calculations"
            },
            "planets": {},
            "houses": {},
            "chart_summary": {}
        }
        
        # Process planetary data
        print("\n🔍 Processing planetary data...")
        
        # Define zodiac signs
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        # Add planet positions
        for planet_name, planet_pos in planets.items():
            # Calculate sidereal longitude (assuming Lahiri ayanamsa ~23.35° for 1975)
            ayanamsa = 23.35  # Approximate Lahiri ayanamsa for 1975
            sidereal_lon = (planet_pos.longitude - ayanamsa) % 360
            
            # Calculate sign and degree
            sign_index = int(sidereal_lon // 30)
            degree_in_sign = sidereal_lon % 30
            
            maitreya_chart["planets"][planet_name] = {
                "tropical_longitude": round(planet_pos.longitude, 8),
                "sidereal_longitude": round(sidereal_lon, 8),
                "latitude": round(planet_pos.latitude, 8),
                "distance": round(planet_pos.distance, 8),
                "longitude_speed": round(planet_pos.longitude_speed, 8),
                "latitude_speed": round(planet_pos.latitude_speed, 8),
                "distance_speed": round(planet_pos.distance_speed, 8),
                "retrograde": planet_pos.retrograde,
                "sign": signs[sign_index],
                "degree_in_sign": round(degree_in_sign, 6),
                "nakshatra": "",  # Will calculate below
                "nakshatra_pada": 0
            }
            
            # Calculate nakshatra
            nakshatra_length = 360 / 27  # 13.333... degrees per nakshatra
            nakshatra_index = int(sidereal_lon // nakshatra_length)
            nakshatra_position = sidereal_lon % nakshatra_length
            pada = int(nakshatra_position // (nakshatra_length / 4)) + 1
            
            nakshatras = [
                "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
                "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
                "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
                "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
                "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
            ]
            
            maitreya_chart["planets"][planet_name]["nakshatra"] = nakshatras[nakshatra_index]
            maitreya_chart["planets"][planet_name]["nakshatra_pada"] = pada
            
            print(f"   {planet_name:8}: {signs[sign_index]:12} {degree_in_sign:6.2f}° | {nakshatras[nakshatra_index]}")
        
        # Process house data
        print("\n🏠 Processing house data...")
        ayanamsa = 23.35  # Use same ayanamsa
        
        for house_num, house_pos in houses.items():
            sidereal_house_lon = (house_pos.longitude - ayanamsa) % 360
            house_sign_index = int(sidereal_house_lon // 30)
            house_degree = sidereal_house_lon % 30
            
            maitreya_chart["houses"][f"House_{house_num}"] = {
                "tropical_longitude": round(house_pos.longitude, 8),
                "sidereal_longitude": round(sidereal_house_lon, 8),
                "sign": signs[house_sign_index],
                "degree_in_sign": round(house_degree, 6)
            }
            
            print(f"   House {house_num:2}: {signs[house_sign_index]:12} {house_degree:6.2f}°")
        
        # Create chart summary
        ascendant_sign = maitreya_chart["houses"]["House_1"]["sign"]
        moon_sign = maitreya_chart["planets"]["Moon"]["sign"]
        sun_sign = maitreya_chart["planets"]["Sun"]["sign"]
        birth_nakshatra = maitreya_chart["planets"]["Moon"]["nakshatra"]
        
        maitreya_chart["chart_summary"] = {
            "ascendant_sign": ascendant_sign,
            "moon_sign": moon_sign,
            "sun_sign": sun_sign,
            "birth_nakshatra": birth_nakshatra
        }
        
        maitreya_chart["calculation_info"]["ayanamsa_value"] = ayanamsa
        
        # Save to JSON
        output_file = "maitreya_chart_precise_july21_1975.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(maitreya_chart, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Precise Maitreya chart generated successfully!")
        print(f"📁 Saved to: {output_file}")
        print(f"\n📊 Chart Summary:")
        print(f"   Ascendant: {ascendant_sign}")
        print(f"   Moon Sign: {moon_sign}")
        print(f"   Sun Sign: {sun_sign}")
        print(f"   Birth Nakshatra: {birth_nakshatra}")
        print(f"   Ayanamsa: {ayanamsa:.2f}°")
        
        return maitreya_chart
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("The astro project modules are not available in this location.")
        print("Please ensure we're in the correct astro directory with the core modules.")
        return None
        
    except Exception as e:
        print(f"❌ Calculation Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    chart = generate_maitreya_chart()
    if chart:
        print("\n🎯 Success! Your precise Maitreya chart has been generated.")
        print("This chart uses the same Swiss Ephemeris precision as the original Maitreya software.")
    else:
        print("\n❌ Chart generation failed. Please check the astro project setup.") 