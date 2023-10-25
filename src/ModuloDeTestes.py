import ModuloDeTestesFonte
import time, threading

class ModuloDeTestes:
    def __init__(self, sistemaPrincipal):
        self.obj_ModuloTestesFonte = ModuloDeTestesFonte.ModuloDeTestesFonte()
        self.running_teste = False
        self.camera = sistemaPrincipal.camera
        self.objeto_reconhecimento_facial = sistemaPrincipal.objeto_reconhecimento_facial
        self.encoded_faces = sistemaPrincipal.encoded_faces
        self.sistemaPrincipal = sistemaPrincipal
        self.path = sistemaPrincipal.faces_registradas_path
        

    def inicar_teste(self, nome_da_planlha: str = 'Default'):
        
        # Inicializar o objeto do módulo de testes e receber os parâmetros
        obj_ModuloFonte = ModuloDeTestesFonte.ModuloDeTestesFonte()
        obj_ModuloFonte.getParametrosDeTeste()
        obj_ModuloFonte.rostos_utilizados = len(self.encoded_faces[0])
        self.nome_esperado = obj_ModuloFonte.nome_esperado # Pega o nome esperado dos resultados

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

        # Aplicar dos testes
        obj_ModuloFonte.rostos_analisados = self.total_face_encoding
        obj_ModuloFonte.rostos_incorretos = self.face_error
        obj_ModuloFonte.rostos_corretos = self.total_face_encoding - self.face_error
        
        # Gerar Planilha e Terminar Processo de testes
        obj_ModuloFonte.gerarPlanilha(nome_da_planlha)

    def _contagem_regressiva(self, segundos: int = 10):
        for i in range(segundos):
            time.sleep(1)
            print(segundos-i)
        print('CONTAGEM REGRESSIVA TERMINADA')

    def _start_camera(self):
        resultados = self.camera.inicializar_camera(self.objeto_reconhecimento_facial, self.encoded_faces, self.nome_esperado)
        
        self.face_error = resultados[0]
        self.total_face_encoding = resultados[1]
        self.face_correct = resultados[2]
        self.total_frames = resultados[3]