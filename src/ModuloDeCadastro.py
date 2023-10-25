import time, threading, cv2, os

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
        #Espera N segundos
        thread_contagem_2.start()
        thread_contagem_2.join()
        #Terminar de registrar  a face
        self.camera.stop_face_register()
        self.camera.stop_camera()
        # Esperar a thread da camera acabar
        thread_start_camera.join()

        #SALVAR ENCODINGS E FOTOS CAPTURADOS
        self._salvar_fotos()

    def remover_usuario(self):
        if os.path.exists(f'{self.path}/{self.id}'):
            for file in os.listdir(f'{self.path}/{self.id}'):
                os.remove(f'{self.path}/{self.id}/{file}')
            os.removedirs(f'{self.path}/{self.id}')
        else:
            print('Usuário não encontrado!')

    def _start_camera(self):
        # inicialização da câmera usando threading, se necessário
        # 0 é identificado como camera padrão(mudar caso nescessario{Eduardo})
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
        # lógica para salvar as fotos
        # Verifique se a codificação da face está ativada
        if not os.path.exists(f'{self.path}/{self.id}'):
            # Verifique se o local de destino existe; se não cria
            os.makedirs(f'{self.path}/{self.id}')
        else:
            if input('ID já cadastrado, deseja sobrescrever arquivos?').lower()[0] == 's':
                pass
            else:
                return 0

        # Salve as fotos no diretório
        for i, foto in enumerate(self.lista_de_fotos):
            nome_do_arquivo = os.path.join(f'{self.path}/{self.id}', f'foto_{i}.jpg')
            cv2.imwrite(nome_do_arquivo, foto)
            #Salva arquivo .enc
        if self.codificarFace:
            self.bancoEncodings._encode_all_faces_list(force=False)
        if self.carregarCodificacao:
            self.sistema_principal._reload_encoded_faces()

        print(f'Fotos salvas com sucesso no diretório: "{self.path}/{self.id}"')

