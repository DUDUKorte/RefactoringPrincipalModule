print()
from SistemaPrincipal import SistemaPrincipal as MainSystem
from UserInterface import Interface
#TODO
"""
- clean tmp .jpeg
- remove load encoding on start
"""
if __name__ == "__main__":
    print('start')
    mainSys = MainSystem()
    
    # #NAO FUNCIONA FORA DA PASTA SRC
    #def iniciar():
    #    mainSys.start_test_module()

    #iniciar()
    interface = Interface(mainSys)
    interface.mainloop()
    #https://www.youtube.com/watch?v=5KEObONUkik
    #https://devfuria.com.br/python/modulos-pacotes/