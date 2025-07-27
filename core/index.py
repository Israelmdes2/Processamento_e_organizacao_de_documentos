"""Módulo para organizar arquivos PDF e TXT."""

import json
import os
import re
import shutil
import unicodedata

from models._extrair_dados_do_txt import extrair_dados_do_txt
from models._extrair_texto_do_pdf import extrair_texto_do_pdf
from models._processar_pdf_em_lote import processar_pdf_em_lote
from models._validar_texto import is_texto_codificado


def organizar_arquivos(diretorio_base, mensagem_erro):
    """
    Organiza arquivos PDF e TXT em um diretório.

    Args:
        diretorio_base: Caminho do diretório a ser processado
        mensagem_erro: Lista para armazenar mensagens de erro

    Returns:
        Lista de mensagens de erro ocorridas durante o processamento
    """
    print(f"Iniciando organização do diretório: {diretorio_base}\n")

    os.makedirs(os.path.join(diretorio_base, "_Lixo"), exist_ok=True)
    pasta_lixo = os.path.join(diretorio_base, "_Lixo")

    try:
        todos_os_arquivos = [
            os.path.join(diretorio_base, f)
            for f in os.listdir(diretorio_base)
            if os.path.isfile(os.path.join(diretorio_base, f))
        ]
    except FileNotFoundError:
        print(f"ERRO: O diretório '{diretorio_base}' não foi encontrado.")
        return

    arquivos_txt = [f for f in todos_os_arquivos if f.lower().endswith(".txt")]
    arquivos_pdf = [f for f in todos_os_arquivos if f.lower().endswith(".pdf")]
    arquivos_para_remover = [
        f for f in todos_os_arquivos
        if not (f.lower().endswith(".txt") or f.lower().endswith(".pdf"))
    ]

    for arquivo in arquivos_para_remover:
        print(
            f"⚠️Arquivo não será processado com extensão incompatível: "
            f"{os.path.basename(arquivo)}"
        )
        mensagem_erro.append(
            f"Arquivo não será processado com extensão incompatível: "
            f"<b>{os.path.basename(arquivo)}</b>"
        )
        os.remove(arquivo)
        print(f"❗Arquivo removido com sucesso: {os.path.basename(arquivo)}\n")

    if not arquivos_txt:
        print("⚠️Nenhum arquivo .txt encontrado no diretório.⚠️")
        return None

    print(f"Quantidade de arquivos .txt encontrados: {len(arquivos_txt)}")

    for caminho_txt in arquivos_txt:
        nome_txt = os.path.basename(caminho_txt)
        print(f"\n--- Processando o .txt: {nome_txt} ---")
        print("Pesquisando CHASSI e NÚMERO da operação no .txt...")
        dados_chassis, op_num = extrair_dados_do_txt(caminho_txt)

        qtd_chassi = len({d["CHASSI"] for d in dados_chassis})
        print(f"Quantidade de chassis esperados: {qtd_chassi}")

        if _validar_dados_txt(
            dados_chassis, nome_txt, caminho_txt, pasta_lixo, mensagem_erro
        ):
            continue

        print(f"  -> ✅Número da operação e chassi(s) encontrado no .txt: {nome_txt}")
        arquivos_para_mover = {caminho_txt}

        if _processar_via_negociavel(
            arquivos_pdf, op_num, arquivos_para_mover,
            nome_txt, caminho_txt, pasta_lixo, mensagem_erro
        ):
            continue

        arquivos_pdf_restantes_nf = [
            pdf for pdf in arquivos_pdf
            if not re.search(
                r"via[-_]*negociavel",
                remover_acentos(os.path.basename(pdf)).lower().replace(" ", "")
            )
        ]

        resultados_pdf = processar_pdf_em_lote(
            arquivos_pdf_restantes_nf, dados_chassis
        )

        if _processar_resultados_pdf(
            resultados_pdf, arquivos_para_mover, arquivos_pdf,
            nome_txt, caminho_txt, pasta_lixo, mensagem_erro
        ):
            continue

        chassis_esperados = {d["CHASSI"] for d in dados_chassis}
        chassis_encontrados = {
            chassi for _, chassis in resultados_pdf for chassi in chassis
        }

        faltando = chassis_esperados - chassis_encontrados
        if faltando:
            print(
                f"  ⚠️Chassis {faltando} do .txt {nome_txt} não encontrados "
                f"nos .pdf🤦‍♀️*****NOTIFICAR IC*****"
            )
            mensagem_erro.append(
                f"Chassis {faltando} do .txt {nome_txt} não encontrados nos .pdf. "
                f"O .txt foi movido: <b>{nome_txt}</b>."
            )
            print('Movendo o .txt para a pasta "Lixo"')
            shutil.move(caminho_txt, pasta_lixo)
            print(f"❗Txt sem os chassis movido para a pasta Lixo: {nome_txt}")
            continue

        if len(arquivos_para_mover) > 1:
            nova_pasta = f"{op_num}"
            destino = os.path.join(diretorio_base, nova_pasta)
            os.makedirs(destino, exist_ok=True)

            for arq in arquivos_para_mover:
                try:
                    shutil.move(
                        arq, os.path.join(destino, os.path.basename(arq))
                    )
                except Exception as e:
                    print(f"[Erro ao mover] {arq}: {e}")

            print("Vai salvar os dados extraídos do .txt em JSON...")
            with open(
                os.path.join(destino, f"{op_num}_dados_extraidos.json"),
                "w", encoding="utf-8"
            ) as f:
                json.dump(dados_chassis, f, indent=4, ensure_ascii=False)
            print(f"  -> ✅Dados extraídos do .txt salvos no JSON: {nova_pasta}")
        else:
            print("  -> ❗Nenhum arquivo adicional encontrado.")

        print(f"--- Fim do processamento do .txt: {nome_txt} ---")

    return mensagem_erro


