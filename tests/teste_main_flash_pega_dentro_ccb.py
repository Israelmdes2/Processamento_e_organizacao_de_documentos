# Importa bibliotecas padrão e externas
import os              # Para manipulação de arquivos e diretórios
import re              # Para expressões regulares (não está sendo usada aqui)
import json            # Para salvar dados em formato JSON
import shutil          # Para mover arquivos entre pastas
import time            # Para medir tempo de execução
import fitz            # Biblioteca PyMuPDF para ler arquivos PDF
import concurrent.futures  # Para executar tarefas em paralelo com threads

from pymupdf.mupdf import pdf_array_insert

# Dicionário para armazenar textos já extraídos de PDFs (evita reprocessar o mesmo PDF)
cache_pdf_textos = {}

# Função para extrair texto de um arquivo PDF
def extrair_texto_do_pdf(caminho_pdf):
    # Se já tiver o texto no cache, retorna direto
    if caminho_pdf in cache_pdf_textos:
        return cache_pdf_textos[caminho_pdf]

    texto_completo = ""
    try:
        # Abre o PDF
        with fitz.open(caminho_pdf) as pdf:
            # Percorre todas as páginas
            for pagina in pdf:
                print(pagina.get_text())
                texto_completo += pagina.get_text() + "\n"
        # Armazena no cache
        cache_pdf_textos[caminho_pdf] = texto_completo
    except Exception as e:
        print(f"[Erro PDF] {os.path.basename(caminho_pdf)} - {e}")
    return texto_completo

