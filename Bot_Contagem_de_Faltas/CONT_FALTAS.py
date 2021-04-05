import requests
import json
import os
import pandas as pd

class TelegramBot:
    def __init__(self):
        token = '<token>'
        self.token = token
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    chat_id = dado["message"]["from"]["id"]
                    try:
                        file_id = dado["message"]["document"]["file_id"]
                        if file_id:
                            self.download_file(file_id)
                            df1 = pd.read_csv('file_0.csv')
                            df2 = pd.read_csv('todos.csv')
                            presentes = list(df1['Full Name'])
                            todos = list(df2['Full Name'])
                            nomes = 'Lista de nomes:\n'
                            for item in [x for x in todos if x not in presentes]:
                                nomes = nomes + item + '\n'
                            print(nomes)
                            self.responder(nomes, chat_id)
                    except:
                        pass
                    try:
                        mensagem = str(dado["message"]["text"])
                    except:
                        break
                    
###################################### DEFINED FUNCTION SECTION ########################################                  

    def download_file(self, file_id):
        file_path = json.loads(requests.post(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}').text)['result']['file_path']
        file = requests.get(f'https://api.telegram.org/file/bot{self.token}/{file_path}').content
        open(f'file_0.csv', 'wb').write(file)

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)

bot = TelegramBot()
bot.Iniciar()
