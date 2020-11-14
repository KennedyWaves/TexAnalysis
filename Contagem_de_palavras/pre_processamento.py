# coding: ISO-8859-1
import nltk
import string
import os
from unicodedata import normalize
nltk.download('stopwords')
nltk.download('rslp')

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

print()
print("LOADING DATA FROM: ")
print(__location__+"/preprocessado.txt AS UTF-8")

# Open the file with read only permit
f = open(__location__+"/preprocessado.txt", encoding="utf-8")
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

stopwordsNLTK = nltk.corpus.stopwords.words('english')

def removeStopWords(texto):
    
    frases=[]
    for(palavras, emocao) in texto:
        semStop = [p for p in palavras if p not in stopwordsNLTK]
        frases.append((semStop, emocao))
    return frases

textoSemStopWords = removeStopWords(textoSemPontuacao)
#print(['Sem Stopwords'] + textoSemStopWords)
print()

def retornaPalavras(texto):
    
    frasesPreProcessadas = []
    for(palavras, emocao) in texto:
        frasesPreProcessadas.extend(palavras)
    return frasesPreProcessadas

def buscaFrequencia(texto):
    qtd = nltk.FreqDist(texto) #retorna a frequencia de cada palavera
    return qtd

frequenciaSW = buscaFrequencia(retornaPalavras(textoSemStopWords))
lista=frequenciaSW.most_common(10000)
f= open("output.csv","w+")
f.write('word,freq')
print('FREQUENCIA_--------------------------')
for x in lista:
    content = '\n"'+x[0]+'","'+str(x[1])+'"'
    print(content)
    f.write(content)



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