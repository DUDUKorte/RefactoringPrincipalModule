import time, threading

class ModuloDeCadastro:
    def __init__(self, id=None, codificarFace=True, carregarCodificacao=True, sistema_principal=None):
        self.sistema_principal = sistema_principal
        self.id = id
        self.camera = sistema_principal.camera
        self.objeto_reconhecimento_facial = sistema_principal.objeto_reconhecimento_facial
        self.path = sistema_principal.faces_registradas_path
        self.encoded_faces = sistema_principal.encoded_faces
        self.codificarFace = codificarFace
        self.carregarCodificacao = carregarCodificacao
        self.bancoEncodings = sistema_principal.bancoEncodings
        
        if id:
            pass
        else:
            raise ValueError('ID INVÁLIDO!!')

    def iniciar_cadastro(self):
        delay = 10

        #TODO
        """
        AQUI VAI A FOTO ENVIADA PELO ALUNO (PEDIR UM VIDEO TALVEZ?)
        REMOVER DELAYS, WAITS, ETC...
        """

        # Criar threads aqui
        thread_contagem_1 = threading.Thread(target= lambda: self._iniciar_contagem_regressiva(delay)) 
        thread_start_camera = threading.Thread(target=self._start_camera)
        thread_contagem_2 = threading.Thread(target=lambda: self._iniciar_contagem_regressiva(delay))

        #Inicializar as threads e cadastrar o usuário
        thread_start_camera.start()
        thread_contagem_1.start()
        thread_contagem_1.join()
        #Iniciar o registro da face
        self.camera.start_face_register()
        #Espera tirar a quantidade de fotos necessária
        # Esperar a thread da camera acabar
        thread_start_camera.join()

        #Espera capturar todos os frames necessários
    
        #SALVAR ENCODINGS E FOTOS CAPTURADOS
        self._salvar_fotos()

    def remover_usuario(self):
        self.bancoEncodings.remove_id(self.id)

    def _start_camera(self):
        # inicialização da câmera usando threading, se necessário
        # 0 é identificado como camera padrão(mudar caso nescessario{Eduardo})
        self.objeto_reconhecimento_facial.tolerance = 0 #Tira a distância mínima da câmera
        resultados = self.camera.inicializar_camera(self.objeto_reconhecimento_facial, self.encoded_faces)
        self.face_encodings = resultados[4]
        self.lista_de_fotos = resultados[5]

    def _iniciar_contagem_regressiva(self, segundos):
        # contagem regressiva antes de começar a registrar
        for i in range(segundos, 0, -1):
            print(f'Iniciando em {i} segundos...')
            time.sleep(1)
        print('CONTAGEM REGRESSIVA TERMINADA')

    def _salvar_fotos(self):
        self.bancoEncodings.registrar_novo_usuario(id=self.id,
                                                    lista_de_fotos= self.lista_de_fotos,
                                                    save_encoding = True if self.codificarFace else False
                                                    )
        if self.carregarCodificacao:
            self.sistema_principal._reload_encoded_faces()

