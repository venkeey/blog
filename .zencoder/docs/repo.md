# Repository Information Overview

## Repository Summary
This repository contains a collection of standalone web applications and trading indicator scripts. It includes HTML-based tools for API testing and QR code generation, as well as several TradingView Pine Script indicators for technical analysis.

## Repository Structure
The repository is organized as a flat structure with individual files serving different purposes:
- HTML applications for web-based tools
- Pine Script files for trading indicators
- VS Code configuration for development settings

### Main Repository Components
- **API Tester**: A Postman-like web tool for testing REST APIs
- **QR Code Generator**: A tool for creating personalized QR codes with photo integration
- **Trading Indicators**: Multiple Pine Script indicators for technical analysis in TradingView

## Projects

### API Tester (Web Application)
**Main File**: api-tester.html

#### Language & Runtime
**Language**: HTML, CSS, JavaScript
**Runtime**: Web Browser
**Framework**: Vanilla JavaScript (No framework)

#### Dependencies
**External Libraries**: None (Pure JavaScript implementation)

#### Usage & Operations
```
Open api-tester.html in any modern web browser
```

#### Main Features
- REST API request configuration (GET, POST, PUT, PATCH, DELETE, OPTIONS)
- Custom header management
- Request body configuration (JSON, Form Data)
- Response visualization with formatting
- Error handling and status code display

### QR Code Generator (Web Application)
**Main File**: qrcodewithphoto.html

#### Language & Runtime
**Language**: HTML, CSS, JavaScript
**Runtime**: Web Browser
**Framework**: Vanilla JavaScript

#### Dependencies
**External Libraries**:
- qrcode-generator (CDN: cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js)

#### Usage & Operations
```
Open qrcodewithphoto.html in any modern web browser
```

#### Main Features
- Generates QR codes with embedded public key data
- Allows photo upload via drag-and-drop or file browser
- Personalizes QR codes with visual elements from photos
- Supports multiple visual styles (center portrait, background blend, etc.)
- Maintains QR code scannability while adding visual personalization

### Kalman Levels (TradingView Indicator)
**Main Files**: kalmanlevels.txt, kalmanlevels_enhanced.txt

#### Language & Runtime
**Language**: Pine Script v5
**Platform**: TradingView

#### Main Features
- Multi-timeframe Kalman filter implementation
- Support for 10 different timeframes (3m to 3M)
- Trend detection and visualization
- Customizable filter parameters
- Enhanced version adds dynamic channels, alerts, and momentum indicators

#### Usage & Operations
```
Import script into TradingView Pine Editor
Add to chart as an overlay indicator
```

### LuxAlgo SR Levels (TradingView Indicator)
**Main File**: luxalsrlevels.txy

#### Language & Runtime
**Language**: Pine Script v5
**Platform**: TradingView

#### Main Features
- Multi-timeframe support and resistance level detection
- Enhanced trend detection with customizable parameters
- Level strength indicators and confluence zones
- Break detection with volume confirmation
- Comprehensive alert system

#### Usage & Operations
```
Import script into TradingView Pine Editor
Add to chart as an overlay indicator
```

### MLM Dashboard (TradingView Indicator)
**Main File**: mlmdashboard.txt

#### Language & Runtime
**Language**: Pine Script v4/v5
**Platform**: TradingView

#### Main Features
- Impulse MACD implementation based on LazyBear's work
- Smoothed moving average (SMMA) calculations
- Zero-lag exponential moving average (ZLEMA)
- Momentum visualization with color-coded histograms
- Optional bar coloring based on indicator values

#### Usage & Operations
```
Import script into TradingView Pine Editor
Add to chart as a separate indicator pane
```

### VS Code Configuration
**Configuration File**: .vscode/settings.json

#### Settings
- Enables repository indexing for Zencoder