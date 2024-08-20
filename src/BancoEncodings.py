import pickle, os, face_recognition
from DebugTools_ import *

class BancoEncodings: 
    def __init__(self, path: str, obj_fireBaseManager: object):
        """Classe BancoEncodings
        Tem métodos para manipular os encodings do banco de dados local
        como salvar, carregar, recarregar etc...
        """

        # Carregar encdings do FireBaseManager
        self.obj_fireBaseManager = obj_fireBaseManager

        # Caminho onde está a pasta raíz dos encodings/fotos de todos os usuários
        self.path = path #Exemplo: /pasta1/pasta2/Encodings/
                         #                                 /Usuário1/fotos ou encodings
                         #                                 /Usuário2/fotos ou encodings
                         #                                 /Usuário3/fotos ou encodings
                         #
                         # path = pasta1/pasta2/Encodings/
        
        # Converter o caminho ('C:/pasta/pasta/pasta') para o caminho do sistema normal
        #drive_letter = self.path[:2]
        self.slash = '/' #BUG: Para diretórios do windows funicona tanto / quanto \ mas no linux só funciona /, pra trocar mais fácil eu fiz essa variável
        self.model='large' # Modelo do face_recognition para usar, 'small' utiliza apenas 5 pontos, 'large' utiliza 128
        self.num_jitters=10 # Quantidade de vezes que a foto é distorcida para fazer o encoding da foto nos métodos

# FUNÇÕES PARA MANIPULAR O BANCO DO FIREBASE ===========================================================================


    
# FUNÇÕES PARA MANIPULAR O BANCO LOCAL ===========================================================================

    # carrega um arquivo .enc específico
    def _load_enc_file(self, specific_path):
        """
        specific_path: caminho específico do arquivo .enc para carregar;
        """
        with open(f'{specific_path}', 'rb') as f: # Modo de leitura binária no arquivo específico
            ids_list, endoded_faces = pickle.load(f) # Carrega o id e o encoding
            #plog(f'INFO: .enc file loaded: {specific_path}.enc') # Informação do terminal

        # NOTA: Está sendo utilizado para carregar o arquivo dataser_faces.enc que tem todas as 13K faces codificadas
        return [ids_list, endoded_faces] # Retorna uma lista com as duas listas para utilizar

    # salva um arquivo .enc específico em um diretório
    def _save_enc_file(self, encoded_faces, specific_path = None):
        """
        encoded_faces: lista com duas listas com todas as codificações e IDs prontas;
        specific_path=None: Especifica um caminho e nome de arquivo para falvar as 
        faces codificadas, valor padrão (None) vai salvar na pasta raíz do sistema
        com o nome 'dataset_faces.enc';
        """
        if not specific_path: # Se não tiver um caminho especificado para salvar utiliza nome de arquivo padrão e salva na raíz do sistema
            with open('dataset_faces.enc', 'wb') as f:
                pickle.dump(encoded_faces, f)
        else: # Salva o arquivo no caminho e nome especificado
            with open(f'{specific_path}.enc', 'wb') as f:
                pickle.dump(encoded_faces, f)

