#!/usr/bin/env python3
"""
Professional Astrological Web Server
Uses the corrected calculator with proper Lahiri Ayanamsa and settings
"""

from flask import Flask, request, jsonify, render_template_string
from professional_astro_calculator import ProfessionalVedicCalculator, BirthDetails
import datetime
import json

app = Flask(__name__)
calculator = ProfessionalVedicCalculator()

# HTML template for the professional web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Vedic Astrology Calculator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .settings-info {
            background: #f8f9fa;
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .settings-info h3 {
            color: #667eea;
            margin-top: 0;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .results {
            margin-top: 30px;
            display: none;
        }
        .chart-section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background: #f9f9f9;
        }
        .chart-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .house-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        .house {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
            text-align: center;
        }
        .house-number {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .planets {
            font-size: 0.9em;
            color: #666;
        }
        .table-section {
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background: #667eea;
            color: white;
        }
        tr:nth-child(even) {
            background: #f2f2f2;
        }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .error {
            color: red;
            text-align: center;
            padding: 10px;
            display: none;
        }
        .download-btn {
            background: #28a745;
            margin-top: 10px;
        }
        .download-btn:hover {
            background: #218838;
        }
        .copy-btn {
            background: #17a2b8;
            margin-top: 10px;
        }
        .copy-btn:hover {
            background: #138496;
        }
        .professional-badge {
            background: #ffc107;
            color: #333;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            display: inline-block;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 Professional Vedic Astrology Calculator <span class="professional-badge">PRO</span></h1>
        
        <div class="settings-info">
            <h3>🔧 Professional Settings Applied:</h3>
            <ul>
                <li><strong>Zodiac Type:</strong> Sidereal (Nirayana)</li>
                <li><strong>Ayanamsa:</strong> Lahiri (Chitrapaksha)</li>
                <li><strong>House System:</strong> Whole Sign Houses</li>
                <li><strong>Ephemeris:</strong> Swiss Ephemeris</li>
                <li><strong>Calculation Method:</strong> Professional Grade</li>
            </ul>
        </div>
        
        <form id="astroForm">
            <div class="form-group">
                <label for="name">Full Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="date">Date of Birth:</label>
                <input type="date" id="date" name="date" required>
            </div>
            
            <div class="form-group">
                <label for="time">Time of Birth:</label>
                <input type="time" id="time" name="time" required>
            </div>
            
            <div class="form-group">
                <label for="place">Place of Birth:</label>
                <input type="text" id="place" name="place" placeholder="e.g., Mumbai, India" required>
            </div>
            
            <button type="submit">Calculate Professional Charts</button>
        </form>
        
        <div class="loading" id="loading">
            <h3>🔮 Calculating your professional astrological charts...</h3>
            <p>Using Lahiri Ayanamsa and Swiss Ephemeris for maximum accuracy.</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <!-- Results will be populated here -->
        </div>
    </div>

    <script>
        document.getElementById('astroForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                name: formData.get('name'),
                date: formData.get('date'),
                time: formData.get('time'),
                place: formData.get('place')
            };
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error('Calculation failed');
                }
                
                const result = await response.json();
                displayResults(result);
                
            } catch (error) {
                document.getElementById('error').textContent = 'Error: ' + error.message;
                document.getElementById('error').style.display = 'block';
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            
            let html = `
                <h2>📊 Professional Astrological Analysis</h2>
                <div class="chart-section">
                    <h3>Birth Details</h3>
                    <p><strong>Name:</strong> ${data.birthDetails.name}</p>
                    <p><strong>Date:</strong> ${data.birthDetails.date}</p>
                    <p><strong>Time:</strong> ${data.birthDetails.time}</p>
                    <p><strong>Place:</strong> ${data.birthDetails.place}</p>
                    <p><strong>Lagna (Ascendant):</strong> ${data.birthDetails.lagna} <span class="professional-badge">PRO</span></p>
                    <p><strong>Rasi (Moon Sign):</strong> ${data.birthDetails.rasi}</p>
                    <p><strong>Nakshatra:</strong> ${data.birthDetails.nakshatraPada}</p>
                    <p><strong>Ayanamsa:</strong> ${data.birthDetails.ayanamsa}</p>
                    <p><strong>House System:</strong> ${data.birthDetails.house_system}</p>
                    <button class="download-btn" onclick="downloadJSON(data)">Download Professional Data (JSON)</button>
                    <button class="copy-btn" onclick="copyToClipboard(data)">Copy JSON to Clipboard</button>
                </div>
                
                <h2>🪐 Planetary Positions (Professional)</h2>
                <div class="chart-section">
                    <table>
                        <thead>
                            <tr>
                                <th>Planet</th>
                                <th>Sign</th>
                                <th>Degree</th>
                                <th>Nakshatra</th>
                                <th>Pada</th>
                                <th>House</th>
                                <th>Retrograde</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.planetaryPositions.forEach(planet => {
                html += `
                    <tr>
                        <td>${planet.planet}</td>
                        <td>${planet.sign}</td>
                        <td>${planet.degree}</td>
                        <td>${planet.nakshatra}</td>
                        <td>${planet.pada}</td>
                        <td>${planet.house}</td>
                        <td>${planet.is_retrograde ? 'Yes' : 'No'}</td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                    </table>
                </div>
            `;
            
            // Add divisional charts
            html += '<h2>📈 Professional Divisional Charts</h2>';
            Object.entries(data.charts).forEach(([chartName, chart]) => {
                html += `
                    <div class="chart-section">
                        <div class="chart-title">${chartName}</div>
                        <div class="house-grid">
                `;
                
                for (let i = 1; i <= 12; i++) {
                    const planets = chart[`House_${i}`] || [];
                    html += `
                        <div class="house">
                            <div class="house-number">House ${i}</div>
                            <div class="planets">${planets.join(', ') || 'Empty'}</div>
                        </div>
                    `;
                }
                
                html += `
                        </div>
                    </div>
                `;
            });
            
            resultsDiv.innerHTML = html;
        }
        
        function downloadJSON(data) {
            try {
                const dataStr = JSON.stringify(data, null, 2);
                const dataBlob = new Blob([dataStr], {type: 'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'professional_astrological_charts.json';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                alert('Professional data download started! Check your downloads folder.');
            } catch (error) {
                console.error('Download error:', error);
                alert('Download failed. Please try again or copy the data manually.');
            }
        }
        
        function copyToClipboard(data) {
            try {
                const dataStr = JSON.stringify(data, null, 2);
                navigator.clipboard.writeText(dataStr).then(function() {
                    alert('Professional JSON data copied to clipboard! You can now paste it into a text file.');
                }).catch(function(err) {
                    console.error('Copy failed:', err);
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = dataStr;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    alert('Professional JSON data copied to clipboard! You can now paste it into a text file.');
                });
            } catch (error) {
                console.error('Copy error:', error);
                alert('Copy failed. Please try the download button instead.');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate astrological charts with professional settings"""
    try:
        data = request.get_json()
        
        # Parse date and time
        date_obj = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
        time_obj = datetime.datetime.strptime(data['time'], '%H:%M').time()
        
        # Get coordinates from place
        lat, lon, tz = calculator.get_coordinates_from_place(data['place'])
        
        # Create birth details
        birth_details = BirthDetails(
            name=data['name'],
            date=date_obj,
            time=time_obj,
            latitude=lat,
            longitude=lon,
            timezone=tz,
            place=data['place']
        )
        
        # Calculate all charts with professional settings
        result = calculator.calculate_all_charts(birth_details)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'Professional astrology calculator is running',
        'settings': {
            'ayanamsa': 'Lahiri (Chitrapaksha)',
            'house_system': 'Whole Sign Houses',
            'zodiac_type': 'Sidereal (Nirayana)',
            'ephemeris': 'Swiss Ephemeris'
        }
    })

if __name__ == '__main__':
    print("🌟 Starting Professional Vedic Astrology Calculator Server")
    print("=" * 70)
    print("🔧 Professional Settings:")
    print("   • Ayanamsa: Lahiri (Chitrapaksha)")
    print("   • House System: Whole Sign Houses")
    print("   • Zodiac: Sidereal (Nirayana)")
    print("   • Ephemeris: Swiss Ephemeris")
    print("=" * 70)
    print("📱 Web Interface: http://localhost:5000")
    print("🔍 Health Check: http://localhost:5000/health")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000) 