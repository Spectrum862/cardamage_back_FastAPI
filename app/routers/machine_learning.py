from fastapi import APIRouter, WebSocket
from mrcnn.config import Config
import mrcnn.model as modellib
import os
import skimage
import numpy as np
import io

router = APIRouter(
    prefix='/model',
    tags=['Model']
)


class DamageConfig(Config):
    NAME = 'damage'
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 4 + 1
    IMAGE_RESIZE_MODE = 'square'
    IMAGE_MIN_DIM = 1024
    IMAGE_MAX_DIM = 1024
    STEPS_PER_EPOCH = 100
    VALIDATION_STEPS = 50
    LEARNING_RATE = 0.001
    LEARNING_MOMENTUM = 0.9
    DETECTION_MIN_CONFIDENCE = 0.8
    GRADIENT_CLIP_NORM = 10.0


class InferenceConfig(DamageConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MIN_DIM = 256
    IMAGE_MAX_DIM = 1024
    DETECTION_MIN_CONFIDENCE = 0.8


@router.post('/predict')
async def predict():
    inference_config = InferenceConfig()
    inference_config.display()
    model_path = 'app/asset/model.h5'
    model = modellib.MaskRCNN(mode='inference', config=inference_config, model_dir=model_path)
    print('Loading weights from ', model_path)
    model.load_weights(model_path, by_name=True)
    data_test_path = 'app/asset/dataset/test'
    image_paths = []
    results = []
    classes = ['BG', '(A)scratch', '(B)minimal pound', '(C)heavy damage', '(D)crush or break']
    for filename in os.listdir(data_test_path):
        if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
            image_paths.append(os.path.join(data_test_path, filename))

    for image_path in image_paths:
        img = skimage.io.imread(image_path)
        img_arr = np.array(img)
        result = model.detect([img_arr], verbose = 1)
        results.append(result[0])
    print(results[0]['masks'])
    return {'result': 'eiei'}



