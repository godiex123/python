# python 3.7
# Usage: searchRegex.py <Phrase to search> Search for a phrase into all txt files where is located. 
#  searchRegex.py <help> show use guide.
import sys, re, os

path = os.path.abspath('.')
if len(sys.argv) == 2 and sys.argv[1] == 'help':
    print(''' Uso: searchRegex.py [FRASE A BUSCAR] | [EXPRESION REGULAR]
    Ejemplo: searchRegex.py 'Hello World' | '[a-zA-Z0-9]\w+?'
    Nota: Buscara en todos los archivos txt donde se encuentre el .py 
    ''')
elif len(sys.argv) == 2 and sys.argv[1] != '':
    matches = []
    for element in os.listdir(path):
        if os.path.isfile(element):
            if element.endswith('.txt'):
                with open(element, 'r') as f:
                    data = f.read()
                    phraseRegex = re.compile(r'' + str(sys.argv[1]), re.IGNORECASE | re.DOTALL | re.VERBOSE)
                    for groups in phraseRegex.findall(data):
                        matches.append(groups)
    if len(matches) > 0:
        print('\n'.join(matches))
    else:
        print('Phrase not found')
    