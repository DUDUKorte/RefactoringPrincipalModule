import customtkinter
from PIL import Image
import os
import TestModuleUserInterface as test
import threading

customtkinter.set_appearance_mode("dark")

class Interface(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, mainSys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # PREPARAR TODAS AS THREADS DO SISTEMA PRINCIPAL
        self.mainSys = mainSys
        self.iniciar_sistema_principal = threading.Thread(target=lambda: self.mainSys.start_face_recognition())

        self.title("Face Recognition System")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/images/bg_gradient.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.create_login_frame()

        # create main frame
        self.create_main_frame()

        # create main system frame
        self.create_mainSys_frame()

        # create User register frame
        self.create_register_frame()

    #FUNÇÕES PARA INCIAR CADA TELA/MÓDULO
    #Evento para prosseguir da tela de login
    def login_event(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

        self.login_frame.grid_forget()  # remove login frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

    #Evento para iniciar o sistema principal
    def startMainSys(self):
        self.iniciar_sistema_principal.start()
        self.main_frame.grid_forget()
        self.mainSysFrame.grid(row=0, column=0, sticky="nsew", padx=100)
        print('main sys started')

    # #Evento para einiciar o módulo de testes
    # def startTestModule(self):
    #     apps = test.App()
    #     apps.mainloop()
    def startTestModule(self):
        pass

    #Evento do botão de voltar funcional para qualquer tela que volta à tela principal
    def back_event(self, currentFrame = None):
        currentFrame.grid_forget()  # remove main frame
        self.main_frame.grid(row=0, column=0, sticky="ns")  # show login frame
    
    def back_and_stop(self, currentFrame = None):
        self.mainSys.stop_face_recognition() #Finaliza a face recognition
        self.iniciar_sistema_principal.join()
        self.iniciar_sistema_principal = threading.Thread(target=lambda: self.mainSys.start_face_recognition()) #Reinicia a thread

        currentFrame.grid_forget()  # remove main frame
        self.main_frame.grid(row=0, column=0, sticky="ns")  # show login frame

    #Criações de cada tela
    def create_login_frame(self):
        #Criação do frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        
        #Configuração da label
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Face_Recognition\nLogin Page",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        
        #Entrada do username para login
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        
        #Entrada da senha para login
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))

        #botão de login
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def create_main_frame(self):
        #Criação do frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        #Configuração da label
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="Face_Recognition\nMain Page",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))

        #botão start main system
        self.other_button = customtkinter.CTkButton(self.main_frame, text="Start Main System", command=self.startMainSys, width=200)
        self.other_button.grid(row=1, column=0, padx=40, pady=(15, 15))

        #botão register
        self.other_button = customtkinter.CTkButton(self.main_frame, text="Register", command=lambda: self.back_event(self.main_frame), width=200)
        self.other_button.grid(row=2, column=0, padx=40, pady=(15, 15))

        #botão remove user
        self.other_button = customtkinter.CTkButton(self.main_frame, text="Remove User", command=lambda: self.back_event(self.main_frame), width=200)
        self.other_button.grid(row=3, column=0, padx=40, pady=(15, 15))

        #botão test module
        self.other_button = customtkinter.CTkButton(self.main_frame, text="Test Module", command=self.startTestModule, width=200)
        self.other_button.grid(row=4, column=0, padx=40, pady=(15, 15))

        #botão BACK
        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=lambda: self.back_event(self.main_frame), width=200)
        self.back_button.grid(row=5, column=0, padx=30, pady=(15, 15))

    def create_mainSys_frame(self):
        #criação do frame
        self.mainSysFrame = customtkinter.CTkFrame(self, corner_radius=0)
        self.mainSysFrame.grid_columnconfigure(0, weight=1)
        
        #Configuração da label
        self.mainSysLabel = customtkinter.CTkLabel(self.mainSysFrame, text="Face_Recognition\nMain System",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.mainSysLabel.grid(row=0, column=0, padx=30, pady=(30, 15))                      #precisa ser lambda : função(args) para usar argumentos no botão
        
        #botão STOP
        self.stop_button = customtkinter.CTkButton(self.mainSysFrame, text="Stop", command= lambda: self.back_and_stop(self.mainSysFrame))
        self.stop_button.grid(row=4, column=0, padx=30, pady=(15, 15))

    def create_register_frame(self):
        #Criação do frame
        self.registerFrame = customtkinter.CTkFrame(self, corner_radius=0)
        self.registerFrame.grid_columnconfigure(0, weight=1)
        
        #Configuração da label
        self.registerLabel = customtkinter.CTkLabel(self.registerFrame, text="Face_Recognition\nRegister User",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.registerLabel.grid(row=0, column = 0, padx=30, pady=(30, 15))
        
        #Botão BACK
        self.back_button = customtkinter.CTkButton(self.registerFrame, text="Back", command= lambda: self.back_event(self.registerFrame), width=200)
        self.back_button.grid(row=5, column = 0, padx = 30, pady=(15, 15))

if __name__ == "__main__":
    app = Interface(None)
    app.mainloop()