from tag import Tag
from token import Token

class TS:
   '''
   columnasse para a tabela de simbolos representada por um dicionario: {'chave' : 'valor'}
   '''
   def __init__(self, n_line, n_column):
      '''
      Repare que as palavras reservadas sao todas cadastradas
      a principio com linha e coluna em zero
      '''
      self.ts = {}

      self.ts['if'] = Token(Tag.KW_IF, 'if', n_line, n_column)
      self.ts['else'] = Token(Tag.KW_ELSE, 'else', n_line, n_column)
      self.ts['num'] = Token(Tag.KW_NUM, 'num', n_line, n_column)
      self.ts['char'] = Token(Tag.KW_CHAR, 'char', n_line, n_column)
      self.ts['while'] = Token(Tag.KW_WHILE, 'while', n_line, n_column)
      self.ts['or'] = Token(Tag.KW_OR, 'or', n_line, n_column)
      self.ts['and'] = Token(Tag.KW_AND, 'and', n_line, n_column)
      self.ts['not'] = Token(Tag.KW_NOT, 'not', n_line, n_column)
      self.ts['program'] = Token(Tag.KW_PROGRAM, 'program', n_line, n_column)
      self.ts['read'] = Token(Tag.KW_READ, 'read', n_line, n_column)
      self.ts['write'] = Token(Tag.KW_WRITE, 'write', n_line, n_column)

   def getToken(self, lexema, n_linha, n_coluna):
      token = self.ts.get(lexema)
      if(token is not None):
         token.setLinha(n_linha)
         token.setColuna(n_coluna)
      else:
         theset = set(k.lower() for k in self.ts)
         if lexema.lower() in theset:
            token = self.ts.get(lexema.lower())
      
      return token

   def addToken(self, lexema, token):
      self.ts[lexema] = token

   def printTS(self):
      for k, t in (self.ts.items()):
         print(k, ":", t.toString())