# Função para extrair dados de um arquivo .txt
def extrair_dados_do_txt(caminho_txt):
    dados_extraidos = []
    numero_operacao_geral = None

    # Função auxiliar para cortar texto com base em posição
    def pegar(linha, ini, fim):
        return linha[ini - 1:fim].strip()

    # Abre o arquivo texto
    with open(caminho_txt, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            # Pula linhas vazias, de header ou trailer
            if not linha.strip() or "HEADER" in linha or "TRAILLER" in linha:
                continue
            try:
                # Extrai os campos fixos da linha
                dados_chassi = {
                    "CHASSI": pegar(linha, 41, 61),
                    "REMARCACAO": pegar(linha, 62, 62),
                    "UF_PLACA": pegar(linha, 65, 66),
                    "PLACA": pegar(linha, 67, 73),
                    "RENAVAM": pegar(linha, 74, 84),
                    "ANO_FABRICACAO": pegar(linha, 85, 88),
                    "ANO_MODELO": pegar(linha, 89, 92),
                    "NUMERO_OPERACAO": pegar(linha, 93, 112),
                    "DATA_OPERACAO": pegar(linha, 113, 120),
                    "TIPO_GRAVAME": pegar(linha, 121, 122),
                    "QUANTIDADE_MESES": pegar(linha, 177, 179),
                    "GRUPO_CONSORCIO": pegar(linha, 191, 196),
                    "COTA_CONSORCIO": pegar(linha, 197, 202),
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
                    "INDICATIVO_PENALIDADE": pegar(linha, 398, 400),
                    "PENALIDADE": pegar(linha, 401, 450),
                    "INDICATIVO_COMISSAO": pegar(linha, 451, 453),
                    "COMISSAO": pegar(linha, 454, 462),
                    "CPF_CNPJ_RECEBEDOR": pegar(linha, 680, 693),
                    "CPF_CNPJ_DEVEDOR": "",  # Não informado no layout atual
                    "NOME_DEVEDOR": "",      # Não informado no layout atual
                }

                # Se o chassi for válido (17 caracteres), adiciona aos dados
                if dados_chassi["CHASSI"] and len(dados_chassi["CHASSI"]) == 17:
                    dados_extraidos.append(dados_chassi)
                    # Salva número de operação se ainda não estiver salvo
                    if not numero_operacao_geral:
                        numero_operacao_geral = dados_chassi["NUMERO_OPERACAO"]
            except IndexError:
                continue  # Pula linhas inválidas

    return dados_extraidos, numero_operacao_geral

# Função para procurar os arquivos PDF que contêm os chassis
def processar_pdf_em_lote(arquivos_pdf, chassis_data):
    resultados = []
    # Conjunto de chassis para facilitar a busca
    chassis_set = {d['CHASSI'] for d in chassis_data}

    # Função interna que verifica se um chassi está no texto de um PDF
    def verificar_pdf(caminho_pdf):
        texto = extrair_texto_do_pdf(caminho_pdf)
        chassi_encontrado = {c for c in chassis_set if c in texto} #set comprehension (compreensão de conjunto)
        return caminho_pdf, chassi_encontrado

    # Executa a verificação em paralelo usando threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = [executor.submit(verificar_pdf, caminho_pdf) for caminho_pdf in arquivos_pdf]
        for futuro in concurrent.futures.as_completed(futuros):
            resultados.append(futuro.result())

    return resultados

# Função principal para organizar os arquivos
def organizar_arquivos(diretorio_base):
    print(f"Iniciando organização do diretório: {diretorio_base}\n")
    try:
        # Lista todos os arquivos no diretório
        todos_os_arquivos = [os.path.join(diretorio_base, f) for f in os.listdir(diretorio_base)
                             if os.path.isfile(os.path.join(diretorio_base, f))]
    except FileNotFoundError:
        print(f"ERRO: O diretório '{diretorio_base}' não foi encontrado.")
        return

    # Separa arquivos por extensão
    arquivos_txt = [f for f in todos_os_arquivos if f.lower().endswith('.txt')]
    arquivos_pdf = [f for f in todos_os_arquivos if f.lower().endswith('.pdf')]

    # Processa cada arquivo .txt
    for caminho_txt in arquivos_txt:
        nome_txt = os.path.basename(caminho_txt)
        print(f"\n--- Processando o .txt: {nome_txt} ---")
        print(f'Pesquisando CHASSI e NÚMERO da operação no .txt...')
        dados_chassis, op_num = extrair_dados_do_txt(caminho_txt)

        if not op_num:
            print(f"Sem número da operação. Pulando o .txt: {nome_txt}")
            continue
        print(f"✅Número da operação encontrado: {op_num}")


        arquivos_para_mover = {caminho_txt}
        via_negociavel_encontrada = False

        print(f'Vai encontrar a Via Negociável...')
        # Busca PDF cujo nome contenha o número da operação
        via_encontrada = False
        for pdf_path in arquivos_pdf:
            if op_num in os.path.basename(pdf_path).replace(" ", ""):
                arquivos_para_mover.add(pdf_path)
                via_negociavel_encontrada = True
                print(f"  -> ✅Via Negociável encontrada: {os.path.basename(pdf_path)}")
                via_encontrada = True
                break
        if not via_encontrada:
            print(f"Via Negociável não encontrada pelo número da operação {op_num}. 😱.")

        # Procura os chassis dentro dos PDFs
        resultados_pdf = processar_pdf_em_lote(arquivos_pdf, dados_chassis)

        chassis_encontrados = set()
        #Verifica se o chassi foi encontrado e em qual arquivo .pdf
        for caminho_pdf, chassis in resultados_pdf:
            if chassis:
                arquivos_para_mover.add(caminho_pdf)
                chassis_encontrados.update(chassis)
                print(f"  -> Chassis {list(chassis)} em {os.path.basename(caminho_pdf)}")

        # Verifica quais chassis esperados não foram encontrados
        chassis_esperados = {d['CHASSI'] for d in dados_chassis}
        faltando = chassis_esperados - chassis_encontrados
        if faltando:
            print(f"  ! Chassis do .txt não encontrados nos .pdf: {faltando}")

        # Se tiver mais de um arquivo relacionado, move para uma nova pasta
        if len(arquivos_para_mover) > 1:
            nome_devedor = dados_chassis[0]["NOME_DEVEDOR"].replace(" ", "_").replace("/", "")
            nova_pasta = f"{op_num}_{nome_devedor}"
            destino = os.path.join(diretorio_base, nova_pasta)
            os.makedirs(destino, exist_ok=True)

            for arq in arquivos_para_mover:
                try:
                    shutil.move(arq, os.path.join(destino, os.path.basename(arq)))
                except Exception as e:
                    print(f"[Erro ao mover] {arq}: {e}")

            # Salva os dados extraídos em JSON
            with open(os.path.join(destino, f"{op_num}_dados_extraidos.json"), 'w', encoding='utf-8') as f:
                json.dump(dados_chassis, f, indent=4, ensure_ascii=False)
            print(f"  -> Arquivos organizados em: {nova_pasta}")
        else:
            print("  -> Nenhum arquivo adicional encontrado.")

        print(f"--- Fim de: {nome_txt} ---")

# Execução principal do script
if __name__ == "__main__":
    start = time.time()  # Marca o início da execução
    home = os.path.expanduser('~')  # Obtém o diretório do usuário
    pasta_nf = os.path.join(home, 'Downloads', 'NF_FLASH')  # Caminho da pasta onde estão os arquivos

    # Verifica se o diretório existe
    if os.path.isdir(pasta_nf):
        organizar_arquivos(pasta_nf)
    else:
        print(f"Diretório não encontrado: {pasta_nf}")

    fim = time.time()  # Marca o fim da execução
    duracao = fim - start  # Calcula duração
    print(f"\n\033[32mConcluído em {duracao:.2f} segundos.\033[m")  # Exibe tempo final formatado em verde
