"""Módulo para processamento em lote de arquivos PDF."""

import concurrent.futures

from models._extrair_texto_do_pdf import extrair_texto_do_pdf


def processar_pdf_em_lote(arquivos_pdf, chassis_data):
    """Procura os arquivos PDF que contêm os chassis.

    Args:
        arquivos_pdf: Lista de caminhos para arquivos PDF
        chassis_data: Lista de dicionários contendo informações de chassis

    Returns:
        Lista de tuplas (caminho_pdf, chassis_encontrados)
    """
    resultados = []
    # Conjunto de chassis para facilitar a busca
    chassis_set = {d["CHASSI"] for d in chassis_data}

    def verificar_pdf(caminho_pdf):
        """Verifica se um chassi está no texto de um PDF.

        Args:
            caminho_pdf: Caminho para o arquivo PDF

        Returns:
            Tupla (caminho_pdf, conjunto_de_chassis_encontrados)
        """
        texto = extrair_texto_do_pdf(caminho_pdf)
        chassi_encontrado = {c for c in chassis_set if c in texto}
        return caminho_pdf, chassi_encontrado

    # Executa a verificação em paralelo usando threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = [
            executor.submit(verificar_pdf, caminho_pdf) 
            for caminho_pdf in arquivos_pdf
        ]
        for futuro in concurrent.futures.as_completed(futuros):
            resultados.append(futuro.result())

    return resultados
