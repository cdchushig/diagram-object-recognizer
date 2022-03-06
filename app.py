import os
import io
import numpy as np
from detector import Detector
from flask import Flask, render_template, request, send_file, abort
from PIL import Image
import requests
from werkzeug.utils import secure_filename
import base64


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', 'pdf']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_SHOW_IMG'] = True

detector = Detector()


def load_image_url(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return img


def run_inference(img_path='file.jpg'):
    result_img, dict_nodes = detector.inference(img_path)
    try:
        os.remove(img_path)
    except:
        pass
    return result_img, dict_nodes


def save_image_to_local(img_bytes, diagram_name):
    path_diagram = app.config['UPLOAD_PATH'] + '/' + diagram_name
    img_bytes.save(path_diagram)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/v1/detect", methods=['POST', 'GET'])
def detect():
    if not request.json or 'image' not in request.json:
        abort(400)

    # get the base64 encoded string
    im_b64 = request.json['image']
    diagram_name = request.json['diagram_name']

    # convert it into bytes
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    # PIL image object to numpy array
    img_arr = np.asarray(img)
    print('img shape', img_arr.shape)

    save_image_to_local(img, diagram_name)

    result_img, dict_nodes = run_inference(os.path.join(app.config['UPLOAD_PATH'], diagram_name))

    return dict_nodes


@app.route("/detect", methods=['POST', 'GET'])
def upload():

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    result_img, dict_nodes = run_inference(os.path.join(app.config['UPLOAD_PATH'], filename))

    if app.config['UPLOAD_SHOW_IMG']:
        file_object = io.BytesIO()
        result_img.save(file_object, 'PNG')
        file_object.seek(0)
        return send_file(file_object, mimetype='image/PNG')
    else:
        return dict_nodes


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
