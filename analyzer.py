#!/usr/bin/env python3
"""
CSV Data Analyzer - A simple tool for analyzing sales data from CSV files
"""

import pandas as pd
import sys


def analyze_sales_data(csv_file):
    """
    Analyze sales data from a CSV file and display key statistics.

    Args:
        csv_file (str): Path to the CSV file containing sales data
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        print("=" * 60)
        print("CSV DATA ANALYZER - SALES REPORT")
        print("=" * 60)
        print()

        # Display basic information
        print("Dataset Overview:")
        print(f"  Total Records: {len(df)}")
        print(f"  Columns: {', '.join(df.columns)}")
        print()

        # Display first few rows
        print("Sample Data (first 5 rows):")
        print(df.head())
        print()

        # Statistical analysis
        print("Statistical Summary:")
        print(df.describe())
        print()

        # Sales-specific analysis
        if 'Amount' in df.columns:
            print("Sales Analysis:")
            print(f"  Total Sales: ${df['Amount'].sum():,.2f}")
            print(f"  Average Sale: ${df['Amount'].mean():,.2f}")
            print(f"  Highest Sale: ${df['Amount'].max():,.2f}")
            print(f"  Lowest Sale: ${df['Amount'].min():,.2f}")
            print()

        # Analysis by category if available
        if 'Product' in df.columns:
            print("Sales by Product:")
            product_sales = df.groupby('Product')['Amount'].agg(['sum', 'count', 'mean'])
            product_sales.columns = ['Total Sales', 'Number of Sales', 'Average Sale']
            product_sales = product_sales.sort_values('Total Sales', ascending=False)
            print(product_sales)
            print()

        # Analysis by region if available
        if 'Region' in df.columns:
            print("Sales by Region:")
            region_sales = df.groupby('Region')['Amount'].agg(['sum', 'count'])
            region_sales.columns = ['Total Sales', 'Number of Sales']
            region_sales = region_sales.sort_values('Total Sales', ascending=False)
            print(region_sales)
            print()

        print("=" * 60)
        print("Analysis Complete!")
        print("=" * 60)

    # Handle the case where the specified CSV file is not found
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    # Handle the case where the CSV file is present but empty
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file}' is empty.")
        sys.exit(1)
    # Handle any other exceptions that may occur during analysis
    except Exception as e:
        print(f"Error analyzing file: {e}")
        sys.exit(1)


def main():
    """Main function to run the analyzer."""
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <csv_file>")
        print("Example: python analyzer.py sales_data.csv")
        sys.exit(1)

    csv_file = sys.argv[1]
    analyze_sales_data(csv_file)


if __name__ == "__main__":
    main()
