# Villa Los Jardines Property Scraper

A specialized web scraper for extracting property listings from Portal Inmobiliario's Villa Los Jardines - Villa Los Presidentes neighborhood in Ñuñoa, Santiago, Chile.

## Target URL
```
https://www.portalinmobiliario.com/venta/casa/rm-metropolitana/nunoa/villa-los-jardines---villa-los-presidentes
```

## Features

- **Specialized for Villa Los Jardines**: Optimized patterns and selectors for this specific neighborhood
- **Multi-page scraping**: Automatically scrapes all available pages
- **Comprehensive data extraction**: 
  - Property titles
  - Prices (CLP and UF)
  - Bedrooms and bathrooms
  - Square meters
  - Address/location
  - Property features (garden, parking, pool, etc.)
- **Data validation**: Filters out invalid or incomplete listings
- **Multiple output formats**: CSV and JSON
- **Detailed logging**: Comprehensive logging for debugging
- **Rate limiting**: Respectful scraping with delays between requests
- **Error handling**: Robust error handling and retry mechanisms

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_villa_jardines.txt
```

2. Or install manually:
```bash
pip install requests beautifulsoup4 lxml
```

## Usage

### Basic Usage

Run the scraper:
```bash
python villa_jardines_scraper.py
```

### Test the Scraper

Before running the full scraper, test it:
```bash
python test_villa_jardines_scraper.py
```

### Programmatic Usage

```python
from villa_jardines_scraper import VillaJardinesScraper

# Create scraper instance
scraper = VillaJardinesScraper()

# Run the scraper
scraper.run()

# Access the scraped data
properties = scraper.properties

# Print summary
scraper.print_summary()
```

## Output

The scraper generates two types of output files:

### JSON Output
```json
{
  "title": "Casa 3d Cerca Mall Portal Ñuñoa Y Futuro Metro",
  "price": 168000000,
  "price_currency": "CLP",
  "location": "Ñuñoa, Región Metropolitana, Chile",
  "bedrooms": 3,
  "bathrooms": 1,
  "square_meters": 65,
  "address": "Pje. Veintiocho 1200 - 1500, Ñuñoa",
  "features": ["jardín", "estacionamiento"],
  "raw_text": "...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### CSV Output
The same data in CSV format for easy analysis in Excel or other tools.

## Configuration

You can modify the scraper behavior by editing the `VillaJardinesScraper` class:

- `max_pages`: Maximum number of pages to scrape (default: 10)
- `delay_between_pages`: Seconds to wait between pages (default: 3)
- `delay_between_requests`: Seconds to wait between requests (default: 2)
- `timeout`: Request timeout in seconds (default: 30)
- `max_retries`: Number of retry attempts (default: 3)

## Data Validation

The scraper includes validation rules specific to the Villa Los Jardines market:

- **Price ranges**: 
  - CLP: 50,000,000 - 500,000,000
  - UF: 1,000 - 20,000
- **Square meters**: 30 - 500 m²
- **Minimum data**: Must have either price or title

## Logging

The scraper creates a log file `villa_jardines_scraper.log` with detailed information about:
- Request attempts and failures
- Number of properties found per page
- Data extraction success/failure
- Export operations

## Error Handling

The scraper includes robust error handling:
- Automatic retries for failed requests
- Graceful handling of missing data
- Validation of extracted data
- Detailed error logging

## Legal and Ethical Considerations

- **Respectful scraping**: Includes delays between requests to avoid overwhelming the server
- **Terms of Service**: Ensure compliance with Portal Inmobiliario's terms of service
- **Data usage**: Use scraped data responsibly and in accordance with applicable laws
- **Rate limiting**: The scraper includes built-in rate limiting to be respectful to the website

## Troubleshooting

### Common Issues

1. **No properties found**: 
   - Check if the website structure has changed
   - Verify the URL is still accessible
   - Check the log file for detailed error messages

2. **Import errors**:
   - Ensure all dependencies are installed: `pip install -r requirements_villa_jardines.txt`

3. **Network errors**:
   - Check your internet connection
   - The scraper will retry automatically, but you may need to increase `max_retries`

### Debug Mode

To enable debug logging, modify the logging level in the scraper:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Example Output Summary

```
=== VILLA LOS JARDINES SCRAPING SUMMARY ===
Total properties found: 19
Price range: $50,000,000 - $239,800,000 CLP
Average price: $189,500,000 CLP
Bedroom range: 2 - 5
Average bedrooms: 3.4
Size range: 50 - 226 m²
Average size: 95.2 m²
==================================================
```

## Files

- `villa_jardines_scraper.py`: Main scraper script
- `test_villa_jardines_scraper.py`: Test script
- `requirements_villa_jardines.txt`: Dependencies
- `README_villa_jardines.md`: This documentation
- `villa_jardines_scraper.log`: Log file (created when running)
- `villa_jardines_properties_YYYYMMDD_HHMMSS.json`: JSON output
- `villa_jardines_properties_YYYYMMDD_HHMMSS.csv`: CSV output 