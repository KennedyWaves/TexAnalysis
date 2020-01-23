# coding: ISO-8859-1
import nltk
import string
import os
import numpy as np
from difflib import SequenceMatcher
from unicodedata import normalize
nltk.download('stopwords')
nltk.download('rslp')
stopwords = nltk.corpus.stopwords.words('portuguese')

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

print()
print("LOADING DATA FROM: ")
print(__location__+"/_chat.txt AS UTF-8")
# Open the file with read only permit
f = open(__location__+"/_chat.txt", encoding='latin-1')
# use readlines to read all lines in the file
# The variable "lines" is a list containing all lines in the file
lines = f.readlines()
# close the file after reading the lines.
f.close()

base=[]

for line in lines:
    pos = line.find(': ')
    if pos < 0:
        continue
    base.append((line[pos+2:],'neutro'))

classes=[('transito',['acidente','semaforo','atropelamento','carro','velocidade','onibus','veiculo','sinal','sinalizacao','transporte','avenida','placa'],0),('mobilidade',['Engarrafamento','Estacionamento','carro','pedestre','gente','pessoa','morador','vizinho','acesso','faixa','ponte','fechamento','cruzamento','ciclofaixa','sinal','bicicleta','bike','lombada','estacionamento,'],0),('Ocupação urbana',['Invasao,'],0),('Furtos',['assalto','comercio','roubo','pessoas','segurança,'],0),('Autoridade pública',['Secretaria','Guarda','Municipal','GMF','Floram','Associacao','Comandante','Coronel','Policial','Diope','Governo'],0),('Bairros',['Parque','Abrao','Posto','arvores','Entorno','Escola','Pista','terreno','Coqueiros'],0),('Ruas',['Tamandare','Max','Souza','Expressa','Aparecida','Abel','Capela'],0)]


# base = [('O amor é lindo!','alegria'),
#         ('Eu sou admirada por muitos.','alegria'), 
#         ('Me sinto completamente amado.','alegria'), 
#         ('Amar é maravilhoso!','alegria'), 
#         ('Estou me sentindo muito animado novamente.','alegria'), 
#         ('Eu estou muito bem hoje.','alegria'), 
#         ('Que belo dia para dirigir um carro novo!','alegria'), 
#         ('O dia está muito bonito!','alegria'), 
#         ('Estou contente com o resultado do teste que fiz no dia de ontem!','alegria'), 
#         ('Nossa amizade é amor, vai durar para sempre!', 'alegria'), 
#         ('Estou amedrontado.', 'medo'), 
#         ('Ele está me ameaçando à dias.', 'medo'), 
#         ('Isso me deixa apavorada!', 'medo'), 
#         ('Este lugar é apavorante?', 'medo'), 
#         ('Se perdermos outro jogo, seremos eliminados, e isso me deixa com pavor.', 'medo'), 
#         ('Tome cuidado com o lobisomem!', 'medo'), 
#         ('Se eles descobrirem, estamos encrencados.', 'medo'), 
#         ('Estou tremendo de medo.', 'medo'), 
#         ('Eu tenho muito medo dele.', 'medo'), 
#         ('Estou com medo do resultado dos meus testes.', 'medo')]

#print(['Base'] + base)
print()
def tokeniza(texto):
    
    tokens = []
    for(palavras, emocao) in texto:
        token = [p for p in palavras.split()]
        tokens.append((token, emocao))
    return tokens

tokens = tokeniza(base)
#print(['Tokens'] + tokens)
print()

def descapitaliza(texto):
    
    descapitalizado = []
    for(palavras, emocao) in texto:
        descap = [p.casefold() for p in palavras]
        descapitalizado.append((descap, emocao))
    return descapitalizado

textoDescapitalizado = descapitaliza(tokens)
#print(['Case Folding'] + textoDescapitalizado)
print()


def removeAcentos(texto):     
    frasesSemAcento = []
    for(palavras, emocao) in texto:
        semAcento = [normalize('NFKD', p).encode('ASCII','ignore').decode('ASCII') for p in palavras]
        frasesSemAcento.append((semAcento, emocao))
    return frasesSemAcento

textoSemAcentos = removeAcentos(textoDescapitalizado)
#print(['Sem acentos'] + textoSemAcentos)
print()

