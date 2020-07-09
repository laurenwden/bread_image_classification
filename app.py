import os
import base64
from google.cloud import automl, automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from capstone import app
from flask import Flask, render_template, request, redirect, url_for


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, "capstone/static/")



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Coulnd't create upload directory: {}".format(target))
    for upload in request.files.getlist('inputFile'):
        filename = upload.filename
        destination = "/".join([target, "temp.jpg"])
        print("Accept incoming file:", filename)
        upload.save(destination)

    prediction_client = automl.PredictionServiceClient()

    model_full_id = prediction_client.model_path(
        project_id, "us-central1", model_id
    )

    destination = "/".join([target, "temp.jpg"])
    # Read the file.
    with open(destination, "rb") as content_file:
        content = content_file.read()

    payload = {'image': {'image_bytes': content}}
    params = {"score_threshold": "0.8"}

    response = prediction_client.predict(model_full_id, payload, params)
    print("Prediction results:")
    for result in response.payload:
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(result.classification.score))
    return render_template("complete.html", response=response)


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        data = request.data
        image = data.split(';')[1]
        image_encoded = image.split(',')[1]
        body = base64.decodebytes(image_encoded.encode('utf-8'))

        prediction_client = automl.PredictionServiceClient()

        model_full_id = prediction_client.model_path(
            project_id, "us-central1", model_id
        )
        # Read the file.
        with open(body, "rb") as content_file:
            content = content_file.read()

        payload = {'image': {'image_bytes': content}}
        params = {"score_threshold": "0.8"}

        response = prediction_client.predict(model_full_id, payload, params)
        print("Prediction results:")
        for result in response.payload:
            print("Predicted class name: {}".format(result.display_name))
            print("Predicted class score: {}".format(result.classification.score))
        return render_template("complete.html", response=response)

if __name__ == '__main__':
    app.run(debug=True)


