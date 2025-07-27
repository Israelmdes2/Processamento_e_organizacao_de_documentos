"""Módulo para envio de mensagens de erro para o Microsoft Teams."""

import os
import requests
from dotenv import load_dotenv


def post_teams_message(params):
    """Publica mensagens de erro no canal do Teams.

    Args:
        params: Dicionário contendo grupo e mensagens de erro
    """
    load_dotenv()
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")

    grupo = params.get("grupo")
    mensagem_erro = params.get("mensagem_erro")

    if grupo == "teste":
        try:
            for erro in mensagem_erro:
                body = {"content": erro}
                requests.post(webhook_url, json=body)
                print("Mensagem enviada para o Teams!")

        except Exception as e:
            print(f"\033[31mErro ao enviar mensagem para o Teams: {e}\033[m")
