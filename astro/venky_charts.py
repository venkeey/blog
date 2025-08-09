#!/usr/bin/env python3
"""
Direct Astrological Calculation for Venky
Birth Details: 21-07-1975, 23:10, Nellore, India
"""

from comprehensive_astro_calculator import VedicAstrologyCalculator, BirthDetails
import datetime
import json
import os

def calculate_venky_charts():
    """Calculate astrological charts for Venky"""
    
    print("🌟 Astrological Charts for Venky")
    print("=" * 50)
    
    # Venky's birth details
    name = "Venky"
    date_obj = datetime.date(1975, 7, 21)
    time_obj = datetime.time(23, 10, 0)
    place = "Nellore, India"
    
    print(f"📅 Name: {name}")
    print(f"📅 Date: {date_obj.strftime('%d %B %Y')}")
    print(f"⏰ Time: {time_obj.strftime('%H:%M:%S')}")
    print(f"📍 Place: {place}")
    print()
    
    # Create calculator
    calculator = VedicAstrologyCalculator()
    
    # Get coordinates
    print("🌍 Getting coordinates for Nellore, India...")
    lat, lon, tz = calculator.get_coordinates_from_place(place)
    print(f"📍 Coordinates: {lat}, {lon}")
    print(f"⏰ Timezone: {tz}")
    print()
    
    # Create birth details object
    birth_details = BirthDetails(
        name=name,
        date=date_obj,
        time=time_obj,
        latitude=lat,
        longitude=lon,
        timezone=tz,
        place=place
    )
    
    # Calculate all charts
    print("🔮 Calculating astrological charts...")
    result = calculator.calculate_all_charts(birth_details)
    
    print("✅ Calculation complete!")
    print()
    
    # Display summary
    print("📊 Venky's Astrological Summary:")
    print(f"   • Lagna (Ascendant): {result['birthDetails']['lagna']}")
    print(f"   • Rasi (Moon Sign): {result['birthDetails']['rasi']}")
    print(f"   • Nakshatra: {result['birthDetails']['nakshatraPada']}")
    print(f"   • Nakshatra Lord: {result['birthDetails']['nakshatraLord']}")
    print(f"   • Rasi Lord: {result['birthDetails']['rasiLord']}")
    print(f"   • Lagna Lord: {result['birthDetails']['lagnaLord']}")
    print(f"   • Sun Sign (Indian): {result['birthDetails']['sunSignIndian']}")
    print()
    
    # Display planetary positions
    print("🪐 Planetary Positions:")
    for planet in result['planetaryPositions']:
        retrograde = " (R)" if planet['is_retrograde'] else ""
        print(f"   • {planet['planet']}: {planet['sign']} {planet['degree']} {retrograde}")
        print(f"     Nakshatra: {planet['nakshatra']} Pada {planet['pada']}")
        print(f"     House: {planet['house']}")
    print()
    
    # Save to file
    filename = "venky_astrological_charts.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Complete data saved to: {filename}")
    print()
    
    # Show key divisional charts
    print("📈 Key Divisional Charts:")
    key_charts = ["Rasi (D1)", "Navamsa (D9)", "Hora (D2)", "Drekkana (D3)", "Chaturthamsa (D4)"]
    
    for chart_name in key_charts:
        if chart_name in result['charts']:
            chart = result['charts'][chart_name]
            print(f"   • {chart_name}:")
            for house_num in range(1, 13):
                planets = chart.get(f"House_{house_num}", [])
                if planets:
                    print(f"     House {house_num}: {', '.join(planets)}")
            print()
    
    # Show friendship table
    print("🤝 Planetary Friendships:")
    friendship = result['tables']['Friendship']
    for planet, relations in friendship.items():
        print(f"   • {planet}:")
        print(f"     Friends: {', '.join(relations['friend'])}")
        print(f"     Enemies: {', '.join(relations['enemy'])}")
        print(f"     Neutral: {', '.join(relations['neutral'])}")
    print()
    
    # Show Shadbala summary
    print("💪 Planetary Strength (Shadbala):")
    shadbala = result['tables']['Shadbala']
    for planet, bala in shadbala.items():
        print(f"   • {planet}: {bala['Total_Bala']:.2f} ({bala['Percentage']:.1f}%)")
    print()
    
    print("🎉 Analysis complete! Check the JSON file for complete details.")
    print(f"📁 File location: {os.path.abspath(filename)}")
    
    return result

if __name__ == "__main__":
    calculate_venky_charts() 