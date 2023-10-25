from SistemaPrincipal import SistemaPrincipal as MainSystem
from UserInterface import Interface
mainSys = MainSystem()

#NAO FUNCIONA FORA DA PASTA SRC
def iniciar():
    mainSys.start_face_recognition()

interface = Interface(mainSys)
interface.mainloop()