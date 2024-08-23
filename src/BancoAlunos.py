from datetime import datetime
import pandas as pd

class BancoAlunos:
    def __init__(self, path:str, nome_planilha:str, obj_fireBaseManager): #TODO
        # dataframe de um excel
        # id | nome
        self.path = path
        self.nome_planilha = nome_planilha
        self.obj_fireBaseManager = obj_fireBaseManager

        # Aqui o banco de dados iria carregar os dados dos alunos
        #TODO
        """
        BAIXAR AQUI OS DADOS DOS ALUNOS
        MATRICULA : {NOME: "", TURMA: "", ANO: ""}
        """
        self.dados_alunos = self.obj_fireBaseManager.get_data()

    def aluno_reconhecido(self, _id:str):
        if _id not in self.dados_alunos:
            return None
        
        # Pega nome do aluno nos dados json
        nome_aluno = str(self.dados_alunos[_id][0])
        turma_aluno = str(self.dados_alunos[_id][1])
        
        date_data = datetime.now() # Pega o horário atual
        horario_atual = date_data.strftime('%H:%M:%S')
        data_atual = str(date_data.date())

        dados = {
            "data" : [[
                nome_aluno,
                turma_aluno,
                horario_atual,
                data_atual,
                _id
            ]],

            "columns" : [
                'Aluno',
                'Turma',
                'Horário',
                'Data',
                'ID'
            ]
        }

        self._adicionar_dado_planilha(dados, self.nome_planilha)
        self.obj_fireBaseManager.send_notification(_id)

    def _adicionar_dado_planilha(self, dados:dict, nome_planilha:str):
        #Adicionar dados na planilha
        nome_planilha += '.xlsx'
        data = dados['data']
        columns = dados['columns']

        try:
            df = pd.read_excel(nome_planilha)
        except:
            df = pd.DataFrame(columns=columns)
        new_data = pd.DataFrame(data, columns=columns)
        df = pd.concat([df, new_data], ignore_index=True)

        df.to_excel(nome_planilha, index=False)
        #print(df)

if __name__ == '__main__':
    planilha = 'alunos_registro'
    banco = BancoAlunos('./', planilha)
    banco.aluno_reconhecido('IDEduardo')
