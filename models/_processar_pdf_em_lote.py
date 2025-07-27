from models._extrair_texto_do_pdf import extrair_texto_do_pdf
import concurrent.futures  # Para executar tarefas em paralelo com threads
# Função para procurar os arquivos PDF que contêm os chassis
def processar_pdf_em_lote(arquivos_pdf, chassis_data):
    resultados = []
    # Conjunto de chassis para facilitar a busca
    chassis_set = {d['CHASSI'] for d in chassis_data}

    # Função interna que verifica se um chassi está no texto de um PDF
    def verificar_pdf(caminho_pdf):
        texto = extrair_texto_do_pdf(caminho_pdf)
        chassi_encontrado = {c for c in chassis_set if c in texto} #set comprehension (compreensão de conjunto) Verifica se um chassi está no texto
        return caminho_pdf, chassi_encontrado

    # Executa a verificação em paralelo usando threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = [executor.submit(verificar_pdf, caminho_pdf) for caminho_pdf in arquivos_pdf]
        for futuro in concurrent.futures.as_completed(futuros):
            resultados.append(futuro.result())

    return resultados