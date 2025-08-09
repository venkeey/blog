#!/usr/bin/env python3
"""
Maitreya-Style Chart Generator for July 21, 1975, 23:10, Nellore, India
"""

import json
import pyswisseph as swe
from datetime import datetime

def generate_chart():
    """Generate comprehensive astrological chart using Maitreya algorithms"""
    
    print("🕉️  Maitreya-Style Chart Calculator")
    print("=" * 50)
    
    # Birth details
    name = "User Chart - Nellore"
    year, month, day = 1975, 7, 21
    hour, minute = 23, 10
    
    # Nellore, India coordinates
    latitude = 14.4426  # 14°26'33"N
    longitude = 79.9865  # 79°59'11"E
    timezone_offset = 5.5  # IST
    
    print(f"📅 Birth: {day}/{month}/{year} at {hour:02d}:{minute:02d}")
    print(f"📍 Location: Nellore, India ({latitude}°N, {longitude}°E)")
    
    # Initialize Swiss Ephemeris
    swe.set_sid_mode(swe.SIDM_LAHIRI)  # Lahiri ayanamsa
    
    # Convert to Julian Day
    hour_decimal = hour + minute / 60.0 - timezone_offset
    jd = swe.julday(year, month, day, hour_decimal, swe.GREG_CAL)
    
    # Get ayanamsa
    ayanamsa = swe.get_ayanamsa(jd)
    
    print(f"📊 Julian Day: {jd}")
    print(f"🔄 Ayanamsa (Lahiri): {ayanamsa:.6f}°")
    
    # Planet mapping
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE
    }
    
    # Rasi names
    rasis = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    # Nakshatra names
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    # Calculate planets
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
        "divisional_charts": {}
    }
    
    print("\n🪐 Calculating Planet Positions:")
    
    # Calculate each planet
    for planet_name, planet_id in planets.items():
        try:
            planet_data = swe.calc_ut(jd, planet_id)
            longitude = planet_data[0][0]
            speed = planet_data[0][3]
            
            # Apply ayanamsa for sidereal longitude
            sidereal_longitude = (longitude - ayanamsa) % 360
            
            # Calculate rasi and nakshatra
            rasi = int(sidereal_longitude // 30)
            rasi_longitude = sidereal_longitude % 30
            nakshatra = int(sidereal_longitude // (360/27))
            nakshatra_position = sidereal_longitude % (360/27)
            nakshatra_pada = int(nakshatra_position // (360/27/4)) + 1
            
            retrograde = speed < 0
            
            chart_data["planets"][planet_name] = {
                "tropical_longitude": round(longitude, 6),
                "sidereal_longitude": round(sidereal_longitude, 6),
                "rasi": rasi,
                "rasi_name": rasis[rasi],
                "rasi_longitude": round(rasi_longitude, 6),
                "nakshatra": nakshatra,
                "nakshatra_name": nakshatras[nakshatra],
                "nakshatra_pada": nakshatra_pada,
                "longitude_speed": round(speed, 6),
                "retrograde": retrograde
            }
            
            print(f"   {planet_name:8}: {rasis[rasi]:12} {rasi_longitude:6.2f}° | {nakshatras[nakshatra]}")
            
        except Exception as e:
            print(f"   Error calculating {planet_name}: {e}")
    
    # Add Ketu (opposite of Rahu)
    if 'Rahu' in chart_data["planets"]:
        rahu_data = chart_data["planets"]['Rahu']
        ketu_sidereal = (rahu_data['sidereal_longitude'] + 180) % 360
        ketu_rasi = int(ketu_sidereal // 30)
        ketu_rasi_long = ketu_sidereal % 30
        ketu_nakshatra = int(ketu_sidereal // (360/27))
        ketu_nakshatra_pos = ketu_sidereal % (360/27)
        ketu_pada = int(ketu_nakshatra_pos // (360/27/4)) + 1
        
        chart_data["planets"]['Ketu'] = {
            "tropical_longitude": round((rahu_data['tropical_longitude'] + 180) % 360, 6),
            "sidereal_longitude": round(ketu_sidereal, 6),
            "rasi": ketu_rasi,
            "rasi_name": rasis[ketu_rasi],
            "rasi_longitude": round(ketu_rasi_long, 6),
            "nakshatra": ketu_nakshatra,
            "nakshatra_name": nakshatras[ketu_nakshatra],
            "nakshatra_pada": ketu_pada,
            "longitude_speed": round(-rahu_data['longitude_speed'], 6),
            "retrograde": rahu_data['retrograde']
        }
        
        print(f"   {'Ketu':8}: {rasis[ketu_rasi]:12} {ketu_rasi_long:6.2f}° | {nakshatras[ketu_nakshatra]}")
    
    # Calculate houses
    print("\n🏠 Calculating Houses:")
    try:
        houses, ascmc = swe.houses(jd, latitude, longitude, b'P')  # Placidus
        
        for i in range(12):
            house_tropical = houses[i]
            house_sidereal = (house_tropical - ayanamsa) % 360
            house_rasi = int(house_sidereal // 30)
            
            chart_data["houses"][f"House_{i+1}"] = {
                "tropical_longitude": round(house_tropical, 6),
                "sidereal_longitude": round(house_sidereal, 6),
                "rasi": house_rasi,
                "rasi_name": rasis[house_rasi]
            }
            
            print(f"   House {i+1:2}: {rasis[house_rasi]:12} {house_sidereal%30:6.2f}°")
    
    except Exception as e:
        print(f"   Error calculating houses: {e}")
    
    # Calculate key divisional charts using Maitreya algorithms
    print("\n📈 Calculating Divisional Charts:")
    
    varga_divisions = {
        'D1': 1, 'D2': 2, 'D3': 3, 'D4': 4, 'D9': 9, 'D10': 10, 'D12': 12, 
        'D16': 16, 'D20': 20, 'D24': 24, 'D27': 27, 'D30': 30, 'D60': 60
    }
    
    for varga_name, division in varga_divisions.items():
        chart_data["divisional_charts"][varga_name] = {}
        
        for planet_name, planet_data in chart_data["planets"].items():
            sidereal_lon = planet_data["sidereal_longitude"]
            
            # Maitreya's Varga calculation algorithms
            if division == 1:  # D1 - Rasi
                varga_rasi = int(sidereal_lon // 30)
            elif division == 2:  # D2 - Hora
                temp = ((sidereal_lon - 15) % 60) + 90
                varga_rasi = int(temp // 30) % 12
            elif division == 9:  # D9 - Navamsa
                temp = (9 * sidereal_lon) % 360
                varga_rasi = int(temp // 30)
            elif division == 12:  # D12 - Dvadasamsa
                rasi = int(sidereal_lon // 30)
                rasi_len = sidereal_lon % 30
                temp = (rasi * 30 + rasi_len * 12) % 360
                varga_rasi = int(temp // 30)
            else:  # Generic formula
                temp = (division * sidereal_lon) % 360
                varga_rasi = int(temp // 30)
            
            chart_data["divisional_charts"][varga_name][planet_name] = {
                "rasi": varga_rasi,
                "rasi_name": rasis[varga_rasi]
            }
        
        print(f"   {varga_name} calculated")
    
    # Chart summary
    ascendant_rasi = chart_data["houses"]["House_1"]["rasi"]
    moon_rasi = chart_data["planets"]["Moon"]["rasi"]
    sun_rasi = chart_data["planets"]["Sun"]["rasi"]
    birth_nakshatra = chart_data["planets"]["Moon"]["nakshatra_name"]
    
    chart_data["chart_summary"] = {
        "ascendant_sign": rasis[ascendant_rasi],
        "moon_sign": rasis[moon_rasi],
        "sun_sign": rasis[sun_rasi],
        "birth_nakshatra": birth_nakshatra
    }
    
    # Save to JSON
    output_file = "maitreya_chart_july21_1975.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chart_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Chart calculation complete!")
    print(f"📁 Output saved to: {output_file}")
    
    print(f"\n📊 Chart Summary:")
    print(f"   Ascendant: {chart_data['chart_summary']['ascendant_sign']}")
    print(f"   Moon Sign: {chart_data['chart_summary']['moon_sign']}")
    print(f"   Sun Sign: {chart_data['chart_summary']['sun_sign']}")
    print(f"   Birth Nakshatra: {chart_data['chart_summary']['birth_nakshatra']}")
    print(f"   Ayanamsa: {ayanamsa:.6f}°")
    
    print(f"\n🎯 Generated {len(chart_data['divisional_charts'])} divisional charts")
    
    return chart_data

if __name__ == "__main__":
    generate_chart() 