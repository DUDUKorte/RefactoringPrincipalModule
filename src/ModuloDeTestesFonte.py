import pandas as pd

class ModuloDeTestesFonte:
    def __init__(
            self,
            rostos_utilizados=0,
            rostos_corretos=0,
            rostos_incorretos=0,
            taxa_de_acerto=0,
            tempo_medio=0,
            rostos_analisados = 0
    ):
        self.rostos_utilizados = rostos_utilizados
        self.rostos_analisados = rostos_analisados
        self.rostos_corretos = rostos_corretos
        self.rostos_incorretos = rostos_incorretos
        self.taxa_de_acerto = taxa_de_acerto
        self.tempo_medio = tempo_medio
        self.paremtros_obtidos = False

    def getParametrosDeTeste(self):
        #Perguntar sobre o algoritmo, entre HOG e CNN
        opcoes_de_algoritmo = ['hog', 'cnn']
        self.algoritmo_de_localizacao = self._getParametro('Algoritmo', opcoes_de_algoritmo)
        #Perguntar sobre a iluminação
        opcoes_de_iluminacao = ["alta", "media", "baixa", "artificial"]
        self.iluminacao = self._getParametro('Iluminação', opcoes_de_iluminacao)
        #Perguntar sobre a qualidade
        opcoes_de_qualidade = ['360p', '480p', '720p', '1080p']
        self.qualidade_de_imagem = self._getParametro('Qualidade de imagem', opcoes_de_qualidade)
        #Perguntar sobre a distância
        opcoes_de_distancia = ['30cm', '1m', '2m', '3m']
        self.distancia = self._getParametro('Distância', opcoes_de_distancia)
        #Perguntar nome do usuário
        print(f'{"-"*35}\nDigite o nome do usuário esperado: ', end='')
        self.nome_esperado = input("\n--> ")
        self.paremtros_obtidos = True

    def _getParametro(self, nome_parametro: str, lista_opcoes: list):
        # Função para pegar cada parâmetro dos testes
        opcoes = set(lista_opcoes) # Transforma a lista em set para não ter opções repetidas
        parametro = '' # Inicializa o parâmetro para ele comparar no início do while
        while parametro.lower() not in opcoes: # Enquanto o parâmetro atual não estiver no set
            print(f'{"-"*35}\nSelecione um modo de {nome_parametro}: \n(', end='')
            for i in opcoes: print(i, end=' ')
            print(')')
            parametro = input('\n--> ') # Recebe o parâmertro digitado
        return parametro # Retorna o parâmetro que for digitado e estiver nas opções do set

    def gerarPlanilha(self, nome_planilha: str):
        nome_planilha += '.xlsx'
        data = [[
            self.algoritmo_de_localizacao,
            self.iluminacao,
            self.qualidade_de_imagem,
            self.distancia,
            self.rostos_utilizados,
            self.rostos_corretos,
            self.rostos_incorretos,
            self.rostos_analisados,
            self.taxa_de_acerto,
            self.tempo_medio
        ]]

        columns=['Algoritmo', 
                'Iluminação',
                'Qualidade',
                'Distância',
                'Rostos Utilizados',
                'Rostos Corretos',
                'Rostos Incorretos',
                'Rostos Analisados',
                'Taxa de Acerto',
                'Tempo Médio'
                ]

        try:
            df = pd.read_excel(nome_planilha)
        except FileNotFoundError:
            df = pd.DataFrame(columns=columns)
        new_data = pd.DataFrame(data, columns=columns)
        df = pd.concat([df, new_data], ignore_index=True)

        df.to_excel(nome_planilha, index=False)
        print(df)
        print(f'Planilha salva com sucesso como: "{nome_planilha}"')