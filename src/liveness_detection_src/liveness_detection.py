import os
import cv2
import numpy as np
import warnings
import time

from liveness_detection_src.src.anti_spoof_predict import AntiSpoofPredict
from liveness_detection_src.src.generate_patches import CropImage
from liveness_detection_src.src.utility import parse_model_name

warnings.filterwarnings('ignore')

class liveness_detector:
    def __init__(self, 
                model_dir = "src/liveness_detection_src/resources/anti_spoof_models", 
                device_id = 0):
        
        self.model_dir = model_dir
        self.device_id = device_id

    def _get_bbox(self, face_location):
        top, right, bottom, left = face_location
        return [int(left), int(top), int(right-left+1), int(bottom-top+1)]
    
    def detect_liveness(self, frame, face_location, model_dir = None, device_id = None):
        model_dir = self.model_dir if not model_dir else model_dir
        device_id = self.device_id if not device_id else device_id

        # Código do git = https://github.com/computervisioneng/Silent-Face-Anti-Spoofing 
        model_test = AntiSpoofPredict(device_id)
        image_cropper = CropImage()

        # frame = cv2.resize(frame, (int(frame.shape[0] * 3/4), frame.shape[0]))
        # if not self._check_image(frame):
        #     return False

        image_bbox = self._get_bbox(face_location) #Aqui ele pega a face da pessoa usando algum algoritmop
        prediction = np.zeros((1, 3))
        
        #model_name = "4_0_0_80x80_MiniFASNetV1SE.pth"
        model_name = "2.7_80x80_MiniFASNetV2.pth"
        teste_for_init = time.time()
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": frame,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))

        # draw result of prediction
        label = np.argmax(prediction)
        value = prediction[0][label]/2
        if label == 1:
            return True
        else:
            return False

    def _check_image(self, image):
        height, width, channel = image.shape
        if width/height != 3/4:
            print("Image is not appropriate!!!\nHeight/Width should be 4/3.")
            return False
        else:
            return True


if __name__ == "__main__":
    teste = liveness_detector()
    teste.detect_liveness()