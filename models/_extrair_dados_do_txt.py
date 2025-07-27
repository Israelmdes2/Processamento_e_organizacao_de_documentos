"""Módulo para extrair dados de arquivos TXT."""


def extrair_dados_do_txt(caminho_txt):
    """Extrai dados de um arquivo .txt.

    Args:
        caminho_txt: Caminho para o arquivo TXT

    Returns:
        Tupla contendo lista de dados extraídos e número de operação geral
    """
    dados_extraidos = []
    numero_operacao_geral = None

    def pegar(linha, ini, fim):
        """Corta texto com base em posição.

        Args:
            linha: Linha de texto a ser processada
            ini: Posição inicial (1-indexed)
            fim: Posição final (inclusive)

        Returns:
            String com o trecho extraído
        """
        return linha[ini - 1: fim].strip()

    with open(caminho_txt, "r", encoding="utf-8", errors="ignore") as f:
        for linha in f:
            # Pula linhas vazias, de header ou trailer
            if not linha.strip() or "HEADER" in linha or "TRAILLER" in linha:
                continue
            try:
                # Extrai os campos fixos da linha
                dados_chassi = {
                    "CHASSI": pegar(linha, 41, 61),
                    "REMARCACAO": pegar(linha, 62, 62),
                    "ANO_FABRICACAO": pegar(linha, 85, 88),
                    "ANO_MODELO": pegar(linha, 89, 92),
                    "NUMERO_OPERACAO": pegar(linha, 93, 112),
                    "DATA_OPERACAO": pegar(linha, 113, 120),
                    "TIPO_GRAVAME": pegar(linha, 121, 122),
                    "QUANTIDADE_MESES": pegar(linha, 177, 179),
                    "TAXA_JUROS_MES": pegar(linha, 203, 208),
                    "TAXA_JUROS_ANO": pegar(linha, 209, 214),
                    "VALOR_TAXA_CONTRATO": pegar(linha, 215, 223),
                    "VALOR_IOF": pegar(linha, 224, 232),
                    "INDICATIVO_MULTA": pegar(linha, 233, 235),
                    "INDICATIVO_MORA": pegar(linha, 236, 238),
                    "VALOR_PRINCIPAL_OPERACAO": pegar(linha, 239, 247),
                    "VALOR_PARCELA": pegar(linha, 248, 256),
                    "VENCIMENTO_PRIMEIRA_PARCELA": pegar(linha, 257, 264),
                    "VENCIMENTO_ULTIMA_PARCELA": pegar(linha, 265, 272),
                    "CIDADE_LIBERACAO_OPERACAO": pegar(linha, 273, 297),
                    "UF_LIBERACAO_OPERACAO": pegar(linha, 298, 299),
                    "DATA_LIBERACAO_OPERACAO": pegar(linha, 300, 307),
                    "INDICES_UTILIZADOS": pegar(linha, 308, 317),
                    "MULTA": pegar(linha, 383, 388),
                    "JUROS_MORA": pegar(linha, 389, 397),
                    "CPF_CNPJ_RECEBEDOR": pegar(linha, 680, 693),
                }
                # Se o chassi for válido (17, 8 ou 21 caracteres), adiciona aos dados
                if (dados_chassi["CHASSI"] and
                        (len(dados_chassi["CHASSI"]) == 17 or
                         len(dados_chassi["CHASSI"]) == 8 or
                         len(dados_chassi["CHASSI"]) == 21)):
                    dados_extraidos.append(dados_chassi)
                    # Salva número de operação se ainda não estiver salvo
                    if not numero_operacao_geral:
                        numero_operacao_geral = dados_chassi["NUMERO_OPERACAO"]
            except IndexError:
                continue  # Pula linhas inválidas

    return dados_extraidos, numero_operacao_geral
