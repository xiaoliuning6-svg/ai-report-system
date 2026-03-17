import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def generate_charts(filepath, chart_folder):
    """
    生成图表并保存到指定目录
    
    参数:
        filepath: Excel文件路径
        chart_folder: 图表保存目录
    
    返回:
        list: 图表文件路径列表
    """
    # 读取Excel文件
    df = pd.read_excel(filepath)
    
    # 生成唯一标识符，用于图表文件名
    unique_id = str(uuid.uuid4())[:8]
    
    chart_paths = []
    
    # 只处理数值列
    numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    
    if numeric_columns:
        # 生成柱状图
        bar_chart_path = os.path.join(chart_folder, f'bar_chart_{unique_id}.png')
        plt.figure(figsize=(10, 6))
        
        # 计算每列的平均值
        means = df[numeric_columns].mean()
        means.plot(kind='bar')
        
        plt.title('各列平均值对比')
        plt.xlabel('列名')
        plt.ylabel('平均值')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(bar_chart_path)
        plt.close()
        
        chart_paths.append(bar_chart_path)
        
        # 生成折线图（如果数据量合适）
        if len(df) <= 50:  # 数据量适中时生成折线图
            line_chart_path = os.path.join(chart_folder, f'line_chart_{unique_id}.png')
            plt.figure(figsize=(10, 6))
            
            for col in numeric_columns:
                plt.plot(df.index, df[col], label=col)
            
            plt.title('数据趋势')
            plt.xlabel('索引')
            plt.ylabel('值')
            plt.legend()
            plt.tight_layout()
            plt.savefig(line_chart_path)
            plt.close()
            
            chart_paths.append(line_chart_path)
    
    return chart_paths