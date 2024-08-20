from DebugTools_ import *
import os, pickle, time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

class FireBaseManager:
    def __init__(self, credentials_path : str, storageBucketName : str):
        # Inicializa SDK do firebase
        self.cred = credentials.Certificate(f'{credentials_path}')
        firebase_admin.initialize_app(self.cred, {'storageBucket' : f'{storageBucketName}'})
        # Cria Objeto referência de armazenamento
        self.bucket = storage.bucket()
        plog("CREDENTIALS LOADED")
        self.prefix_path = 'FaceRecognitionFiles/Alunos'
        self.cache_path = './cache'
        self.tmp_enc_path = 'tmp_enc'

    def update_storage_all(self, path_to_encodings):
        for matricula in os.listdir(path_to_encodings):
            # Verificar se existe pasta da matricula no firebase
            if self._if_path_exists(f'{self.prefix_path}/{matricula}/'):
                pass
            else:
                #TODO 
                # VERIFICAR SE A MATRÍCULA EXISTE
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

    def load_storage_files(self):
        blobs = self.bucket.list_blobs()
        # CRIAR PASTA DE CACHE DE ARQUIVOS TEMPORARIOS
        if os.path.exists(f'{self.cache_path}/'):
            if os.path.exists(f'{self.cache_path}/{self.tmp_enc_path}/'):
                pass
            else:
                os.mkdir(f'{self.cache_path}/{self.tmp_enc_path}')
        else:
            os.mkdir(f'{self.cache_path}/')
            os.mkdir(f'{self.cache_path}/{self.tmp_enc_path}/')

        start_time = time.time()
        # Baixar os arquivos, ler, interpretar e retornar a lista
        for blob in blobs:
            for path in blob.name.split(','):
                if path.endswith('.enc'):
                    #b_file = self._read_file(f'{path}')
                    b_file_path = self._download_file(f'{path}')

                    # Ler arquivo em rb e excluir
                    with open(b_file_path, 'rb') as f:
                        data1, data2 = pickle.load(f)
                    os.remove(b_file_path)
        plog(f'{time.time() - start_time} TO LOAD ALL ENCODINGS')

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
    credentials_path = './google-credentials.json'
    storage_bucket_name = ''
    firebasemanager = FireBaseManager(credentials_path, storage_bucket_name)
    #firebasemanager._upload_files('foto_0.jpg.enc', 'FaceRecognitionFiles/Alunos/esquilo/foto_0.enc')
    #firebasemanager._create_folder('FaceRecognitionFiles/Alunos/esquilo/')
    #firebasemanager._if_path_exists('FaceRecognitionFiles/Alunos/esquilo/')
    #firebasemanager.update_storage_all('dataset_faces')
    firebasemanager.load_storage_files()
