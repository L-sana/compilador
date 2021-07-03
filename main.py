from tag import Tag
from token import Token
from lexer import Lexer
from parserAnali import ParserAnali

if __name__ == "__main__":
   lexer = Lexer('ProgramTestClass.pasc')
   print("Grupo: { \n    Lais Sana\n    Alan Eremita\n    Leandro Gama\n}\n******Recuperação de erro implementada")
   print("\n=>Lista de tokens:")
   parserAnali = ParserAnali(lexer)

   parserAnali.Programa()

   parserAnali.lexer.closeFile()

   print("\n=>Tabela de simbolos:")
   lexer.printTS()
   lexer.closeFile()
    
   print('\n=> Fim da compilacao')
