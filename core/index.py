import os # Para manipulação de arquivos e diretórios
import shutil # Para mover arquivos entre pastas
import unicodedata # Para remover acentos
import re              # Para expressões regulares (não está sendo usada aqui)
import json            # Para salvar dados em formato JSON
from models._extrair_dados_do_txt import extrair_dados_do_txt
from models._processar_pdf_em_lote import processar_pdf_em_lote
from models._validar_texto import is_texto_codificado
from models._extrair_texto_do_pdf import extrair_texto_do_pdf

# Função principal para organizar os arquivos
def organizar_arquivos(diretorio_base, mensagem_erro):
    print(f"Iniciando organização do diretório: {diretorio_base}\n")
    #Se a pasta Lixo nao existir cria ela
    os.makedirs(os.path.join(diretorio_base, '_Lixo'), exist_ok=True)  # exist_ok=True cria a pasta se ela nao existir
    '''if not os.path.exists(os.path.join(diretorio_base, '_Lixo')):
        os.mkdir(os.path.join(diretorio_base, '_Lixo'))'''

    #Nova pasta lixo
    pasta_lixo = os.path.join(diretorio_base, '_Lixo') #join() junta o diretório com o arquivo
    try:
        # Lista todos os arquivos no diretório
        todos_os_arquivos = [os.path.join(diretorio_base, f) for f in os.listdir(diretorio_base) #listdir() lista os arquivos no diretório
                             if os.path.isfile(os.path.join(diretorio_base, f))] #isfile() verifica se é um arquivo join() junta o diretório com o arquivo
    except FileNotFoundError:
        print(f"ERRO: O diretório '{diretorio_base}' não foi encontrado.")
        return

    # Separa arquivos por extensão
    arquivos_txt = [f for f in todos_os_arquivos if f.lower().endswith('.txt')] #lower() converte para minúsculo endswith() verifica se o arquivo termina com .txt
    arquivos_pdf = [f for f in todos_os_arquivos if f.lower().endswith('.pdf')] #lower() converte para minúsculo endswith() verifica se o arquivo termina com .pdf
    arquivos_para_remover = [f for f in todos_os_arquivos if not (f.lower().endswith('.txt') or f.lower().endswith('.pdf'))]

    if arquivos_para_remover:
        for arquivo in arquivos_para_remover:
            print(f'⚠️Arquivo não será processados com extesão incompatível: {os.path.basename(arquivo)}')
            mensagem_erro.append(f'Arquivo não será processados com extesão incompatível: <b>{os.path.basename(arquivo)}</b>')
            os.remove(arquivo)
            print(f'❗Arquivo removido com sucesso: {os.path.basename(arquivo)}\n')


    if not arquivos_txt:
        print("⚠️Nenhum arquivo .txt encontrado no diretório.⚠️")
        return None

    print(f'Quantidade. de arquivos .txt encontrados: {len(arquivos_txt)}')


    # Processa cada arquivo .txt
    for caminho_txt in arquivos_txt:
        nome_txt = os.path.basename(caminho_txt)
        print(f"\n--- Processando o .txt: {nome_txt} ---")
        print(f'Pesquisando CHASSI e NÚMERO da operação no .txt...')
        dados_chassis, op_num = extrair_dados_do_txt(caminho_txt)

        # Contar quantos chassis existem em dados_chassis
        qtd_chassi ={d['CHASSI'] for d in dados_chassis}
        qtd_chassi = len(qtd_chassi)
        print(f'Quantidade de chassis esperados: {qtd_chassi}')

        sair = False
        for item in dados_chassis:
            if item['CHASSI'] == "":
                print(f'Sem chassi no .txt: {nome_txt} NOTIFICAR IC')
                #add mensagem na lista
                mensagem_erro.append(f'Sem chassi no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['REMARCACAO'] == "":
                print(f'Sem remarcação no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem remarcação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['ANO_FABRICACAO'] == "":
                print(f'Sem ano de fabricação no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem ano de fabricação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['ANO_MODELO'] == "":
                print(f'Sem ano de modelo no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem ano de modelo no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['NUMERO_OPERACAO'] == "":
                print(f'Sem número da operação no .txt: {nome_txt} NOTIFICAR IC')
                # add mensagem na lista
                mensagem_erro.append(f'Sem número da operação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['DATA_OPERACAO'] == "":
                print(f'Sem data da operação no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem data da operação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['TIPO_GRAVAME'] == "":
                print(f'Sem tipo de gravame no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem tipo de gravame no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['QUANTIDADE_MESES'] == "":
                print(f'Sem quantidade de meses no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem quantidade de meses no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['TAXA_JUROS_MES'] == "":
                print(f'Sem taxa de juros no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem taxa de juros no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['TAXA_JUROS_ANO'] == "":
                print(f'Sem taxa de juros no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem taxa de juros no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['VALOR_TAXA_CONTRATO'] == "":
                print(f'Sem valor da taxa do contrato no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem valor da taxa do contrato no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['VALOR_IOF'] == "":
                print(f'Sem valor do IOF no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem valor do IOF no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['INDICATIVO_MULTA'] == "":
                print(f'Sem indicativo de multa no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem indicativo de multa no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['INDICATIVO_MORA'] == "":
                print(f'Sem indicativo de mora no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem indicativo de mora no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['VALOR_PRINCIPAL_OPERACAO'] == "":
                print(f'Sem valor principal da operação no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem valor principal da operação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['VALOR_PARCELA'] == "":
                print(f'Sem valor da parcela no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem valor da parcela no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['VENCIMENTO_PRIMEIRA_PARCELA'] == "":
                print(f'Sem vencimento da primeira parcela no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem vencimento da primeira parcela no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['VENCIMENTO_ULTIMA_PARCELA'] == "":
                print(f'Sem vencimento da ultima parcela no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem vencimento da ultima parcela no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['CIDADE_LIBERACAO_OPERACAO'] == "":
                print(f'Sem cidade de liberação da operação no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem cidade de liberação da operação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['UF_LIBERACAO_OPERACAO'] == "":
                print(f'Sem UF de liberação da operação no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem UF de liberação da operação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
            elif item['DATA_LIBERACAO_OPERACAO'] == "":
                print(f'Sem data de liberação da operação no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem data de liberação da operação no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['INDICES_UTILIZADOS'] == "":
                print(f'Sem índices utilizados no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem índices utilizados no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['MULTA'] == "":
                print(f'Sem multa no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem multa no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['JUROS_MORA'] == "":
                print(f'Sem juros de mora no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem juros de mora no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break
            elif item['CPF_CNPJ_RECEBEDOR'] == "":
                print(f'Sem CPF/CNPJ do recebedor no .txt: {nome_txt}')
                # add mensagem na lista
                mensagem_erro.append(f'Sem CPF/CNPJ do recebedor no .txt: {nome_txt}. O .txt foi movido: <b>{nome_txt}</b>')
                # move o .txt pasta Lixo
                shutil.move(caminho_txt, pasta_lixo)
                sair = True
                break

        if sair:
            continue
        print(f"  -> ✅Número da operação e chassi(s) encontrado no .txt: {nome_txt}")
        arquivos_para_mover = {caminho_txt}
        via_negociavel_encontrada = False

        def remover_acentos(texto):# Função para remover acentos
            return ''.join(
                c for c in unicodedata.normalize('NFD', texto)
                if unicodedata.category(c) != 'Mn'
            )

        print(f'Vai encontrar a Via Negociável...')
        # Lista para armazenar os PDFs que *não* são a Via Negociável atual
        arquivos_pdf_restantes_nf = []
        sair = False
        # Normaliza número da operação para busca
        op_normalizado = remover_acentos(op_num).lower().replace(" ", "")
        for pdf_path in arquivos_pdf:

            nome_pdf = os.path.basename(pdf_path)
            nome_normalizado = remover_acentos(nome_pdf).lower().replace(" ", "")# Normaliza nome: sem acento, minúsculo, sem espaços

            if (re.search(r'^via[-_]*negociavel', nome_normalizado)# Busca por “via negociavel” com ou sem separadores + número da operação
                    and op_normalizado in nome_normalizado):
                arquivos_para_mover.add(pdf_path)
                arquivos_pdf.remove(pdf_path)
                print(f"  -> ✅Via Negociável encontrada: {nome_pdf}")

                # Verifica se o .pdf mais de 10MB
                tamanho_arquivo = os.path.getsize(pdf_path) / (1024 * 1024)  # Converte bytes para MB
                if tamanho_arquivo > 10:
                    print(f'⚠️O PDF "{nome_pdf}" tem mais de 10MB. NOTIFICAR IC 😱 *****NOTIFICAR IC*****')
                    # add mensagem na lista
                    mensagem_erro.append(f'O PDF "{nome_pdf}" tem mais de 10MB. O .txt foi movido: <b>{nome_txt}</b>.')
                    print(f'Movendo o .txt para a pasta "Lixo"')
                    shutil.move(caminho_txt, pasta_lixo)  # move o .txt pasta Lixo
                    print(f"❗Txt com Via Negociável maior que 10MB movido para a pasta Lixo: {nome_txt}")
                    sair = True
                    break

                via_negociavel_encontrada = True
                break

            if re.search(r'via[-_]*negociavel', nome_normalizado):
                pass
            else:
                arquivos_pdf_restantes_nf.append(pdf_path)

        if sair:
            continue

        if not via_negociavel_encontrada:
            print(f'⚠️Via Negociável não encontrada pelo número da operação {op_num}. NOTIFICAR IC 😱 *****NOTIFICAR IC*****')
            # add mensagem na lista
            mensagem_erro.append(f'Via Negociável não encontrada pelo número da operação {op_num}. O .txt foi movido: <b>{nome_txt}</b>.')
            #Remover o .txt sem a Via Negociável da lista de arquivos para mover
            arquivos_para_mover.remove(caminho_txt)
            print(f'Movendo o .txt para a pasta "Lixo"')
            #move o .txt pasta Lixo
            shutil.move(caminho_txt, pasta_lixo)
            print(f"❗Txt sem a Via Negociável movido para a pasta Lixo: {nome_txt}")
            continue

        print(f'Vai procurar os chassis...')
        # Procura os chassis dentro dos PDFs
        resultados_pdf = processar_pdf_em_lote(arquivos_pdf_restantes_nf, dados_chassis)

        chassis_encontrados = set()
        pdf_com_erro_extracao = False  # Flag para controlar erro de extração

        # Verifica se o chassi foi encontrado e em qual arquivo .pdf
        for caminho_pdf, chassis in resultados_pdf:
            # --- NOVA VALIDAÇÃO DE TEXTO ---
            texto_extraido = extrair_texto_do_pdf(caminho_pdf)
            if is_texto_codificado(texto_extraido):
                nome_pdf_erro = os.path.basename(caminho_pdf)
                print(
                    f'  ⚠️ A extração de texto do PDF "{nome_pdf_erro}" falhou (texto codificado). NOTIFICAR IC 😱 *****NOTIFICAR IC*****')
                mensagem_erro.append(f'A extração de texto do PDF "{nome_pdf_erro}" falhou (texto codificado). O .txt foi movido: <b>{nome_txt}</b>.')
                pdf_com_erro_extracao = True
                #remove de resultados_pdf
                arquivos_pdf.remove(caminho_pdf)
                break  # Interrompe a verificação dos outros PDFs para esta operação

            if chassis:
                arquivos_para_mover.add(caminho_pdf)
                chassis_encontrados.update(chassis)
                print(f"  -> Chassis {list(chassis)} em {os.path.basename(caminho_pdf)}")

                # Verifica se o .pdf mais de 10MB
                tamanho_arquivo = os.path.getsize(caminho_pdf) / (1024 * 1024)
                if tamanho_arquivo > 10:
                    print(
                        f'⚠️O .pdf "{os.path.basename(caminho_pdf)}" tem mais de 10MB. NOTIFICAR IC 😱 *****NOTIFICAR IC*****')
                    mensagem_erro.append(f'O .pdf "{os.path.basename(caminho_pdf)}" tem mais de 10MB. O .txt foi movido: <b>{nome_txt}</b>.')
                    print(f'Movendo o .txt para a pasta "Lixo"')
                    shutil.move(caminho_txt, pasta_lixo)
                    print(f"❗Txt com NF maior que 10MB movido para a pasta Lixo: {nome_txt}")
                    sair = True
                    break
        if sair:
            continue

        # Se um PDF falhou na extração, move o .txt e continua para a próxima operação
        if pdf_com_erro_extracao:
            print(f'Movendo o .txt para a pasta "Lixo" devido à falha na extração do PDF.')
            shutil.move(caminho_txt, pasta_lixo)
            print(f'❗Txt movido para a pasta Lixo: {nome_txt}')
            continue

        #print(chassis_encontrados)
        # Verifica quais chassis esperados não foram encontrados
        chassis_esperados = {d['CHASSI'] for d in dados_chassis}
        faltando = chassis_esperados - chassis_encontrados
        if faltando:
            print(f'  ⚠️Chassis {faltando} do .txt {nome_txt} não encontrados nos .pdf🤦‍♀️*****NOTIFICAR IC*****')
            # add mensagem na lista
            mensagem_erro.append(f'Chassi {faltando} do .txt {nome_txt} não encontrados nos .pdf. O .txt foi movido: <b>{nome_txt}</b>.')
            print(f'Movendo o .txt para a pasta "Lixo"')
            # move o .txt pasta Lixo
            shutil.move(caminho_txt, pasta_lixo)
            print(f'❗Txt sem os chassis movido para a pasta Lixo: {nome_txt}')
            continue

        # Se tiver mais de um arquivo relacionado, move para uma nova pasta
        if len(arquivos_para_mover) > 1:
            #nome_devedor = dados_chassis[0]["NUMERO_OPERACAO"].replace(" ", "_").replace("/", "")# Normaliza nome: sem acento, minúsculo, sem espaços
            #nova_pasta = f"{op_num}_{nome_devedor}" # Nome da nova pasta
            nova_pasta = f"{op_num}"
            destino = os.path.join(diretorio_base, nova_pasta) # Caminho da nova pasta
            os.makedirs(destino, exist_ok=True) # Cria a nova pasta

            for arq in arquivos_para_mover:
                try:
                    shutil.move(arq, os.path.join(destino, os.path.basename(arq)))
                except Exception as e:
                    print(f"[Erro ao mover] {arq}: {e}")

            print(f'Vai salvar os dados extraídos do .txt em JSON...')
            # Salva os dados extraídos do .txt em JSON
            with open(os.path.join(destino, f"{op_num}_dados_extraidos.json"), 'w', encoding='utf-8') as f: # Salva os dados em um arquivo JSON
                json.dump(dados_chassis, f, indent=4, ensure_ascii=False)#Para melhor visualização, sem acentos e sem espaços
            print(f"  -> ✅Dados extraídos do .txt salvos no JSON: {nova_pasta}")
        else:
            print("  -> ❗Nenhum arquivo adicional encontrado.")

        print(f"--- Fim do processamento do .txt: {nome_txt} ---")

    return mensagem_erro