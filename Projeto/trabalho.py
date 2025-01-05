import FreeSimpleGUI as sg
import json
import os
import matplotlib.pyplot as plt

# Definindo o nome do arquivo de base de dados
basedados = 'ata_medica_papers.json'
caminho_basedados = os.path.join(os.path.dirname(os.path.abspath(__file__)), basedados)


#~~~~~~~~~~~~~~~~~~~~GERENCIAMENTO DE DADOS~~~~~~~~~~~~~~~~~~~~#

def carregar_dados():
    try:
        with open(caminho_basedados, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []
    return dados

def salvar_dados(dados):
    with open(caminho_basedados, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


#~~~~~~~~~~~~~~~~~~~~JANELA PRINCIPAL~~~~~~~~~~~~~~~~~~~~#

def criar_janela_principal():
    layout = [
        [sg.Text(
            "Bem-vindo, o que deseja fazer?",
            font=("Helvetica", 24, "bold"),
        )],
        [
            sg.Column([
                [sg.Button("Criação de publicações", size=(25, 2), font=("Helvetica", 14))],
                [sg.Button("Visualização de publicações", size=(25, 2), font=("Helvetica", 14))],
                [sg.Button("Atualização de publicações", size=(25, 2), font=("Helvetica", 14))],
            ]),
            sg.Column([
                [sg.Button("Remoção de publicações", size=(25, 2), font=("Helvetica", 14))],
                [sg.Button("Autores", size=(25, 2), font=("Helvetica", 14))],
                [sg.Button("Estatísticas", size=(25, 2), font=("Helvetica", 14))],
            ]),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Ajuda", size=(15, 1), font=("Helvetica", 12)),
            sg.Button("Importar Publicações", size=(20, 1), font=("Helvetica", 12)),
            sg.Button("Sair", size=(15, 1), font=("Helvetica", 12))
        ]
    ]

    return sg.Window("Menu Principal", layout, size=(700, 320), element_justification="center", finalize=True)


#~~~~~~~~~~~~~~~~~~~~JANELA CRIAÇÃO DE PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#´

def criar_janela_criacao():
    layout = [
        [sg.Text("Título:"), sg.InputText(key='titulo')],
        [sg.Text("Resumo:"), sg.Multiline(key='resumo')],
        [sg.Text("Palavras-chave:"), sg.InputText(key='palavras_chave')],
        [sg.Text("DOI:"), sg.InputText(key='doi')],
        [sg.Text("Autores (nomes separados por vírgula):"), sg.InputText(key='autores')],
        [sg.Text("Afiliações (afiliações separadas por vírgula):"), sg.InputText(key='afiliacoes')],
        [sg.Text("URL do PDF:"), sg.InputText(key='url_pdf')],
        [sg.Text("Data de Publicação:"), sg.InputText(key='data_publicacao')],
        [sg.Text("URL do Artigo:"), sg.InputText(key='url_artigo')],
        [sg.Button("Salvar"), sg.Button("Cancelar")]
    ]
    return sg.Window("Criação de Publicações", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA VISUALIZAÇÃO DE PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def criar_janela_visualizacao():
    layout = [
        [sg.Text("Pesquisar por título:"), sg.InputText(key='filtro_titulo')],
        [sg.Text("Pesquisar por autor:"), sg.InputText(key='filtro_autor')],
        [sg.Text("Pesquisar por afiliação:"), sg.InputText(key='filtro_afilacao')],
        [sg.Text("Pesquisar por palavras-chave:"), sg.InputText(key='filtro_palavras_chave')],
        [sg.Text("Pesquisar por data de publicação:"), sg.InputText(key='filtro_data_publicacao')],
        [sg.Button("Filtrar"), sg.Button("Ordenar por Título"), sg.Button("Ordenar por Data"), sg.Button("Exportar Publicações"), sg.Button("Fechar")],
        [sg.Listbox(values=[], size=(80, 20), key='resultado_visualizacao')]
    ]
    return sg.Window("Visualização de Publicações", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA ATUZALIZAÇÃO DE PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def criar_janela_atualizacao(titulos):
    layout = [
        [sg.Text("Selecione a publicação para atualizar:")],
        [sg.Listbox(values=titulos, size=(80, 20), key='publicacao_selecionada')],
        [sg.Button("Selecionar"), sg.Button("Cancelar")]
    ]
    return sg.Window("Atualização de Publicações", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA EXPORTAR PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def exportar_publicacoes(resultados):
    caminho_arquivo = sg.popup_get_file("Salvar como", save_as=True, file_types=(('Arquivos JSON', '*.json'),))
    if caminho_arquivo:
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, indent=4, ensure_ascii=False)
            sg.popup("Exportação concluída com sucesso!")
        except Exception as e:
            sg.popup_error(f"Erro ao exportar publicações: {e}")


#~~~~~~~~~~~~~~~~~~~~JANELA REMOÇÃO DE PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def criar_janela_remocao(titulos):
    layout = [
        [sg.Text("Selecione a publicação para remover:")],
        [sg.Listbox(values=titulos, size=(80, 20), key='publicacao_selecionada')],
        [sg.Button("Remover"), sg.Button("Cancelar")]
    ]
    return sg.Window("Remoção de Publicações", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA AUTORES DE PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def criar_janela_autores(autores):
    layout = [
        [sg.Listbox(values=autores, size=(80, 20), key='autor_selecionado')],
        [sg.Button("Ver Publicações"), sg.Button("Fechar")]
    ]
    return sg.Window("Autores", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA PUBLICAÇÕES DE UM AUTOR ESPECÍFICO~~~~~~~~~~~~~~~~~~~~#

def criar_janela_publicacoes_autor(publicacoes, autor):
    layout = [
        [sg.Text(f"Publicações de {autor}:")],
        [sg.Listbox(values=publicacoes, size=(80, 20), key='publicacoes_autor')],
        [sg.Button("Fechar")]
    ]
    return sg.Window(f"Publicações de {autor}", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA ESTATÍTICAS DE PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def criar_janela_estatisticas():
    layout = [
        [sg.Text("Selecione a estatística que deseja visualizar:")],
        [sg.Button("Distribuição de publicações por ano")],
        [sg.Button("Distribuição de publicações por mês de um determinado ano")],
        [sg.Button("Número de publicações por autor (top 20 autores)")],
        [sg.Button("Distribuição de publicações de um autor por anos")],
        [sg.Button("Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave)")],
        [sg.Button("Distribuição de palavras-chave mais frequente por ano")],
        [sg.Button("Voltar")]
    ]
    return sg.Window("Estatísticas", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA AJUDA~~~~~~~~~~~~~~~~~~~~#
  
def criar_janela_ajuda():
    funcionalidades = """
    Funcionalidades disponíveis:
    1. Criação de publicações: Adiciona novos artigos à base de dados.
    2. Atualização de publicações: Permite editar informações de artigos existentes.
    3. Visualização de publicações: Pesquisa e permite visualizar artigos por filtros.
    4. Remoção de publicações: Exclui os artigos selecionados da base de dados.
    5. Estatísticas: Gera gráficos e permite visualizar informações detalhadas sobre publicações.
    6. Autores: Lista os autores e permite visualizar artigos associados a eles.
    7. Importar Publicações:  Permite importar novos registos dum outro ficheiro que tenha a mesma 
       estrutura do ficheiro de suporte.
    8. Exportar Publicações: Permite exportar para um ficheiro os registos resultantes de uma 
       pesquisa.
    """
    layout = [
        [sg.Multiline(funcionalidades, size=(85, 15), disabled=True)],
        [sg.Button("Fechar")]
    ]
    return sg.Window("Ajuda", layout)


#~~~~~~~~~~~~~~~~~~~~JANELA IMPORTAR PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def criar_janela_importar():
    layout = [
        [sg.Text("Selecione o arquivo JSON para importar:")],
        [sg.Input(), sg.FileBrowse(file_types=(('Arquivos JSON', '*.json'),))],
        [sg.Button("Importar"), sg.Button("Cancelar")]
    ]
    return sg.Window("Importar Publicações", layout)


def importar_json(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            registros = json.load(arquivo)
        return registros
    except Exception as e:
        sg.popup_error(f"Erro ao importar arquivo: {e}")
        return []



#~~~~~~~~~~~~~~~~~~~~JANELA EDITAR PUBLICAÇÕES~~~~~~~~~~~~~~~~~~~~#

def criar_janela_editar_publicacao(publicacao):
    layout = [
        [sg.Text("Título:"), sg.InputText(publicacao['title'], key='titulo')],
        [sg.Text("Resumo:"), sg.Multiline(publicacao['abstract'], key='resumo')],
        [sg.Text("Palavras-chave:"), sg.InputText(publicacao['keywords'], key='palavras_chave')],
        [sg.Text("DOI:"), sg.InputText(publicacao['doi'], key='doi')],
        [sg.Text("Autores (nomes separados por vírgula):"), sg.InputText(','.join([autor['name'] for autor in publicacao['authors']]), key='autores')],
        [sg.Text("Afiliações (afiliações separadas por vírgula):"), sg.InputText(','.join([autor['affiliation'] for autor in publicacao['authors']]), key='afiliacoes')],
        [sg.Text("URL do PDF:"), sg.InputText(publicacao['pdf'], key='url_pdf')],
        [sg.Text("Data de Publicação:"), sg.InputText(publicacao['publish_date'], key='data_publicacao')],
        [sg.Text("URL do Artigo:"), sg.InputText(publicacao['url'], key='url_artigo')],
        [sg.Button("Salvar"), sg.Button("Cancelar")]
    ]
    return sg.Window("Editar Publicação", layout)


#~~~~~~~~~~~~~~~~~~~~FUNÇÕES DE APOIO~~~~~~~~~~~~~~~~~~~~#

def filtrar_artigos(dados, filtro_titulo, filtro_autor, filtro_afilacao, filtro_palavras_chave, filtro_data_publicacao):
    resultados = []
    for artigo in dados:
        titulo_ok = filtro_titulo in artigo.get('title', '').lower() or not filtro_titulo
        autor_ok = any(filtro_autor in autor.get('name', '').lower() for autor in artigo.get('authors', [])) or not filtro_autor
        afilacao_ok = any(filtro_afilacao in autor.get('affiliation', '').lower() for autor in artigo.get('authors', [])) or not filtro_afilacao
        palavras_chave_ok = filtro_palavras_chave in artigo.get('keywords', '').lower() or not filtro_palavras_chave
        if filtro_data_publicacao:
            filtro_data_publicacao = filtro_data_publicacao.replace("-", "")
            data_ok = filtro_data_publicacao in artigo.get('publish_date', '').replace("-", "")
        else:
            data_ok = True
        if titulo_ok and autor_ok and afilacao_ok and palavras_chave_ok and data_ok:
            resultados.append(artigo)
    return resultados


def listar_autores(dados):
    autores = set()
    for artigo in dados:
        for autor in artigo.get('authors', []):
            autores.add(autor.get('name'))
    return list(autores)


def obter_publicacoes_por_autor(dados, autor_procurado):
    publicacoes = [artigo['title'] for artigo in dados if any(autor.get('name') == autor_procurado for autor in artigo.get('authors', []))]
    return publicacoes


#~~~~~~~~~~~~~~~~~~~~ANÁLISE DE DADOS~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~ESTATÍSTICAS GERAIS~~~~~~~~~~~~~~~~~~~~#

def distribuir_publicacoes_por_ano(dados):
    anos = {}
    for artigo in dados:
        try:
            ano = artigo['publish_date'][:4]
            anos[ano] = anos.get(ano, 0) + 1
        except KeyError:
            print(f"Erro: O artigo {artigo.get('title', 'Sem título')} não possui 'publish_date'.")
    return anos


def distribuir_publicacoes_por_mes(dados, ano):
    meses = {str(i).zfill(2): 0 for i in range(1, 13)}
    for artigo in dados:
        try:
            data = artigo['publish_date']
            if data.startswith(ano):
                mes = data[5:7]
                if mes in meses:
                    meses[mes] += 1
        except KeyError:
            print(f"Erro: O artigo {artigo.get('title', 'Sem título')} não possui 'publish_date'.")
    return meses


#~~~~~~~~~~~~~~~~~~~~ESTATÍSTICAS DE AUTORES~~~~~~~~~~~~~~~~~~~~#

def numero_publicacoes_por_autor(dados):
    autores = {}
    for artigo in dados:
        for autor in artigo['authors']:
            nome = autor['name']
            if nome in autores:
                autores[nome] += 1
            else:
                autores[nome] = 1
    return dict(sorted(autores.items(), key=lambda item: item[1], reverse=True)[:20])


def distribuicao_publicacoes_por_ano_autor(dados, autor_procurado):
    anos = {}
    for artigo in dados:
        try:
            for autor in artigo['authors']:
                if autor.get('name') == autor_procurado:  
                    ano = artigo['publish_date'][:4]
                    anos[ano] = anos.get(ano, 0) + 1
        except KeyError:
            print(f"Erro: O artigo {artigo.get('title', 'Sem título')} não possui 'authors' ou 'publish_date'.")
    return anos


#~~~~~~~~~~~~~~~~~~~~ESTATÍSTICAS DE PALAVRAS-CHAVE~~~~~~~~~~~~~~~~~~~~#

def distribuicao_palavras_chave(dados):
    palavras_chave = {}
    for artigo in dados:
        try:
            palavras = artigo['keywords'].split(',') 
            for palavra in palavras:
                palavra = palavra.strip()
                palavras_chave[palavra] = palavras_chave.get(palavra, 0) + 1
        except KeyError:
            print(f"Erro: O artigo {artigo.get('title', 'Sem título')} não possui 'keywords'.")
    return dict(sorted(palavras_chave.items(), key=lambda item: item[1], reverse=True)[:20])


def distribuicao_palavras_chave_por_ano(dados):
    palavras_chave_por_ano = {}
    
    for artigo in dados:
        try:
            ano = artigo['publish_date'][:4]  # Extrai o ano
            palavras = artigo['keywords'].split(',')  # Divide as palavras-chave
            for palavra in palavras:
                palavra = palavra.strip()  # Remove espaços extras
                
                if ano not in palavras_chave_por_ano:
                    palavras_chave_por_ano[ano] = {}
                    
                # Incrementa a contagem de palavras-chave
                palavras_chave_por_ano[ano][palavra] = palavras_chave_por_ano[ano].get(palavra, 0) + 1
        except KeyError:
            print(f"Erro: O artigo {artigo.get('title', 'Sem título')} não possui 'publish_date' ou 'keywords'.")
    
    # Filtra palavras-chave que aparecem 2 ou mais vezes
    for ano in palavras_chave_por_ano:
        palavras_chave_por_ano[ano] = {palavra: contagem for palavra, contagem in palavras_chave_por_ano[ano].items() if contagem >= 2}
    
    return palavras_chave_por_ano


#~~~~~~~~~~~~~~~~~~~~GRÁFICOS~~~~~~~~~~~~~~~~~~~~#

def gerar_grafico(x, y, titulo, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='skyblue')
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


#~~~~~~~~~~~~~~~~~~~~MENU PRINCIPAL~~~~~~~~~~~~~~~~~~~~#

def main():
    dados = carregar_dados()
    janela_principal = criar_janela_principal()

    while True:
        evento, valores = janela_principal.read()
        if evento in (sg.WINDOW_CLOSED, "Sair"):
            exit()
        if evento == "Criação de publicações":
            janela_criacao = criar_janela_criacao()
            continuar_criando = True
            
            while continuar_criando:
                evento_criacao, valores_criacao = janela_criacao.read()
                
                if evento_criacao in (sg.WINDOW_CLOSED, "Cancelar"):
                    janela_criacao.close()
                    continuar_criando = False  
                
                elif evento_criacao == "Salvar":
                    nova_publicacao = {
                        "abstract": valores_criacao['resumo'],
                        "keywords": valores_criacao['palavras_chave'],
                        "authors": [{"name": nome.strip(), "affiliation": afil.strip()} 
                                    for nome, afil in zip(valores_criacao['autores'].split(','), valores_criacao['afiliacoes'].split(','))],
                        "doi": valores_criacao['doi'],
                        "pdf": valores_criacao['url_pdf'],
                        "publish_date": valores_criacao['data_publicacao'],
                        "title": valores_criacao['titulo'],
                        "url": valores_criacao['url_artigo']
                    }
                    dados.append(nova_publicacao)
                    salvar_dados(dados)
                    sg.popup("Publicação salva com sucesso!")

        if evento == "Atualização de publicações":
            titulos =sorted([artigo['title'] for artigo in dados])
            janela_atualizacao = criar_janela_atualizacao(titulos)
            continuar_atualizando = True
            
            while continuar_atualizando:
                evento_atualizacao, valores_atualizacao = janela_atualizacao.read()
                
                if evento_atualizacao in (sg.WINDOW_CLOSED, "Cancelar"):
                    janela_atualizacao.close()
                    continuar_atualizando = False
                
                elif evento_atualizacao == "Selecionar":
                    if valores_atualizacao['publicacao_selecionada']:
                        titulo_selecionado = valores_atualizacao['publicacao_selecionada'][0]
                        publicacao = next((art for art in dados if art['title'] == titulo_selecionado), None)
                        if publicacao:
                            janela_editar = criar_janela_editar_publicacao(publicacao)
                            continuar_editando = True
                            
                            while continuar_editando:
                                evento_editar, valores_editar = janela_editar.read()
                                
                                if evento_editar in (sg.WINDOW_CLOSED, "Cancelar"):
                                    janela_editar.close()
                                    continuar_editando = False
                                
                                elif evento_editar == "Salvar":
                                    publicacao_atualizada = {
                                        "title": valores_editar['titulo'],
                                        "abstract": valores_editar['resumo'],
                                        "keywords": valores_editar['palavras_chave'],
                                        "doi": valores_editar['doi'],
                                        "authors": [{"name": nome.strip(), "affiliation": afil.strip()}
                                                    for nome, afil in zip(valores_editar['autores'].split(','), valores_editar['afiliacoes'].split(','))],
                                        "pdf": valores_editar['url_pdf'],
                                        "publish_date": valores_editar['data_publicacao'],
                                        "url": valores_editar['url_artigo']
                                    }
                                    index = dados.index(publicacao)
                                    dados[index] = publicacao_atualizada
                                    salvar_dados(dados)
                                    sg.popup("Publicação atualizada com sucesso!")

        if evento == "Visualização de publicações":
            janela_visualizacao = criar_janela_visualizacao()
            resultados = []
            continuar_execucao = True

            while continuar_execucao:
                try:
                    evento_visualizacao, valores_visualizacao = janela_visualizacao.read()
                    if evento_visualizacao in (sg.WINDOW_CLOSED, "Fechar"):
                        janela_visualizacao.close()
                        continuar_execucao = False

                    if evento_visualizacao == "Filtrar":
                        filtro_titulo = valores_visualizacao['filtro_titulo'].lower()
                        filtro_autor = valores_visualizacao['filtro_autor'].lower()
                        filtro_afilacao = valores_visualizacao['filtro_afilacao'].lower()
                        filtro_palavras_chave = valores_visualizacao['filtro_palavras_chave'].lower()
                        filtro_data_publicacao = valores_visualizacao['filtro_data_publicacao']

                        resultados = filtrar_artigos(dados, filtro_titulo, filtro_autor, filtro_afilacao, filtro_palavras_chave, filtro_data_publicacao)
                        janela_visualizacao['resultado_visualizacao'].update([artigo['title'] for artigo in resultados])
                        print(f"Resultados Filtrados: {[artigo['title'] for artigo in resultados]}")

                    if evento_visualizacao == "Ordenar por Título":
                        resultados = sorted(resultados, key=lambda x: x['title'])
                        janela_visualizacao['resultado_visualizacao'].update([artigo['title'] for artigo in resultados])
                        print(f"Resultados Ordenados por Título: {[artigo['title'] for artigo in resultados]}")

                    if evento_visualizacao == "Ordenar por Data":
                        resultados = sorted(resultados, key=lambda x: x['publish_date'])
                        janela_visualizacao['resultado_visualizacao'].update([artigo['title'] for artigo in resultados])
                        print(f"Resultados Ordenados por Data: {[artigo['title'] for artigo in resultados]}")

                    if evento_visualizacao == "Exportar Publicações":
                        caminho_arquivo = sg.popup_get_file("Selecionar ou criar arquivo", save_as=True, file_types=(('Arquivos JSON', '*.json'),))
                        if not caminho_arquivo:
                            sg.popup("Nenhum arquivo selecionado!")
                        else:
                            try:
                                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                                    registros_existentes = json.load(f)
                            except (FileNotFoundError, json.JSONDecodeError):
                                registros_existentes = []

                            registros_existentes.extend(resultados)

                            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                                json.dump(registros_existentes, f, indent=4, ensure_ascii=False)
                            sg.popup("Publicações exportadas com sucesso!")

                except Exception as e:
                    sg.popup_error(f"Ocorreu um erro: {e}")


        if evento == "Remoção de publicações":
            titulos = sorted([artigo['title'] for artigo in dados])
            janela_remocao = criar_janela_remocao(titulos)
            continuar_removendo = True

            while continuar_removendo:
                evento_remocao, valores_remocao = janela_remocao.read()
                
                if evento_remocao in (sg.WINDOW_CLOSED, "Cancelar"):
                    janela_remocao.close()
                    continuar_removendo = False
                
                elif evento_remocao == "Remover":
                    if valores_remocao['publicacao_selecionada']:
                        titulo_selecionado = valores_remocao['publicacao_selecionada'][0]
                        dados = [artigo for artigo in dados if artigo['title'] != titulo_selecionado]
                        salvar_dados(dados)
                        sg.popup("Publicação removida com sucesso!")
                    else:
                        sg.popup("Por favor, selecione uma publicação para remover.")

        if evento == "Estatísticas":
            janela_estatisticas = criar_janela_estatisticas()
            continuar_estatisticas = True

            while continuar_estatisticas:
                evento_estatisticas, valores_estatisticas = janela_estatisticas.read()
                
                if evento_estatisticas in (sg.WINDOW_CLOSED, "Voltar"):
                    janela_estatisticas.close()
                    continuar_estatisticas = False
                
                elif evento_estatisticas == "Distribuição de publicações por ano":
                    distrib_ano = distribuir_publicacoes_por_ano(dados)
                    gerar_grafico(list(distrib_ano.keys()), list(distrib_ano.values()), 
                                'Distribuição de Publicações por Ano', 'Ano', 'Número de Publicações')
                
                elif evento_estatisticas == "Distribuição de publicações por mês de um determinado ano":
                    ano = sg.popup_get_text('Digite o ano:')
                    if ano:
                        distrib_mes = distribuir_publicacoes_por_mes(dados, ano)
                        gerar_grafico(list(distrib_mes.keys()), list(distrib_mes.values()), 
                                    f'Distribuição de Publicações por Mês em {ano}', 'Mês', 'Número de Publicações')
                
                elif evento_estatisticas == "Número de publicações por autor (top 20 autores)":
                    pub_autor = numero_publicacoes_por_autor(dados)
                    gerar_grafico(list(pub_autor.keys()), list(pub_autor.values()), 
                                'Número de Publicações por Autor (Top 20)', 'Autor', 'Número de Publicações')
                
                elif evento_estatisticas == "Distribuição de publicações de um autor por anos":
                    autor = sg.popup_get_text('Digite o nome do autor:')
                    if autor:
                        distrib_ano_autor = distribuicao_publicacoes_por_ano_autor(dados, autor)
                        gerar_grafico(list(distrib_ano_autor.keys()), list(distrib_ano_autor.values()), 
                                    f'Distribuição de Publicações por Ano para {autor}', 'Ano', 'Número de Publicações')
                
                elif evento_estatisticas == "Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave)":
                    palavras_chave = distribuicao_palavras_chave(dados)
                    gerar_grafico(list(palavras_chave.keys()), list(palavras_chave.values()), 
                                'Distribuição de Palavras-chave pela Frequência (Top 20)', 'Palavra-chave', 'Frequência')
                
                elif evento_estatisticas == "Distribuição de palavras-chave mais frequente por ano":
                    ano_selecionado = sg.popup_get_text('Digite o ano para o qual deseja ver a distribuição de palavras-chave:')
                    palavras_chave_por_ano = distribuicao_palavras_chave_por_ano(dados)
                    if ano_selecionado and ano_selecionado in palavras_chave_por_ano:
                        palavras = palavras_chave_por_ano[ano_selecionado]
                        gerar_grafico(list(palavras.keys()), list(palavras.values()), 
                                    f'Distribuição de Palavras-chave em {ano_selecionado}', 'Palavra-chave', 'Frequência')
                    else:
                        sg.popup("Ano não encontrado", f"O ano {ano_selecionado} não possui dados de palavras-chave.")


        if evento == "Autores":
            autores = sorted(listar_autores(dados))
            janela_autores = criar_janela_autores(autores)
            continuar_autores = True 

            while continuar_autores:
                evento_autores, valores_autores = janela_autores.read()
                
                if evento_autores in (sg.WINDOW_CLOSED, "Fechar"):
                    janela_autores.close()
                    continuar_autores = False
                
                elif evento_autores == "Ver Publicações":
                    if valores_autores['autor_selecionado']:
                        autor_selecionado = valores_autores['autor_selecionado'][0]
                        publicacoes = obter_publicacoes_por_autor(dados, autor_selecionado)
                        janela_publicacoes_autor = criar_janela_publicacoes_autor(publicacoes, autor_selecionado)
                        continuar_publicacoes_autor = True

                        while continuar_publicacoes_autor:
                            evento_publicacoes_autor, valores_publicacoes_autor = janela_publicacoes_autor.read()
                            
                            if evento_publicacoes_autor in (sg.WINDOW_CLOSED, "Fechar"):
                                janela_publicacoes_autor.close()
                                continuar_publicacoes_autor = False


        if evento == "Importar Publicações":
            caminho_arquivo = sg.popup_get_file("Selecione um arquivo JSON para importar:")
            if caminho_arquivo:
                novos_registros = importar_json(caminho_arquivo)
                if novos_registros:
                    dados.extend(novos_registros)
                    salvar_dados(dados)
                    sg.popup("Publicações importadas com sucesso!")
        
        if evento == "Ajuda":
            janela_ajuda = criar_janela_ajuda()
            continuar_ajuda = True

            while continuar_ajuda:
                evento_ajuda, _ = janela_ajuda.read()
                
                if evento_ajuda in (sg.WINDOW_CLOSED, "Fechar"):
                    janela_ajuda.close()
                    continuar_ajuda = False    

main()
