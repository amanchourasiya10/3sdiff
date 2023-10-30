from flask import Flask, request, json
from flask_cors import CORS, cross_origin
from harParser import parseHar
from txtParser import parseText
import os

app = Flask(__name__, static_url_path='', static_folder='build')

CORS(app, resources={r"/files": {"origins": "*"}})

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route("/files", methods=['POST'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def handleFiles():

    try:
        file1 = request.files['file1']
        filename1 = file1.filename
        _, extension1 = os.path.splitext(filename1)
        file1Content = file1.read().decode('utf-8-sig')
    except:
        file1Content = ''

    try:
        file2 = request.files['file2']
        filename2 = file2.filename
        _, extension2 = os.path.splitext(filename2)
        file2Content = file2.read().decode('utf-8-sig')
    except:
        file2Content = ''
    
    if (extension1 == '.txt'):
        parsedFile1 = parseText(file1Content)
    elif (extension1 == '.har'):
        parsedFile1 = parseHar(file1Content)
    
    if (extension2 == '.txt'):
        parsedFile2 = parseText(file2Content)
    elif (extension2 == '.har'):
        parsedFile2 = parseHar(file2Content)
    
    return json.dumps({'file1': parsedFile1, 'file2': parsedFile2})


if __name__ == "__main__":
    app.run(debug=True)