# FUNÇÕES COM ENCODE E LOAD DE TODAS AS FACES ARQUIVO POR ARQUIVO COM LISTAS ===========================================================================

    # Apenas faz o encoding de todas as faces e salva o arquivo .enc para cada foto
    def _encode_all_faces_list(self, force = False):
        log_file = 'encoding_00.log'
        erros = 0
        erros_log = []

        #Criar arquivo de log para salvar tudo
        start_logFile(log_file)

        for ids in os.listdir(self.path):
            for file in os.listdir(f'{self.path}{self.slash}{ids}'):
                if not f'{self.path}{self.slash}{ids}{self.slash}{file}'.endswith('.enc'):
                    if not os.path.exists(f'{self.path}{self.slash}{ids}{self.slash}{file}.enc') or force:
                        plog(f'CODIFICANDO FACE: {ids}...')
                        #fazer encoding, criar arquivo e salvar
                        file_loaded = face_recognition.load_image_file(f'{self.path}{self.slash}{ids}{self.slash}{file}')
                        # Dependendo da versão da biblioteca face_recognition precisa usar [0]
                        file_encoded = face_recognition.face_encodings(file_loaded, model=self.model, num_jitters=self.num_jitters)
                        try:
                            file_encoded = file_encoded[0]
                        except:
                            file_encoded = file_encoded

                        try:
                            verificar_codificacao = file_encoded.shape
                            codificacao_bem_sucedida = True
                        except:
                            codificacao_bem_sucedida = False
                        if codificacao_bem_sucedida:
                            #Salvar arquivo
                            self._save_enc_file([ids, file_encoded], f'{self.path}{self.slash}{ids}{self.slash}{file}')
                            plog(f'ARQUIVO CODIFICADO E SALVO COM SUCESSO: {self.path}{self.slash}{ids}{self.slash}{file}')
                            #Adicionar ao arquivo de log
                            add_to_logFile(log_file, f'ARQUIVO CODIFICADO E SALVO COM SUCESSO: {self.path}{self.slash}{ids}{self.slash}{file}')
                            #excluir imagem TODO
                            #os.remove(f'{self.path}{self.slash}{ids}{self.slash}{file}')
                        else:
                            plog(f'ERRO AO CODIFICAR ARQUIVO: {self.path}{self.slash}{ids}{self.slash}{file}')
                            erros += 1
                            erros_log.append(f'ERRO AO CODIFICAR ARQUIVO: {self.path}{self.slash}{ids}{self.slash}{file}')
                            add_to_logFile(log_file, f'ERRO AO CODIFICAR ARQUIVO: {self.path}{self.slash}{ids}{self.slash}{file}')
                    else:
                        plog(f'INFO: CODIFICAÇÃO JÁ EXISTENTE: {self.path}{self.slash}{ids}{self.slash}{file}')
                        add_to_logFile(log_file, f'INFO: CODIFICAÇÃO JÁ EXISTENTE: {self.path}{self.slash}{ids}{self.slash}{file}')

        for i in erros_log: plog(i)
        plog(f'ERROS TOTAIS: {erros}')

    # Apenas carrega todas as codificações para listas e retorna elas
    def _load_all_faces_list(self):
        ids_list = []
        encoded_faces_list = []

        #Criar arquivo log para salvar tudo
        log_file = 'load_encodings_00.log'
        start_logFile(log_file)

        for ids in os.listdir(self.path):
            for file in os.listdir(f'{self.path}{self.slash}{ids}'):
                if not file.endswith('.enc'):
                    continue

                #fazer encoding, carregar arquivo e salvar
                try:
                    tmp_id, tmp_encode = self._load_enc_file(f'{self.path}{self.slash}{ids}{self.slash}{file}')
                    ids_list.append(tmp_id)
                    encoded_faces_list.append(tmp_encode)
                    add_to_logFile(log_file, f'SUCESSO AO CARREGAR ARQUIVO: {self.path}{self.slash}{ids}{self.slash}{file}')
                except:
                    #plog(f'ERRO AO CARREGAR ARQUIVO: {self.path}{self.slash}{ids}{self.slash}{file}')
                    add_to_logFile(log_file, f'ERRO AO CARREGAR ARQUIVO: {self.path}{self.slash}{ids}{self.slash}{file}')
        #plog(encoded_faces_list)
        return [ids_list, encoded_faces_list]

