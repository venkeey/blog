#!/usr/bin/env python3
"""
Test script for the Comprehensive Vedic Astrology Calculator
"""

from comprehensive_astro_calculator import VedicAstrologyCalculator, BirthDetails
import datetime
import json

def test_calculator():
    """Test the calculator with sample data"""
    
    print("🧪 Testing Comprehensive Vedic Astrology Calculator")
    print("=" * 50)
    
    # Create calculator instance
    calculator = VedicAstrologyCalculator()
    
    # Test birth details
    birth_details = BirthDetails(
        name="Test Person",
        date=datetime.date(1990, 6, 15),
        time=datetime.time(14, 30, 0),
        latitude=19.0760,
        longitude=72.8777,
        timezone=5.5,
        place="Mumbai, India"
    )
    
    print(f"📅 Testing with birth details:")
    print(f"   Name: {birth_details.name}")
    print(f"   Date: {birth_details.date}")
    print(f"   Time: {birth_details.time}")
    print(f"   Place: {birth_details.place}")
    print(f"   Coordinates: {birth_details.latitude}, {birth_details.longitude}")
    print()
    
    try:
        # Calculate all charts
        print("🔮 Calculating astrological charts...")
        result = calculator.calculate_all_charts(birth_details)
        
        print("✅ Calculation successful!")
        print()
        
        # Display summary
        print("📊 Results Summary:")
        print(f"   • Lagna: {result['birthDetails']['lagna']}")
        print(f"   • Rasi: {result['birthDetails']['rasi']}")
        print(f"   • Nakshatra: {result['birthDetails']['nakshatraPada']}")
        print(f"   • Divisional Charts: {len(result['charts'])} charts")
        print(f"   • Tables: {len(result['tables'])} tables")
        print()
        
        # Display planetary positions
        print("🪐 Planetary Positions:")
        for planet in result['planetaryPositions']:
            print(f"   • {planet['planet']}: {planet['sign']} {planet['degree']} ({planet['nakshatra']} Pada {planet['pada']})")
        print()
        
        # Display some divisional charts
        print("📈 Sample Divisional Charts:")
        for chart_name, chart in list(result['charts'].items())[:3]:
            print(f"   • {chart_name}:")
            for house_num in range(1, 4):  # Show first 3 houses
                planets = chart.get(f"House_{house_num}", [])
                print(f"     House {house_num}: {', '.join(planets) if planets else 'Empty'}")
            print()
        
        # Display friendship table
        print("🤝 Friendship Table:")
        friendship = result['tables']['Friendship']
        for planet, relations in friendship.items():
            print(f"   • {planet}: Friends={', '.join(relations['friend'])}, Enemies={', '.join(relations['enemy'])}")
        print()
        
        # Save test results
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print("💾 Test results saved to: test_results.json")
        print()
        print("🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Error during calculation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_calculator() 