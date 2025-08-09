#!/usr/bin/env python3
"""
Generate Precise Maitreya Chart - July 21, 1975, 23:10, Nellore, India
"""

import json
from datetime import datetime

def main():
    print("🕉️  Precise Maitreya Chart Calculator")
    print("=" * 50)
    
    try:
        from core.calculations import calculate_all_planets, calculate_chart_data
        
        # Birth details
        birth_datetime = datetime(1975, 7, 21, 23, 10)
        latitude, longitude = 14.4426, 79.9865
        timezone_offset = 5.5
        
        print(f"Birth: {birth_datetime}")
        print(f"Location: Nellore, India")
        
        # Calculate precise chart
        chart_data = calculate_chart_data(birth_datetime, latitude, longitude, timezone_offset, "Placidus", "Lahiri")
        
        # Create Maitreya-style output
        maitreya_chart = {
            "personal_info": {
                "name": "User Chart - Nellore (Precise)",
                "birth_date": "21/07/1975",
                "birth_time": "23:10",
                "birth_place": "Nellore, India",
                "latitude": latitude,
                "longitude": longitude,
                "timezone": f"UTC+{timezone_offset}"
            },
            "calculation_info": {
                "ayanamsa_type": "Lahiri",
                "ayanamsa_value": chart_data.get("ayanamsa", 0),
                "house_system": "Placidus",
                "ephemeris": "Swiss Ephemeris",
                "calculator": "Maitreya Precise Implementation"
            },
            "planets": chart_data.get("planets", {}),
            "houses": chart_data.get("houses", {}),
            "chart_summary": {
                "ascendant_sign": chart_data.get("ascendant_sign", ""),
                "moon_sign": chart_data.get("moon_sign", ""),
                "sun_sign": chart_data.get("sun_sign", ""),
                "birth_nakshatra": chart_data.get("birth_nakshatra", "")
            }
        }
        
        # Save chart
        with open("maitreya_precise_july21_1975.json", "w", encoding="utf-8") as f:
            json.dump(maitreya_chart, f, indent=2, ensure_ascii=False)
        
        print("✅ Precise chart saved!")
        print(f"Ascendant: {maitreya_chart['chart_summary']['ascendant_sign']}")
        print(f"Moon Sign: {maitreya_chart['chart_summary']['moon_sign']}")
        print(f"Sun Sign: {maitreya_chart['chart_summary']['sun_sign']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 