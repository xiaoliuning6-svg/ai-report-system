from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
pdfmetrics.registerFont(TTFont('SimHei', 'C:\\Windows\\Fonts\\simhei.ttf'))

def generate_pdf(report_text, chart_paths, output_path):
    """
    生成PDF报告
    
    参数:
        report_text: 分析报告文本
        chart_paths: 图表文件路径列表
        output_path: PDF输出路径
    """
    # 创建PDF文档，设置页边距
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    # 获取样式
    styles = getSampleStyleSheet()
    
    # 设置中文字体和样式
    for style_name in styles.byName:
        styles[style_name].fontName = 'SimHei'
    
    # 调整样式
    styles['Title'].fontSize = 24
    styles['Title'].alignment = 1  # 居中对齐
    styles['Title'].spaceAfter = 30
    
    styles['Heading1'].fontSize = 18
    styles['Heading1'].textColor = colors.HexColor('#4CAF50')
    styles['Heading1'].spaceAfter = 20
    
    styles['Heading2'].fontSize = 16
    styles['Heading2'].textColor = colors.HexColor('#333333')
    styles['Heading2'].spaceAfter = 15
    
    styles['Heading3'].fontSize = 14
    styles['Heading3'].textColor = colors.HexColor('#555555')
    styles['Heading3'].spaceAfter = 10
    
    styles['BodyText'].fontSize = 12
    styles['BodyText'].leading = 20  # 行间距
    styles['BodyText'].spaceAfter = 10
    
    # 构建PDF内容
    story = []
    
    # 标题
    title = Paragraph("数据分析报告", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # 报告内容
    report_lines = report_text.split('\n')
    for line in report_lines:
        if line.startswith('# '):
            # 一级标题
            para = Paragraph(line[2:], styles['Heading1'])
        elif line.startswith('## '):
            # 二级标题
            para = Paragraph(line[3:], styles['Heading2'])
        elif line.startswith('### '):
            # 三级标题
            para = Paragraph(line[4:], styles['Heading3'])
        elif line.startswith('- '):
            # 列表项
            para = Paragraph(f'• {line[2:]}', styles['BodyText'])
        else:
            # 普通文本
            para = Paragraph(line, styles['BodyText'])
        story.append(para)
    
    # 添加图表
    if chart_paths:
        story.append(Spacer(1, 20))
        story.append(Paragraph("## 数据可视化", styles['Heading2']))
        
        for chart_path in chart_paths:
            img = Image(chart_path, width=18*cm, height=10*cm)
            story.append(img)
            story.append(Spacer(1, 10))
    
    # 生成PDF
    doc.build(story)