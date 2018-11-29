# Crear una gramatica
import nltk
from nltk import CFG
from nltk.parse.generate import generate

Gramatica1 = CFG.fromstring("""

F -> SU P
SU -> 'juan' | 'pedro' | 'maria' | 'salgado'
P -> VT OD
P -> VI
VT -> 'ama' | 'lava' | 'peina' | 'adora'
OD -> 'paula' | 'antonio' | 'sultan'
VI -> 'corre' | 'salta' | 'camina'
""")

print('La gramatica:', Gramatica1)
print('Inicio =>', Gramatica1.start())
print('Producciones =>')

# Mostrar las producciones de la gramatica
print(Gramatica1.productions())

print('Cobertura de palabras ingresadas a la gramatica:')
mis_palabras = ['maria','corre', 'peina', 'pedro','ama']
print(mis_palabras)

try:
    #maría ama antonio
    Gramatica1.check_coverage(mis_palabras)
    print("Todas las palabras estan cubiertas")
except:
    print("Error")


print("\n\nGenerando sentencias:\n")
for sentence in generate(Gramatica1, n = 5): #si deseo ver todas las sentencias no usar parametro n
    print(' '.join(sentence))


print("\n\nArbol:\n")
Frase = ['maria', 'peina', 'sultan']
parser = nltk.ChartParser(Gramatica1)
for arbol in parser.parse(Frase):
    print(arbol)

