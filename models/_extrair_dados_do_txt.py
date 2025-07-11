
# Função para extrair dados de um arquivo .txt
def extrair_dados_do_txt(caminho_txt):
    dados_extraidos = []
    numero_operacao_geral = None

    # Função auxiliar para cortar texto com base em posição
    def pegar(linha, ini, fim):
        return linha[ini - 1:fim].strip()

    # Abre o arquivo texto
    with open(caminho_txt, 'r', encoding='utf-8', errors='ignore') as f: #Abre o arquivo para leitura em UTF-8, ignorando erros. O UTF-8 eh usado para lidar com caracteres especiais
        for linha in f:
            # Pula linhas vazias, de header ou trailer
            if not linha.strip() or "HEADER" in linha or "TRAILLER" in linha:
                continue
            try:
                # Extrai os campos fixos da linha
                dados_chassi = {
                    "CHASSI": pegar(linha, 41, 61), #SIM
                    "REMARCACAO": pegar(linha, 62, 62), #SIM
                    "ANO_FABRICACAO": pegar(linha, 85, 88),#SIM
                    "ANO_MODELO": pegar(linha, 89, 92),#SIM
                    "NUMERO_OPERACAO": pegar(linha, 93, 112),#SIM
                    "DATA_OPERACAO": pegar(linha, 113, 120),#SIM
                    "TIPO_GRAVAME": pegar(linha, 121, 122),#SIM
                    "QUANTIDADE_MESES": pegar(linha, 177, 179),#SIM
                    "TAXA_JUROS_MES": pegar(linha, 203, 208),#SIM
                    "TAXA_JUROS_ANO": pegar(linha, 209, 214),#SIM
                    "VALOR_TAXA_CONTRATO": pegar(linha, 215, 223),#SIM
                    "VALOR_IOF": pegar(linha, 224, 232),#SIM
                    "INDICATIVO_MULTA": pegar(linha, 233, 235),#SIM
                    "INDICATIVO_MORA": pegar(linha, 236, 238),#SIM
                    "VALOR_PRINCIPAL_OPERACAO": pegar(linha, 239, 247),#SIM
                    "VALOR_PARCELA": pegar(linha, 248, 256),#SIM
                    "VENCIMENTO_PRIMEIRA_PARCELA": pegar(linha, 257, 264),#SIM
                    "VENCIMENTO_ULTIMA_PARCELA": pegar(linha, 265, 272),#SIM
                    "CIDADE_LIBERACAO_OPERACAO": pegar(linha, 273, 297),#SIM
                    "UF_LIBERACAO_OPERACAO": pegar(linha, 298, 299),#SIM
                    "DATA_LIBERACAO_OPERACAO": pegar(linha, 300, 307),#SIM
                    "INDICES_UTILIZADOS": pegar(linha, 308, 317),#SIM
                    "MULTA": pegar(linha, 383, 388),#SIM
                    "JUROS_MORA": pegar(linha, 389, 397),#SIM
                    "CPF_CNPJ_RECEBEDOR": pegar(linha, 680, 693),#SIM

                }
                # Se o chassi for válido (17 caracteres), adiciona aos dados
                if dados_chassi["CHASSI"] and len(dados_chassi["CHASSI"]) == 17 or len(dados_chassi["CHASSI"]) == 8 or len(dados_chassi["CHASSI"]) == 21:
                    dados_extraidos.append(dados_chassi)
                    # Salva número de operação se ainda não estiver salvo
                    if not numero_operacao_geral:
                        numero_operacao_geral = dados_chassi["NUMERO_OPERACAO"]
            except IndexError:
                continue  # Pula linhas inválidas

    return dados_extraidos, numero_operacao_geral