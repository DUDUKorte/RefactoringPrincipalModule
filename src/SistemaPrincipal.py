import json, time, winsound
from DebugTools_ import *

#Classes imports
from BancoAlunos import BancoAlunos
from ProcessoReconhecimento import ProcessoReconhecimento
from BancoEncodings import BancoEncodings
from FireBaseManager import FireBaseManager # <==========
from Camera import Camera
from ModuloDeTestes import ModuloDeTestes
from ModuloDeCadastro import ModuloDeCadastro
from FaceRecognitionMethod import FaceRecognitionMethod

class SistemaPrincipal:
    def __init__(self):
        # primeiras operações do sistema, carregar tudo, iniciar câmera, etc
        print(f'INFO: CARREGANDO CONFIGURAÇÕES...')
        self.load_config_files()
        self.faces_registradas_path = self.system_settings['banco_faces_registradas_path']
        # Criação das classes necessárias
        print(f'INFO: CARREGANDO DATA BASE')
        self.obj_fireBaseManager = FireBaseManager(self.fbm_config)
        self.bancoEncodings = BancoEncodings(self.faces_registradas_path, self.obj_fireBaseManager)
        self.bancoAlunos = BancoAlunos(self.system_settings['alunos_planilha_path'], self.system_settings['alunos_planilha'], self.obj_fireBaseManager)
        
        print('INFO: CARREGANDO FACES CODIFICADAS...')
        self.encoded_faces = self.bancoEncodings.load_face_encoding()
        
        print(f'INFO: OBTENDO CÂMERA...')
        self.camera = Camera(self.cam_settings)
        self.cam_param = self.camera.get_camera_object()
        
        # Iniciar o objeto de reconhecimento facial
        if self.detect_settings['detect_method'] == 'face_recognition':
            self.objeto_reconhecimento_facial = FaceRecognitionMethod(self.detect_settings)
        else:
            raise ValueError("detect_settings[detect_method] possui valor inválido")
        
        self.cooldown_alunos = {}

    #PRONTO
    def start_face_recognition(self):
        # iniciar o objeto da classe do reconhecimento com os parâmetros
        self.processoReconhecimento = ProcessoReconhecimento(self.detect_settings, self)
        self.processoReconhecimento.process()
    
    #PRONTO
    def stop_face_recognition(self):
        self.processoReconhecimento.running = False

    #PRONTO
    def notificacaoReconhecimento(self, id):
        # notificar o banco de dados com o id do aluno reconhecido
        # no sistema do reconhecimento facial
        if id == 'DESCONHECIDO':
            #self.bancoAlunos.aluno_reconhecido('DESCONHECIDO')
            winsound.Beep(1800, 500)
            return None

        if not id in self.cooldown_alunos:
            self.bancoAlunos.aluno_reconhecido(id)
            winsound.Beep(2500, 500)
            self.cooldown_alunos[id] = time.time()

        else:
            time_now = time.time()
            if time_now - self.cooldown_alunos[id] >= 30:
                self.cooldown_alunos.pop(id)
                self.notificacaoReconhecimento(id)

    #PRONTO
    def start_user_register(self, id = '1', codificarFace=True, carregarCodificacao=True):
        if not id:
            return 0
        obj_modulo_de_cadastro = ModuloDeCadastro(id,
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
        obj_modulo_de_testes = ModuloDeTestes(self)
        #obj_modulo_de_testes.inicar_teste(nomePlanilha)
        #obj_modulo_de_testes.video_teste(nomePlanilha)
        obj_modulo_de_testes.fotos_teste(nomePlanilha, 'testes')

    #PRONTO
    def load_config_files(self):
        with open("system_settings.json", 'r') as f:
            self.system_settings = json.load(f)
            update_debug_var(self.system_settings['debug'])

        with open("detect_settings.json", 'r') as f:
            self.detect_settings = json.load(f)
        print(f'INFO: CONFIGURAÇÕES DE DETECÇÃO CARREGADAS!')

        with open("cam_settings.json", 'r') as f:
            self.cam_settings = json.load(f)
        print(f'INFO: CONFIGURAÇÕES DE CÂMERA CARRREGADO!')

        with open("fbm_config.json", 'r') as f:
            self.fbm_config = json.load(f)
        print(f'INFO: FBM CONFIG CARREGADO!')
    
    #PRONTO
    def _reload_encoded_faces(self):
        #self.encoded_faces = self.bancoEncodings._load_all_faces_list()
        self.encoded_faces = self.bancoEncodings.load_face_encoding()
        plog(f'ENCODED FACES ATUALIZADO')