def removePontuacao(texto):
    frasesSemPonto = []
    for(frase, emocao) in texto:
        palavrasSemPonto = []
        for palavras in frase:
            semPonto=''
            semPonto = [char for char in palavras if char not in string.punctuation]
            palavraSemPonto = ''.join(semPonto)
            palavrasSemPonto.append(palavraSemPonto)
        frasesSemPonto.append((palavrasSemPonto,emocao))   
    return frasesSemPonto

textoSemPontuacao = removePontuacao(textoSemAcentos)
#print(['Sem pontuação'] + textoSemPontuacao)
print()    

stopwordsNLTK = nltk.corpus.stopwords.words('portuguese')
stopwordsSpanish = nltk.corpus.stopwords.words('spanish')

def removeStopWords(texto):
    
    frases=[]
    for(palavras, emocao) in texto:
        semStop = [p for p in palavras if p not in stopwordsNLTK]
        frases.append((semStop, emocao))
    return frases

textoSemStopWords = removeStopWords(textoSemPontuacao)

# def removeStopWordsSpanish(texto):
    
#     frases=[]
#     for(palavras, emocao) in texto:
#         semStop = [p for p in palavras if p not in stopwordsSpanish]
#         frases.append((semStop, emocao))
#     return frases

# textoSemStopWords = removeStopWordsSpanish(textoSemStopWords)
#print(['Sem Stopwords'] + textoSemStopWords)
print()

def retornaPalavras(texto):
    
    frasesPreProcessadas = []
    for(palavras, emocao) in texto:
        frasesPreProcessadas.extend(palavras)
    return frasesPreProcessadas


palavras= retornaPalavras(textoSemStopWords)
print(len(classes))
print()
print()
def fuzzy_search(search_key, word, strictness):
    similarity = SequenceMatcher(None, word, search_key)
    if(similarity.ratio() > strictness):
        return True
    else:
        return False
printClasses=""
for x in range(0,len(classes)):
    frequencia=0
    print()
    print()
    print("============"+classes[x][0]+"============")
    print()
    for palavra in palavras:
        if(palavra.find("http")<0):
            for termo in classes[x][1]:
                #print(levDist)
                if (fuzzy_search(termo,palavra,0.84)):
                    print(palavra+" = "+termo)
                    frequencia+=1
    printClasses+=classes[x][0]+","+str(frequencia)+"\n"
print()
print()
print("WARNING: THE OUTPUT IS ALREADY FORMATTED AS CSV!")
print()
print()
print("categoria,frequencia")
print(printClasses)


           

# def buscaFrequencia(texto):
#     qtd = nltk.FreqDist(texto) #retorna a frequencia de cada palavera
#     return qtd

# frequenciaSW = buscaFrequencia(retornaPalavras(textoSemStopWords))
# print('FREQUENCIA_--------------------------')
# print(frequenciaSW.most_common(10000)) #10000 primeiras palavas mais frequentes

# def aplicaStemmer(texto):
    
#     stemmer = nltk.stem.RSLPStemmer() #metodo para a utlizacao da lingua portuguesa
#     frasesStemming = []
#     for(palavras, emocao) in texto:
#         comStemming = [str(stemmer.stem(p)) for p in palavras]
#         frasesStemming.append((comStemming, emocao))
#     return frasesStemming

# textoStemming = aplicaStemmer(textoSemStopWords)
# print(['Stemming'] + textoStemming)
# print()

# textoPreProcessado = retornaPalavras(textoStemming)
# frequencia = buscaFrequencia(textoPreProcessado)

# print('FREQUENCIA_--------------------------')

# print(frequencia.most_common(100)) #50 primeiras palavas mais frequentes

# def removePalavrasRepetidas(freq):
#     palavras = freq.keys()
#     return palavras

# textoSemRepeticao = removePalavrasRepetidas(frequencia)

# def extraiPalavras(documento):
    
#     doc = set(documento)
#     carcteristicas = {}
#     for palavras in textoSemRepeticao:
#         carcteristicas['%s' % palavras] = (palavras in doc)
#     return carcteristicas

# caracteristicasFrase = extraiPalavras(['am', 'nov','dia'])
# print(caracteristicasFrase)
# print()

# baseCompleta = nltk.classify.apply_features(extraiPalavras, textoStemming) #aplica uma caracteristica (caracteristica,base a ser aplicada).    o objetivo aqui eh indicar quais palavras aparecem em cada tipo de frase. essa base que vai ser passada como parametro para o algoritmo de aprendizagem"""

# print(baseCompleta)