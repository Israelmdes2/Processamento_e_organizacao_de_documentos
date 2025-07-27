# models/_validar_texto.py

"""Módulo para validação de texto extraído de PDFs."""

import re

# Lista de palavras comuns em português. Quanto mais palavras, mais preciso,
# mas uma lista pequena já é suficiente para detectar texto completamente codificado.
PALAVRAS_COMUNS_PT = {
    "de",
    "a",
    "o",
    "que",
    "e",
    "do",
    "da",
    "em",
    "um",
    "para",
    "é",
    "com",
    "não",
    "uma",
    "os",
    "no",
    "se",
    "na",
    "por",
    "mais",
    "as",
    "dos",
    "como",
    "mas",
    "foi",
    "ao",
    "ele",
    "das",
    "tem",
    "à",
    "seu",
    "sua",
    "ou",
    "ser",
    "quando",
    "muito",
    "há",
    "nos",
    "já",
    "está",
    "eu",
    "também",
    "só",
    "pelo",
    "pela",
    "até",
    "isso",
    "ela",
    "entre",
    "era",
    "depois",
    "sem",
    "mesmo",
    "aos",
    "ter",
    "seus",
    "quem",
    "nas",
    "me",
    "esse",
    "eles",
    "estão",
    "você",
    "tinha",
    "foram",
    "essa",
    "num",
    "nem",
    "suas",
    "meu",
    "às",
    "minha",
    "têm",
    "numa",
    "pelos",
    "elas",
    "havia",
    "seja",
    "qual",
    "será",
    "nós",
    "tenho",
    "lhe",
    "deles",
    "essas",
    "esses",
    "pelas",
    "este",
    "fosse",
    "dele",
    "tu",
    "te",
    "vocês",
    "vos",
    "lhes",
    "meus",
    "minhas",
    "teu",
    "tua",
    "teus",
    "tuas",
    "nosso",
    "nossa",
    "nossos",
    "nossas",
    "dela",
    "delas",
    "esta",
    "estes",
    "estas",
    "aquele",
    "aquela",
    "aqueles",
    "aquelas",
    "isto",
    "aquilo",
    "chassi",
    "nota",
    "fiscal",
    "valor",
    "data",
    "produto",
    "serviços",
    "cliente",
    "endereço",
    "código",
    "município",
    "total",
}


def is_texto_codificado(texto: str, threshold_percent=10) -> bool:
    """
    Verifica se um texto extraído de um PDF parece codificado ou ilegível.

    Args:
        texto: O texto extraído do PDF.
        threshold_percent: O percentual mínimo de palavras reconhecíveis para
                           considerar o texto válido.

    Returns:
        True se o texto parece codificado, False caso contrário.
    """
    # Verifica a presença do caractere de substituição Unicode (forte indício de erro)
    if "\ufffd" in texto:
        return True

    # Limpa o texto, mantendo apenas letras e espaços, e converte para minúsculas
    texto_limpo = re.sub(r"[^a-zA-Z\s]", "", texto).lower()

    # Divide o texto em palavras
    palavras = texto_limpo.split()

    if not palavras:
        return True  # Se não há palavras, o texto é inválido

    palavras_reconhecidas = 0
    for palavra in palavras:
        if palavra in PALAVRAS_COMUNS_PT:
            palavras_reconhecidas += 1

    # Calcula o percentual de palavras que são conhecidas
    percentual_reconhecido = (palavras_reconhecidas / len(palavras)) * 100

    # print(f"  -> Análise de texto: {percentual_reconhecido:.2f}% de palavras reconhecidas.")

    # Se o percentual for menor que o limite, considera o texto como codificado
    return percentual_reconhecido < threshold_percent
