from urllib.parse import parse_qs
from flask import Flask, request
from PIL import Image
import io
import base64
import cv2
import numpy as np
import fingerprint_feature_extractor
import json

def process_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    FeaturesTerm, FeaturesBif = fingerprint_feature_extractor.extract_minutiae_features(img_gray, spuriousMinutiaeThresh=10, invertImage = False, showResult=False, saveResult = False, crop_size=False)
    json_string = fingerprint_feature_extractor.features_to_json(FeaturesTerm, FeaturesBif)
    # Transforma o JSON string de volta em uma lista de dicionários
    features = json.loads(json_string)

    # todas as características em uma lista
    fingerprint_features = []
    for feature in features:
        if feature['Type'] == 'Termination': #Termination ou Bifurcation
            fingerprint_features.extend([feature['locX'], feature['locY'], feature['Orientation'][0]])

    # Se temos mais de 300 características, usamos apenas as primeiras 300, lembrando que recortamos as bordas da imagem
    if len(fingerprint_features) > 300:
        fingerprint_features = fingerprint_features[:300]
    # Se temos menos de 300 características, preenchemos a lista com zeros até ter 300
    else:
        fingerprint_features.extend([0] * (300 - len(fingerprint_features)))

    # Transforme a lista em uma array NumPy e a retorne
    return np.array(fingerprint_features)

app = Flask(__name__)

@app.route('/compare', methods=['POST'])
def compare():
    data = parse_qs(request.data.decode())
    img1_base64 = data['img1'][0]
    img2_base64 = data['img2'][0]
    
    img1_data = base64.b64decode(img1_base64)
    img1_np = np.frombuffer(img1_data, np.uint8)
    img1 = cv2.imdecode(img1_np, cv2.IMREAD_COLOR)

    img2_data = base64.b64decode(img2_base64)
    img2_np = np.frombuffer(img2_data, np.uint8)
    img2 = cv2.imdecode(img2_np, cv2.IMREAD_COLOR)

    feature1 = process_image(img1)
    feature2 = process_image(img2)
    
    distance = np.linalg.norm(feature1 - feature2)
    inverted_distance = (distance // -100) + 100

    return {'ssim': inverted_distance}

if __name__ == '__main__':
    app.run(port=8000, debug=True)
