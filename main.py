# IMPORTANDO REQUESTS
import requests

# Importando o google tradutor
from googletrans import Translator

# Inicializar o tradutor
translator = Translator()

api_key = "27954b9558664a5c84b75b4377b531ba"

# traduzir = translator.translate(artigo['title'], dest='pt').text
#print(traduzir)

pesquisa = "Google"

# Definir uma funcao para coletar noticias
def dados():
    noticias_url = f"https://newsapi.org/v2/everything?q={pesquisa}&apiKey={api_key}"

    # fazer uma solicitacao
    response = requests.get(noticias_url)

    # converter os dados da resposta em json
    json_data = response.json()

    # obter os primeiros 5 artigos
    artigos = json_data["articles"][:5]

    titles = []
    descricoes = []
    urls = []
    imagens = []

    for artigo in artigos:
        # titlo
        titles.append(translator.translate(artigo['title'], dest='pt').text)

        # descricoes
        descricoes.append(translator.translate(artigo['description'], dest='pt').text)

        # urls
        urls.append(artigo['url'])

        # imagens
        imagens.append(artigo['urlToImage'])


    # retornando o título
    return [titles]

#chamar a funcao
print(dados())
