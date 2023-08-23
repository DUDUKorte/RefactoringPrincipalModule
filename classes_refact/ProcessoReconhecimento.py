import FaceRecognitionMethod
import cv2

class ProcessoReconhecimento:
    
    def __init__(self, detect_param, cam_param, sistemaPrincial, encoded_faces):
        # self.running define se o while deve estar rodando
        self.running = False
        self.detect_param = detect_param
        self.cam = cam_param
        self.encoded_faces = encoded_faces
        
        # usar isso para chamar função de notificação do sistema principal
        self.sistemaPrincipal = sistemaPrincial
        # detect_param e cam_param devem ser dicionários com configurações
        # exemplo: 

        # detect_param = {
        #     'detect_method' : 'face_recognition',
        #     'face_encoding_resample' : 3,
        #     'model' : 'hog' ou 'cnn',
        #     'locations_upsample' : 0,
        #     'tolerance' : 0.5 ou 0.4,
        #     'min_detecion_confidence' : 0.5
        #     #outros parâmetros se precisar... 
        # }
        print('PROCESSO RECONHECIMENTO CRIADO')
        pass

    def process(self):
        # sistema while está rodando
        self.running = True
        # se o detect_param['detect_method'] == face_recognition ou mediapipe
        # cria o objeto de cada qual e manda detect_param como parâmetro
        #TODO: Colocar opção do mediapipe
        if self.detect_param['detect_method'] == 'face_recognition':
            objeto_reconhecimento_facial = FaceRecognitionMethod.FaceRecognitionMethod(self.detect_param)
        else:
            raise ValueError("detect_settings > detect_method possui valor inválido")
        
        face_error = 0
        total_face_encoding = 0

        print("RODANDO WHILE PRINCIPAL")
        while self.running:
            # tudaoo
            # ler imagem da câmera
            success, frame = self.cam.read()
            # se leu a imagem da câmera com sucesso continua
            if success:
                # pega o face_locations(mostrar tempo?)
                face_locations = objeto_reconhecimento_facial.get_face_locations(frame)
                
                # tem face?
                # tá perto o suficiente? (usar variável??)

                # se sim, faz a face_encoding com a face_locations que pegamos
                # usar detect_param['face_encoding_resample'] para escolher
                # a quantidade de resamples do face encoding
                if face_locations:
                    face_encoding = objeto_reconhecimento_facial.get_encoded_face(frame, face_locations)
                    #print(face_encoding) if self.detect_param["DEBUG"] else None

                    # comparar face codificada com a lista de faces reconhecidas
                    # (usar face_distance)
                    #found_id = objeto_reconhecimento_facial.decode_face(self.encoded_faces, face_encoding)
                    
                    #Faz a codificação utilizando listas
                    found_id = objeto_reconhecimento_facial._decode_face_lists(self.encoded_faces, face_encoding, True)
                    
                    if found_id:
                        face_error += 1 if not found_id == "AaEsquilo" else 0
                        total_face_encoding += 1

                    print(f'FACE ERRORS: {face_error}')
                    print(f'TOTAL FACE ENCODINGS: {total_face_encoding}')


                    # alguma das distâncias é menor ou menor ou igual á tolerância? (0.5 ou 0.4)
                    # sim? então vamos pegar o menor valor da lista (min(valores)?)
                    
                    # pegar a primeira coluna (ID) da mesma linha que tem o encoding encontrado
                    # notificar sistema principal com o id reconhecido

                    self.sistemaPrincipal.notificacaoReconhecimento(found_id)

            # atualiza o frame?? se não for mostrar na tela, não
            # se for mostrar na tela, usar variável DEBUG para testes
            # e atualizar o frame da tela aqui, precisa usar cv2.waitkey(1)
                if self.detect_param['DEBUG']:
                    cv2.imshow('test', frame)
                    cv2.waitKey(1)
            pass