# FUNÇÕES COM APENAS UM ARQUIVO E COM LISTA ===========================================================================

    # Cria o encoding de todas as faces em um arquivo, armazena em uma lista e salva tudo em um arquivo apenas, em seguida retorna a lista
    def _encode_all_faces_onefile(self, force = True):
        ids_list = []
        encoded_faces = []
        for ids in os.listdir(self.path):
            for file in os.listdir(f'{self.path}{self.slash}{ids}'):
                if not f'{self.path}{self.slash}{ids}{self.slash}{file}'.endswith('.enc'):
                    if not os.path.exists(f'{self.path}{self.slash}{ids}{self.slash}{file}.enc') or force == True:
                        # Fazer encoding do arquivo se não existir e salvar como .enc
                        file_loaded = face_recognition.load_image_file(f'{self.path}{self.slash}{ids}{self.slash}{file}')
                        file_encoded = face_recognition.face_encodings(file_loaded, model=self.model, num_jitters=self.num_jitters)
                        try:
                            # Verifica se a codificação é válida  
                            verificar_codificacao = file_encoded.shape
                            codificacao_bem_sucedida = True
                        except:
                            codificacao_bem_sucedida = False

                        if codificacao_bem_sucedida:
                            ids_list.append(ids)
                            encoded_faces.append(file_encoded)
                            print(f'INFO: Codificação {ids} - OK')
                            #print(file_encoded.shape)
                        else:
                            print(f'INFO: Codificação {ids} - FALHA')

                    elif os.path.exists(f'{self.path}{self.slash}{ids}{self.slash}{file}.pkl'):
                        print('já existe')
                        continue

        self._save_enc_file([ids_list, encoded_faces])

        return [ids_list, encoded_faces]
    
    # Carrega um arquivo específico .enc com todos os ids e faces
    def _load_encoded_lists_onefile(self, file):
        with open(file, 'rb') as f:
            ids_list, endoded_faces = pickle.load(f)
        return [ids_list, endoded_faces]

    def _load_FBM_files(self):
        encodings_data = self.obj_fireBaseManager.load_storage_files()
        # Salvar temporariamente aqui os encodings para minimizar os downloads
        self.obj_fireBaseManager.create_temp_file(encodings_data)
        return encodings_data


# FUNÇÕES "PÚBLICAS" ===========================================================================

    def registrar_novo_usuario(self, id, lista_de_fotos, save_encoding):
        overwrite = False

        # Verifique se a codificação da face está ativada
        if not os.path.exists(f'{self.path}{self.slash}{id}'):
            # Verifique se o local de destino existe; se não cria
            os.makedirs(f'{self.path}{self.slash}{id}')
        else:
            if input('ID já cadastrado, deseja sobrescrever arquivos?').lower()[0] == 's':
                overwrite = True
            else:
                return 0

        # Salve as fotos no diretório
        for i, foto in enumerate(lista_de_fotos):
            nome_do_arquivo = os.path.join(f'{self.path}{self.slash}{id}', f'foto_{i}.jpg')
            if overwrite:
                try:
                    os.remove(f'{nome_do_arquivo}.enc')
                except:
                    print(f'ERRO AO APAGAR ARQUIVO {self.path}{self.slash}{id}{self.slash}{nome_do_arquivo}.enc')
            cv2.imwrite(nome_do_arquivo, foto)
        
        print(f'Fotos salvas com sucesso no diretório: "{self.path}{self.slash}{id}"')
        
        if save_encoding:
            #TODO
            # Substituir pelo upload do FBM
            self._encode_all_faces_list(force=False)

    def remove_id(self, id):
        #TODO
        # Colocar função do FBM
        if os.path.exists(f'{self.path}{self.slash}{id}'):
            for file in os.listdir(f'{self.path}{self.slash}{id}'):
                os.remove(f'{self.path}{self.slash}{id}{self.slash}{file}')
            os.removedirs(f'{self.path}{self.slash}{id}')
        else:
            print('Usuário não encontrado!')

    # Aqui seria a função de carregar os .enc do banco de dados online real
    def load_face_encoding(self):
        print('CARREGANDO FACE ENCODINGS CONHECIDOS')
        #TODO
        # Colocar aqui o load do banco de dados do FBM
        #self.obj_fireBaseManager.load_storage_files()

        #plog('CRIAR NOVO FACE ENCODINGS')
        #return self._load_encoded_lists_onefile('./dataset_faces.enc')
        #return self._load_all_faces_list()
        return self._load_FBM_files()