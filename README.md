# CSV Analyzer

Data analysis tool with visualizations and multi-format export.

## What It Does

This enhanced tool provides powerful sales data analysis with:

### Core Analysis Features
- **Dataset Overview**: Total records and column information
- **Sample Data Display**: Shows the first few rows of your data
- **Statistical Summary**: Comprehensive statistics for all numerical columns
- **Sales Analysis**:
  - Total sales amount
  - Average sale value
  - Highest and lowest sales
  - Growth rate calculations
- **Product Analysis**: Detailed sales breakdown by product category
- **Regional Analysis**: Sales breakdown by geographic region

### NEW: Advanced Features
- **Data Visualizations**: 5 types of professional charts
  - Sales by Product (Bar Chart)
  - Sales by Region (Pie Chart)
  - Sales Trend Over Time (Line Chart)
  - Quantity Distribution (Box Plot)
  - Product vs Region Heatmap
- **Time-Series Analysis**: Trend analysis with daily/weekly aggregations
- **Sales Forecasting**: 7-day forecast using moving averages
- **Multiple File Formats**: Support for CSV, Excel (.xlsx, .xls), and JSON
- **Export Capabilities**:
  - PDF reports with visualizations
  - Excel workbooks with multiple analysis sheets

## Project Structure

```
week1-csv-analyzer/
├── analyzer.py          # Main analysis script
├── sales_data.csv      # Sample sales data
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Requirements

- Python 3.7 or higher
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- openpyxl >= 3.1.0

## Installation

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

### Basic Usage

Run the analyzer with any supported file format:

```bash
# Basic analysis (CSV, Excel, or JSON)
python3 analyzer.py sales_data.csv
python3 analyzer.py sales_data.xlsx
python3 analyzer.py sales_data.json
```

### Advanced Usage

Use command-line options to enable advanced features:

```bash
# Generate visualizations
python3 analyzer.py sales_data.csv --visualize

# Export to Excel
python3 analyzer.py sales_data.csv --export-excel

# Export to PDF
python3 analyzer.py sales_data.csv --export-pdf

# Perform sales forecasting
python3 analyzer.py sales_data.csv --forecast

# Enable ALL features at once
python3 analyzer.py sales_data.csv --all

# Custom output directory
python3 analyzer.py sales_data.csv --all --output-dir my_reports
```

### Command-Line Options

- `--visualize`: Generate PNG visualizations (saved to output directory)
- `--export-excel`: Export analysis to Excel workbook with multiple sheets
- `--export-pdf`: Export visualizations to PDF report
- `--forecast`: Perform 7-day sales forecasting
- `--all`: Enable all features (visualizations, exports, forecasting)
- `--output-dir DIR`: Specify custom output directory (default: `output/`)

### Expected CSV Format

The analyzer works best with CSV files containing the following columns:
- `Date`: Transaction date
- `Product`: Product name
- `Region`: Sales region
- `Amount`: Sale amount (required for sales analysis)
- `Quantity`: Number of items sold
- `Salesperson`: Name of the salesperson

The script will adapt to your CSV structure and provide relevant analysis based on available columns.

## Example Output

```
============================================================
CSV DATA ANALYZER - SALES REPORT
============================================================

Dataset Overview:
  Total Records: 25
  Columns: Date, Product, Region, Amount, Quantity, Salesperson

Sample Data (first 5 rows):
[Data table displayed here]

Statistical Summary:
[Statistical analysis displayed here]

Sales Analysis:
  Total Sales: $17,999.50
  Average Sale: $719.98
  Highest Sale: $1,299.99
  Lowest Sale: $29.99

Sales by Product:
[Product breakdown displayed here]

Sales by Region:
[Regional breakdown displayed here]
============================================================
Analysis Complete!
============================================================
```

## Sample Data

The included `sales_data.csv` file contains 25 sample sales records from January 2024, featuring:
- 4 products: Laptop, Mouse, Keyboard, Monitor
- 4 regions: North, South, East, West
- 4 salespeople
- Various quantities and amounts

## Output Files

When using advanced features, the analyzer creates an `output/` directory (or custom directory) containing:

- **Visualizations** (when `--visualize` is used):
  - `sales_by_product.png` - Bar chart of product sales
  - `sales_by_region.png` - Pie chart of regional distribution
  - `sales_trend.png` - Time series line chart
  - `quantity_distribution.png` - Box plot of quantities
  - `sales_heatmap.png` - Product vs Region heatmap

- **Excel Report** (when `--export-excel` is used):
  - `analysis_report.xlsx` with sheets:
    - Raw Data
    - Summary Statistics
    - Product Analysis
    - Region Analysis

- **PDF Report** (when `--export-pdf` is used):
  - `analysis_report.pdf` with visualization pages

## Learning Objectives

This project demonstrates:

### Core Skills
- Reading and processing multiple file formats (CSV, Excel, JSON)
- Performing comprehensive data analysis and aggregation
- Grouping and summarizing data with pandas
- Error handling and exception management
- Command-line argument processing with argparse

### Advanced Skills (Day 2 Enhancements)
- **Data Visualization**: Creating professional charts with matplotlib and seaborn
- **Time-Series Analysis**: Analyzing trends over time
- **Forecasting**: Simple predictive modeling with moving averages
- **Export Functionality**: Generating PDF and Excel reports
- **Code Organization**: Modular function design for complex features

## Version History

### Version 2.0 (Day 2 - Enhanced)
- Added 5 types of data visualizations
- Implemented time-series analysis with trend calculations
- Added sales forecasting using moving averages
- Added support for Excel and JSON input files
- Added PDF export functionality
- Added Excel export with multiple sheets
- Enhanced command-line interface with argparse
- Improved error handling and user feedback

### Version 1.0 (Day 1 - Basic)
- Basic CSV analysis
- Console output only
- Product and region analysis
- Statistical summaries

## Future Enhancements

Additional ideas for further development:
- Interactive dashboard with Streamlit or Dash
- Advanced forecasting models (ARIMA, Prophet)
- Database integration (PostgreSQL, SQLite)
- RESTful API for data access
- Real-time data streaming support
- Machine learning for anomaly detection
- Email report delivery
- Multi-currency support
- Automated report scheduling

---

## Built

**Date:** Nov 4-5, 2025 (Week 1, Days 1-2)
**Approach:** AI-generated (learning phase)
**Purpose:** Introduction to pandas, data visualization, and Python data analysis
**Status:** ✅ Complete
