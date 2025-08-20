"""
E-Commerce RFM Analysis Main Script
"""
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(file_path: str) -> pd.DataFrame:
    """加载数据并处理编码问题"""
    logger.info("开始加载数据...")
    
    encodings = ['ISO-8859-1', 'latin1', 'windows-1252', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            logger.info(f"成功使用编码: {encoding}")
            return df
        except UnicodeDecodeError:
            continue
    
    raise ValueError("无法使用任何支持的编码加载数据")

def main():
    """主函数"""
    try:
        logger.info("=== 开始电子商务RFM分析 ===")
        
        # 加载数据
        df = load_data('data/raw/sample_data.csv')
        logger.info(f"数据加载成功，形状: {df.shape}")
        
        print("✅ 数据分析管道设置完成！")
        print("📊 下一步可以添加数据清洗和RFM分析功能")
        
    except Exception as e:
        logger.error(f"分析失败: {e}")
        raise

if __name__ == "__main__":
    main()
