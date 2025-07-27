"""Módulo principal para processamento e organização de documentos."""

import os
import time

from core.index import organizar_arquivos
from utils.postTeams import post_teams_message


if __name__ == "__main__":
    start = time.time()
    home = os.path.expanduser("~")
    pasta_nf = os.path.join(home, "Downloads", "NF_FLASH")

    mensagem_erro = []
    if os.path.isdir(pasta_nf):
        mensagem_erro = organizar_arquivos(pasta_nf, mensagem_erro)
    else:
        print(f"Diretório não encontrado: {pasta_nf}")

    fim = time.time()
    duracao = fim - start
    print(
        f"\n\033[32mProcessamento de todos os arquivos concluído em "
        f"{duracao:.2f} segundos.\033[m"
    )
    print("\nVai enviar mensagens dos erros")

    if mensagem_erro:
        params = {
            "mensagem_erro": mensagem_erro,
            "grupo": "teste",
        }
        post_teams_message(params)
