from tag import Tag
from token import Token

class TS:
   '''
   columnasse para a tabela de simbolos representada por um dicionario: {'chave' : 'valor'}
   '''
   def __init__(self,line=0,column=0):
      '''
      Repare que as palavras reservadas sao todas cadastradas
      a principio com linha e coluna em zero
      '''
      self.ts = {}

      self.ts['if'] = Token(Tag.KW_IF, 'if', line,column)
      self.ts['else'] = Token(Tag.KW_ELSE, 'else',line,column)
      self.ts['then'] = Token(Tag.KW_THEN, 'then',line,column)
      self.ts['print'] = Token(Tag.KW_PRINT, 'print', line,column)
      self.ts['while']=Token(Tag.KW_WHILE, 'while', line,column)
      self.ts['read']=Token(Tag.KW_READ, 'read', line,column)
      self.ts['write']=Token(Tag.KW_WRITE, 'write', line,column)
      self.ts['or']=Token(Tag.KW_OR, 'or', line,column)
      self.ts['and']=Token(Tag.KW_AND, 'and', line,column)
      self.ts['not']=Token(Tag.KW_WHILE, 'not', line,column)
      self.ts['program']=Token(Tag.KW_PROGRAM, 'program', line,column)

      
      

   def getToken(self, lexema):
      token = self.ts.get(lexema.lower()) #**
      return token

   def addToken(self, lexema, token):
      self.ts[lexema.lower()] = token #**

   def printTS(self):
      for k, t in (self.ts.items()):
         print(k, ":", t.toString())
