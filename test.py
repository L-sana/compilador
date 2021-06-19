import os

from ts import TS
from tag import Tag
from token import Token

class Test():
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
        
      except IOError:
         print('Erro de abertura do arquivo. Encerrando.')
         sys.exit(0)
   def closeFile(self):
        try:
            self.input_file.close()
        except IOError:
            print('Erro ao fechar arquivo. Encerrando.')
            sys.exit(0)

if __name__ == '__main__':
    test=Test('prog1.txt')
    cont=0
    lookahead = test.input_file.read(1)
    c =lookahead.decode('ascii')
    

    while cont<150:
      cont+=1
      lookahead = test.input_file.read(1)
   

      c =lookahead.decode('ascii')
      if c=='\n':
         print('bn')
      elif c=='\r':
         print('br')
      elif c=='\t':
         print('bt')
      elif c=='"':
         print('PARENTESES')

      else:
         print(str(c))
   
    
    """
    x=test.input_file.read()
    print("len"+str(len(x)))
    print("xxx")
    print(test.)
    """