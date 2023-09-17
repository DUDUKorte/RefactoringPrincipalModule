import customtkinter, time, threading
import SistemaPrincipal

# O MENU AINDA NÃO É FUNCIONAL, É APENAS UMA PRÉVIA

class uiMainMenu:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

    def _adicionar_botao(self, master, text, command):
        self.button = customtkinter.CTkButton(master=master, text=text, command=command)
        self.button.pack(pady=12, padx=10)

    def start_ui_menu(self):
        ui_menu = uiMainMenu.janelaPrincipal()
        ui_menu.mainloop()

    # Criação da janela principal
    class janelaPrincipal(customtkinter.CTk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("500x350")
            self.title("Face Recognition System")

            # Quadrado pra ficar bonito
            self.frame = customtkinter.CTkFrame(master=self)
            self.frame.pack(pady=20, padx=60, fill="both", expand=True)

            # Texto que apareçe no topo da tela
            self.label = customtkinter.CTkLabel(master=self.frame, text="Main Menu")
            self.label.pack(pady=12, padx=10)

            uiMainMenu._adicionar_botao(self, master=self.frame, text = "Start Main System", command = self._iniciar_sistema_principal)
            uiMainMenu._adicionar_botao(self, master=self.frame, text="Register", command=self.abrirJanela_cadastrar_usuario)
            uiMainMenu._adicionar_botao(self, master=self.frame, text="Remove User", command=self.abrirJanela_removerUsuario)
            uiMainMenu._adicionar_botao(self, master=self.frame, text="Test Module", command=self._inicar_modulo_testes)

            self.janelaSistemaPrincipal = None
            self.janelaCadastro = None
            self.janelaRemoverUsuario = None
            self.janelaModuloTestes = None

        def _iniciar_sistema_principal(self):
            if self.janelaSistemaPrincipal is None or not self.janelaSistemaPrincipal.winfo_exists():
                self.janelaSistemaPrincipal = uiMainMenu.janelaSistemaPrincipal(self)
            else:
                self.janelaSistemaPrincipal.focus()

        def abrirJanela_cadastrar_usuario(self):
            if self.janelaCadastro is None or not self.janelaCadastro.winfo_exists():
                self.janelaCadastro = uiMainMenu.janelaCadastro(self)
            else:
                self.janelaCadastro.focus()

        def abrirJanela_removerUsuario(self):
            if self.janelaRemoverUsuario is None or not self.janelaRemoverUsuario.winfo_exists():
                self.janelaRemoverUsuario = uiMainMenu.janelaRemoverUsuario(self)
            else:
                self.janelaRemoverUsuario.focus()
        
        def _inicar_modulo_testes(self):
            if self.janelaModuloTestes is None or not self.janelaModuloTestes.winfo_exists():
                self.janelaModuloTestes = uiMainMenu.janelaModuloTestes(self)
            else:
                self.janelaModuloTestes.focus()

    # Criação da janela do Sistema Principal
    class janelaSistemaPrincipal(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("400x300")
            self.title("Main System")

            # Quadrado pra ficar bonito
            self.frame = customtkinter.CTkFrame(master=self)
            self.frame.pack(pady=20, padx=60, fill="both", expand=True)

            # Texto que apareçe no topo da tela
            self.label = customtkinter.CTkLabel(master=self.frame, text="Sistema Principal")
            self.label.pack(pady=12, padx=10)

            uiMainMenu._adicionar_botao(self, master=self.frame, text="Encerrar Sistema", command=self.encerrar_sistema)

        def encerrar_sistema(self):
            print("SISTEMA ENCERRADO")
            self.destroy()

    # Criação da janela de cadastro
    class janelaCadastro(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("400x300")
            self.title("Cadastro de usuário")

            # Quadrado pra ficar bonito
            self.frame = customtkinter.CTkFrame(master=self)
            self.frame.pack(pady=20, padx=60, fill="both", expand=True)

            # Texto que apareçe no topo da tela
            self.label = customtkinter.CTkLabel(master=self.frame, text="Cadastro de usuário")
            self.label.pack(pady=12, padx=10)

            # Informações do usuário para inserir
            # ID
            self.entrada_ID = customtkinter.CTkEntry(master=self.frame, placeholder_text="ID")
            self.entrada_ID.pack(pady = 12, padx=10)

            # Opções
            self.opcao_codificar_face = customtkinter.CTkCheckBox(master=self.frame, text="Codificar Face")
            self.opcao_codificar_face.pack(pady=12, padx=10)
            self.opcao_codificar_face.select()
            self.opcao_carregar_codificacao = customtkinter.CTkCheckBox(master=self.frame, text="Carregar codificação")
            self.opcao_carregar_codificacao.pack(pady=12, padx=10)
            self.opcao_carregar_codificacao.select()

            uiMainMenu._adicionar_botao(self, master=self.frame, text="Cadastrar!", command=self.cadastro)

        def cadastro(self):
            id = self.entrada_ID.get()
            if id:
                print(f'Usuário {id} cadastrado com sucesso!')
                self.destroy()
            else:
                print(f'ID INVÁLIDO')
            
    # Criação da janela de remover usuário
    class janelaRemoverUsuario(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("400x300")
            self.title("Remoção de usuário")

            # Quadrado pra ficar bonito
            self.frame = customtkinter.CTkFrame(master=self)
            self.frame.pack(pady=20, padx=60, fill="both", expand=True)

            # Texto que apareçe no topo da tela
            self.label = customtkinter.CTkLabel(master=self.frame, text="Remoção de usuário")
            self.label.pack(pady=12, padx=10)

            # Informações do usuário para inserir
            # ID
            self.entrada_ID = customtkinter.CTkEntry(master=self.frame, placeholder_text="ID Para Remover")
            self.entrada_ID.pack(pady = 12, padx=10)

            # Opções
            self.opcao_carregar_codificacao = customtkinter.CTkCheckBox(master=self.frame, text="Recarregar Usuários cadastrados")
            self.opcao_carregar_codificacao.pack(pady=12, padx=10)
            self.opcao_carregar_codificacao.select()

            uiMainMenu._adicionar_botao(self, master=self.frame, text="Remover!", command=self.remover_usuario)
        
        def remover_usuario(self):
            id = self.entrada_ID.get()
            if id:
                print(f'Usuário {id} removido com sucesso!')
                
                self.destroy()
            else:
                print(f'ID INVÁLIDO')


    # Criação da janela do Módulo de testes
    class janelaModuloTestes(customtkinter.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("800x600")
            self.title("Test Module")

            # Quadrado pra ficar bonito
            self.frame = customtkinter.CTkFrame(master=self)
            self.frame.pack(pady=20, padx=60, fill="both", expand=True)

            # Texto que apareçe no topo da tela
            self.label = customtkinter.CTkLabel(master=self.frame, text="Módulo de testes")
            self.label.pack(pady=12, padx=10)

            # Opções
            self.opcao_carregar_codificacao = customtkinter.CTkCheckBox(master=self.frame, text="360p")
            self.opcao_carregar_codificacao.pack(pady=12, padx=10)
            # Opções
            self.opcao_carregar_codificacao = customtkinter.CTkCheckBox(master=self.frame, text="480p")
            self.opcao_carregar_codificacao.pack(pady=12, padx=10)
            # Opções
            self.opcao_carregar_codificacao = customtkinter.CTkCheckBox(master=self.frame, text="720p")
            self.opcao_carregar_codificacao.pack(pady=12, padx=10)
            # Opções
            self.opcao_carregar_codificacao = customtkinter.CTkCheckBox(master=self.frame, text="1080p")
            self.opcao_carregar_codificacao.pack(pady=12, padx=10)

            uiMainMenu._adicionar_botao(self, master=self.frame, text="Encerrar Testes", command=self.encerrar_testes)

        def encerrar_testes(self):
            print("TESTES ENCERRADOS")
            self.destroy()

# PARA TESTAR O MENU
if __name__ == "__main__":
    mainMenu = uiMainMenu()
    mainMenu.start_ui_menu()