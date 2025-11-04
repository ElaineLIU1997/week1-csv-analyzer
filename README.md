# Week 1 CSV Analyzer

A Python-based CSV data analyzer designed to process and analyze sales data from CSV files.
Tools: Claude, Claude Code, Cursor

## What It Does

This tool reads CSV files containing sales data and provides:

- **Dataset Overview**: Total records and column information
- **Sample Data Display**: Shows the first few rows of your data
- **Statistical Summary**: Basic statistics for numerical columns
- **Sales Analysis**:
  - Total sales amount
  - Average sale value
  - Highest and lowest sales
- **Product Analysis**: Sales breakdown by product category
- **Regional Analysis**: Sales breakdown by geographic region

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
- pandas library

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the analyzer with a CSV file:

```bash
python analyzer.py sales_data.csv
```

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

## Learning Objectives

This project demonstrates:
- Reading and processing CSV files with pandas
- Performing data analysis and aggregation
- Grouping and summarizing data
- Error handling in Python
- Command-line argument processing
- Data visualization in text format

## Next Steps

Potential enhancements:
- Add data visualization with matplotlib
- Export analysis results to PDF or Excel
- Support for multiple file formats
- Interactive mode for exploring data
- Time-series analysis for date-based trends
