import ModuloDeTestesFonte, FaceRecognitionMethod
import time, threading
from DebugTools_ import *
import os

class ModuloDeTestes:
    def __init__(self, sistemaPrincipal):
        self.obj_ModuloTestesFonte = ModuloDeTestesFonte.ModuloDeTestesFonte()
        self.running_teste = False
        self.camera = sistemaPrincipal.camera
        self.objeto_reconhecimento_facial = sistemaPrincipal.objeto_reconhecimento_facial
        self.encoded_faces = sistemaPrincipal.encoded_faces
        self.sistemaPrincipal = sistemaPrincipal
        self.path = sistemaPrincipal.faces_registradas_path
        self.obj_ModuloFonte = ModuloDeTestesFonte.ModuloDeTestesFonte()

        self.face_error = 0
        self.total_face_encoding = 0
        self.face_correct = 0
        self.total_frames = 0
        self.tempo_medio = 0

    def inicar_teste(self, nome_da_planilha: str = 'Default'):
        
        # Inicializar o objeto do módulo de testes e receber os parâmetros
        self.obj_ModuloFonte.getParametrosDeTeste()
        self.obj_ModuloFonte.rostos_utilizados = len(self.encoded_faces[0])
        self.nome_esperado = self.obj_ModuloFonte.nome_esperado # Pega o nome esperado dos resultados

        # Criar threads aqui
        thread_contagem_1 = threading.Thread(target=self._contagem_regressiva)
        thread_start_camera = threading.Thread(target=self._start_camera)
        thread_contagem_2 = threading.Thread(target=self._contagem_regressiva)

        # Incizalizar as threads e realizar cada teste
        thread_start_camera.start()
        thread_contagem_1.start()
        thread_contagem_1.join()
        #self.running_face_recognition = True
        self.camera.start_face_recognition()
        thread_contagem_2.start()
        thread_contagem_2.join()
        #self.running_face_recognition = False
        self.camera.stop_face_recognition()
        #self.running_teste = False
        self.camera.stop_camera()
        # Esperar a thread da camera acabar para garantir que pegou todos os resultados antes de continuar
        thread_start_camera.join()

        # Aplicar os resultados dos testes nas variáveis
        self._aplicar_resultados()
        
        # Gerar Planilha e Terminar Processo de testes
        self.obj_ModuloFonte.gerarPlanilha(nome_da_planilha)

    def video_teste(self, nome_da_planilha = "Default"):
        thread_start_camera = threading.Thread(target=self._start_camera)
        thread_start_camera.start()
        self.camera.start_face_recognition()
        thread_start_camera.join()

        # Aplicar resultados dos testes
        self._aplicar_resultados()

        # Gerar Planilha e Terminar Processo de testes
        self.obj_ModuloFonte.gerarPlanilha(nome_da_planilha)

    def fotos_teste(self, nome_da_planilha = "Default", images_path = 'testes'):
        opcoes_de_algoritmo = ['hog', 'cnn']
        opcoes_de_iluminacao = ["alta", "media", "baixa", "artificial"]
        opcoes_de_qualidade = ['360p', '480p', '720p', '1080p']
        opcoes_de_distancia = ['30cm', '1m', '2m']
        
        testes = 0
        self.tempo_registrado = []

        for algoritmo in opcoes_de_algoritmo:
            #plog(f'ALGORITMO: {algoritmo}')
            for qualidade in opcoes_de_qualidade:
                #plog(f'QUALIDADE {qualidade}')
                for distancia in opcoes_de_distancia:
                    #plog(f'DISTANCIA: {distancia}')
                    for iluminacao in opcoes_de_iluminacao:
                        #plog(f'ILUMINAÇÃO {iluminacao}')
                        self.obj_ModuloFonte.setParametro(algoritmo, qualidade, distancia, iluminacao)

                        for id in os.listdir(images_path):
                            #plog(f'Teste {algoritmo} | {qualidade} | {distancia} | {iluminacao}\nEM {images_path}/{id}/{distancia}/ilum_{iluminacao}/foto.jpg')
                            folder = f'{images_path}/{id}/{distancia}/ilum_{iluminacao}/'
                            self._aplicar_teste(algoritmo, qualidade, distancia, iluminacao, folder, id)
                            testes += 1

                        #TODO SALVAR NA PLANILHA AQUI
                        self.tempo_medio = (sum(self.tempo_registrado)/len(self.tempo_registrado)) if (len(self.tempo_registrado) > 0) else 0
                        self._aplicar_resultados()
                        self.obj_ModuloFonte.gerarPlanilha(nome_da_planilha)
                        self._reset_resultados()

        plog(f'TESTES TOTAIS: {testes}')

    def _aplicar_teste(self, algoritmo, qualidade, distancia, iluminacao, folder, id):
        detect_settings = {
            "detect_method" : "face_recognition",
            "face_encoding_resample" : 0,
            "model" : algoritmo,
            "locations_upsample" : 0,
            "tolerance" : 0.45,
            "min_detection_confidence" : 0.4,
            "distance_percentage" : 0,
            "liveness_detection" : False,
            "DEBUG" : True
        }

        self.objeto_reconhecimento_facial.update_detect_settings(detect_settings)
        for file in os.listdir(folder):
            frame = cv2.imread(f'{folder}/{file}', 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.camera.escalonar_frame(frame, self.camera.escala[qualidade])

            start_recognition = time.time()
            face_location = self.objeto_reconhecimento_facial.get_main_face_location(frame)
            if face_location:
                if self.objeto_reconhecimento_facial.detect_liveness(frame, face_location):
                    face_encoding = self.objeto_reconhecimento_facial.get_encoded_face(frame, face_location)
                    found_id = self.objeto_reconhecimento_facial.decode_face_lists(self.encoded_faces, face_encoding, False)
                    if found_id:
                        self.tempo_registrado.append(time.time() - start_recognition)
                        if found_id == id: self.face_correct += 1
                        else: self.face_error += 1
                        self.total_face_encoding += 1

    def _aplicar_resultados(self):
        # Aplicar dos testes
        self.obj_ModuloFonte.rostos_utilizados = len(self.encoded_faces[0])
        self.obj_ModuloFonte.rostos_analisados = self.total_face_encoding
        self.obj_ModuloFonte.rostos_incorretos = self.face_error
        self.obj_ModuloFonte.rostos_corretos = self.face_correct
        self.obj_ModuloFonte.tempo_medio = f'{self.tempo_medio:.2f}s'
        self.obj_ModuloFonte.taxa_de_acerto = f'{((self.face_correct / self.total_face_encoding) * 100):.2f}%' if (self.total_face_encoding > 0) else f'N/A'

    def _reset_resultados(self):
            # Reseta os valores dos testes
            self.total_face_encoding = 0
            self.face_error = 0
            self.face_correct = 0
            self.tempo_medio = 0
            self.taxa_de_acerto = 0

    def _contagem_regressiva(self, segundos: int = 10):
        for i in range(segundos):
            time.sleep(1)
            print(segundos-i)
        print('CONTAGEM REGRESSIVA TERMINADA')

    def _start_camera(self):
        resultados = self.camera.inicializar_camera(self.objeto_reconhecimento_facial, self.encoded_faces, self.nome_esperado)
        plog(resultados)
        self.face_error = resultados[0]
        self.total_face_encoding = resultados[1]
        self.face_correct = resultados[2]
        self.total_frames = resultados[3]
        self.tempo_medio = resultados[6]