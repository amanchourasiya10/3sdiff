from flask import Flask, request, json
from flask_cors import CORS, cross_origin
from harParser import parseHar
from sazParser import parseSaz, update_dict
from txtParser import parseText
import os
import zipfile

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
    except:
        extension1 = None

    try:
        file2 = request.files['file2']
        filename2 = file2.filename
        _, extension2 = os.path.splitext(filename2)
    except:
        extension2 = None
    try:
        if (extension1 == '.txt'):
            file1Content = file1.read().decode('utf-8-sig')
            parsedFile1 = parseText(file1Content)
        elif (extension1 == '.har'):
            file1Content = file1.read().decode('utf-8-sig')
            parsedFile1 = parseHar(file1Content)
        elif (extension1 == '.saz'):
            with zipfile.ZipFile(file1, 'r') as saz_zip:
                c_txt_content = saz_zip.read('raw/1_c.txt').decode('utf-8-sig')
                s_txt_content = saz_zip.read('raw/1_s.txt').decode('utf-8-sig')
                
                parsedFile1 = {**parseSaz(c_txt_content), **parseSaz(s_txt_content)}
                parsedFile1 = update_dict(parsedFile1)
        else:
            parsedFile1 = {"queryHeader": '{}', "query": '{}', "responseHeader": '{}', "response": '{}'}
    except:
        parsedFile1 = {"queryHeader": '{}', "query": '{}', "responseHeader": '{}', "response": '{}'}

    try:
        if (extension2 == '.txt'):
            file2Content = file2.read().decode('utf-8-sig')
            parsedFile2 = parseText(file2Content)
        elif (extension2 == '.har'):
            file2Content = file2.read().decode('utf-8-sig')
            parsedFile2 = parseHar(file2Content)
        elif (extension2 == '.saz'):
            with zipfile.ZipFile(file2, 'r') as saz_zip:
                c_txt_content = saz_zip.read('raw/1_c.txt').decode('utf-8-sig')
                s_txt_content = saz_zip.read('raw/1_s.txt').decode('utf-8-sig')
                
                parsedFile2 = {**parseSaz(c_txt_content), **parseSaz(s_txt_content)}
                parsedFile2 = update_dict(parsedFile2)
        else:
            parsedFile2 = {"queryHeader": '{}', "query": '{}', "responseHeader": '{}', "response": '{}'}
    except:
        parsedFile2 = {"queryHeader": '{}', "query": '{}', "responseHeader": '{}', "response": '{}'}

    return json.dumps({'file1': parsedFile1, 'file2': parsedFile2})


if __name__ == "__main__":
    app.run(debug=True)
