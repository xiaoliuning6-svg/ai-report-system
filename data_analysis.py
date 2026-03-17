import pandas as pd

def analyze_data(filepath):
    """
    分析Excel数据并返回统计信息
    
    参数:
        filepath: Excel文件路径
    
    返回:
        dict: 包含统计信息的字典
    """
    # 读取Excel文件
    df = pd.read_excel(filepath)
    
    # 初始化统计信息字典
    stats = {
        'summary': {},
        'columns': [],
        'data_shape': df.shape
    }
    
    # 对每一列进行统计分析
    for column in df.columns:
        # 只对数值列进行统计
        if pd.api.types.is_numeric_dtype(df[column]):
            col_stats = {
                'name': column,
                'mean': df[column].mean(),
                'max': df[column].max(),
                'min': df[column].min(),
                'std': df[column].std(),
                'count': df[column].count(),
                'non_null_count': df[column].notnull().sum(),
                'null_count': df[column].isnull().sum()
            }
            stats['columns'].append(col_stats)
    
    # 整体数据摘要
    stats['summary']['total_rows'] = df.shape[0]
    stats['summary']['total_columns'] = df.shape[1]
    stats['summary']['numeric_columns'] = len(stats['columns'])
    
    return stats