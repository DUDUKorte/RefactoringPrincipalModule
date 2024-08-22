import cv2
from DebugTools_ import *
import time, threading

class ProcessoReconhecimento:
    
    def __init__(self, detect_settings, sistemaPrincipal):
        # self.running define se o while deve estar rodando
        self.running = False
        self.detect_settings = detect_settings
        self.cam_obj = sistemaPrincipal.cam_param
        self.camera = sistemaPrincipal.camera
        self.encoded_faces = sistemaPrincipal.encoded_faces
        self.objeto_reconhecimento_facial = sistemaPrincipal.objeto_reconhecimento_facial
        
        # usar isso para chamar função de notificação do sistema principal
        self.sistemaPrincipal = sistemaPrincipal

    def process(self):
        # sistema while está rodando
        self.running = True
        face_error = 0
        total_face_encoding = 0
        tempo_médio = 0
        tempo_registrado = []
        self.cooldown = False

        print("RODANDO WHILE PRINCIPAL")
        while self.running:
            # tudaoo
            # ler imagem da câmera
            #self.cam_obj.open('http://pas:123@192.168.42.129:8080/video') camera pelo webcam ip do cell
            success, bgr_frame = self.cam_obj.read()
            # se leu a imagem da câmera com sucesso continua
            if success:
                # Converte o frame do formato de cor bgr, que é utilizado pelo opencv, para o formato rgb, que é utilizado pelo face_recognition
                frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
                frame = self.camera.escalonar_frame(frame, self.camera.rescale_porcentage)

                # pega o face_locations(mostrar tempo?)
                encoding_start = time.time()
                face_location = self.objeto_reconhecimento_facial.get_main_face_location(frame)
                plog(f'LOCATION TIME : {time.time() - encoding_start}')
                if face_location:
                    #cv2.rectangle(bgr_frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 0, 255), 1)
                    rectanglelog(frame=bgr_frame, locations=face_location, color=(0,0,255), thickness=1)

                if face_location:
                    plog(face_location)
                    
                    #Verifica se é uma face verdadeira ou não
                    if self.objeto_reconhecimento_facial.detect_liveness(frame, face_location):
                        plog("Face Real")
                        textlog(frame=bgr_frame, text="Face Real", locations=face_location, bottom=True)

                        time_encoding_start = time.time()
                        face_encoding = self.objeto_reconhecimento_facial.get_encoded_face(frame, face_location)
                        plog(f'ENCODING TIME : {time.time() - time_encoding_start}')

                        found_id = self.objeto_reconhecimento_facial.decode_face_lists(self.encoded_faces, face_encoding, False)
                        encoding_end = time.time()
                        
                        if found_id and not self.cooldown:
                            tempo_registrado.append(encoding_end-encoding_start)
                            #face_error += 1 if not found_id == "AaEsquilo" else 0
                            total_face_encoding += 1

                            #cv2.rectangle(bgr_frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 255, 0), 4)
                            rectanglelog(frame=bgr_frame, locations=face_location, color=(0,255,0), thickness=4)
                            #cv2.putText(bgr_frame, found_id, (face_location[3]+6, face_location[0]-6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                            textlog(frame=bgr_frame, text=found_id, locations=face_location, font=cv2.FONT_HERSHEY_COMPLEX, font_size=1, color=(0,255,0), thickness=1)

                            if not self.cooldown:
                                self.sistemaPrincipal.notificacaoReconhecimento(found_id)
                                #self.cooldown = True
                                #thread_contagem = threading.Thread(target= lambda:self._iniciar_recognition_cooldown(1))
                                #thread_contagem.start()
                        else:
                            self.sistemaPrincipal.notificacaoReconhecimento('DESCONHECIDO')


                        plog(f'FACE ERRORS: {face_error}')
                        plog(f'TOTAL FACE ENCODINGS: {total_face_encoding}')
                        tempo_médio = (sum(tempo_registrado)/len(tempo_registrado)) if len(tempo_registrado) != 0 else 0
                        plog(f'Tempo Médio: {tempo_médio}')

                    else:
                        plog("Face FAKE")
                        textlog(frame=bgr_frame, text="Face Fake", locations=face_location, bottom=True, color=(0, 0, 255))
                #Exibe o frame na tela
                bgr_frame = self.camera.escalonar_frame(bgr_frame, 50)
                cv2.imshow('Face Recognition', bgr_frame)
                cv2.waitKey(1)
        cv2.destroyAllWindows()

    def _iniciar_recognition_cooldown(self, segundos):
        # contagem regressiva antes de começar a registrar
        for i in range(segundos, 0, -1):
            print(f'Passou {i} segundos...')
            time.sleep(1/2)
        self.cooldown = False
        print('CONTAGEM REGRESSIVA TERMINADA')

    def update_encoded_faces(self):
        self.encoded_faces = self.sistemaPrincipal.encoded_faces