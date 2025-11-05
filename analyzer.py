#!/usr/bin/env python3
"""
CSV Data Analyzer - Enhanced tool for analyzing sales data with visualizations,
forecasting, and multiple export formats
"""

import pandas as pd
import sys
import os
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_data(file_path):
    """
    Load data from various file formats (CSV, Excel, JSON).

    Args:
        file_path (str): Path to the data file

    Returns:
        pandas.DataFrame: Loaded data
    """
    file_ext = Path(file_path).suffix.lower()

    try:
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_ext == '.json':
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

        # Convert Date column if present
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)


def create_visualizations(df, output_dir='output'):
    """
    Create various visualizations for the sales data.

    Args:
        df (pandas.DataFrame): Sales data
        output_dir (str): Directory to save visualizations
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)

    print("\nGenerating visualizations...")

    # 1. Sales by Product (Bar Chart)
    if 'Product' in df.columns and 'Amount' in df.columns:
        plt.figure(figsize=(10, 6))
        product_sales = df.groupby('Product')['Amount'].sum().sort_values(ascending=False)
        sns.barplot(x=product_sales.index, y=product_sales.values, palette='viridis')
        plt.title('Total Sales by Product', fontsize=16, fontweight='bold')
        plt.xlabel('Product', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/sales_by_product.png', dpi=300)
        print(f"  ✓ Saved: {output_dir}/sales_by_product.png")
        plt.close()

    # 2. Sales by Region (Pie Chart)
    if 'Region' in df.columns and 'Amount' in df.columns:
        plt.figure(figsize=(8, 8))
        region_sales = df.groupby('Region')['Amount'].sum()
        colors = sns.color_palette('pastel')[0:len(region_sales)]
        plt.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%',
                startangle=90, colors=colors)
        plt.title('Sales Distribution by Region', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/sales_by_region.png', dpi=300)
        print(f"  ✓ Saved: {output_dir}/sales_by_region.png")
        plt.close()

    # 3. Time Series Analysis (if Date column exists)
    if 'Date' in df.columns and 'Amount' in df.columns:
        plt.figure(figsize=(12, 6))
        daily_sales = df.groupby('Date')['Amount'].sum().sort_index()
        plt.plot(daily_sales.index, daily_sales.values, marker='o', linewidth=2)
        plt.title('Sales Trend Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Sales ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/sales_trend.png', dpi=300)
        print(f"  ✓ Saved: {output_dir}/sales_trend.png")
        plt.close()

    # 4. Product Quantity Distribution (Box Plot)
    if 'Product' in df.columns and 'Quantity' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='Product', y='Quantity', palette='Set2')
        plt.title('Quantity Distribution by Product', fontsize=16, fontweight='bold')
        plt.xlabel('Product', fontsize=12)
        plt.ylabel('Quantity', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/quantity_distribution.png', dpi=300)
        print(f"  ✓ Saved: {output_dir}/quantity_distribution.png")
        plt.close()

    # 5. Sales Heatmap by Product and Region
    if all(col in df.columns for col in ['Product', 'Region', 'Amount']):
        plt.figure(figsize=(10, 6))
        heatmap_data = df.pivot_table(values='Amount', index='Product',
                                       columns='Region', aggfunc='sum', fill_value=0)
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5)
        plt.title('Sales Heatmap: Product vs Region', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/sales_heatmap.png', dpi=300)
        print(f"  ✓ Saved: {output_dir}/sales_heatmap.png")
        plt.close()


def time_series_analysis(df):
    """
    Perform time-series analysis on sales data.

    Args:
        df (pandas.DataFrame): Sales data with Date column
    """
    if 'Date' not in df.columns or 'Amount' not in df.columns:
        print("\nTime-series analysis requires 'Date' and 'Amount' columns.")
        return

    print("\n" + "=" * 60)
    print("TIME-SERIES ANALYSIS")
    print("=" * 60)

    # Daily sales
    daily_sales = df.groupby('Date')['Amount'].sum().sort_index()

    # Weekly aggregation
    weekly_sales = daily_sales.resample('W').sum()

    print(f"\nDaily Sales Statistics:")
    print(f"  Average Daily Sales: ${daily_sales.mean():,.2f}")
    print(f"  Highest Daily Sales: ${daily_sales.max():,.2f} on {daily_sales.idxmax().strftime('%Y-%m-%d')}")
    print(f"  Lowest Daily Sales: ${daily_sales.min():,.2f} on {daily_sales.idxmin().strftime('%Y-%m-%d')}")

    # Growth rate
    if len(daily_sales) > 1:
        growth_rate = ((daily_sales.iloc[-1] - daily_sales.iloc[0]) / daily_sales.iloc[0]) * 100
        print(f"  Overall Growth Rate: {growth_rate:+.2f}%")


def sales_forecasting(df, periods=7):
    """
    Simple sales forecasting using moving average.

    Args:
        df (pandas.DataFrame): Sales data with Date column
        periods (int): Number of periods to forecast
    """
    if 'Date' not in df.columns or 'Amount' not in df.columns:
        print("\nForecasting requires 'Date' and 'Amount' columns.")
        return

    print("\n" + "=" * 60)
    print("SALES FORECASTING")
    print("=" * 60)

    # Daily sales
    daily_sales = df.groupby('Date')['Amount'].sum().sort_index()

    # Calculate moving average
    ma_window = min(7, len(daily_sales) // 2)
    moving_avg = daily_sales.rolling(window=ma_window).mean().iloc[-1]

    print(f"\n{ma_window}-Day Moving Average: ${moving_avg:,.2f}")
    print(f"\nForecast for next {periods} days (based on moving average):")

    last_date = daily_sales.index[-1]
    for i in range(1, periods + 1):
        forecast_date = last_date + pd.Timedelta(days=i)
        print(f"  {forecast_date.strftime('%Y-%m-%d')}: ${moving_avg:,.2f} (estimated)")


def export_to_excel(df, analysis_results, output_file='output/analysis_report.xlsx'):
    """
    Export analysis results to Excel.

    Args:
        df (pandas.DataFrame): Original data
        analysis_results (dict): Dictionary containing analysis results
        output_file (str): Output Excel file path
    """
    Path(output_file).parent.mkdir(exist_ok=True)

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Raw data
        df.to_excel(writer, sheet_name='Raw Data', index=False)

        # Summary statistics
        if 'Amount' in df.columns:
            summary = df.describe()
            summary.to_excel(writer, sheet_name='Summary Statistics')

        # Product analysis
        if 'Product' in df.columns and 'Amount' in df.columns:
            product_sales = df.groupby('Product')['Amount'].agg(['sum', 'count', 'mean'])
            product_sales.columns = ['Total Sales', 'Number of Sales', 'Average Sale']
            product_sales.to_excel(writer, sheet_name='Product Analysis')

        # Region analysis
        if 'Region' in df.columns and 'Amount' in df.columns:
            region_sales = df.groupby('Region')['Amount'].agg(['sum', 'count', 'mean'])
            region_sales.columns = ['Total Sales', 'Number of Sales', 'Average Sale']
            region_sales.to_excel(writer, sheet_name='Region Analysis')

    print(f"\n✓ Excel report saved: {output_file}")


def export_to_pdf(df, output_file='output/analysis_report.pdf'):
    """
    Export analysis results to PDF.

    Args:
        df (pandas.DataFrame): Sales data
        output_file (str): Output PDF file path
    """
    try:
        from matplotlib.backends.backend_pdf import PdfPages

        Path(output_file).parent.mkdir(exist_ok=True)

        with PdfPages(output_file) as pdf:
            # Page 1: Sales by Product
            if 'Product' in df.columns and 'Amount' in df.columns:
                fig, ax = plt.subplots(figsize=(11, 8))
                product_sales = df.groupby('Product')['Amount'].sum().sort_values(ascending=False)
                product_sales.plot(kind='bar', ax=ax, color=sns.color_palette('viridis', len(product_sales)))
                ax.set_title('Total Sales by Product', fontsize=18, fontweight='bold', pad=20)
                ax.set_xlabel('Product', fontsize=14)
                ax.set_ylabel('Total Sales ($)', fontsize=14)
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig()
                plt.close()

            # Page 2: Sales by Region
            if 'Region' in df.columns and 'Amount' in df.columns:
                fig, ax = plt.subplots(figsize=(11, 8))
                region_sales = df.groupby('Region')['Amount'].sum()
                ax.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%',
                       startangle=90, colors=sns.color_palette('pastel'))
                ax.set_title('Sales Distribution by Region', fontsize=18, fontweight='bold', pad=20)
                plt.tight_layout()
                pdf.savefig()
                plt.close()

            # Page 3: Time Series
            if 'Date' in df.columns and 'Amount' in df.columns:
                fig, ax = plt.subplots(figsize=(11, 8))
                daily_sales = df.groupby('Date')['Amount'].sum().sort_index()
                ax.plot(daily_sales.index, daily_sales.values, marker='o', linewidth=2)
                ax.set_title('Sales Trend Over Time', fontsize=18, fontweight='bold', pad=20)
                ax.set_xlabel('Date', fontsize=14)
                ax.set_ylabel('Sales ($)', fontsize=14)
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                pdf.savefig()
                plt.close()

        print(f"✓ PDF report saved: {output_file}")

    except ImportError:
        print("✗ PDF export requires matplotlib. Skipping PDF generation.")


def analyze_sales_data(file_path, visualize=True, export_excel=False, export_pdf=False,
                       forecast=False, output_dir='output'):
    """
    Comprehensive analysis of sales data with enhanced features.

    Args:
        file_path (str): Path to the data file
        visualize (bool): Generate visualizations
        export_excel (bool): Export to Excel
        export_pdf (bool): Export to PDF
        forecast (bool): Perform sales forecasting
        output_dir (str): Output directory for exports
    """
    try:
        # Load data
        print("Loading data...")
        df = load_data(file_path)
        print(f"✓ Loaded {len(df)} records from {file_path}")

        print("\n" + "=" * 60)
        print("CSV DATA ANALYZER - ENHANCED SALES REPORT")
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
        if 'Product' in df.columns and 'Amount' in df.columns:
            print("Sales by Product:")
            product_sales = df.groupby('Product')['Amount'].agg(['sum', 'count', 'mean'])
            product_sales.columns = ['Total Sales', 'Number of Sales', 'Average Sale']
            product_sales = product_sales.sort_values('Total Sales', ascending=False)
            print(product_sales)
            print()

        # Analysis by region if available
        if 'Region' in df.columns and 'Amount' in df.columns:
            print("Sales by Region:")
            region_sales = df.groupby('Region')['Amount'].agg(['sum', 'count'])
            region_sales.columns = ['Total Sales', 'Number of Sales']
            region_sales = region_sales.sort_values('Total Sales', ascending=False)
            print(region_sales)
            print()

        # Time-series analysis
        if 'Date' in df.columns:
            time_series_analysis(df)

        # Forecasting
        if forecast and 'Date' in df.columns:
            sales_forecasting(df)

        # Generate visualizations
        if visualize:
            create_visualizations(df, output_dir)

        # Export to Excel
        if export_excel:
            analysis_results = {}
            export_to_excel(df, analysis_results, f'{output_dir}/analysis_report.xlsx')

        # Export to PDF
        if export_pdf:
            export_to_pdf(df, f'{output_dir}/analysis_report.pdf')

        print("\n" + "=" * 60)
        print("Analysis Complete!")
        print("=" * 60)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: File '{file_path}' is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main function with enhanced command-line interface."""
    parser = argparse.ArgumentParser(
        description='Enhanced CSV Data Analyzer with visualizations, forecasting, and exports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sales_data.csv
  %(prog)s sales_data.xlsx --visualize --export-excel
  %(prog)s sales_data.json --forecast --export-pdf
  %(prog)s data.csv --all
        """
    )

    parser.add_argument('file', help='Input file (CSV, Excel, or JSON)')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualizations')
    parser.add_argument('--export-excel', action='store_true',
                       help='Export analysis to Excel')
    parser.add_argument('--export-pdf', action='store_true',
                       help='Export analysis to PDF')
    parser.add_argument('--forecast', action='store_true',
                       help='Perform sales forecasting')
    parser.add_argument('--all', action='store_true',
                       help='Enable all features (visualize, export, forecast)')
    parser.add_argument('--output-dir', default='output',
                       help='Output directory for exports (default: output)')

    args = parser.parse_args()

    # Enable all features if --all flag is used
    if args.all:
        args.visualize = True
        args.export_excel = True
        args.export_pdf = True
        args.forecast = True

    analyze_sales_data(
        args.file,
        visualize=args.visualize,
        export_excel=args.export_excel,
        export_pdf=args.export_pdf,
        forecast=args.forecast,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
