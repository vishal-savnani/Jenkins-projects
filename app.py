from flask import Flask, request, redirect, url_for, render_template_string
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_FORM = """
<!doctype html>
<title>Upload CSV</title>
<h2>Upload a CSV file</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file accept=".csv">
  <input type=submit value=Upload>
</form>
{% if filename %}
<p>✅ File uploaded:{{ filename }}</a></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    filename = None
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".csv"):
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(save_path)  # Save to uploads folder
            filename = file.filename
    return render_template_string(HTML_FORM, filename=filename)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return app.send_static_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
