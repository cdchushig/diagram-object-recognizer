from detector import Detector
import io
from flask import Flask, render_template, request, send_from_directory, send_file, abort
from PIL import Image
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

detector = Detector()


def load_image_url(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return img


def run_inference(img_path='file.jpg'):
    result_img = detector.inference(img_path)
    try:
        os.remove(img_path)
    except:
        pass
    return result_img


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=['POST', 'GET'])
def upload():

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    result_img = run_inference(os.path.join(app.config['UPLOAD_PATH'], filename))
    file_object = io.BytesIO()
    result_img.save(file_object, 'PNG')
    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
