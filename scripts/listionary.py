# -*- coding = utf-8 -*-
import random
from art import *

class Game:

    def __init__(self, name):

        ################################################################
        # Variables globales definidas en el inicializador de la clase.#
        # @self.player -> Atributos del jugador (nombre y puntos)      #
        # @self.goods -> Lista de respuestas buenas                    #
        # @self.bads -> Lista de respuestas malas                      #
        # @self.pwin y @self.plose -> dibujo ASCII                     #
        ################################################################ 
        self.player = {'name': name, 'point': 0}
        self.goods, self.bads = [], []
        self.pwin = """
                        _____________
                       |             |
                       |  000   000  |
                       |  000   000  |
                       |             |
                       |  000   000  |
                       |   0000000   |
                       |_____________|
        """
        self.plose = """
                        _____________
                       |             |
                       |  000   000  |
                       |  000   000  |
                       |             |
                       |   0000000   |
                       |  000   000  |
                       |_____________|
        """
    ############################################################
    # Funcion que almacena los mensajes a mostrar en una lista.#
    # recive un numero (posicion) y devuelve el mensaje.       #
    # @menssage -> Variable que almacena la lista de mensajes. #
    ############################################################
    def messages(self, number):
        message = [
            # Mensaje de inicio de juego (Primer nivel - Noob)
            '\33[93m' + '\n**Get Ready Noob** ' + '\33[0m' + 'POINTS: {}'.format(self.player['point']),
            # Mensaje de avance de nivel (Segundo nivel - Intermedio)
            '\33[93m' + '\n**Well Done!!. Let\'s Level Up** ' + '\33[0m' + 'POINTS: {}/60'.format(self.player['point']),
            # Mensaje de avance de nivel (Tercer nivel - Expert)
            '\33[93m' + '\n**Great!! The Final Level** ' + '\33[0m' + 'POINTS: {}/120'.format(self.player['point']),
            # Mensaje de perder el juego en el primer nivel
            '\33[93m' + '\n**YOU LOSE!! Minimum Points Needed 40/60 for Next Level** ' + '\33[0m' + 'POINTS REACHED: {}'.format(self.player['point']),
            # Mensaje de perder el juego en segundo nivel
            '\33[93m' + '\n**YOU LOSE!! Minimum Points Needed 100/120 for Last Level** ' + '\33[0m' + 'POINTS REACHED: {}'.format(self.player['point']),
            # Mensaje de perder el juego sin alcanzar el puntaje final
            '\33[93m' + '\n**YOU LOSE!! Points Needed To Win > 160** ' + '\33[0m' + 'POINTS REACHED: {}'.format(self.player['point']),
            # Mensaje de victoria si alcanza todos los puntos necesarios
            '\33[93m' + '\n**YOU WIN!! Points Reached {} of 180 Possible** '.format(self.player['point']) + '\33[0m' + '\nCORRECTS = {} \nINCORRECTS = {}'.format(len(self.goods), len(self.bads))
        ]
        print(message[number])


    ############################################################
    # Funcion que muestra en pantalla las preguntas y compara  #
    # la respuesta con lo que introduce el jugador en consola, #
    # Si la respuesta es correcta suma 10 puntos y 0 en caso   #
    # de que sea erronea.                                      #
    ############################################################
    def test(self, question):
        print('\n' + question['question'])
        anwser = input(">>> ")
        if anwser.upper() == question['correct']:
            self.player['point'] += 10
            self.goods.append(anwser)
            print('\x1b[92;5m'+'Correct, +10 Points!!'+'\x1b[0m')
        else:
            self.bads.append(anwser)
            print('\x1b[31;5m'+'Incorrect +0 Points!! Anwser: {}'.format(question['correct']) +'\x1b[0m')
            

    #############################################################
    # Funcion que lleva los niveles por los que pasa el jugador #
    # dependiendo el puntaje alcanzado.                         #
    # @self.message() -> Se llama funcion y se envia el numero  #
    # del mensaje a mostrar.                                    #
    # @self.cicle() -> Se llama a la funcion ciclo de preguntas #
    # y se envia como parametro el nivel.                       #
    #############################################################
    def levels(self):
        level = 'noob'
        while True:
            if len(self.goods) == 0 and len(self.bads) == 0:
                self.messages(0)
                self.cicle(level)
                level = 'inter'
            elif level == 'inter' and self.player['point'] >= 40:
                self.messages(1)
                self.cicle(level)
                level = 'expert'
            elif level == 'expert' and self.player['point'] >= 100:
                self.messages(2)
                self.cicle(level)
                level = 'final'
            else:
                if level == 'inter':
                    print(self.plose)
                    self.messages(3)
                    break
                elif level == 'expert':
                    print(self.plose)
                    self.messages(4)
                    break
                elif level == 'final' and self.player['point'] < 160:
                    print(self.plose)
                    self.messages(5)
                    break
                else:
                    print(self.pwin)
                    self.messages(6)
                    break

    
    #####################################################################
    # Funcio que lleva el cilo de preguntas, por defecto se establece   #
    # 6 preguntas por nivel. Las preguntas son escogidas aleatoriamente #
    # por un numero random y que no se puede repetir.                   #
    # @used -> Almacena los numeros de las preguntas que van saliendo   #
    # (con el fin de no repetir las preguntas)                          #
    # @self.question(parametro) -> Se llama a la funcion question y se  #
    # le envia los parametros de nivel y numero.                        #
    # @self.test(parametro) -> Se llama la funcion test y se le envia   #
    # la pregunta obtenida en la funcion question para que imprima en   #
    # pantalla.                                                         #
    #####################################################################
    def cicle(self, level):
        limit, used = 0, []
        while limit < 6:
            number = random.randint(0, 8)
            if number not in used:
                limit += 1
                used.append(number)
                question = self.questions(level, number) 
                self.test(question)
            else:
                continue
    
    
    #####################################################################
    # Funcion que almacena todas las preguntas del juego divididas por  #
    # niveles. Consta de 3 opciones como respuesta y una sola correcta. #
    #####################################################################
    def questions(self, level, number):
        noob = {
            # First
            0: {'question': """How is defined a List in Python?\n \nA. Values between () \nB. Values between {} \nC. Values between []""", 'correct': 'C'},
            # Second
            1: {'question': """How is defined a Dict in Python?\n \nA. Values between {} \nB. Values between '' \nC. Values between +""", 'correct': 'A'},
            # Third
            2: {'question': """Lists are:\n \nA. Collections unordered \nB. Collections ordered \nC. Collections unindexed""", 'correct': 'B'},
            # Fourth
            3: {'question': """Dicts are:\n \nA. Unchangeables \nB. Unindexed \nC. Changeables and Indexed""", 'correct': 'C'},
            # Fifth
            4: {'question': """Can Lists have any type of items?\n \nA. True \nB. False""", 'correct': 'A'},
            # Sixth
            5: {'question': """Dicts structure are:\n \nA. Value-Position \nB. Key-Value \nC. Index position""", 'correct': 'B'},
            # Seventh
            6: {'question': """Can a List permit negative Index?\n \nA. Yes, It Can \nB. No, It's imposible \nC. Some cases""", 'correct': 'A'},
            # Eighth
            7: {'question': """Can a Dict have a List inside?\n \nA. True \nB. False \nC. I don't know""", 'correct': 'A'},
            # ninth
            8: {'question': """Is this posible in a list x[0]?\n \nA. Yes, it is! \nB. No, it isn't \nC. How is it possible?""", 'correct': 'A'}
        }
        inter = {
            # First
            0: {'question': """Which is the output of:\nx = len([1,2,3,4])\nprint(x)\n \nA. 0 \nB. 4 \nC. 6""", 'correct': 'B'},
            # Second
            1: {'question': """Which is the output of:\nx = ['Hello', 'world', 10, 1]\nprint(x[3])\n \nA. 10 \nB. ['world']\nC. 1""", 'correct': 'C'},
            # Third
            2: {'question': """Which is the output of:\nxs = {'name':'Mark', 'surname':'Wallet', 'age':25}\nxs['age'] = 30\nprint(xs)\n \nA. {'name': 'Mark', 'surname': 'Wallet', 'age':30} \nB. {'name': 'Mark', 'surname': 'Wallet', 'age':25, 'age': 30 } \nC. {'name': 'Mark', 'surname': 'Wallet', 'age':55}""", 'correct': 'A'},
            # Fourth
            3: {'question': """Which is the output of:\nys = {'name': 'Jose', 'age':20}\nprint(ys.get('surname', 0))\n  \nA. Jose \nB. 0 \nC. surname """, 'correct': 'B'},
            # Fifth
            4: {'question': """Which is the output of:\ns = [5,8,6,3,1,2]\ns.sort()\nprint(s)\n \nA. [8,6,5,3,2,1] \nB. [8,1,2,3,5,6] \nC. [1,2,3,5,6,8]""", 'correct': 'C'},
            # Sixth
            5: {'question': """Which is the output of:\nx = [10, 20, 30]\nprint(sum(x), min(x), max(x))\n \nA. 60 10 30 \nB. 50 20 10 \nC. 10 20 30""", 'correct': 'A'},
            # Seventh
            6: {'question': """Which is the output of:\ny = {'A': 'Python, 'B': 'Django'}\ny.setdefault('C', 'Data Science')\nprint(y)\n \nA. {'A': 'Python, 'B': 'Django'} \nB. {'A': 'Python, 'B': 'Django', 'C': 'Data Science'} \nC. KeyError""", 'correct': 'B'},
            # Eighth
            7: {'question': """Which is the output of:\nx = [{'A': 10}, {'A': 20}, {'A':30}]\nprint(x[1]['A'])\n \nA. {'A':30} \nB. [{'A'}] \nC. 20""", 'correct': 'C'},
            # Ninth
            8: {'question': """Which is the output of:\nb = [0, 80, 100, 'Hi', '10']\nb.pop(-2)\nprint(b)\n \nA. [0, 80, 100, '10'] \nB. [] \nC. [0, 80, 3, 'Hi', '10']""", 'correct': 'A'}
        }
        expert = {
            # First
            0: {'question': """Which is the output of:\nxs = [x*2 for x in range(10) if x % 2 == 0]\nprint(xs)\n \nA. TypeError \nB. [2, 4, 6, 8, 10] \nC. [0, 4, 8, 12, 16]""", 'correct': 'C'},
            # Second
            1: {'question': """Which is the output of:\nd = {'A': 1, 'B': {'C': 2, 'D': {'E': 3}}}\ndef recursive(d):\n for k,v in param.items():\n  if isinstance(v, int):\n   print(k, ' ', v)\n  else:\n   recursive(v)\n \nA. (A B C D E) \nB. (A 1 C 2 E 3) \nC. (1 2 3)""", 'correct': 'B'},
            # Third
            2: {'question': """Which is the output of:\nl = [10, 20, 30, 40, 50, 60, 70, 80]\nprint(l[::-2])\n \nA. [80, 60, 40, 20] \nB. [10, 30] \nC. [20, 40, 60, 80]""", 'correct': 'A'},
            # Fourth
            3: {'question': """Which is the output of:\nd = {'F': 1, 'G':5}\nprint(d[0])\n \nA. 'F': 1 \nB. KeyError \nC. 1""", 'correct': 'B'},
            # Fifth
            4: {'question': """Which is the output of:\nd = {'A': 30, 'B':10, 'C':20}\nd.sort()\nprint(d)\n \nA. {'B':10, 'C':20, 'A':30} \nB. {'A':10, 'B':20, 'C':30} \nC. AttributeError""", 'correct': 'C'},
            # Sixth
            5: {'question': """Which is the output of:\nx = ['Cat', 'Dog', 'Parrot']\nprnt(x[1:])\n \nA. NameError \nB. ['Dog', 'Parrot'] \nC. ['Cat', 'Dog']""", 'correct': 'A'},
            # Seventh
            6: {'question': """Which is the output of:\nx = [1, 2, 3]\nprint(x*2)\n \nA. [[1,2,3], [1,2,3]] \nB. [1,2,3,1,2,3] \nC. [2,4,6]""", 'correct': 'B'},
            # Eighth
            7: {'question': """Which is the output of:\nz = []\nx = [lambda a, b: z.append(x*y) for x,y in zip(a, b)]\nx([4,5,6], [4,5,6])\nprint(sum(z))\n \nA. 110 \nB. 55 \nC. 77""", 'correct': 'C'},
            # Ninth
            8: {'question': """Which is the output of:\nx = lambda x, y: {x: y*3}\nprint(x('A', [1,2,3]))\n \nA. {'A': [1,2,3,1,2,3,1,2,3]} \nB. {'A': [3,6,9]} \nC. {'A': 15}""", 'correct': 'A'}
        }

        if level == 'noob':
            return noob[number]
        elif level == 'inter':
            return inter[number]
        else:
            return expert[number]



if __name__ == "__main__":

    ###############################
    # Nombre en consola del juego #
    ###############################
    print(text2art('LISTIONARY'))
    #####################
    # Breve descripcion #
    #####################
    print('\x1b[91m'+'A Python (List and Dictionary) Test'.center(65, '*') + '\x1b[0m')
    ######################
    # Nombre del jugador #
    ######################
    name = input("\nType your name: ")
    print("")
    #############################################
    # Mensaje de bienvenida y detalle del juego #
    #############################################
    print('Welcome {}. Do Ur Best Effort And Anwser Correctly. \nEach Level Consists Of 6 Questions, Be Sure To Make Enough Points To Level Up. \nGood luck!!!\n'.format(name))
    ###################################################
    # Pausa del juego para comenzar cuando este listo #
    ###################################################
    input('\x1b[5m' + 'Press enter to start >>>' + '\x1b[0m')
    ######################
    # Llamado a la clase #
    ######################
    game = Game(name)
    game.levels()
    