import numpy as np
import pickle
import os
import face_recognition
import random

class BancoEncodings:
    def __init__(self, path):
        self.path = path
        # Converter o caminho ('C:/pasta/pasta/pasta') para o caminho do sistema normal
        drive_letter = self.path[:2]
        self.path = os.path.join(*self.path[2:].split('/'))
        self.path = drive_letter+'\\'+self.path

        self.model='large' 
        self.num_jitters=500

    def create_face_encoding(self, force = False):
        # path.split('/')?
        # os.path.join(pasta, pasta, pasta) << caminho de pasta funcional para qualquer OS

        # varrer as pastas se não tiver o .enc, criar
        # /pessoas/id/imagens 
                            #1.jpg
                            #2.jpg
                            #Exemplos dos codificados (.enc)
                            #1.enc (objeto numpy)
                            #2.enc (objeto numpy)

        for ids in os.listdir(self.path):
            for file in os.listdir(f'{self.path}\\{ids}'):
                if not f'{self.path}\\{ids}\\{file}'.endswith('.enc'):
                    if not os.path.exists(f'{self.path}\\{ids}\\{file}.enc') or force == True:
                        # Fazer encoding do arquivo se não existir e salvar como .enc
                        file_loaded = face_recognition.load_image_file(f'{self.path}\\{ids}\\{file}')
                        file_encoded = face_recognition.face_encodings(file_loaded, model='large', num_jitters=500)
                        try:
                            file_encoded = file_encoded[0]
                        except:
                            file_encoded = file_encoded

                        pessoa_codificada = {ids : file_encoded}
                        with open(f'{self.path}\\{ids}\\{file}.enc', 'wb') as f:
                            pickle.dump(pessoa_codificada, f)
                        print('criado para ' + ids)
                        print(file_encoded.shape)

                    elif os.path.exists(f'{self.path}\\{ids}\\{file}.enc'):
                        print('já existe')
                        continue

    def load_face_encoding(self):
        # varrer as pastas e carregar .enc
        #exemplo do sistema da variável com encodings:

        # encoded_faces = np.array(
        #     [
                ##[id, np.array([encoded face])]
        #         [1, np.array([1, 2, 3, 4, 5])],
        #         [2, np.array([6, 7, 8, 9, 1])]
        #     ]
        # )

        ## printa do array linha 1 coluna 0
        #print(arr[1, 0])
        ## pega linha 0 de todas as colunas/ coluna 0 e todas as linhas
        #encoded_faces[0,:]
    #     encoded_faces = {
    #         'eduardo' : [np.array([-6.35698065e-02,  4.88367751e-02,  2.14696974e-02, -3.76028121e-02,
    #    -1.42204121e-01,  2.85983607e-02, -4.53492403e-02, -1.00860886e-01,
    #     1.76801473e-01, -1.69181079e-01,  1.95860267e-01, -3.85432318e-02,
    #    -2.21384764e-01, -4.85594422e-02, -4.02193144e-02,  7.92598203e-02,
    #    -1.24565974e-01, -1.47997379e-01, -3.94460633e-02, -7.11060166e-02,
    #     6.37327507e-02,  6.30514994e-02, -6.34450614e-02,  1.22183710e-01,
    #    -1.82681903e-01, -3.48841369e-01, -8.79415423e-02, -1.18595004e-01,
    #     8.18245299e-03, -5.09650931e-02, -4.45256755e-02,  6.24415092e-02,
    #    -1.74658701e-01, -2.31795013e-02,  1.16534289e-02,  7.89758265e-02,
    #    -2.76405062e-03,  8.63476098e-03,  1.58031300e-01,  6.40539378e-02,
    #    -1.92458868e-01,  7.50927851e-02,  1.78985554e-03,  2.87185013e-01,
    #     1.29126310e-01,  7.47005567e-02,  5.82563085e-03, -2.83772312e-02,
    #     1.10320270e-01, -2.25567758e-01,  6.29791170e-02,  1.96883485e-01,
    #     1.92984685e-01,  4.15139794e-02,  2.01633852e-02, -1.16399541e-01,
    #     2.37909462e-02,  9.81391296e-02, -2.23563716e-01,  1.32040545e-01,
    #     7.39307255e-02, -1.88201115e-01,  3.09204310e-02,  1.08743701e-02,
    #     2.12191746e-01,  5.43357991e-02, -1.20807759e-01, -4.90851253e-02,
    #     1.17412746e-01, -2.29023740e-01, -5.94561771e-02,  4.17843610e-02,
    #    -7.55506977e-02, -1.92065686e-01, -2.64849693e-01,  7.20319599e-02,
    #     4.70367253e-01,  2.20232651e-01, -2.15574473e-01,  3.14094946e-02,
    #    -1.06141686e-01, -4.19612974e-04,  1.07907653e-01,  8.50032195e-02,
    #    -4.55505960e-02, -6.17471896e-02, -1.06197916e-01,  3.08075901e-02,
    #     2.27102488e-01,  7.18673086e-03,  1.07047390e-02,  2.89655626e-01,
    #     4.05286103e-02,  3.09266448e-02,  3.92940231e-02,  1.95240062e-02,
    #    -1.02547489e-01, -6.31815195e-02,  9.90020670e-03,  3.55077200e-02,
    #    -3.63175981e-02, -1.13198183e-01,  9.14459489e-03,  2.78960466e-02,
    #    -2.47959495e-01,  1.95056021e-01, -2.66295429e-02, -5.73965125e-02,
    #     6.09104708e-03,  5.44868186e-02, -1.04978725e-01, -5.79501502e-02,
    #     1.61832422e-01, -3.09029043e-01,  1.68820783e-01,  1.63688779e-01,
    #     5.96956424e-02,  2.31314749e-01,  4.16474305e-02,  5.87733500e-02,
    #    -2.45528873e-02, -1.06235832e-01, -1.11115694e-01, -1.55661702e-01,
    #     6.06288128e-02, -7.76916593e-02,  1.11467957e-01,  2.13993024e-02])],
    #     'esquilo' : [np.array([-6.35698065e-02,  4.88367751e-02,  2.14696974e-02, -3.76028121e-02,
    #    -1.42204121e-01,  2.85983607e-02, -4.53492403e-02, -1.00860886e-01,
    #     1.76801473e-01, -1.69181079e-01,  1.95860267e-01, -3.85432318e-02,
    #    -2.21384764e-01, -4.85594422e-02, -4.02193144e-02,  7.92598203e-02,
    #    -1.24565974e-01, -1.47997379e-01, -3.94460633e-02, -7.11060166e-02,
    #     6.37327507e-02,  6.30514994e-02, -6.34450614e-02,  1.22183710e-01,
    #    -1.82681903e-01, -3.48841369e-01, -8.79415423e-02, -1.18595004e-01,
    #     8.18245299e-03, -5.09650931e-02, -4.45256755e-02,  6.24415092e-02,
    #    -1.74658701e-01, -2.31795013e-02,  1.16534289e-02,  7.89758265e-02,
    #    -2.76405062e-03,  8.63476098e-03,  1.58031300e-01,  6.40539378e-02,
    #    -1.92458868e-01,  7.50927851e-02,  1.78985554e-03,  2.87185013e-01,
    #     1.29126310e-01,  7.47005567e-02,  5.82563085e-03, -2.83772312e-02,
    #     1.10320270e-01, -2.25567758e-01,  6.29791170e-02,  1.96883485e-01,
    #     1.92984685e-01,  4.15139794e-02,  2.01633852e-02, -1.16399541e-01,
    #     2.37909462e-02,  9.81391296e-02, -2.23563716e-01,  1.32040545e-01,
    #     7.39307255e-02, -1.88201115e-01,  3.09204310e-02,  1.08743701e-02,
    #     2.12191746e-01,  5.43357991e-02, -1.20807759e-01, -4.90851253e-02,
    #     1.17412746e-01, -2.29023740e-01, -5.94561771e-02,  4.17843610e-02,
    #    -7.55506977e-02, -1.92065686e-01, -2.64849693e-01,  7.20319599e-02,
    #     4.70367253e-01,  2.20232651e-01, -2.15574473e-01,  3.14094946e-02,
    #    -1.06141686e-01, -4.19612974e-04,  1.07907653e-01,  8.50032195e-02,
    #    -4.55505960e-02, -6.17471896e-02, -1.06197916e-01,  3.08075901e-02,
    #     2.27102488e-01,  7.18673086e-03,  1.07047390e-02,  2.89655626e-01,
    #     4.05286103e-02,  3.09266448e-02,  3.92940231e-02,  1.95240062e-02,
    #    -1.02547489e-01, -6.31815195e-02,  9.90020670e-03,  3.55077200e-02,
    #    -3.63175981e-02, -1.13198183e-01,  9.14459489e-03,  2.78960466e-02,
    #    -2.47959495e-01,  1.95056021e-01, -2.66295429e-02, -5.73965125e-02,
    #     6.09104708e-03,  5.44868186e-02, -1.04978725e-01, -5.79501502e-02,
    #     1.61832422e-01, -3.09029043e-01,  1.68820783e-01,  1.63688779e-01,
    #     5.96956424e-02,  2.31314749e-01,  4.16474305e-02,  5.87733500e-02,
    #    -2.45528873e-02, -1.06235832e-01, -1.11115694e-01, -1.55661702e-01,
    #     6.06288128e-02, -7.76916593e-02,  1.11467957e-01,  2.13993024e-02])]
    #     }

        print('CARREGANDO FACE ENCODINGS CONHECIDOS')
        return 0
    
    def insert_face(self, id, image, encoding = True, load_encoding = True):
        # encoded_aces append
        # pega id/cria id/recebe id
        # cria pasta com id dentro do self.path
        # se encoding = True, realiza o encoding e salva na pasta
        # se load_encoding = True, carrega os valores do id e face no encoded_faces e atualiza
        pass

    def remove_id(self, id, load_encoding = True):
        # remover encoded_faces
        # apagar pastas com os IDs
        # remover id de encoded_faces
        # atualiza o encoding se load_encoding = True
        pass

    def save_face_encodings(self, encoded_faces):
        with open('dataset_faces.enc', 'wb') as f:
            pickle.dump(encoded_faces, f)

    def encode_all_faces(self):
