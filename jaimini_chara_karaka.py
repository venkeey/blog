#!/usr/bin/env python3
"""
Jaimini Chara Karaka Calculator using Maitreya's Exact Algorithm
July 21, 1975, 23:10, Nellore, India
"""

import json
from datetime import datetime

def calculate_jaimini_chara_karakas():
    """Calculate Chara Karakas using Maitreya's exact algorithm"""
    
    print("🕉️  Jaimini Chara Karaka Calculator")
    print("=" * 50)
    print("Using Maitreya's exact algorithm")
    print()
    
    try:
        # Import from the working astro project
        from core.calculations import calculate_all_planets
        from utils.time_utils import datetime_to_julian_day
        
        print("✅ Astro modules imported successfully")
        
        # Birth details
        birth_datetime = datetime(1975, 7, 21, 23, 10)
        latitude, longitude = 14.4426, 79.9865
        timezone_offset = 5.5
        
        print(f"📅 Birth: {birth_datetime}")
        print(f"📍 Location: Nellore, India ({latitude}, {longitude})")
        print()
        
        # Calculate planets using astro project
        planets = calculate_all_planets(birth_datetime, latitude, longitude)
        
        print("🪐 Planetary Positions (Sidereal):")
        
        # Apply Lahiri Ayanamsa (approximate for 1975)
        ayanamsa = 23.35
        
        # Calculate sidereal degrees for each planet
        planet_degrees = {}
        
        # Include only the 7 traditional planets (Sun through Saturn)
        # Exclude Rahu/Ketu as per Maitreya's algorithm
        traditional_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        for planet_name in traditional_planets:
            if planet_name in planets:
                planet_pos = planets[planet_name]
                
                # Calculate sidereal longitude
                sidereal_lon = (planet_pos.longitude - ayanamsa) % 360
                
                # Get degree within sign (0-30)
                rasi_longitude = sidereal_lon % 30
                
                # Store the exact degree within sign (Maitreya uses this)
                planet_degrees[planet_name] = rasi_longitude
                
                sign_index = int(sidereal_lon // 30)
                signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
                
                print(f"   {planet_name:8}: {signs[sign_index]:12} {rasi_longitude:8.4f}°")
        
        print(f"\n🔢 Applying Maitreya's Chara Karaka Algorithm:")
        print("   (Based on highest degrees within signs)")
        
        # Sort planets by their degrees within signs (highest first)
        # This follows Maitreya's exact algorithm
        sorted_planets = sorted(planet_degrees.items(), key=lambda x: x[1], reverse=True)
        
        # Define the 7 Chara Karakas in Maitreya's order
        karaka_names = [
            "Atmakaraka (Soul)",
            "Amatyakaraka (Minister)", 
            "Bhratrukaraka (Siblings)",
            "Matrukaraka (Mother)",
            "Pitrukaraka (Father)",
            "Putrakaraka (Children)",
            "Gnatikaraka (Relatives/Knowledge)",
            # "Darakaraka (Spouse)"  # 8th karaka if using 8-karaka system
        ]
        
        # Calculate Chara Karakas
        chara_karakas = {}
        
        print(f"\n⭐ Your Jaimini Chara Karakas:")
        print("   " + "=" * 45)
        
        for i, (planet, degree) in enumerate(sorted_planets[:7]):  # Take top 7
            karaka = karaka_names[i]
            chara_karakas[karaka] = {
                "planet": planet,
                "degree_in_sign": degree,
                "rank": i + 1
            }
            print(f"   {i+1}. {karaka:25} = {planet:8} ({degree:6.2f}°)")
        
        # Create comprehensive result
        jaimini_result = {
            "personal_info": {
                "name": "User Chart - Nellore",
                "birth_date": "21/07/1975",
                "birth_time": "23:10",
                "birth_place": "Nellore, India",
                "calculation_method": "Maitreya Jaimini Algorithm"
            },
            "planetary_degrees": planet_degrees,
            "chara_karakas": chara_karakas,
            "ranking_order": [planet for planet, _ in sorted_planets],
            "significance": {
                "Atmakaraka": "Represents your soul's deepest desires and spiritual path",
                "Amatyakaraka": "Your advisor, career, and worldly achievements",
                "Bhratrukaraka": "Siblings, courage, and communication",
                "Matrukaraka": "Mother, emotions, and nurturing",
                "Pitrukaraka": "Father, authority, and guidance",
                "Putrakaraka": "Children, creativity, and intelligence",
                "Gnatikaraka": "Relatives, community, and acquired knowledge"
            }
        }
        
        # Save results
        with open("jaimini_chara_karakas_july21_1975.json", "w", encoding="utf-8") as f:
            json.dump(jaimini_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Jaimini analysis complete!")
        print(f"📁 Results saved to: jaimini_chara_karakas_july21_1975.json")
        
        # Key insights
        atmakaraka = chara_karakas["Atmakaraka (Soul)"]["planet"]
        amatyakaraka = chara_karakas["Amatyakaraka (Minister)"]["planet"]
        
        print(f"\n🎯 Key Insights:")
        print(f"   Your Atmakaraka (Soul Planet): {atmakaraka}")
        print(f"   Your Amatyakaraka (Career Planet): {amatyakaraka}")
        print(f"   This reveals your soul's primary focus and career path.")
        
        return jaimini_result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = calculate_jaimini_chara_karakas()
    if result:
        print("\n🕉️  Jaimini Chara Karaka calculation successful!")
    else:
        print("\n❌ Calculation failed!") 