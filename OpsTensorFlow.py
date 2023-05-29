import os
import numpy as np
import tensorflow as tf
import cv2

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Caminho para o diretório com o modelo pré-treinado
PATH_TO_MODEL_DIR = 'path/to/model/directory'

# Caminho para o arquivo de rótulo
PATH_TO_LABELS = os.path.join(PATH_TO_MODEL_DIR, 'label_map.pbtxt')

# Caminho para o arquivo do modelo
PATH_TO_SAVED_MODEL = os.path.join(PATH_TO_MODEL_DIR, 'saved_model')

# Carrega o modelo
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

# Carrega o arquivo de rótulo
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

# Carrega a imagem
image_path = 'path/to/image.jpg'
image_np = cv2.imread(image_path)

# Converte a imagem em um tensor
input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

# Executa a detecção de objetos no tensor
detections = detect_fn(input_tensor)

# Converte os resultados da detecção em um formato legível
num_detections = int(detections.pop('num_detections'))
detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
detections['num_detections'] = num_detections

# Visualiza os resultados da detecção
vis_util.visualize_boxes_and_labels_on_image_array(
    image_np,
    detections['detection_boxes'],
    detections['detection_classes'].astype(np.int32),
    detections['detection_scores'],
    category_index,
    use_normalized_coordinates=True,
    line_thickness=8)

# Mostra a imagem com os objetos detectados
cv2.imshow('Object Detection', cv2.resize(image_np, (800, 600)))
cv2.waitKey(0)
cv2.destroyAllWindows()