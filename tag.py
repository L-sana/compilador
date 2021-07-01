from enum import Enum

class Tag(Enum):
   '''
   Uma representacao em constante de todos os nomes 
   de tokens para a linguagem.
   '''
   #Analisador Léxico
   # Fim de arquivo
   EOF = -1

   # Palavras-chave
   KW_IF = 0
   KW_ELSE = 1
   KW_THEN = 2
   KW_PRINT = 3
   KW_WHILE = 4
   KW_READ =5
   KW_WRITE =6
   KW_OR = 7
   KW_AND =8
   KW_NOT = 9
   KW_READ=50
   KW_WRITE=51

   # Operadores 
   OP_MENOR = 10
   OP_MENOR_IGUAL = 11
   OP_MAIOR_IGUAL = 12
   OP_MAIOR = 13
   OP_IGUAL = 14
   OP_DIFERENTE = 15
   OP_DIV=16
   OP_ATRIB=17
   OP_AD = 18#+
   OP_MIN = 19#-
   OP_MUL = 20
    
   # Identificador
   ID = 21
   # Numeros
   NUM= 22
    #Símbolos
   SMB_OBC=23 #{
   SMB_CBC=24 #}
   SMB_OPA=25 #(
   SMB_CPA=26 #)
   SMB_COM=27 #,
   SMB_SEM=28@#;

   #char
   CHAR=29
   #constante
   CHAR_CONST=30
   NUM_CONST=31

   #Analisador Sintatico
   KW_PROGRAM=32






