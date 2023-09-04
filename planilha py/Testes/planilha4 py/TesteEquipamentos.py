import pandas as pd

Algoritimo_usado = input("Você está utilizando HOG ou CNN: ")
Algoritimo_usado = Algoritimo_usado.upper()
while True:
    Iluminacao = input("A iluminação utilizada é: ")
    Iluminacao = Iluminacao.upper()
    if(Iluminacao == "ALTA" or Iluminacao == "MEDIA" or Iluminacao == "BAIXA" or Iluminacao == "ILUMINACAO ARTIFICIAL"):
        break
while True:
    Equipamento = input("Qual a qualidade da Camera utilizada: ")
    Equipamento = Equipamento.lower()
    if(Equipamento == "360p" or Equipamento == "480p" or Equipamento == "720p" or Equipamento == "1080p"):
        break
while True:
    Distancia = input("Em que Distancia vc estará da Camera: ")
    Distancia = Distancia.lower()
    if(Distancia == "30cm" or Distancia == "1m" or Distancia == "2m" or Distancia == "3m"):
        break
class Equipamentos:
    def __init__(self, Algoritimo_usado, Iluminacao, Equipamento_Utilizado, Distancia, Rostos_Utilizados, Rostos_Corretos, Rostos_Incorretos, taxa_acerto, Tempo):
        self.algoritimo = Algoritimo_usado
        self.iluminacao = Iluminacao
        self.qualidade = Equipamento_Utilizado
        self.distancia = Distancia
        self.fmUtilizados = Rostos_Utilizados
        self.fmCorretos = Rostos_Corretos
        self.fmIncorretos = Rostos_Incorretos
        self.taxa_acertos = taxa_acerto
        self.tempo = Tempo
        self.planilha_teste = None

    def calcular_e_imprimir(self):
        self.planilha_teste = input("Digite o nome da página: ")
        
        data = [[self.algoritimo, self.iluminacao, self.qualidade, self.distancia, self.fmUtilizados, self.fmCorretos, self.fmIncorretos, self.taxa_acertos, self.tempo]]
        
        try:
            self.df = pd.read_excel('Testes.xlsx')
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['Algoritimo', 'Iluminação', 'Qualidade', 'Distancia', 'Rostos_Utilizados', 'Rostos_Corretos', 'Rostos_Incorretos', 'Taxa De Acerto', 'Tempo'])

        new_data = pd.DataFrame(data, columns=['Algoritimo', 'Iluminação', 'Qualidade', 'Distancia', 'Rostos_Utilizados', 'Rostos_Corretos', 'Rostos_Incorretos', 'Taxa De Acerto', 'Tempo'])
        self.df = pd.concat([self.df, new_data], ignore_index=True)

        self.df.to_excel('Testes.xlsx', index=False)
    
        print(self.df)
        print(f'salfo em: Testes.xlsx')

equipamentos = Equipamentos(Algoritimo_usado, Iluminacao, Equipamento, Distancia, '0', '0', '0', '0', '0')
equipamentos.calcular_e_imprimir()
 