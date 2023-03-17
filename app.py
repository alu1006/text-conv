from flask import Flask, render_template, request, send_file, send_from_directory
from opencc import OpenCC
import io

app = Flask(__name__)
cc = OpenCC('s2twp')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file uploaded", 400

    converted_content = cc.convert(file.read().decode('utf-8'))
    return send_file(
        io.BytesIO(converted_content.encode('utf-8')),
        as_attachment=True,
        download_name=f"{file.filename.split('.')[0]}_converted.srt",
        mimetype='text/plain'
    )
    # return send_from_directory('data', f"{file.filename.split('.')[0]}_converted.srt", as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)