"""
Projeto: Face Recognition MeuIF Implementation
Descrição: Implementação do projto Face Recognition para o App MeuIF
Versão: 1.0.0
Contato: seu.email@dominio.com
Licença: MIT
Dependências: easydict==1.10, wheel, numpy==1.23.5, tqdm==4.66.3, torchvision, torch, opencv-python==4.6.0.66, Pillow==10.3.0, tensorboardX==2.5.1, cmake==3.27.7, dlib==19.24.2, face-recognition==1.3.0, pandas==2.0.3, customtkinter==5.2.1, packaging==21.3, openpyxl==3.1.2, firebase-admin==6.5.0

"""

# Metadados
__description__ = "Face Recognition For MeuIF App"
__version__ = "1.0.0"
__author__ = "@DUDUKorte"
__license__ = "MIT"
__dependencies__ = [
    "easydict>=1.10",
    "wheel",
    "numpy>=1.23.5",
    "tqdm>=4.66.3",
    "torchvision",
    "torch",
    "opencv-python>=4.6.0.66",
    "Pillow>=10.3.0",
    "tensorboardX>=2.5.1",
    "cmake>=3.27.7",
    "dlib>=19.24.2",
    "face-recognition>=1.3.0",
    "pandas>=2.0.3",
    "customtkinter>=5.2.1",
    "packaging>=21.3",
    "openpyxl>=3.1.2",
    "firebase-admin>=6.5.0"
]

from .SistemaPrincipal import SistemaPrincipal
from .UserInterface import Interface

__all__ = ["SistemaPrincipal", "Interface", "UserInterface"]