def remover_acentos(texto):
    """Remove acentos de um texto.

    Args:
        texto: Texto a ser processado

    Returns:
        Texto sem acentos
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def _validar_dados_txt(dados_chassis, nome_txt, caminho_txt, pasta_lixo,
                       mensagem_erro):
    """Valida os dados extraídos do arquivo TXT.

    Args:
        dados_chassis: Lista de dicionários com dados dos chassis
        nome_txt: Nome do arquivo TXT
        caminho_txt: Caminho completo do arquivo TXT
        pasta_lixo: Caminho da pasta para arquivos rejeitados
        mensagem_erro: Lista para armazenar mensagens de erro

    Returns:
        True se houve erro na validação, False caso contrário
    """
    campos = [
        "CHASSI", "REMARCACAO", "ANO_FABRICACAO", "ANO_MODELO",
        "NUMERO_OPERACAO", "DATA_OPERACAO", "TIPO_GRAVAME",
        "QUANTIDADE_MESES", "TAXA_JUROS_MES", "TAXA_JUROS_ANO",
        "VALOR_TAXA_CONTRATO", "VALOR_IOF", "INDICATIVO_MULTA",
        "INDICATIVO_MORA", "VALOR_PRINCIPAL_OPERACAO", "VALOR_PARCELA",
        "VENCIMENTO_PRIMEIRA_PARCELA", "VENCIMENTO_ULTIMA_PARCELA",
        "CIDADE_LIBERACAO_OPERACAO", "UF_LIBERACAO_OPERACAO",
        "DATA_LIBERACAO_OPERACAO", "INDICES_UTILIZADOS", "MULTA",
        "JUROS_MORA", "CPF_CNPJ_RECEBEDOR"
    ]

    for item in dados_chassis:
        for campo in campos:
            if not item[campo]:
                print(f"Sem {campo.lower()} no .txt: {nome_txt}")
                mensagem_erro.append(
                    f"Sem {campo.lower()} no .txt: {nome_txt}. "
                    f"O .txt foi movido: <b>{nome_txt}</b>"
                )
                shutil.move(caminho_txt, pasta_lixo)
                return True

    return False


def _processar_via_negociavel(arquivos_pdf, op_num, arquivos_para_mover,
                              nome_txt, caminho_txt, pasta_lixo, mensagem_erro):
    """Processa a via negociável nos arquivos PDF.

    Args:
        arquivos_pdf: Lista de caminhos para arquivos PDF
        op_num: Número da operação
        arquivos_para_mover: Conjunto de arquivos para mover
        nome_txt: Nome do arquivo TXT
        caminho_txt: Caminho completo do arquivo TXT
        pasta_lixo: Caminho da pasta para arquivos rejeitados
        mensagem_erro: Lista para armazenar mensagens de erro

    Returns:
        True se houve erro no processamento, False caso contrário
    """
    print("Vai encontrar a Via Negociável...")
    via_negociavel_encontrada = False
    op_normalizado = remover_acentos(op_num).lower().replace(" ", "")

    for pdf_path in arquivos_pdf[:]:
        nome_pdf = os.path.basename(pdf_path)
        nome_normalizado = (
            remover_acentos(nome_pdf).lower().replace(" ", "")
        )

        if (re.search(r"^via[-_]*negociavel", nome_normalizado)
                and op_normalizado in nome_normalizado):
            arquivos_para_mover.add(pdf_path)
            arquivos_pdf.remove(pdf_path)
            print(f"  -> ✅Via Negociável encontrada: {nome_pdf}")

            tamanho_arquivo = os.path.getsize(pdf_path) / (1024 * 1024)
            if tamanho_arquivo > 10:
                print(
                    f'⚠️O PDF "{nome_pdf}" tem mais de 10MB. '
                    f'NOTIFICAR IC 😱 *****NOTIFICAR IC*****'
                )
                mensagem_erro.append(
                    f'O PDF "{nome_pdf}" tem mais de 10MB. '
                    f'O .txt foi movido: <b>{nome_txt}</b>.'
                )
                print('Movendo o .txt para a pasta "Lixo"')
                shutil.move(caminho_txt, pasta_lixo)
                print(
                    f"❗Txt com Via Negociável maior que 10MB "
                    f"movido para a pasta Lixo: {nome_txt}"
                )
                return True

            via_negociavel_encontrada = True
            break

    if not via_negociavel_encontrada:
        print(
            f"⚠️Via Negociável não encontrada pelo número da operação "
            f"{op_num}. NOTIFICAR IC 😱 *****NOTIFICAR IC*****"
        )
        mensagem_erro.append(
            f"Via Negociável não encontrada pelo número da operação {op_num}. "
            f"O .txt foi movido: <b>{nome_txt}</b>."
        )
        arquivos_para_mover.remove(caminho_txt)
        print('Movendo o .txt para a pasta "Lixo"')
        shutil.move(caminho_txt, pasta_lixo)
        print(f"❗Txt sem a Via Negociável movido para a pasta Lixo: {nome_txt}")
        return True

    return False


def _processar_resultados_pdf(resultados_pdf, arquivos_para_mover,
                              arquivos_pdf, nome_txt, caminho_txt,
                              pasta_lixo, mensagem_erro):
    """Processa os resultados da análise dos PDFs.

    Args:
        resultados_pdf: Lista de resultados da análise dos PDFs
        arquivos_para_mover: Conjunto de arquivos para mover
        arquivos_pdf: Lista de caminhos para arquivos PDF
        nome_txt: Nome do arquivo TXT
        caminho_txt: Caminho completo do arquivo TXT
        pasta_lixo: Caminho da pasta para arquivos rejeitados
        mensagem_erro: Lista para armazenar mensagens de erro

    Returns:
        True se houve erro no processamento, False caso contrário
    """
    print("Vai procurar os chassis...")
    pdf_com_erro_extracao = False

    for caminho_pdf, chassis in resultados_pdf:
        texto_extraido = extrair_texto_do_pdf(caminho_pdf)
        if is_texto_codificado(texto_extraido):
            nome_pdf_erro = os.path.basename(caminho_pdf)
            print(
                f'  ⚠️ A extração de texto do PDF "{nome_pdf_erro}" falhou '
                f'(texto codificado). NOTIFICAR IC 😱 *****NOTIFICAR IC*****'
            )
            mensagem_erro.append(
                f'A extração de texto do PDF "{nome_pdf_erro}" falhou '
                f'(texto codificado). O .txt foi movido: <b>{nome_txt}</b>.'
            )
            pdf_com_erro_extracao = True
            arquivos_pdf.remove(caminho_pdf)
            break

        if chassis:
            arquivos_para_mover.add(caminho_pdf)
            print(
                f"  -> Chassis {list(chassis)} em "
                f"{os.path.basename(caminho_pdf)}"
            )

            tamanho_arquivo = os.path.getsize(caminho_pdf) / (1024 * 1024)
            if tamanho_arquivo > 10:
                print(
                    f'⚠️O .pdf "{os.path.basename(caminho_pdf)}" tem mais '
                    f'de 10MB. NOTIFICAR IC 😱 *****NOTIFICAR IC*****'
                )
                mensagem_erro.append(
                    f'O .pdf "{os.path.basename(caminho_pdf)}" tem mais de 10MB. '
                    f'O .txt foi movido: <b>{nome_txt}</b>.'
                )
                print('Movendo o .txt para a pasta "Lixo"')
                shutil.move(caminho_txt, pasta_lixo)
                print(
                    f"❗Txt com NF maior que 10MB movido para a pasta Lixo: "
                    f"{nome_txt}"
                )
                return True

    if pdf_com_erro_extracao:
        print(
            'Movendo o .txt para a pasta "Lixo" devido à falha na '
            'extração do PDF.'
        )
        shutil.move(caminho_txt, pasta_lixo)
        print(f"❗Txt movido para a pasta Lixo: {nome_txt}")
        return True

    return False
