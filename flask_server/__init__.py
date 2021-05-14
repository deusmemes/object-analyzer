import cv2
import numpy as np
from flask import Flask, send_file, request, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.curdir, '..', 'data')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run():
    app.run(debug=True)


def stop():
    pass


def restart():
    pass


@app.route('/hello')
def hello():
    return 'hello'


@app.route('/test')
def test():
    return send_file(os.path.join(UPLOAD_FOLDER, 'img1.tif'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("files")
        print(files)
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                frame = cv2.imdecode(np.fromstring(file.stream.read(), np.uint8), cv2.IMREAD_COLOR)
                cv2.imwrite(f'{filename}', frame)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=files multiple>
      <input type=submit value=Upload>
    </form>
    '''
