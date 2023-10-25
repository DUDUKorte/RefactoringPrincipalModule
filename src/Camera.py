import cv2

class Camera:
    def __init__(self, cam_param):
        # inicializar câmera
        # pegar valores da câmera para usar (fps, resolução etc)
        self.running_camera = True
        self.running_face_recognition = False
        self.running_face_register = False
        
        self.params = cam_param
        camera_object = cv2.VideoCapture(cam_param["camera_index"])
        camera_object.set(3, cam_param["height"])
        camera_object.set(4, cam_param["width"])
        self.params["camera_object"] = camera_object

        print("CAMERA INICIALIZADA")
    
    def get_camera_object(self):
        return self.params["camera_object"]

    def escalonar_frame(self, frame, porcentagem = 75):
        width = int(frame.shape[1] * porcentagem / 100)
        height = int(frame.shape[0] * porcentagem / 100)
        return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    #INICIALIZA CAMERA, PRECISA SER THREAD
    def inicializar_camera(self, objeto_reconhecimento_facial, encoded_faces, nome_esperado = "AaEsquilo"):
        face_error = 0
        total_face_encoding = 0
        face_correct = 0
        total_frames = 0
        camera_object = self.params["camera_object"]
        face_encodings = []
        frames_capturados = []

        while self.running_camera:
            success, frame = camera_object.read()
            #frame "limpo" para salvar na pasta
            clean_frame = frame
            if success:

                if self.running_face_recognition or self.running_face_register:
                    face_location = objeto_reconhecimento_facial.get_main_face_location(frame)
                    if face_location:
                        cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 0, 255), 1)
                        
                        face_encoding = objeto_reconhecimento_facial.get_encoded_face(frame, face_location)
                        if self.running_face_register:
                            face_encodings.append(face_encoding)
                            frames_capturados.append(clean_frame)

                        if self.running_face_recognition:
                            found_id = objeto_reconhecimento_facial.decode_face_lists(encoded_faces, face_encoding, True)
                            #found_id = None
                            if found_id:
                                face_error += 1 if not found_id == nome_esperado else 0
                                total_face_encoding += 1
                                face_correct += 1 if found_id == nome_esperado else 0
                                cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 255, 0), 4)
                    total_frames += 1
                # Atualiza quadro da tela
                # Diminui o tamanho do frame
                frame = self.escalonar_frame(frame, 50)
                cv2.imshow('TESTE RODANDO', frame)
                cv2.waitKey(1)

        return [face_error, total_face_encoding, face_correct, total_frames, face_encodings, frames_capturados]


    def stop_camera(self):
        self.running_camera = False

    def start_face_recognition(self):
        self.running_face_recognition = True
    
    def stop_face_recognition(self):
        self.running_face_recognition = False

    def start_face_register(self):
        self.running_face_register = True

    def stop_face_register(self):
        self.running_face_register = False