import ProcessoReconhecimento
import BancoEncodings
import Camera
import ModuloDeTestes
import ModuloDeCadastro
import json
import FaceRecognitionMethod
from DebugTools_ import *

class SistemaPrincipal:
    def __init__(self):

        # Criação das classes necessárias
        #self.faces_registradas_path = '\DUDU\Programinhas_PC\TCC\ModuloPrincipal\known_faces'
        self.faces_registradas_path = 'known_50_faces_test'
        self.bancoEncodings = BancoEncodings.BancoEncodings(self.faces_registradas_path)

        # primeiras operações do sistema, carregar tudo, iniciar câmera, etc
        print(f'INFO: CARREGANDO CONFIGURAÇÕES...')
        self.detect_settings = None
        self.cam_settings = None
        self.load_config_files()

        print('INFO: CARREGANDO FACES CODIFICADAS...')
        self.encoded_faces = self.bancoEncodings.load_face_encoding()
        
        print(f'INFO: OBJTENDO CÂMERA...')
        self.camera = Camera.Camera(self.cam_settings)
        self.cam_param = self.camera.get_camera_object()
        
        # Iniciar o objeto de reconhecimento facial
        if self.detect_settings['detect_method'] == 'face_recognition':
            self.objeto_reconhecimento_facial = FaceRecognitionMethod.FaceRecognitionMethod(self.detect_settings)
        else:
            raise ValueError("detect_settings[detect_method] possui valor inválido")

    #PRONTO
    def start_face_recognition(self):
        # iniciar o objeto da classe do reconhecimento com os parâmetros
        self.processoReconhecimento = ProcessoReconhecimento.ProcessoReconhecimento(self.detect_settings, self)
        self.processoReconhecimento.process()
    
    #PRONTO
    def stop_face_recognition(self):
        self.processoReconhecimento.running = False

    #PRONTO
    def notificacaoReconhecimento(self, id):
        # notificar o banco de dados com o id do aluno reconhecido
        # no sistema do reconhecimento facial
        plog(id)

    #PRONTO
    def start_user_register(self, id = '1', codificarFace=True, carregarCodificacao=True):
        if not id:
            return 0
        obj_modulo_de_cadastro = ModuloDeCadastro.ModuloDeCadastro(id,
                                                                   codificarFace=codificarFace,
                                                                   carregarCodificacao=carregarCodificacao,
                                                                   sistema_principal = self
                                                                   )
        obj_modulo_de_cadastro.iniciar_cadastro()

    #PRONTO
    def start_user_remove(self, id = '1'):
        self.bancoEncodings.remove_id(id)

    #PRONTO
    def start_test_module(self, nomePlanilha = 'PlanilhaTeste01'):
        obj_modulo_de_testes = ModuloDeTestes.ModuloDeTestes(self)
        obj_modulo_de_testes.inicar_teste(nomePlanilha)

    #PRONTO
    def load_config_files(self):
        with open("detect_settings.json", 'r') as f:
            self.detect_settings = json.load(f)
        print(f'INFO: CONFIGURAÇÕES DE DETECÇÃO CARREGADAS!')

        with open("cam_settings.json", 'r') as f:
            self.cam_settings = json.load(f)
        print(f'INFO: CONFIGURAÇÕES DE CÂMERA CARRREGADO!')
    
    #PRONTO
    def _reload_encoded_faces(self):
        self.encoded_faces = self.bancoEncodings._load_all_faces_list()