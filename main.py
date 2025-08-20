"""
E-Commerce Customer Behavior Analysis Pipeline
Author: Paul Ning
Date: 08/20/2025
Description: RFM Analysis of Online Retail Data for Customer Segmentation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Tuple, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ECommerceAnalyzer:
    """E-commerce data analysis and RFM segmentation pipeline"""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df_raw = None
        self.df_clean = None
        self.df_optimized = None
        self.rfm_results = None
        
    def load_data(self) -> pd.DataFrame:
        """Load data with automatic encoding detection"""
        encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'windows-1252', 'cp1252']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(self.data_path, encoding=encoding)
                logger.info(f"Successfully loaded data with {encoding} encoding")
                return df
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.warning(f"Error with {encoding}: {e}")
                continue
        
        raise ValueError("Failed to load data with any supported encoding")
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess e-commerce data"""
        logger.info("Starting data cleaning process")
        
        df_clean = df.copy()
        
        initial_shape = df_clean.shape
        df_clean = df_clean.dropna(subset=['CustomerID'])
        logger.info(f"Removed {initial_shape[0] - df_clean.shape[0]} rows with missing CustomerID")
        
        df_clean = df_clean[df_clean['Quantity'] > 0]
        df_clean = df_clean[df_clean['UnitPrice'] > 0]
        logger.info(f"Removed invalid transactions, current shape: {df_clean.shape}")
        
        df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
        df_clean['InvoiceYearMonth'] = df_clean['InvoiceDate'].dt.to_period('M')
        df_clean['InvoiceHour'] = df_clean['InvoiceDate'].dt.hour.astype('int8')
        df_clean['InvoiceDayOfWeek'] = df_clean['InvoiceDate'].dt.day_name().astype('category')
        df_clean['InvoiceWeek'] = df_clean['InvoiceDate'].dt.isocalendar().week.astype('int8')
        
        df_clean['TotalSales'] = (df_clean['Quantity'] * df_clean['UnitPrice']).astype('float32')
        df_clean['LineItemProfit'] = (df_clean['TotalSales'] * 0.3).astype('float32')  # Assuming 30% margin
        
        logger.info("Data cleaning completed successfully")
        return df_clean
    
    def optimize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Optimizing data types for memory efficiency")
        
        df_opt = df.copy()
        initial_memory = df_opt.memory_usage(deep=True).sum() / 1024**2  # MB
        
        optimization_rules = {
            'CustomerID': 'category',
            'StockCode': 'category',
            'Country': 'category',
            'Description': 'category',
            'InvoiceNo': 'category',
            'Quantity': 'int16',
            'UnitPrice': 'float32'
        }
        
        for col, dtype in optimization_rules.items():
            if col in df_opt.columns:
                try:
                    df_opt[col] = df_opt[col].astype(dtype)
                except Exception as e:
                    logger.warning(f"Could not convert {col} to {dtype}: {e}")
        
        for col in df_opt.columns:
            if df_opt[col].dtype == 'object' and df_opt[col].nunique() / len(df_opt[col]) < 0.3:
                df_opt[col] = df_opt[col].astype('category')
        
        final_memory = df_opt.memory_usage(deep=True).sum() / 1024**2
        memory_reduction = (initial_memory - final_memory) / initial_memory * 100
        
        logger.info(f"Memory optimization: {initial_memory:.2f}MB → {final_memory:.2f}MB "
                   f"({memory_reduction:.1f}% reduction)")
        
        return df_opt
    
    def calculate_rfm_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Calculating RFM metrics")
        
        analysis_date = df['InvoiceDate'].max() + timedelta(days=1)
        
        rfm = df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (analysis_date - x.max()).days,
            'InvoiceNo': 'nunique',
            'TotalSales': 'sum'
        }).rename(columns={
            'InvoiceDate': 'Recency',
            'InvoiceNo': 'Frequency',
            'TotalSales': 'Monetary'
        })
        
        rfm['RecencyPercentile'] = rfm['Recency'].rank(pct=True)
        rfm['FrequencyPercentile'] = rfm['Frequency'].rank(pct=True)
        rfm['MonetaryPercentile'] = rfm['Monetary'].rank(pct=True)
        
        return rfm
    
    def segment_customers(self, rfm: pd.DataFrame) -> pd.DataFrame:
        logger.info("Segmenting customers using RFM analysis")
        
        def calculate_score(percentile_series: pd.Series, reverse: bool = False) -> pd.Series:
            if reverse:
                return (5 - (percentile_series * 5).astype(int)).clip(1, 5)
            return ((percentile_series * 5).astype(int) + 1).clip(1, 5)
        
        rfm_segmented = rfm.copy()
        rfm_segmented['R_Score'] = calculate_score(rfm_segmented['RecencyPercentile'], reverse=True)
        rfm_segmented['F_Score'] = calculate_score(rfm_segmented['FrequencyPercentile'])
        rfm_segmented['M_Score'] = calculate_score(rfm_segmented['MonetaryPercentile'])
        
        rfm_segmented['RFM_Score'] = (
            rfm_segmented['R_Score'].astype(str) + 
            rfm_segmented['F_Score'].astype(str) + 
            rfm_segmented['M_Score'].astype(str)
        )
        
        segment_definitions = {
            '555|554|545|455': 'Champions',
            '543|444|435|355|354|345|344|335': 'Loyal Customers',
            '553|551|552|541|542|533|532|531|452|451|442|441|431|453|433|432|423|353|352|351|342|341|333|323': 'Potential Loyalists',
            '512|511|422|421|412|411|311': 'New Customers',
            '525|524|523|522|521|515|514|513|425|424|413|414|415|315|314|313': 'Promising',
            '331|321|312|221|213': 'Customers Needing Attention',
            '255|254|245|244|235|234|225|224|153|152|145|143|142|134|133|124|123|155': 'At Risk',
            '332|322|231|241|251|215|114|113': 'About to Sleep',
            '135|131|125|115': 'Cannot Lose Them',
            '111|112|211': 'Lost Customers'
        }
        
        rfm_segmented['Segment'] = 'Other'
        for patterns, segment_name in segment_definitions.items():
            pattern_list = patterns.split('|')
            for pattern in pattern_list:
                mask = rfm_segmented['RFM_Score'] == pattern
                rfm_segmented.loc[mask, 'Segment'] = segment_name
        
        return rfm_segmented
    
    def generate_insights(self, rfm: pd.DataFrame) -> Dict[str, Any]:
        logger.info("Generating business insights")
        
        insights = {
            'total_customers': len(rfm),
            'segment_distribution': rfm['Segment'].value_counts().to_dict(),
            'avg_monetary_by_segment': rfm.groupby('Segment')['Monetary'].mean().sort_values(ascending=False).to_dict(),
            'top_segments_by_value': rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False).head(5).to_dict()
        }
        
        return insights
    
    def run_analysis(self):
        logger.info("Starting E-commerce analysis pipeline")
        
        try:
            self.df_raw = self.load_data()
            self.df_clean = self.clean_data(self.df_raw)
            self.df_optimized = self.optimize_data_types(self.df_clean)
            
            rfm_metrics = self.calculate_rfm_metrics(self.df_optimized)
            self.rfm_results = self.segment_customers(rfm_metrics)
            
            insights = self.generate_insights(self.rfm_results)
            
            logger.info("Analysis pipeline completed successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise

# Example usage
if __name__ == "__main__":
    analyzer = ECommerceAnalyzer('data/ecommerce-data.csv')
    
    try:
        insights = analyzer.run_analysis()
        
        print("\n" + "="*50)
        print("E-COMMERCE RFM ANALYSIS RESULTS")
        print("="*50)
        
        print(f"\nTotal Customers Analyzed: {insights['total_customers']:,}")
        
        print("\nCustomer Segment Distribution:")
        for segment, count in insights['segment_distribution'].items():
            percentage = (count / insights['total_customers']) * 100
            print(f"  {segment}: {count:,} ({percentage:.1f}%)")
        
        print("\nAverage Monetary Value by Segment:")
        for segment, value in insights['avg_monetary_by_segment'].items():
            print(f"  {segment}: ${value:,.2f}")
            
        analyzer.rfm_results.to_csv('results/rfm_analysis_detailed.csv', index=True)
        analyzer.df_optimized.to_parquet('data/processed_data.parquet', index=False)
        
        print("\nResults saved to 'results/rfm_analysis_detailed.csv'")
        print("Processed data saved to 'data/processed_data.parquet'")
        
    except Exception as e:
        print(f"Analysis failed: {e}")
