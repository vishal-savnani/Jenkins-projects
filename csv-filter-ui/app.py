from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Upload CSV
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            df = pd.read_csv(filepath)
            columns = df.columns.tolist()
            
            return render_template('columns.html', columns=columns, filename=file.filename)
    return render_template('upload.html')

# Filter columns and provide download link
@app.route('/filter', methods=['POST'])
def filter_columns():
    filename = request.form['filename']
    selected_columns = request.form.getlist('columns')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    df = pd.read_csv(filepath)
    filtered_df = df[selected_columns]
    
    filtered_filename = f"filtered_{filename}"
    filtered_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filtered_filename)
    filtered_df.to_csv(filtered_filepath, index=False)
    
    return render_template('download.html', filtered_file=filtered_filename)

# Serve uploaded/filtered files
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

