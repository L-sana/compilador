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
   KW_PROGRAM = 1
   KW_IF = 2
   KW_ELSE = 3
   KW_WHILE = 4
   KW_WRITE = 5
   KW_READ = 6
   KW_NUM = 7
   KW_CHAR = 8
   KW_NOT = 9
   KW_OR = 10
   KW_AND = 11

#Operadores 
   OP_EQ = 12
   OP_NE = 13
   OP_GT = 14
   OP_LT = 15
   OP_GE = 16
   OP_LE = 17
   OP_ADD = 18
   OP_MIN = 19
   OP_MUL = 20
   OP_DIV = 21
   OP_ATRIB = 22

# Símbolos
   SMB_OBC = 30
   SMB_CBC = 31
   SMB_OPA = 32
   SMB_CPA = 33
   SMB_COM = 34
   SMB_SEM = 35

# Identificador
   ID = 40

# Constante
   NUM_CONST = 50
   CHAR_CONST = 51

# Constantes para tipos
   TIPO_CHAR = 1000;
   TIPO_NUM  = 1001;
   TIPO_BOOL = 1002;
   TIPO_VOID = 1003;
   TIPO_ERRO = 1004;
