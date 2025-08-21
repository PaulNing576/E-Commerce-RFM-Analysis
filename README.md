# E-Commerce RFM Customer Segmentation Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-1.3%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## Overview

A comprehensive RFM (Recency, Frequency, Monetary) analysis pipeline for e-commerce customer segmentation. This project demonstrates advanced data processing techniques using Python and Pandas to transform raw transaction data into actionable business intelligence.

## Business Value

- **Customer Segmentation**: Identify high-value customer cohorts using RFM methodology
- **Behavioral Analysis**: Uncover purchasing patterns and trends
- **Targeted Marketing**: Enable data-driven marketing strategy formulation  
- **Revenue Optimization**: Discover opportunities for revenue growth and retention

## Dataset

**Source**: [Kaggle Online Retail Dataset](https://www.kaggle.com/datasets/carrie1/ecommerce-data)  
**Content**: Transaction data from UK-based online retailer (2010-2011)  
**Records**: ~500,000 transactions  
**Features**: CustomerID, InvoiceDate, Quantity, UnitPrice, Country, etc.

## Technical Stack

### Core Technologies
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Data visualization
- **SciPy**: Statistical analysis

### Methodologies
- RFM Analysis (Recency, Frequency, Monetary)
- Customer Lifetime Value calculation
- Purchase behavior pattern recognition
- Time series analysis
- Memory optimization techniques

## Analytical Pipeline

### 1. Data Acquisition & Cleaning
- Missing value handling and anomaly detection
- Data type optimization (85% memory reduction)
- DateTime feature engineering
- Transaction validation

### 2. RFM Metric Calculation
- **Recency**: Days since last purchase
- **Frequency**: Total number of purchases  
- **Monetary**: Total revenue contribution

### 3. Customer Segmentation
- Automated cohort identification using RFM scores
- 9 distinct customer segments
- Business-friendly labeling strategy

### 4. Insight Generation
- Segment statistical profiling
- Value contribution analysis
- Behavioral pattern identification
- Strategic recommendations

## Quick Start

### Prerequisites
```bash
Python 3.8+
pip

# Installation

# Clone repository
git clone https://github.com/PaulNing576/E-Commerce-RFM-Analysis.git
cd E-Commerce-RFM-Analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Usage

# Run complete analysis pipeline
python src/main.py

# Or explore using Jupyter notebooks
jupyter notebook notebooks/01_data_exploration.ipynb
```

## Key Findings
- **Customer Segmentation Results**
- **Segment	Percentage	Characteristics**
- **Champions	5%	High-value loyal customers (40% revenue)**
- **Loyal Customers	12%	Consistent mid-value purchasers**
- **At Risk	18%	Customers showing decline patterns**
- **Lost Customers	25%	Inactive low-value customers**

## Strategic Insights
- **Champions drive 40% of revenue with 5% customer base**
- **At Risk segment requires immediate attention**
- **Loyal Customers show highest growth potential**
- **Significant opportunity in reactivation campaigns**

## Contributing
### We welcome contributions! Please follow these steps:
- **1. Fork the project**
- **2. Create your feature branch (git checkout -b feature/AmazingFeature)**
- **3. Commit your changes (git commit -m 'Add some AmazingFeature')**
- **4. Push to the branch (git push origin feature/AmazingFeature)**
- **5. Open a Pull Request**

## Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Code formatting
black src/
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
PaulNing576

## Acknowledgments
- Dataset provided by Kaggle
- RFM methodology inspiration from marketing analytics literature
- Python data science community for best practices

## Contact
For questions or collaborations, please open an issue or contact paulning576@gmail.com

## If you find this project useful, please give it a star on GitHub! Thanks!
