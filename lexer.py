import sys

from ts import TS
from tag import Tag
from token import Token


class Lexer():
    '''
   Classe que representa o Lexer (AFD):
   
   [1] Voce devera se preocupar quando incremetar as linhas e colunas,
   assim como, quando decrementar ou reinicia-las. Lembre-se, ambas 
   comecam em 1.
   [2] Toda vez que voce encontrar um lexema completo, voce deve retornar
   um objeto Token(Tag, "lexema", linha, coluna). Cuidado com as
   palavras reservadas, que ja sao cadastradas na TS. Essa consulta
   voce devera fazer somente quando encontrar um Identificador.
   [3] Se o caractere lido nao casar com nenhum caractere esperado,
   apresentar a mensagem de erro na linha e coluna correspondente.
   Obs.: lembre-se de usar o metodo retornaPonteiro() quando necessario. 
         lembre-se de usar o metodo sinalizaErroLexico() para mostrar
         a ocorrencia de um erro lexico.
   '''

    def __init__(self, input_file):
        try:
            self.input_file = open(input_file, 'rb')
            self.lookahead = 0
            self.n_line = 1
            self.n_column = 1
            self.ts = TS()
            self.n_error = 1
        except IOError:
            print('Erro de abertura do arquivo. Encerrando.')
            sys.exit(0)

    def closeFile(self):
        try:
            self.input_file.close()
        except IOError:
            print('Erro ao fechar arquivo. Encerrando.')
            sys.exit(0)

    def sinalizaErroLexico(self, message):
        print("[Erro Lexico]: ", message, "\n")
        self.n_error += 1


    def retornaPonteiro(self):
        if (self.lookahead.decode('ascii') != ''):
            self.input_file.seek(self.input_file.tell() - 1)
            self.n_column -= 1

    def printTS(self):
        self.ts.printTS()

    def inc_line(self):
        self.n_line += 1
        self.init_column()
        self.inc_column()

    def init_column(self):
        self.n_column = 0

    def inc_column(self):
        self.n_column += 1

    def proxToken(self):
        # Implementa um AFD.

        estado = 1
        lexema = ""
        c = '\u0000'
        cont_ponto = 0
        while (True):
            self.lookahead = self.input_file.read(1)
            c = self.lookahead.decode('ascii')
            # print('***'+str(c))
            self.inc_column()  # ** Atualiza a coluna ao ser EOF
            if (c == ''):
                self.n_column -= 1

            if (estado == 1):

                if (c == ''):
                    self.n_column -= 1
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column)

                elif (c == ' ' or c == '\t' or c == '\n' or c == '\r'):
                    if c == '\n':  # **Regras linha e coluna
                        self.inc_line()
                    estado = 1
                elif (c == '='):
                    estado = 2
                elif (c == '!'):
                    estado = 4
                elif (c == '<'):
                    estado = 6
                elif c == '>':
                    estado = 9
                elif (c.isdigit()):
                    lexema += c
                    estado = 12
                elif (c.isalpha()):
                    lexema += c
                    estado = 14
                # -----
                elif (c == '/'):
                    estado = 16
                elif (c == '+'):
                    estado = 17
                elif (c == '-'):
                    estado = 18
                elif (c == '*'):
                    estado = 19
                elif (c == '{'):
                    estado = 20
                elif (c == '}'):
                    estado = 21
                elif (c == '('):
                    estado = 22
                elif (c == ')'):
                    estado = 23
                elif (c == '"'):
                    lexema += c
                    estado = 24
                elif (c == ','):                    
                    estado = 25
                elif (c == ';'):                    
                    estado = 26
                else:
                    self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                                            str(self.n_line) + " e coluna " + str(self.n_column - 1))
                    if self.n_error>3:
                      return None
            elif (estado == 2):
                if (c == '='):
                    return Token(Tag.OP_IGUAL, "==", self.n_line, self.n_column)

                    # self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                # str(self.n_line) + " e coluna " + str(self.n_column))

                self.retornaPonteiro()
                return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)
            elif (estado == 4):
                if (c == '='):
                    return Token(Tag.OP_DIFERENTE, "!=", self.n_line, self.n_column)

                self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                                        str(self.n_line) + " e coluna " + str(self.n_column - 1))
                if self.n_error > 3:
                   return None
            elif (estado == 6):
                if (c == '='):
                    return Token(Tag.OP_MENOR_IGUAL, "<=", self.n_line, self.n_column)

                self.retornaPonteiro()
                return Token(Tag.OP_MENOR, "<", self.n_line, self.n_column)
            elif (estado == 9):
                if (c == '='):
                    return Token(Tag.OP_MAIOR_IGUAL, ">=", self.n_line, self.n_column)

                self.retornaPonteiro()
                return Token(Tag.OP_MAIOR, ">", self.n_line, self.n_column)
            elif (estado == 12):

                if (c.isdigit()):
                    lexema += c
                elif cont_ponto <1 and c == '.':
                    cont_ponto += 1
                    lexema += c
                else:
                    self.retornaPonteiro()
                    return Token(Tag.NUM, lexema, self.n_line, self.n_column)
            elif (estado == 14):
                if (c.isalnum()):
                    lexema += c
                else:
                    self.retornaPonteiro()
                    token = self.ts.getToken(lexema)

                    if (token is None):
                        token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    token.setLinha(self.n_line)
                    token.setColuna(self.n_column)

                    return token
            elif (estado == 16):
                if (c == '/'):

                    while c != '\n':
                        self.lookahead = self.input_file.read(1)
                        c = self.lookahead.decode('ascii')
                    if c == '\n':
                       self.inc_line()
                    estado = 1

                elif (c == '*'):
                    comentario=''
                    while True:

                        self.lookahead = self.input_file.read(1)
                        c = self.lookahead.decode('ascii')
                        self.inc_column()
                        if c == '\n':
                            self.inc_line()
                        if c == '':

                            self.sinalizaErroLexico("Comentario não fechado na linha " +
                            str(self.n_line) + " e coluna " + str(self.n_column))
                            self.retornaPonteiro()
                            return None
                        if c == '*':
                            comentario = c

                        elif c == '/' and comentario=='*':
                            comentario += c
                        else:
                           comentario=''

                        if comentario == '*/':

                            break

                    estado = 1

                else:
                    self.retornaPonteiro()
                    return Token(Tag.OP_DIV, "/", self.n_line, self.n_column)
            elif (estado == 17):
                self.retornaPonteiro()
                return Token(Tag.OP_AD, "+", self.n_line, self.n_column)
            elif (estado == 18):
                self.retornaPonteiro()
                return Token(Tag.OP_MIN, "-", self.n_line, self.n_column)
            elif (estado == 19):
                self.retornaPonteiro()
                return Token(Tag.OP_MUL, "*", self.n_line, self.n_column)
            elif (estado == 20):
                self.retornaPonteiro()
                return Token(Tag.SMB_OBC, "{", self.n_line, self.n_column)
            elif (estado == 21):
                self.retornaPonteiro()
                return Token(Tag.SMB_CBC, "}", self.n_line, self.n_column)
            elif (estado == 22):
                self.retornaPonteiro()
                return Token(Tag.SMB_OPA, "(", self.n_line, self.n_column)
            elif (estado == 23):
                self.retornaPonteiro()
                return Token(Tag.SMB_CPA, ")", self.n_line, self.n_column)
            elif (estado == 24):
                if c == '"':
                    lexema += c
                    return Token(Tag.CHAR, lexema, self.n_line, self.n_column)
                while True:
                    lexema += c
                    self.inc_column()
                    if c == '"':
                        return Token(Tag.CHAR, lexema, self.n_line, self.n_column - 1)
                        break

                    elif c == '\n':
                        self.sinalizaErroLexico('"'+ " não fechada na linha " +
                              str(self.n_line) + " e coluna " + str(self.n_column - 2))
                        self.inc_line()
                        if self.n_error > 3:
                           return None
                    elif c == '':
                        self.sinalizaErroLexico('"'+ " não fechada na linha "  +
                        str(self.n_line) + " e coluna " + str(self.n_column - 1))

                        return None
                    self.lookahead = self.input_file.read(1)
                    c = self.lookahead.decode('ascii')
                estado = 1
                self.retornaPonteiro()
            elif (estado == 25):
                self.retornaPonteiro()
                return Token(Tag.SMB_COM, ",", self.n_line, self.n_column)
            elif (estado == 26):
                self.retornaPonteiro()
                return Token(Tag.SMB_SEM, ";", self.n_line, self.n_column)
            # [TAREFA] Quem quiser, pode completar a logica para o cometario conforme o AFD.

            # fim if's de estados
        # fim while
