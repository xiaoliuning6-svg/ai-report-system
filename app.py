from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from data_analysis import analyze_data
from chart_generator import generate_charts
from ai_report import generate_report
from pdf_generator import generate_pdf

app = Flask(__name__)

# 配置上传文件的路径
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
CHART_FOLDER = 'static/charts'

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER
app.config['CHART_FOLDER'] = CHART_FOLDER

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # 保存上传的文件
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 分析数据
        stats = analyze_data(filepath)
        
        # 生成图表
        chart_paths = generate_charts(filepath, CHART_FOLDER)
        
        # 生成分析报告
        report_text = generate_report(stats)
        
        # 生成PDF报告
        pdf_filename = f"{os.path.splitext(filename)[0]}_report.pdf"
        pdf_path = os.path.join(app.config['REPORT_FOLDER'], pdf_filename)
        generate_pdf(report_text, chart_paths, pdf_path)
        
        # 渲染报告页面
        return render_template('report.html', 
                           report=report_text, 
                           charts=chart_paths, 
                           pdf_url=url_for('download_pdf', filename=pdf_filename))
    
    return redirect(request.url)

@app.route('/download/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)