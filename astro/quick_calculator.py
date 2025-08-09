#!/usr/bin/env python3
"""
Quick Astrological Calculator - Command Line Version
Enter your birth details and get all charts instantly!
"""

from comprehensive_astro_calculator import VedicAstrologyCalculator, BirthDetails
import datetime
import json
import os

def get_birth_details():
    """Get birth details from user input"""
    print("🌟 Quick Vedic Astrology Calculator")
    print("=" * 40)
    
    # Get name
    name = input("Enter your full name: ").strip()
    if not name:
        name = "User"
    
    # Get date
    while True:
        try:
            date_str = input("Enter date of birth (DD/MM/YYYY): ").strip()
            day, month, year = map(int, date_str.split('/'))
            date_obj = datetime.date(year, month, day)
            break
        except:
            print("❌ Invalid date format. Please use DD/MM/YYYY")
    
    # Get time
    while True:
        try:
            time_str = input("Enter time of birth (HH:MM): ").strip()
            hour, minute = map(int, time_str.split(':'))
            time_obj = datetime.time(hour, minute)
            break
        except:
            print("❌ Invalid time format. Please use HH:MM")
    
    # Get place
    place = input("Enter place of birth (e.g., Mumbai, India): ").strip()
    if not place:
        place = "Mumbai, India"
    
    return name, date_obj, time_obj, place

def main():
    """Main function"""
    try:
        # Get birth details
        name, date_obj, time_obj, place = get_birth_details()
        
        print(f"\n🔮 Calculating charts for {name}...")
        print(f"📅 Date: {date_obj.strftime('%d %B %Y')}")
        print(f"⏰ Time: {time_obj.strftime('%H:%M')}")
        print(f"📍 Place: {place}")
        print()
        
        # Create calculator
        calculator = VedicAstrologyCalculator()
        
        # Get coordinates
        print("🌍 Getting coordinates...")
        lat, lon, tz = calculator.get_coordinates_from_place(place)
        
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
        print("📊 Your Astrological Summary:")
        print(f"   • Lagna (Ascendant): {result['birthDetails']['lagna']}")
        print(f"   • Rasi (Moon Sign): {result['birthDetails']['rasi']}")
        print(f"   • Nakshatra: {result['birthDetails']['nakshatraPada']}")
        print(f"   • Nakshatra Lord: {result['birthDetails']['nakshatraLord']}")
        print(f"   • Rasi Lord: {result['birthDetails']['rasiLord']}")
        print(f"   • Lagna Lord: {result['birthDetails']['lagnaLord']}")
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
        filename = f"astro_charts_{name.replace(' ', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Complete data saved to: {filename}")
        print()
        
        # Show some divisional charts
        print("📈 Key Divisional Charts:")
        key_charts = ["Rasi (D1)", "Navamsa (D9)", "Hora (D2)", "Drekkana (D3)"]
        
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
        
        print("🎉 Analysis complete! Check the JSON file for complete details.")
        print(f"📁 File location: {os.path.abspath(filename)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 