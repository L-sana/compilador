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
         self.contadorErros = 0
         self.lastChar = ''
         self.ts = TS(self.n_line, self.n_column)
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
      print("[Erro Lexico]: ", message, "\n");

   def retornaPonteiro(self):
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()-1)
         self.n_column -= 1

   def proximoPonteiro(self):
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()+1)

   def printTS(self):
      self.ts.printTS()

   def proxToken(self):

      estado = 1
      lexema = ""
      c = '\u0000'

      while(True):

         if(self.contadorErros == 3):
            return None

         self.lookahead = self.input_file.read(1)
         self.n_column += 1
         c = self.lookahead.decode('ascii')
         self.lastChar = c

         if(estado == 1):
            if(c == ''):
               self.n_column = 1 
               return Token(Tag.EOF, "EOF", self.n_line, self.n_column)

            elif(c == ' ' or c == '\t' or c == '\r'):
               estado = 1
            elif(c == '='):
               estado = 2
            elif(c == '!'):
               estado = 5
            elif(c == '<'):
               estado = 7
            elif(c == '>'):
               estado = 10
            elif(c == '+'):
               estado = 13
            elif(c == '-'):
               estado = 14
            elif(c == '*'):
               estado = 15
            elif(c == '/'):
               estado = 16
            elif(c == '{'):
               estado = 19
            elif(c == '}'):
               estado = 20
            elif(c == '('):
               estado = 21
            elif(c == ')'):
               estado = 22
            elif(c == ','):
               estado = 23
            elif(c == ';'):
               estado = 24
            elif(c == '"'):
               estado = 25
            elif(c.isdigit()):
               lexema += c
               estado = 29
            elif(c.isalpha()):
               lexema += c
               estado = 31
            elif(c == '.'):
               estado = 32
            elif(c == '\n'):
                self.n_line += 1
                self.n_column = 1
            else:
               print(c)
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               self.contadorErros += 1
               continue
         elif(estado == 2):
            if(c == '='):
               return Token(Tag.OP_EQ, "==", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)

         elif(estado == 5):
            if(c == '='):
               return Token(Tag.OP_NE, "!=", self.n_line, self.n_column)

            self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
            str(self.n_line) + " e coluna " + str(self.n_column))
            self.contadorErros += 1
            continue

         elif(estado == 7):
            if(c == '='):
               return Token(Tag.OP_LE, "<=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_LT, "<", self.n_line, self.n_column)

         elif(estado == 10):
            if(c == '='):
               return Token(Tag.OP_GE, ">=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_GT, ">", self.n_line, self.n_column)

         elif(estado == 13):
            self.retornaPonteiro()
            return Token(Tag.OP_ADD, "+", self.n_line, self.n_column)

         elif(estado == 14):
            self.retornaPonteiro()
            return Token(Tag.OP_MIN, "-", self.n_line, self.n_column)

         elif(estado == 15):
            self.retornaPonteiro()
            return Token(Tag.OP_MUL, "*", self.n_line, self.n_column)

         elif(estado == 19):
            self.retornaPonteiro()
            return Token(Tag.SMB_OBC, "{", self.n_line, self.n_column)

         elif(estado == 20):
            self.retornaPonteiro()
            return Token(Tag.SMB_CBC, "}", self.n_line, self.n_column)

         elif(estado == 21):
            self.retornaPonteiro()
            return Token(Tag.SMB_OPA, "(", self.n_line, self.n_column)

         elif(estado == 22):
            self.retornaPonteiro()
            return Token(Tag.SMB_CPA, ")", self.n_line, self.n_column)

         elif(estado == 23):
            self.retornaPonteiro()
            return Token(Tag.SMB_COM, ",", self.n_line, self.n_column)

         elif(estado == 24):
            self.retornaPonteiro()
            return Token(Tag.SMB_SEM, ";", self.n_line, self.n_column)

         elif(estado == 25):
            if(c == '') or (c == '\n'):
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               self.contadorErros += 1
               self.n_line += 1
               self.n_column = 1
               #continue
            if(c != '"'):
               lexema += c
            else:
               return Token(Tag.CHAR_CONST, lexema, self.n_line, self.n_column)

         elif(estado == 16):
            if((len(lexema) == 0) and c == '/'):
               self.n_line += 1
               self.input_file.readline()
               estado = 1
               lexema = ''
               continue

            if(c == '*'):
              lexema += c
              estado = 17

            if(len(lexema) == 0):
               self.retornaPonteiro()
               return Token(Tag.OP_DIV, "/", self.n_line, self.n_column)

         elif(estado == 17):
            if(c == ''):
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               self.contadorErros += 1
               continue

            lexema += c
            if(c == '\n'):
               self.n_column = 1 
               self.n_line += 1


            if(c == '/'):
               if('*/' not in lexema):
                  self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                  str(self.n_line) + " e coluna " + str(self.n_column))
                  self.contadorErros += 1
                  continue
               else:
                  estado = 1
                  lexema = ''
                  continue

         elif(estado == 29):
            if(c.isdigit()):
               lexema += c
            else:
               if(c == '.'):
                  lexema += c
                  estado = 32
               else:
                  self.retornaPonteiro()
                  return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)
         elif(estado == 31):
            if(c.isalnum()):
               lexema += c
            else:
               self.retornaPonteiro()
               token = self.ts.getToken(lexema, self.n_line, self.n_column)
               if(token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)

               return token

         elif(estado == 32):
            if(c.isdigit()):
               lexema += c
            else:
               if(lexema[-1] == '.'):
                  self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                  str(self.n_line) + " e coluna " + str(self.n_column))
                  self.contadorErros += 1
                  continue

               self.retornaPonteiro()
               return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)
# fim if's de estados
# fim while