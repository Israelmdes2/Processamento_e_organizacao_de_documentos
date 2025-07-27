import os              # Para manipulação de arquivos e diretórios
import time            # Para medir tempo de execução
#from models._organizar_arquivos import organizar_arquivos
from core.index import organizar_arquivos
from utils.postTeams import post_teams_message


# Execução principal do script
if __name__ == "__main__":
    start = time.time()  # Marca o início da execução
    home = os.path.expanduser('~')  # Obtém o diretório do usuário
    pasta_nf = os.path.join(home, 'Downloads', 'NF_FLASH')  # Caminho da pasta onde estão os arquivos

    mensagem_erro = [] #lista para armazenar as mensagens de erro
    # Verifica se o diretório existe
    if os.path.isdir(pasta_nf):
        mensagem_erro = organizar_arquivos(pasta_nf, mensagem_erro)
    else:
        print(f"Diretório não encontrado: {pasta_nf}")

    fim = time.time()  # Marca o fim da execução
    duracao = fim - start  # Calcula duração
    print(f"\n\033[32mProcessamento de todos os arquivos concluído em {duracao:.2f} segundos.\033[m")  # Exibe tempo final formatado em verde
    print(f'\nVai enviar mensagens dos erros')

    if mensagem_erro:
        params = {
            'mensagem_erro':mensagem_erro,
            'grupo': 'teste',
        }
        post_teams_message(params)