#        with open('dataset_faces.enc', 'rb') as f:
#            encoded_faces = pickle.load(f)
        encoded_faces = dict()

        for ids in os.listdir(self.path):
            for file in os.listdir(f'{self.path}\\{ids}'):
                if not f'{self.path}\\{ids}\\{file}'.endswith('.enc'):
                    if os.path.exists(f'{self.path}\\{ids}\\{file}.enc'):
                        #Faz o load
                        with open(f'{self.path}\\{ids}\\{file}.enc', 'rb') as f:
                            tmp_noname = pickle.load(f)
                            #tmp_noname = {'ids': nparray}
                            print(tmp_noname)
                            tmp_key = list(tmp_noname.keys())[0]
                            tmp_value = np.array(list(tmp_noname.values())[0])  

                            if tmp_key in encoded_faces:
                                tmp_key = tmp_key+str(random.randint(10, 99))
                            encoded_faces[tmp_key] = [tmp_value]

                    elif not os.path.exists(f'{self.path}\\{ids}\\{file}.enc'):
                        print(f'{file}.enc não existe')
        
        return encoded_faces
    
    def _encode_all_faces_onefile(self, force = True):
        ids_list = []
        encoded_faces = []
        for ids in os.listdir(self.path):
            for file in os.listdir(f'{self.path}\\{ids}'):
                if not f'{self.path}\\{ids}\\{file}'.endswith('.enc'):
                    if not os.path.exists(f'{self.path}\\{ids}\\{file}.enc') or force == True:
                        # Fazer encoding do arquivo se não existir e salvar como .enc
                        file_loaded = face_recognition.load_image_file(f'{self.path}\\{ids}\\{file}')
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

                    elif os.path.exists(f'{self.path}\\{ids}\\{file}.pkl'):
                        print('já existe')
                        continue

        self._save_face_encodings([ids_list, encoded_faces])

        return [ids_list, encoded_faces]
    
    def _load_encoded_lists_onefile(self):

        with open('dataset_faces.enc', 'rb') as f:
            ids_list, endoded_faces = pickle.load(f)

        return [ids_list, endoded_faces]