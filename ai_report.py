def generate_report(stats):
    """
    根据统计信息生成分析报告
    
    参数:
        stats: 包含统计信息的字典
    
    返回:
        str: 分析报告文本
    """
    # 构建报告
    report = []
    
    # 数据基本信息
    report.append("## 数据基本信息\n")
    report.append(f"- 总行数: {stats['summary']['total_rows']}\n")
    report.append(f"- 总列数: {stats['summary']['total_columns']}\n")
    report.append(f"- 数值列数: {stats['summary']['numeric_columns']}\n\n")
    
    # 各列统计信息
    if stats['columns']:
        report.append("## 各列统计信息\n")
        for col in stats['columns']:
            report.append(f"### {col['name']}\n")
            report.append(f"- 平均值: {col['mean']:.2f}\n")
            report.append(f"- 最大值: {col['max']:.2f}\n")
            report.append(f"- 最小值: {col['min']:.2f}\n")
            report.append(f"- 标准差: {col['std']:.2f}\n")
            report.append(f"- 非空值数量: {col['non_null_count']}\n")
            report.append(f"- 空值数量: {col['null_count']}\n\n")
    
    # 分析结论
    report.append("## 分析结论\n")
    if stats['columns']:
        # 找出平均值最高的列
        max_mean_col = max(stats['columns'], key=lambda x: x['mean'])
        report.append(f"- 平均值最高的列是: {max_mean_col['name']} (平均值: {max_mean_col['mean']:.2f})\n")
        
        # 找出标准差最大的列（波动最大）
        max_std_col = max(stats['columns'], key=lambda x: x['std'])
        report.append(f"- 数据波动最大的列是: {max_std_col['name']} (标准差: {max_std_col['std']:.2f})\n")
        
        # 检查是否有缺失值
        has_null = any(col['null_count'] > 0 for col in stats['columns'])
        if has_null:
            null_cols = [col['name'] for col in stats['columns'] if col['null_count'] > 0]
            report.append(f"- 存在缺失值的列: {', '.join(null_cols)}\n")
        else:
            report.append("- 所有列均无缺失值\n")
    else:
        report.append("- 未发现数值列，无法进行统计分析\n")
    
    return ''.join(report)