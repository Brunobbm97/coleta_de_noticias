from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkscrolledframe import ScrolledFrame 
# IMPORTANDO REQUESTS
import requests
# Importando o google tradutor
from googletrans import Translator

from io import BytesIO

#Definição das cores
cor_de_fundo = "#f2f2f2" # Cinza claro
cor_texto = "#333333" # Cinza escuro
cor_detaque = "#197602" # Azul

janela = Tk()
janela.title("Notícias")
janela.geometry("612x600")
janela.configure(bg=cor_de_fundo)
janela.resizable(width=FALSE, height=FALSE)

#criando as divisoes da janela
frameCima = Frame(janela, width=612, height=55, bg=cor_de_fundo, relief="flat")
frameCima.grid(row = 0, column=0, sticky=NSEW)

frameMeio = Frame(janela, width=590, height=50, bg=cor_de_fundo, relief="solid")
frameMeio.grid(row = 1, column=0, sticky=NSEW)

frameBaixo = Frame(janela, width=590, height=450, bg=cor_de_fundo, relief="raised")
frameBaixo.grid(row = 2, column=0, sticky=NSEW)

# criacao de Scroll
sf = ScrolledFrame(frameBaixo, width = 590, height = 450, bg=cor_de_fundo)
sf.grid(row=0, column=0, sticky=NSEW, padx=0, pady=5)

framecanva = sf.display_widget(Frame, bg=cor_texto)


#criando logo
app_img = Image.open('categoria.png')
app_img = app_img.resize((50,50))
app_img = ImageTk.PhotoImage(app_img)
app_logo = Label(frameCima, image=app_img, width=900, compound=LEFT, padx=5, 
                 relief=FLAT, anchor=NW, bg=cor_de_fundo, fg=cor_detaque)
app_logo.place(x=5, y=8)
app_ = Label(frameCima, text="Automacao de Coleta de noticias", compound=LEFT, padx=5, relief=FLAT, anchor=NW,
             font=('Verdana 17 bold'), bg=cor_de_fundo, fg=cor_detaque)
app_.place(x=55, y=10)
app_linha = Label(frameCima, width=612, relief=GROOVE, anchor=NW,
             font=('Verdana 1'), bg=cor_de_fundo, fg=cor_detaque)
app_linha.place(x=5, y=52)




# Inicializar o tradutor
translator = Translator()

api_key = "27954b9558664a5c84b75b4377b531ba"

# traduzir = translator.translate(artigo['title'], dest='pt').text
#print(traduzir)


# Definir uma funcao para coletar noticias
def pesquisar_dados(pesquisa):
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
    return [titles, descricoes, urls, imagens]

def apresentar_dados():
    pesquisa = app_procura_e.get()
    if not pesquisa:
        messagebox.showerror("Consulta Vazia", "Por favor, insira uma consulta de pesquisa")
        return
    
    dados = pesquisar_dados(pesquisa)
    titles, descricoes, urls, imagens = dados[0],dados[1],dados[2],dados[3]

    # criacao de quadros para exibir noticias
    frames = {}
    num_row = 0

    for i in range(len(titles)):
        frames["F{}".format(i)] = i
        frames["F{}".format(i)] = Frame(framecanva, width=580, height=140, bg=cor_de_fundo,)
        frames["F{}".format(i)].grid(row = num_row, column=0, sticky=NSEW, pady=1)

        # carregar e exibir a imagem da noticia
        response = requests.get(imagens[i])
        imagem_dado = response.content
        imagem = Image.open(BytesIO(imagem_dado))
        imagem = imagem.resize((110,100))
        foto = ImageTk.PhotoImage(imagem)

        imagem_label = Label(frames["F{}".format(i)], image = foto)
        imagem_label.image = foto
        imagem_label.place(x=9, y=5)

        app_titulo = Label(frames["F{}".format(i)], text=titles[i], compound=LEFT, justify='left', wraplength=350,
             font=('Arial 11 bold'), bg=cor_de_fundo, fg=cor_detaque)
        app_titulo.place(x=130, y=5)

        app_desc = Label(frames["F{}".format(i)], text=titles[i], compound=LEFT, justify='left', wraplength=350,
             font=('Arial 9'), bg=cor_de_fundo, fg=cor_texto)
        app_desc.place(x=130, y=45)

        b_titulo = Button(frames["F{}".format(i)], text="Copiar Titulo", overrelief=RIDGE, bg=cor_de_fundo, fg=cor_texto,
                          font=('Ivy 10'), anchor="center", relief=FLAT)
        b_titulo.place(x=500, y=5)
        b_titulo.bind("<Button-1>", lambda e, title=titles[i]: callback_title(title))

        b_desc = Button(frames["F{}".format(i)], text="Copiar Texto", overrelief=RIDGE, bg=cor_de_fundo, fg=cor_texto,
                          font=('Ivy 10'), anchor="center", relief=FLAT)
        b_desc.place(x=500, y=40)
        b_desc.bind("<Button-1>", lambda e, texto=descricoes[i]: callback_texto(texto))

        b_link = Button(frames["F{}".format(i)], text="Copiar Link", overrelief=RIDGE, bg=cor_de_fundo, fg=cor_texto,
                          font=('Ivy 10'), anchor="center", relief=FLAT)
        b_link.place(x=500, y=75)
        b_link.bind("<Button-1>", lambda e, link=urls[i]: callback_link(link))

        # incrementando o valor da linha
        num_row += 1


def callback_title(title):
    janela.clipboard_clear()
    janela.clipboard_append(title)
    janela.update()
    messagebox.showinfo("Texto Copiado", "Titulo copiado para a area de transferência")

def callback_texto(texto):
    janela.clipboard_clear()
    janela.clipboard_append(texto)
    janela.update()
    messagebox.showinfo("Texto Copiado", "Titulo copiado para a area de transferência")

def callback_link(link):
    janela.clipboard_clear()
    janela.clipboard_append(link)
    janela.update()
    messagebox.showinfo("Texto Copiado", "Titulo copiado para a area de transferência")


# interface para procurar

app_procura = Label(frameMeio, text="Consulta ou pesquisa",font=('Ivy 11'), bg=cor_de_fundo)
app_procura.place(x=10, y=10)
app_procura_e = Entry(frameMeio, bg=cor_de_fundo, font=('Ivy 14'))
app_procura_e.place(x=165, y=10)
app_procura_b = Button(frameMeio,command=apresentar_dados, text="Pesquisar", width=10, bg=cor_de_fundo)
app_procura_b.place(x=380, y=10)


janela.mainloop()
