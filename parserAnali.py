import sys
import copy
from tag import Tag
from token import Token
from lexer import Lexer
from no import No

class ParserAnali():
#Classe que representa o analisador sintático

   def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() 
      self.contadorErros = 0
      if self.token is None:
        sys.exit(0)

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
      if self.token is None: 
        sys.exit(0)
   
   def skip(self, message):
      self.sinalizaErroSintatico(message)
      self.advance()

   def contadorErro(self):
      self.contadorErros += 1
      print(self.contadorErros)
      if (self.contadorErros > 3):
          sys.exit(0)
      else:
          self.advance()

   def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False

   def Programa(self):	
      self.prog()

   def prog(self):
     if(self.token.getNome() == Tag.KW_PROGRAM):
         self.eat(Tag.KW_PROGRAM)
         if(not self.eat(Tag.ID)):
             self.sinalizaErroSintatico("Esperado \"id\", encontrado " + "\"" + self.token.getLexema() + "\"")
             self.contadorErro()
         self.body()
     if(self.token.getNome() == Tag.EOF):
         self.eat(Tag.EOF)

#decl-list “{“ stmt-list “}” 
   def body(self):
     if(self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR):
         self.declList()
         if(self.token.getNome() == Tag.SMB_OBC):
             self.eat(Tag.SMB_OBC)
         else:
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
            self.contadorErro()
         if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE
            or self.token.getNome() == Tag.KW_READ or self.token.getNome() == Tag.KW_WRITE):
            self.stmtList()
         if(not self.eat(Tag.SMB_CBC)): 
             self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
             self.contadorErro()
     else:
       self.sinalizaErroSintatico("Esperado \"num, char\", encontrado " + "\"" + self.token.getLexema() + "\"")
       self.contadorErro()
         
#decl-list -> decl “;” decl-list |ε  
   def declList(self):
     if(self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR):
         self.decl()
         if(not self.eat(Tag.SMB_SEM)):
              self.skip("Esperado \";\", encontrado "  + "\"" + self.token.getLexema() + "\"")
              self.contadorErro()
         self.declList()
      
