# Portal Inmobiliario Rental Property Scraper

A powerful web scraper for extracting rental property data from [Portal Inmobiliario](https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana), Chile's leading real estate website.

## 🏠 Features

- **Multiple Scraper Implementations**: Selenium-based and requests-based scrapers
- **Comprehensive Data Extraction**: Price, location, bedrooms, bathrooms, square meters
- **Multiple Output Formats**: CSV and JSON exports
- **Robust Error Handling**: Logging and retry mechanisms
- **Respectful Scraping**: Configurable delays to avoid overwhelming servers
- **Environment Variable Support**: Secure configuration management
- **Security Best Practices**: API key protection and debug file exclusions

## 📋 Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium scraper)
- Internet connection

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ggoni/rent-scraper.git
cd rent-scraper
```

### 2. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env .env.local

# Edit .env.local with your specific settings
# This is where you should store any API keys or sensitive configuration
```

### 3. Create and Activate Virtual Environment

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Alternative: using Python's built-in venv
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 4. Install Dependencies

```bash
# Using uv (faster and more reliable)
uv pip install -r requirements.txt

# Alternative: using pip
pip install -r requirements.txt
```

### 5. Run the Scraper

```bash
# Selenium-based scraper (recommended)
python scraper.py

# Simple requests-based scraper
python simple_scraper.py

# Minimal scraper (no compilation required)
python simple_scraper_no_selenium.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file (not tracked by git) with your settings:

```bash
# Scraper settings
SCRAPER_DELAY=3
SCRAPER_MAX_PAGES=5
SCRAPER_HEADLESS=true

# API Keys (if needed)
MAP_API_KEY=your_google_maps_api_key_here
EXTERNAL_API_KEY=your_external_api_key_here
```

### Configuration File

Edit `config.py` to customize scraping behavior:

```python
# Base URL for different property types
BASE_URL = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"

# Scraping settings
MAX_PAGES = 3  # Maximum number of pages to scrape
DELAY_BETWEEN_PAGES = 2  # Seconds to wait between page requests

# Output settings
OUTPUT_FORMATS = ["csv", "json"]  # Available: "csv", "json"
OUTPUT_PREFIX = "rental_properties"
```

## 📊 Output

The scraper generates files with the following naming convention:
- `rental_properties_YYYYMMDD_HHMMSS.csv`
- `rental_properties_YYYYMMDD_HHMMSS.json`

### Data Fields Extracted

- **Price**: Rental price in CLP
- **Location**: Property address and neighborhood
- **Bedrooms**: Number of bedrooms
- **Bathrooms**: Number of bathrooms
- **Square Meters**: Property size
- **Raw Text**: Original listing text for debugging
- **Timestamp**: When the data was scraped

## 🛠️ Scraper Options

### Option 1: Selenium-based Scraper (Recommended)

```bash
python scraper.py
```

**Features:**
- Handles JavaScript-rendered content
- More accurate data extraction
- Better handling of dynamic elements
- Automatic browser management

### Option 2: Simple Requests-based Scraper

```bash
python simple_scraper.py
```

**Features:**
- Faster execution
- Lower resource usage
- No browser dependency
- Good for static content

### Option 3: Minimal Scraper (No Compilation Required)

```bash
# Install minimal dependencies
pip install -r requirements-minimal.txt

# Run the minimal scraper
python simple_scraper_no_selenium.py
```

**Features:**
- No compilation required
- Minimal dependencies
- Good for environments with limited resources

## 🔒 Security

### Environment Variables and Security

This project supports environment variables for configuration. Create a `.env.local` file (not tracked by git) with your specific settings:

```bash
# Copy the example file
cp .env .env.local

# Edit .env.local with your settings
```

### Security Best Practices

- **Never commit API keys or sensitive data to git**
- **Use `.env.local` for local development** (already in `.gitignore`)
- **The `.env` file is tracked and contains only example values**
- **Debug files are automatically ignored** to prevent exposing sensitive data
- **Always review scraped data** before committing to ensure no sensitive information is included

## 🐛 Troubleshooting

### Common Issues

#### Compilation Errors
If you encounter compilation errors with clang/gcc:

```bash
# Try the minimal installation instead
pip install -r requirements-minimal.txt

# Or install system dependencies first
# On macOS:
xcode-select --install

# On Ubuntu/Debian:
sudo apt-get install build-essential python3-dev

# On CentOS/RHEL:
sudo yum groupinstall "Development Tools"
```

#### Chrome Driver Issues
The Selenium scraper automatically downloads the appropriate ChromeDriver. If you encounter issues:

```bash
# Manually install ChromeDriver
pip install webdriver-manager
```

#### Memory Issues
For large scraping jobs, consider:
- Reducing `MAX_PAGES` in config.py
- Using the simple scraper instead of Selenium
- Running on a machine with more RAM

### Debug Mode

To run in debug mode (non-headless):

```python
# In config.py
HEADLESS_MODE = False
```

## 📈 Customization

### Adding New Data Fields

To extract additional information, modify the `extract_property_data` method:

```python
# Example: Extract property features
features_elem = property_element.find(string=lambda text: text and 'gimnasio' in text.lower())
if features_elem:
    property_data['features'] = features_elem.strip()
```

### Changing Search Parameters

To scrape different types of properties or locations:

```python
# For houses instead of apartments
self.base_url = "https://www.portalinmobiliario.com/arriendo/casa/santiago-metropolitana"

# For different cities
self.base_url = "https://www.portalinmobiliario.com/arriendo/departamento/valparaiso"
```

### Filtering Data

Configure filters in `config.py`:

```python
# Filter settings
MIN_BEDROOMS = 2  # Minimum number of bedrooms
MAX_PRICE_FILTER = 500000  # Maximum price in CLP
MIN_SQUARE_METERS = 50  # Minimum square meters
```

## 📦 Dependencies

### Core Dependencies
- **requests**: HTTP library for making requests
- **beautifulsoup4**: HTML parsing
- **selenium**: Browser automation
- **pandas**: Data manipulation and CSV export
- **fake-useragent**: Random User-Agent generation
- **webdriver-manager**: Automatic ChromeDriver management
- **python-dotenv**: Environment variable management

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes. Please ensure compliance with the target website's terms of service and applicable laws when using this scraper.

## ⚠️ Disclaimer

This scraper is for educational and research purposes only. Users are responsible for:
- **Compliance with website terms of service**
- **Respectful scraping practices** (reasonable delays, not overwhelming servers)
- **Data usage**: Use the scraped data responsibly and in accordance with applicable laws
- **Legal compliance**: Ensure your use case complies with local laws and regulations

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the configuration options in `config.py`
3. Open an issue on GitHub with detailed information about your problem


## ⚠️ Pending Features

- [ ] Add a way to filter by property filter borough/sector (apartment, house, etc.)


**Happy Scraping! 🏠📊** 