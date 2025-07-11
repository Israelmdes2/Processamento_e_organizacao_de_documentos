import os
import requests
from dotenv import load_dotenv

def post_teams_message(params):
    load_dotenv()
    # Extrai o texto e o grupo dos parâmetros recebidos

    grupo = params.get('grupo')
    mensagem_erro = params.get('mensagem_erro')
    # Se o grupo for 'teste', usa o webhook de logs
    if grupo == 'teste':
        try:
            for erro in mensagem_erro:
                # Obtém o webhook de teste das variáveis de ambiente
                webhook = os.getenv('TEMAS_WEBHOOK_LOG')

                # Cria o corpo da mensagem com o texto recebido
                body = {
                    "content": erro
                }

                # Envia a requisição POST para o webhook do Teams
                requests.post(webhook, json=body)
                print(f'Mensagem enviada para o Teams!')

        except Exception as e:
            # Em caso de erro, exibe mensagem em vermelho no console
            print(f'\033[31mErro ao enviar mensagem para o Teams: {e}\033[m')


