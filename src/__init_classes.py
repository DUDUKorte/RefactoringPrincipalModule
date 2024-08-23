"""
CLASSES IMPORT FILE
"""

#Classes imports
from .BancoAlunos import BancoAlunos
from .ProcessoReconhecimento import ProcessoReconhecimento
from .BancoEncodings import BancoEncodings
from .FireBaseManager import FireBaseManager # <==========
from .Camera import Camera
from .ModuloDeTestes import ModuloDeTestes
from .ModuloDeCadastro import ModuloDeCadastro
from .FaceRecognitionMethod import FaceRecognitionMethod

__all__ = ["BancoAlunos",
           "ProcessoReconhecimento",
           "BancoEncodings", 
           "FireBaseManager", 
           "Camera", 
           "ModuloDeTestes", 
           "ModuloDeCadastro", 
           "FaceRecognitionMethod"]

# #Classes imports
# from .BancoAlunos import BancoAlunos
# from .ProcessoReconhecimento import ProcessoReconhecimento
# from .BancoEncodings import BancoEncodings
# from .FireBaseManager import FireBaseManager # <========== DB
# from .Camera import Camera
# from .ModuloDeTestes import ModuloDeTestes
# from .ModuloDeCadastro import ModuloDeCadastro
# from .FaceRecognitionMethod import FaceRecognitionMethod
# from .SistemaPrincipal import SistemaPrincipal
# from liveness_detection_src.liveness_detection import liveness_detector

# #Tools
# from .DebugTools_ import *
# from face_recognition import *

# __all__ = ["BancoAlunos",
#            "ProcessoReconhecimento",
#            "BancoEncodings", 
#            "FireBaseManager", 
#            "Camera", 
#            "ModuloDeTestes", 
#            "ModuloDeCadastro", 
#            "FaceRecognitionMethod",
#            "SistemaPrincipal",
#            "update_debug_var",
#            "plog",
#            "rectanglelog",
#            "textlog",
#            "start_logFile",
#            "add_to_logFile",
#            "debugInput",
#            "load_image_file",
#            "face_encodings",
#            "face_locations",
#            "face_distance",
#            "compare_faces",
#            "liveness_detector"]