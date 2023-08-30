import ProcessoReconhecimento
import BancoEncodings
import Camera
import json

class SistemaPrincipal:
    def __init__(self):
        print(f'INFO: CARREGANDO CONFIGURAÇÕES...')
        # Carregar arquivos de configuração
        self.load_config_files()

        # Criação das classes necessárias
        faces_registradas_path = 'F:\DUDU\Programinhas_PC\TCC\ModuloPrincipal\known_faces'
        self.bancoEncodings = BancoEncodings.BancoEncodings(faces_registradas_path)

        # primeiras operações do sistema, carregar tudo, iniciar câmera, etc
        #encoded_faces = self.bancoEncodings.load_face_encoding()
        
        # Teste de salvar e carregar as faces atuais em encoded_faces
        #self.bancoEncodings._save_face_encodings(encoded_faces) # NÃO DEVE TER ISSO NO PROJETO FINALIZADO, SALVAR FACES É EM OUUTRA FUNÇÃO

        #encoded_faces = self.bancoEncodings._load_pickle_face_encodings()
        #print(f'INFO: CODIFICANDO FACES REGISTRADAS EM: {faces_registradas_path}')
        #encoded_faces = self.bancoEncodings._encode_all_faces_onefile() #Codifica rostos com listas
        print('INFO: CARREGANDO FACES CODIFICADAS...')
        self.encoded_faces = self.bancoEncodings._load_encoded_lists_onefile() #Carrega sistema com listas

        #Verificando se todos as codificações são válidas
        # if detect_settings['DEBUG']:
        #     for i in encoded_faces[1]:
        #         print(i.shape)
        
        # Cria Câmera e inicializa a classe
        self.camera = Camera.Camera(self.cam_settings)
        self.cam_param = self.camera.get_camera_object()

        # iniciar o objeto da classe do reconhecimento com os parâmetros
        self.processoReconhecimento = ProcessoReconhecimento.ProcessoReconhecimento(self.detect_settings, self)

    def start_face_recognition(self):
        # iniciar o sistema de reconhecimento, usar threads
        # exemplo de usar as threads
        # thread = Thread(target = self.processoReconhecimento.process())
        self.processoReconhecimento.process()
        pass

    def notificacaoReconhecimento(self, id):
        # notificar o banco de dados com o id do aluno reconhecido
        # no sistema do reconhecimento facial
        print(id)
        pass

    def start_user_register(self):
        pass

    def start_user_remove(self):
        pass

    def start_test_module(self):
        pass

    def start_register_folder(self):
        self.bancoEncodings.create_face_encoding(True)
        
    def load_config_files(self):
        with open("detect_settings.json", 'r') as f:
            self.detect_settings = json.load(f)
        print(f'INFO: DETECT SETTINGS CARREGADO')

        with open("cam_settings.json", 'r') as f:
            self.cam_settings = json.load(f)
        print(f'INFO: CAMERA SETTINGS CARREGADO')

sys = SistemaPrincipal()
sys.start_face_recognition()