import cv2
import fingerprint_feature_extractor
import numpy as np
import json


# if __name__ == '__main__':
#     img = cv2.imread('enhanced/img_2.png', 0)				# read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library
#     #FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage = False, showResult=True, saveResult = True)
#     FeaturesTerm, FeaturesBif = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage = False, showResult=True, saveResult = True)
#     json_string = fingerprint_feature_extractor.features_to_json(FeaturesTerm, FeaturesBif)
#     print(json_string)
if __name__ == '__main__':
    
    def process_image(path):
        img = cv2.imread(path, 0)				
        FeaturesTerm, FeaturesBif = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage = False, showResult=False, saveResult = True, crop_size=(350, 410))
        json_string = fingerprint_feature_extractor.features_to_json(FeaturesTerm, FeaturesBif)
        
        # Transforma o JSON string de volta em uma lista de dicionários
        features = json.loads(json_string)
        # todas as características em uma lista
        fingerprint_features = []
        for feature in features:
            if feature['Type'] == 'Termination': #Termination ou Bifurcation
                #fingerprint_features.extend([feature['locX'], feature['locY'], feature['Orientation'][0],feature['Orientation'][1]])
                fingerprint_features.extend([feature['locX'], feature['locY'], feature['Orientation'][0]])

        # Se temos mais de 300 características, usamos apenas as primeiras 300, lembrando que recortamos as bordas da imagem
        if len(fingerprint_features) > 300:
            fingerprint_features = fingerprint_features[:300]
        # Se temos menos de 300 características, preenchemos a lista com zeros até ter 300
        else:
            fingerprint_features.extend([0] * (300 - len(fingerprint_features)))
        
        # Transforme a lista em uma array NumPy e a retorne
        return np.array(fingerprint_features)

    paths = ['enhanced/img_login.png', 'enhanced/img_1.png', 'enhanced/img_2.png', 'enhanced/img_3.png', 'enhanced/img_4.png', 'enhanced/img_5.png']  # Lista dos caminhos das imagens
    feature_arrays = [process_image(path) for path in paths]  # Processa cada imagem e armazena os resultados

    # Agora você tem uma lista de matrizes de características que você pode comparar
    for i in range(1, len(feature_arrays)):
        distance = np.linalg.norm(feature_arrays[0] - feature_arrays[i])
        print(f"Distância entre a imagem 1 e a imagem {i+1}: {distance}")