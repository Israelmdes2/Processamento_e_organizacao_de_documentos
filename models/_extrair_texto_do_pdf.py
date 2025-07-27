import fitz            # Biblioteca PyMuPDF para ler arquivos PDF
import os              # Para manipulação de arquivos e diretórios

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
                #print(pagina.get_text())
                texto_completo += pagina.get_text() + "\n"
                #print(texto_completo)
        # Armazena no cache
        cache_pdf_textos[caminho_pdf] = texto_completo
    except Exception as e:
        print(f"[Erro PDF] {os.path.basename(caminho_pdf)} - {e}")
    return texto_completo