from fastapi import APIRouter
import mrcnn.model as modellib
from ..utils.ml_helper import get_base64_instant, InferenceConfig
import os
import skimage
import numpy as np
from pydantic import BaseModel
from typing import List
import base64

router = APIRouter(
    prefix='/model',
    tags=['Model']
)


class PredictRequestBody(BaseModel):
    images: List[str]


@router.post('/predict')
async def predict(body: PredictRequestBody):
    inference_config = InferenceConfig()
    inference_config.display()
    model_path = 'app/asset/model.h5'
    model = modellib.MaskRCNN(mode='inference', config=inference_config, model_dir=model_path)
    print('Loading weights from ', model_path)
    model.load_weights(model_path, by_name=True)
    data_test_path = 'app/asset/dataset/test_uni'
    image_paths = []
    results = []
    instant_images = []
    classes = ['BG', '(A)scratch', '(B)minimal pound', '(C)heavy damage', '(D)crush or break']

    for filename in os.listdir(data_test_path):
        if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
            image_paths.append(os.path.join(data_test_path, filename))

    for base64image in body.images:
        if isinstance(base64image, bytes):
            base64image = base64image.decode("utf-8")
        imgdata = base64.b64decode(base64image)
        img = skimage.io.imread(imgdata, plugin='imageio')
        img_arr = np.array(img)
        result = model.detect([img_arr], verbose = 1)
        r = result[0]
        results.append(result[0])
        base64_img = get_base64_instant(img, r['rois'], r['masks'], r['class_ids'], classes, r['scores'], figsize = (12,12))
        instant_images.append(base64_img)
    return {'result': instant_images}



