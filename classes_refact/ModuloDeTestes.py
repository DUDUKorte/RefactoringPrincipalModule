import ModuloDeTestesFonte
import FaceRecognitionMethod
import time, threading, cv2

class ModuloDeTestes:
    def __init__(self, detect_param, sistemaPrincipal):
        self.obj_ModuloTestesFonte = ModuloDeTestesFonte.ModuloDeTestesFonte()
        self.running_teste = False
        self.detect_param = detect_param
        self.cam_obj = sistemaPrincipal.cam_param
        self.encoded_faces = sistemaPrincipal.encoded_faces
        self.sistemaPrincipal = sistemaPrincipal

    def inicar_teste(self):
        # Inicializar o objeto do módulo de testes e receber os parâmetros
        obj_ModuloFonte = ModuloDeTestesFonte.ModuloDeTestesFonte()
        obj_ModuloFonte.getParametrosDeTeste()
        obj_ModuloFonte.rostos_utilizados = len(self.encoded_faces[0])


        # Criar threads aqui
        thread_contagem_1 = threading.Thread(target=self._contagem_regressiva)
        thread_start_camera = threading.Thread(target=self.start_camera)
        thread_contagem_2 = threading.Thread(target=self._contagem_regressiva)

        # Incizalizar as threads e realizar cada teste
        thread_start_camera.start()
        thread_contagem_1.start()
        thread_contagem_1.join()
        self.running_face_recognition = True
        thread_contagem_2.start()
        thread_contagem_2.join()
        self.running_face_recognition = False
        self.running_teste = False

        # Aplicar dos testes
        obj_ModuloFonte.rostos_analisados = self.total_face_encoding
        obj_ModuloFonte.rostos_incorretos = self.face_error
        obj_ModuloFonte.rostos_corretos = self.total_face_encoding - self.face_error
        
        # Gerar Planilha e Terminar Processo de testes
        obj_ModuloFonte.gerarPlanilha('TesteTal')

    def _contagem_regressiva(self, segundos: int = 10):
        for i in range(segundos):
            time.sleep(1)
            print(segundos-i)
        print('CONTAGEM REGRESSIVA TERMINADA')

    def start_camera(self):
        if self.detect_param['detect_method'] == 'face_recognition':
            objeto_reconhecimento_facial = FaceRecognitionMethod.FaceRecognitionMethod(self.detect_param)
        else:
            raise ValueError("detect_settings > detect_method possui valor inválido")
        self.face_error = 0
        self.total_face_encoding = 0
        self.face_correct = 0
        self.total_frames = 0
        self.running_teste = True
        self.running_face_recognition = False

        while self.running_teste:
            success, frame = self.cam_obj.read()
            if success:
                self.global_frame = frame
                if self.running_face_recognition:
                    face_location = objeto_reconhecimento_facial.get_main_face_location(frame)
                    if face_location:
                        cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 0, 255), 1)
                        
                        face_encoding = objeto_reconhecimento_facial.get_encoded_face(frame, face_location)
                        found_id = objeto_reconhecimento_facial._decode_face_lists(self.encoded_faces, face_encoding, True)
                        
                        if found_id:
                            self.face_error += 1 if not found_id == "AaEsquilo" else 0
                            self.total_face_encoding += 1
                            self.face_correct += 1 if found_id == "AaEsquilo" else 0
                            cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 255, 0), 4)
                    self.total_frames += 1
                # Atualiza quadro da tela
                cv2.imshow('TESTE RODANDO', frame)
                cv2.waitKey(1)
        self.cam_obj.release()
        self.cam_obj.destroyAllWindows()