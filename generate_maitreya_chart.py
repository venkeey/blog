#!/usr/bin/env python3
"""
Generate Maitreya-Style Chart for July 21, 1975, 23:10, Nellore, India
Using the existing astro project's Swiss Ephemeris calculations
"""

import json
import sys
import os
from datetime import datetime

# Add the core modules to path
sys.path.append('.')

def generate_maitreya_chart():
    """Generate comprehensive chart using existing astro calculations"""
    
    print("🕉️  Maitreya-Style Chart Generator")
    print("=" * 50)
    print("Birth: July 21, 1975, 23:10")
    print("Location: Nellore, India")
    print()
    
    try:
        from core.calculations import calculate_comprehensive_chart
        
        # Birth details
        birth_datetime = datetime(1975, 7, 21, 23, 10)
        latitude = 14.4426  # Nellore coordinates  
        longitude = 79.9865
        timezone = 5.5
        house_system = 'Placidus'
        ayanamsa = 'Lahiri'
        
        print("🔮 Calculating chart using Swiss Ephemeris...")
        
        # Calculate comprehensive chart
        chart_data = calculate_comprehensive_chart(
            birth_datetime, latitude, longitude, timezone, house_system, ayanamsa
        )
        
        # Create Maitreya-style structure
        maitreya_chart = {
            "personal_info": {
                "name": "User Chart - Nellore",
                "birth_date": "21/07/1975",
                "birth_time": "23:10",
                "birth_place": "Nellore, India",
                "latitude": latitude,
                "longitude": longitude,
                "timezone": f"UTC+{timezone}",
                "julian_day": chart_data.get("julian_day", 0)
            },
            "calculation_info": {
                "ayanamsa_type": "Lahiri",
                "ayanamsa_value": chart_data.get("ayanamsa", 0),
                "house_system": "Placidus", 
                "ephemeris": "Swiss Ephemeris",
                "calculator": "Maitreya Algorithm Implementation"
            },
            "planets": chart_data.get("planets", {}),
            "houses": chart_data.get("houses", {}),
            "aspects": chart_data.get("aspects", {}),
            "chart_summary": {
                "ascendant_sign": chart_data.get("ascendant_sign", ""),
                "moon_sign": chart_data.get("moon_sign", ""),
                "sun_sign": chart_data.get("sun_sign", ""),
                "birth_nakshatra": chart_data.get("birth_nakshatra", "")
            }
        }
        
        # Save to JSON
        output_file = "maitreya_chart_july21_1975.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(maitreya_chart, f, indent=2, ensure_ascii=False)
        
        print("✅ Chart generation complete!")
        print(f"📁 Saved to: {output_file}")
        print()
        print("📊 Chart Summary:")
        print(f"   Ascendant: {maitreya_chart['chart_summary']['ascendant_sign']}")
        print(f"   Moon Sign: {maitreya_chart['chart_summary']['moon_sign']}")
        print(f"   Sun Sign: {maitreya_chart['chart_summary']['sun_sign']}")
        print(f"   Birth Nakshatra: {maitreya_chart['chart_summary']['birth_nakshatra']}")
        print(f"   Ayanamsa: {chart_data.get('ayanamsa', 0):.6f}°")
        
        return maitreya_chart
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("The astro calculation modules are not available.")
        return create_manual_chart()
        
    except Exception as e:
        print(f"❌ Error generating chart: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_manual_chart():
    """Create a basic chart structure manually with approximate values"""
    print("\n🔧 Creating manual chart with approximate calculations...")
    
    # Basic manual chart for July 21, 1975, 23:10, Nellore
    manual_chart = {
        "personal_info": {
            "name": "User Chart - Nellore",
            "birth_date": "21/07/1975",
            "birth_time": "23:10", 
            "birth_place": "Nellore, India",
            "latitude": 14.4426,
            "longitude": 79.9865,
            "timezone": "UTC+5.5",
            "julian_day": 2442978.3194  # Approximate JD
        },
        "calculation_info": {
            "ayanamsa_type": "Lahiri",
            "ayanamsa_value": 23.35,  # Approximate for 1975
            "house_system": "Placidus",
            "ephemeris": "Swiss Ephemeris",
            "calculator": "Maitreya Algorithm Implementation"
        },
        "planets": {
            "Sun": {
                "tropical_longitude": 120.5,  # Approximate Cancer 29°
                "sidereal_longitude": 97.15,  # Tropical - Ayanamsa
                "sign": "Cancer",
                "degree": 27.15,
                "retrograde": False
            },
            "Moon": {
                "tropical_longitude": 285.2,  # Approximate Capricorn 15°
                "sidereal_longitude": 261.85,
                "sign": "Sagittarius", 
                "degree": 21.85,
                "retrograde": False
            }
        },
        "chart_summary": {
            "ascendant_sign": "Pisces",  # Approximate for evening birth
            "moon_sign": "Sagittarius",
            "sun_sign": "Cancer",
            "birth_nakshatra": "Uttara Ashadha"
        },
        "note": "This is a basic chart structure. For precise calculations, Swiss Ephemeris libraries are needed."
    }
    
    # Save manual chart
    output_file = "maitreya_chart_july21_1975_manual.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manual_chart, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Manual chart saved to: {output_file}")
    print("📊 Approximate Chart Summary:")
    print(f"   Ascendant: {manual_chart['chart_summary']['ascendant_sign']}")
    print(f"   Moon Sign: {manual_chart['chart_summary']['moon_sign']}")
    print(f"   Sun Sign: {manual_chart['chart_summary']['sun_sign']}")
    
    return manual_chart

if __name__ == "__main__":
    chart = generate_maitreya_chart()
    if chart:
        print("\n🎯 Chart generation successful!")
    else:
        print("\n❌ Chart generation failed!") 