import cv2

class Camera:
    def __init__(self, cam_param):
        # inicializar câmera
        # pegar valores da câmera para usar (fps, resolução etc)
        # APENAS EXEMPLOS
        
        self.params = cam_param
        self.params["camera_object"] = cv2.VideoCapture(cam_param["camera_index"])

        print("CAMERA INICIALIZADA")
    
    def get_camera_object(self):
        return self.params["camera_object"]