#decl -> type id-list 
   def decl(self):
     if(self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR):
        self.type()
        self.idList()
     else:
        self.sinalizaErroSintatico("Esperado \"numero, char\", encontrado " + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()

#type -> num | char 
   def type(self):
     if(self.token.getNome() == Tag.KW_NUM):
         self.eat(Tag.KW_NUM)
     elif(self.token.getNome() == Tag.KW_CHAR): 
         self.eat(Tag.KW_CHAR)
     else:
        self.skip("Esperado \"num, char\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
       
#id-list -> “id” id-list’ 
   def idList(self):
      if(self.token.getNome() == Tag.ID):
        self.eat(Tag.ID)
        self.idListLinha()
    
#id-listLinha -> “,” id-list | ε
   def idListLinha(self):
      if(self.token.getNome() == Tag.SMB_COM):
          self.eat(Tag.SMB_COM)
          self.idList()
       
#smt-list -> stmt “;” stmt-list | ε 
   def stmtList(self):
       if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE
            or self.token.getNome() == Tag.KW_READ or self.token.getNome() == Tag.KW_WRITE):
          self.stmt()
          if(not self.eat(Tag.SMB_SEM)):
              self.skip("Esperado \";\", encontrado "  + "\"" + self.token.getLexema() + "\"")
              self.contadorErro()
          else:
              self.stmtList()
      
#stmt -> assign-stmt | if-stmt | while-stmt | read-stmt | write-stmt 
   def stmt(self):
       if(self.token.getNome() == Tag.ID):
          self.assignStmt()
       elif(self.token.getNome() == Tag.KW_IF):
          self.ifStmt() 
       elif(self.token.getNome() == Tag.KW_WHILE):
          self.whileStmt() 
       elif(self.token.getNome() == Tag.KW_READ):
          self.readStmt()
       elif(self.token.getNome() == Tag.KW_WRITE):
          self.writeStmt() 
       else:
         self.sinalizaErroSintatico("Esperado \"id, if, while, read, write\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.contadorErro()
      
#assign-stmt -> “id” “=” simple_expr
   def assignStmt(self):
      if(self.eat(Tag.ID)):
        self.eat(Tag.ID)  
        if(not self.eat(Tag.OP_ATRIB)):
            self.skip("Esperado \"=\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            self.contadorErro()
        self.simpleExpr()
       
#if-stmt -> “if” “(“ expression “)” “{“ stmt-list “}” if-stmt’
   def ifStmt(self):
      if(self.eat(Tag.KW_IF)):
        if(not self.eat(Tag.SMB_OPA)):
            self.skip("Esperado \"(\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            self.contadorErro()
        self.expression()
        if(not self.eat(Tag.SMB_CPA)):
            self.skip("Esperado \")\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            self.contadorErro()
        if(not self.eat(Tag.SMB_OBC)):
            self.skip("Esperado \"{\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            self.contadorErro()
        self.stmtList()
        if(not self.eat(Tag.SMB_CBC)):
            self.skip("Esperado \"}\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            self.contadorErro()
        self.ifStmtLinha()
       
#if-stmt’ -> “else” “{“ stmt-list “}” | ε
   def ifStmtLinha(self):
      if(self.eat(Tag.KW_ELSE)):
        if(not self.eat(Tag.SMB_OBC)):
           self.skip("Esperado \"{\", encontrado "  + "\"" + self.token.getLexema() + "\"")
           self.contadorErro()
        self.stmtList()
        if(not self.eat(Tag.SMB_CBC)):
            self.skip("Esperado \"}\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            self.contadorErro()

#while-stmt -> stmt-prefix “{“ stmt-list “}”   
   def whileStmt(self):
     if(self.token.getNome() == Tag.KW_WHILE):
        self.eat(Tag.KW_WHILE)
        self.stmtPrefix()
     if(not self.eat(Tag.SMB_OBC)):
        self.skip("Esperado \"{\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
     self.stmtList()
     if(not self.eat(Tag.SMB_CBC)):
        self.skip("Esperado \"}\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
      
#stmt-prefix -> “while” “(“ expression “)”    
   def stmtPrefix(self):
     if(self.token.getNome() == Tag.KW_WHILE):
        self.eat(Tag.KW_WHILE)
     if(not self.eat(Tag.SMB_OPA)):
         self.skip("Esperado \"(\", encontrado "  + "\"" + self.token.getLexema() + "\"")
         self.contadorErro()
     self.expression()
     if(not self.eat(Tag.SMB_CPA)):
        self.skip("Esperado \")\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
      
#read-stmt -> “read” “id”   
   def readStmt(self):
     if(self.token.getNome() == Tag.KW_READ):
        self.eat(Tag.KW_READ)
     if(not self.eat(Tag.ID)):
         self.sinalizaErroSintatico("Esperado \"id\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.contadorErro()      
       
#write-stmt -> “write” simple-expr
   def writeStmt(self):
     if(self.token.getNome() == Tag.KW_WRITE):
        self.eat(Tag.KW_WRITE)
        self.simpleExpr()
     else:
        self.skip("Esperado \"write\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()   

#expression -> simple-expr expression’      
   def expression(self):
     if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.CHAR_CONST or self.token.getNome() == Tag.NUM_CONST or self.token.getNome() == Tag.SMB_OPA or self.token.getNome() == Tag.KW_NOT):
        self.simpleExpr()
        self.expressionLinha()
     else:
        self.skip("Esperado \"id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()   
      
#expression’ -> logop simple-expr expression’| ε   
   def expressionLinha(self):
     if(self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND):
        self.logop() 
        self.simpleExpr()
        self.expressionLinha()

#simple-expr -> term simple-exp’       
   def simpleExpr(self):
     if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.NUM_CONST or self.token.getNome() == Tag.CHAR_CONST or self.token.getNome() == Tag.SMB_OPA or self.token.getNome() == Tag.KW_NOT):
        self.term()
        self.simpleExprLinha()
     else:
        self.skip("Esperado \"id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()   

#simple-exp’ -> relop term simple-exp’| ε  
   def simpleExprLinha(self):
     if(self.token.getNome() == Tag.OP_EQ or self.token.getNome() == Tag.OP_GT or self.token.getNome() == Tag.OP_GE
        or self.token.getNome() == Tag.OP_LT or self.token.getNome() == Tag.OP_LE or self.token.getNome() == Tag.OP_NE):
        self.relop() 
        self.term()       
        self.simpleExprLinha()       

#term -> factor-b term’      
   def term(self):
     if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.NUM_CONST or self.token.getNome() == Tag.CHAR_CONST or self.token.getNome() == Tag.SMB_OPA or self.token.getNome() == Tag.KW_NOT):
        self.factorb()
        self.termLinha()
     else:
        self.skip("Esperado \"id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()       
      
#termLinha -> addop factor-b term’ | ε     
   def termLinha(self):
      if(self.token.getNome() == Tag.OP_ADD or self.token.getNome() == Tag.OP_MIN):
        self.addop() 
        self.factorb()       
        self.termLinha()      

#factor-b -> factor-a factor-b’      
   def factorb(self):
      if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.NUM_CONST or self.token.getNome() == Tag.CHAR_CONST or self.token.getNome() == Tag.SMB_OPA or self.token.getNome() == Tag.KW_NOT):
        self.factora()
        self.factorbLinha()
      else:
        self.skip("Esperado \"id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
      
#factor-b' -> mulop factor-a factor-b’ | ε
   def factorbLinha(self):
      if(self.token.getNome() == Tag.OP_MUL or self.token.getNome() == Tag.OP_DIV):
        self.mulop()
        self.factora()
        self.factorbLinha()
             
#factor-a -> factor | not factor
   def factora(self):
      if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.NUM_CONST or self.token.getNome() == Tag.CHAR_CONST or self.token.getNome() == Tag.SMB_OPA):
        self.factor()
      elif(self.token.getNome() == Tag.KW_NOT):
        self.eat(Tag.KW_NOT)
        self.factor()
      else:
        self.skip("Esperado \"id, not\", encontrado " + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
      
#factor -> “id” | constant | “(“ expression “)”
   def factor(self):
      if(self.token.getNome() == Tag.ID):
        self.eat(Tag.ID)
      elif(self.token.getNome() == Tag.NUM_CONST or self.token.getNome() == Tag.CHAR_CONST):
        self.constant()
      elif(self.token.getNome() == Tag.SMB_OPA):
         self.eat(Tag.SMB_OPA)
         self.expression()
         self.eat(Tag.SMB_CPA)
      else:
         self.skip("Esperado \"id, constant, (\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.contadorErro()
      
#logop -> “or” | “and”
   def logop(self):
     if(not self.eat(Tag.KW_OR)) and (not self.eat(Tag.KW_AND)):
        self.skip("Esperado \"or, and\", encontrado " + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()

#relop -> “==” | “>” | “>=” | “<” | “<=” | “!=”
   def relop(self):
      if(not (self.eat(Tag.OP_EQ)) and (not self.eat(Tag.OP_GT)) and (not self.eat(Tag.OP_GE)) and 
        (not self.eat(Tag.OP_LT)) and (not self.eat(Tag.OP_LE)) and (not self.eat(Tag.OP_NE))):
        self.skip("Esperado \"==, >, >=, <, <=, !=\", encontrado " + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
       
#addop -> “+” | “-”
   def addop(self):
      if(not self.eat(Tag.OP_ADD)) and (not self.eat(Tag.OP_MIN)):
        self.skip("Esperado \"+,-\", encontrado " + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()  
     
#mulop -> “*” | “/” 
   def mulop(self):
      if(not self.eat(Tag.OP_MUL)) and (not self.eat(Tag.OP_DIV)):
        self.skip("Esperado \"*, /\", encontrado " + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()
       
#constant -> “num_const” | “char_const”
   def constant(self):  
      if(not self.eat(Tag.NUM_CONST) and not self.eat(Tag.CHAR_CONST)):
        self.skip("Esperado \"numero, char\", encontrado " + "\"" + self.token.getLexema() + "\"")
        self.contadorErro()