from DebugTools_ import *
import os, pickle, time, json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

class FireBaseManager:
    def __init__(self, fbm_config: dict):
        # Inicialização das variáveis do FireBaseManager
        credentials_path = fbm_config["credentials_path"]
        storageBucketName = fbm_config["storage_bucket_name"]
        self.prefix_path = fbm_config["prefix_path"]
        self.cache_path = './cache'
        self.tmp_enc_path = 'tmp_enc'

        # Inicializa SDK do firebase
        self.cred = credentials.Certificate(f'{credentials_path}')
        firebase_admin.initialize_app(self.cred, {'storageBucket' : f'{storageBucketName}'})

        # Cria Objeto referência de armazenamento
        self.bucket = storage.bucket()
        self.db = firestore.client()
        plog("INFO: CREDENTIALS LOADED")

    # Pega os dados dos alunos no bd
    def get_data(self):
        raw_data = self.db.collection('FaceRecognitionData').stream()
        data = {}
        for db_data in raw_data:
            data[f'{db_data.id}'] = db_data.to_dict()['Dados']
            plog(f'{db_data.id} => {db_data.to_dict()}')
        
        plog(data)
        return data

    # Envia notificação para o bd
    def send_notification(self, matricula):
        entrada_atual = self.db.collection('Reports').document(f'{matricula}').get().to_dict()['entradas']
        self.db.collection('Reports').document(f'{matricula}').set({"entradas" : entrada_atual+1}, merge=True)

    # Atualiza todos os dados no storage
    def update_storage_files(self, path_to_encodings, data_base : dict):
        for matricula in os.listdir(path_to_encodings):
            # Verificar se existe pasta da matricula no firebase
            if self._if_path_exists(f'{self.prefix_path}/{matricula}/'):
                pass
            else:
                #TODO 
                # VERIFICAR SE A MATRÍCULA EXISTE
                if matricula in data_base.keys():
                    self._create_folder(f'{self.prefix_path}/{matricula}/')
            
            for file in os.listdir(f'{path_to_encodings}/{matricula}'):
                if file.endswith('.enc'):
                    # Verificar se o arquivo já está no storage
                    if self._if_path_exists(f'{self.prefix_path}/{matricula}/{file}'):
                        pass
                        plog('EXISTE')
                    else:
                        #Upar Arquivo aqui
                        self._upload_file(f'{path_to_encodings}/{matricula}/{file}', f'{self.prefix_path}/{matricula}/{file}')
                        pass

    # Carrega todos os .enc do storage
    def load_storage_files(self):
        #TODO
        if os.path.exists(f'{self.cache_path}/tmp_db_files.enc'):
            with open(f'{self.cache_path}/tmp_db_files.enc', 'rb') as f:
                temp_enc_file = pickle.load(f)

        #Criar arquivo log para salvar tudo
        log_file = 'load_encodings_db_00.log'
        start_logFile(log_file)

        blobs = self.bucket.list_blobs()
        ids_list = []
        encoded_faces = []

        # CRIAR PASTA DE CACHE DE ARQUIVOS TEMPORARIOS
        if os.path.exists(f'{self.cache_path}/'):
            if os.path.exists(f'{self.cache_path}/{self.tmp_enc_path}/'):
                pass
            else:
                os.mkdir(f'{self.cache_path}/{self.tmp_enc_path}')
                add_to_logFile(log_file, f'PASTA TMP INEXISTENTE. CRIANDO...')
        else:
            os.mkdir(f'{self.cache_path}/')
            os.mkdir(f'{self.cache_path}/{self.tmp_enc_path}/')
            add_to_logFile(log_file, f'PASTA CACHE INEXISTENTE. CRIANDO...')

        start_time = time.time()
        # Baixar os arquivos, ler, interpretar e retornar a lista
        for blob in blobs:
            for path in blob.name.split(','):
                if path.endswith('.enc'):
                    try:
                        #b_file = self._read_file(f'{path}')
                        b_file_path = self._download_file(f'{path}')

                        # Ler arquivo em rb e excluir
                        with open(b_file_path, 'rb') as f:
                            tmp_ids_list, tmp_encoded_faces = pickle.load(f)
                            ids_list.append(tmp_ids_list)
                            encoded_faces.append(tmp_encoded_faces)
                            add_to_logFile(log_file, f'SUCESSO AO CARREGAR ARQUIVO: {b_file_path}')
                        os.remove(b_file_path)
                    except:
                        add_to_logFile(log_file, f'ERRO AO CARREGAR ARQUIVO: {path}')
                        pass


        plog(f'{time.time() - start_time} TO LOAD ALL ENCODINGS')
        return [ids_list, encoded_faces]

    def create_temp_file(self, encoding_data):
        # CRIAR PASTA DE CACHE DE ARQUIVOS TEMPORARIOS
        if not os.path.exists(f'{self.cache_path}/'):
            os.mkdir(f'{self.cache_path}/')
        
        with open(f'{self.cache_path}/tmp_db_files.enc', 'wb') as f:
            pickle.dump(encoding_data, f)

    # Enviar o arquivo para o storage
    def _upload_file(self, file_path: str, file_name: str):
        blob = self.bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        plog(f'ARQUIVO {file_name} ENVIADO COM SUCESSO')

    # Baixar arquivo para diretório local
    def _download_file(self, blob_path: str):
        blob = self.bucket.blob(blob_path)
        file_name = [name for name in blob.name.split('/') if name.endswith('.enc')][0]

        blob.download_to_filename(f'{self.cache_path}/{self.tmp_enc_path}/{file_name}')
        plog(f'ARQUIVO BAIXADO COM SUCESSO')
        return f'{self.cache_path}/{self.tmp_enc_path}/{file_name}'

    # Ler arquivo diretamente na memória NÃO TÁ FUNCIONANDO MT BEM
    def _read_file(self, file_name: str):
        blob = self.bucket.blob(file_name)
        data = blob.download_as_string()
        #data = blob.download_as_bytes(raw_download=True)
        plog(f'DATA RECEBIDA COM SUCESSO:\n{data}')
        return data

    # Criar pastas/subpastas dentro do storage
    def _create_folder(self, folder_name: str):
        blob = self.bucket.blob(folder_name)
        blob.upload_from_string('')
        plog(f'PASTA {folder_name} CRIADA COM SUCESSO')

    def _if_path_exists(self, path: str):
        blob = self.bucket.blob(f'{path}')
        return blob.exists()

if __name__ == '__main__':
    """
    pip install firebase-admin
    """
    with open('fbm_config.json', 'r') as f:
        fbm_config = json.load(f)

    firebasemanager = FireBaseManager(fbm_config)
    #firebasemanager._upload_files('foto_0.jpg.enc', 'FaceRecognitionFiles/Alunos/esquilo/foto_0.enc')
    #firebasemanager._create_folder('FaceRecognitionFiles/Alunos/esquilo/')
    #firebasemanager._if_path_exists('FaceRecognitionFiles/Alunos/esquilo/')
    #firebasemanager.update_storage_all('dataset_faces')
    #firebasemanager.load_storage_files()
    firebasemanager.get_data()
    firebasemanager.send_notification('esquilo_')
