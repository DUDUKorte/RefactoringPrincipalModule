import cv2
from DebugTools_ import *
import time

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
        # detect_settings e cam_param devem ser dicionários com configurações
        # exemplo: 

        # detect_settings = {
        #     'detect_method' : 'face_recognition',
        #     'face_encoding_resample' : 3,
        #     'model' : 'hog' ou 'cnn',
        #     'locations_upsample' : 0,
        #     'tolerance' : 0.5 ou 0.4,
        #     'min_detecion_confidence' : 0.5
        #     #outros parâmetros se precisar... 
        # }
        plog('PROCESSO RECONHECIMENTO CRIADO')
        pass

    def process(self):
        # sistema while está rodando
        self.running = True
        face_error = 0
        total_face_encoding = 0
        tempo_médio = 0
        tempo_registrado = []

        print("RODANDO WHILE PRINCIPAL")
        while self.running:
            # tudaoo
            # ler imagem da câmera
            #self.cam_obj.open('http://pas:123@192.168.42.129:8080/video')
            success, bgr_frame = self.cam_obj.read()
            # se leu a imagem da câmera com sucesso continua
            if success:
                # Converte o frame do formato de cor bgr, que é utilizado pelo opencv, para o formato rgb, que é utilizado pelo face_recognition
                frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)

                # pega o face_locations(mostrar tempo?)
                encoding_start = time.time()
                face_location = self.objeto_reconhecimento_facial.get_main_face_location(frame)
                if face_location:
                    #cv2.rectangle(bgr_frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 0, 255), 1)
                    rectanglelog(frame=bgr_frame, locations=face_location, color=(0,0,255), thickness=1)

                # tem face?
                # tá perto o suficiente? (usar variável??)

                # se sim, faz a face_encoding com a face_locations que pegamos
                # usar detect_settings['face_encoding_resample'] para escolher
                # a quantidade de resamples do face encoding
                if face_location:
                    plog(face_location)
                    
                    #Verifica se é uma face verdadeira ou não
                    if self.objeto_reconhecimento_facial.detect_liveness(frame, face_location):
                        plog("Face Real")
                        textlog(frame=bgr_frame, text="Face Real", locations=face_location, bottom=True)

                        face_encoding = self.objeto_reconhecimento_facial.get_encoded_face(frame, face_location)
                        #print(face_encoding) if self.detect_settings["DEBUG"] else None

                        # comparar face codificada com a lista de faces reconhecidas
                        # (usar face_distance)
                        #found_id = self.objeto_reconhecimento_facial.decode_face(self.encoded_faces, face_encoding)

                        #Faz a codificação utilizando listas
                        found_id = self.objeto_reconhecimento_facial._decode_face_lists(self.encoded_faces, face_encoding, False)
                        encoding_end = time.time()
                        
                        if found_id:
                            tempo_registrado.append(encoding_end-encoding_start)
                            face_error += 1 if not found_id == "AaEsquilo" else 0
                            total_face_encoding += 1

                            #cv2.rectangle(bgr_frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 255, 0), 4)
                            rectanglelog(frame=bgr_frame, locations=face_location, color=(0,255,0), thickness=4)
                            #cv2.putText(bgr_frame, found_id, (face_location[3]+6, face_location[0]-6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                            textlog(frame=bgr_frame, text=found_id, locations=face_location, font=cv2.FONT_HERSHEY_COMPLEX, font_size=1, color=(0,255,0), thickness=1)

                        plog(f'FACE ERRORS: {face_error}')
                        plog(f'TOTAL FACE ENCODINGS: {total_face_encoding}')
                        tempo_médio = (sum(tempo_registrado)/len(tempo_registrado)) if len(tempo_registrado) != 0 else 0
                        plog(f'Tempo Médio: {tempo_médio}')

                        # alguma das distâncias é menor ou menor ou igual á tolerância? (0.5 ou 0.4)
                        # sim? então vamos pegar o menor valor da lista (min(valores)?)
                        
                        # pegar a primeira coluna (ID) da mesma linha que tem o encoding encontrado
                        # notificar sistema principal com o id reconhecido

                        self.sistemaPrincipal.notificacaoReconhecimento(found_id)
                    else:
                        plog("Face FAKE")
                        textlog(frame=bgr_frame, text="Face Fake", locations=face_location, bottom=True, color=(0, 0, 255))

            # atualiza o frame?? se não for mostrar na tela, não
            # se for mostrar na tela, usar variável DEBUG para testes
            # e atualizar o frame da tela aqui, precisa usar cv2.waitkey(1)
                if self.detect_settings['DEBUG']:
                    #TESTE
                    #img_gray = cv2.cvtColor(bgr_frame, cv2.COLOR_RGB2GRAY)
                    #img_sobelx = cv2.Sobel(src=img_gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
                    #img_sobely = cv2.Sobel(src=img_gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
                    #img_sobelxy = cv2.Sobel(src=img_gray, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)
                    #img_sobelxy = cv2.addWeighted(img_sobelx, 0.5, img_sobely, 0.5, 0) #melhor usar assim
                    bgr_frame = self.camera.escalonar_frame(bgr_frame, 50)
                    cv2.imshow('test', bgr_frame)
                    cv2.waitKey(1)
            pass