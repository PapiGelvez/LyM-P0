import ply.lex as lex
import re
import codecs
import os
import sys

tokens = [
    'ID', 'NUMBER', 'LSPARENT', 'RSPARENT', 'COMMA', 'SEMICOLON', 'COLON', 'VERTICALBAR'    
]

reservadas = {
    'PROCEDURE':'PROCEDURE','ROBOT_R':'ROBOT_R', 'VARS':'VARS', 'PROCS':'PROCS', 'assignTo':'ASSIGNTO', 'goto':'GOTO', 'move':'MOVE',
    'turn':'TURN', 'face':'FACE', 'put':'PUT', 'pick':'PICK', 'moveToThe':'MOVETOTHE', 'moveInDir':'MOVEINDIR',
    'jumpToThe':'JUMPTOTHE', 'jumpInDir':'JUMPINDIR', 'nop':'NOP', 'if':'IF', 'while':'WHILE', 'then':'THEN',
    'else':'ELSE', 'do':'DO', 'repeat':'REPEAT', 'facing':'FACING', 'canPut':'CANPUT', 'canPick':'CANPICK',
    'canMoveInDir':'CANMOVEINDIR', 'canJumpInDir':'CANJUMPINDIR', 'canMoveToThe':'CANMOVETOTHE', 'canJumpToThe':'CANJUMPTOTHE',
    'not':'NOT'
}

tokens = tokens + list(reservadas.values())


t_ignore = ' \t'
t_LSPARENT = r'\['
t_RSPARENT = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_VERTICALBAR = r'\|'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    #t.type = reservadas.get(t.value, 'ID')
    #t.value = t.value.upper()
    if t.value.upper() in reservadas.values():
        t.value = t.value.upper()
        t.type = t.value

    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    t.lexer.skip(1)

def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print(cont)
        print(str(cont)+ ". " + file)
        cont += 1

    while respuesta == False:
        numArchivo = input('\nNumero del test: ')
        for file in files:
            if file == files[int(numArchivo) - 1]:
                respuesta = True
                break
    print("Has escogido \'%s' \n" % files[int(numArchivo) - 1])  

    return files[int(numArchivo) - 1]

directorio = "C:/Users/garav/OneDrive/Escritorio/LYM/test/"


archivo = buscarFicheros(directorio)
test = directorio + archivo
fp =codecs.open(test, "r", "utf-8")
cadena = fp.read()
fp.close()

analizador = lex.lex()

analizador.input(cadena)

tokens_doc = []

while True:
    tok = analizador.token()
    if not tok: break
    tokens_doc.append(tok)
    
    
def encontrarProc(lista, pos):
    respuesta = []
    if lista[pos].type == 'LSPARENT':
        while pos < len(lista):
            if lista[pos].type != 'RSPARENT':
                pos += 1
                respuesta.append(lista[pos])
            else:
                return respuesta
        else:
            return None

def formatoParametro(lista):
    y = 0
    parametros = []
    tipo = ''
    if lista[y].type == 'VERTICALBAR':
        y += 1
        while tipo != 'VERTICALBAR':
            parametros.append(lista[y])
            tipo = lista[y].type
            y += 1
            if y == len(lista)-1:
                return False
    z = 0
    barB = False
    
    while z < len(parametros)-2:
        if parametros[0].type != 'ID' or parametros[len(parametros)-1].type != 'VERTICALBAR':
            return False, parametros
        else:
            if parametros[z].type != 'ID' or parametros[z].type != 'COMMA':
                return False, parametros
            else:
                if parametros[z].type == 'ID':
                    if parametros[z+1].type != 'COMMA' and barB == True:
                        return False, parametros
                    elif parametros[z+1].type == 'VERTICALBAR':
                        barB = True
                    else:
                        z += 1
                else:
                    if parametros[z+1].type != 'ID':
                        return False, parametros
                    else:
                        z += 1
    else:
        return True, parametros

primer_id = False

x = 0
while True:
    if tokens_doc[x].type != 'ROBOT_R':
        print('Programa invalido!! - No inicia el robot')
        break
    else:
        x+=1
        if tokens_doc[x].type != 'VARS':
            print('Programa invalido!! - no declara variables')
            break
        else:
            x += 1
            while tokens_doc[x].type != 'PROCS':
                if tokens_doc[x].type == 'ID' or tokens_doc[x].type == 'COMMA':
                    if tokens_doc[x].type == 'ID':
                        if tokens_doc[x-1].type != 'COMMA':    
                            if tokens_doc[x-1].type == 'VARS' and primer_id == False:
                                primer_id = True
                            else:
                                print('Programa invalido!! - formato incorrecto')
                                break
                        else:
                            x += 1    
                    else:
                        if tokens_doc[x-1].type != 'ID' or tokens_doc[x+1].type != 'ID':
                            print('Programa invalido!! - formato incorrecto')
                            break
                        else:
                            x += 1
                    if x == len(tokens_doc)-1:
                        print('Programa invalido!! - no declara procs')
                        break
                    else:
                        x += 1
                else:
                    print('Programa invalido!! - formato incorrecto')
                    break
            else:
                x += 1
                if tokens_doc[x].type != 'ID' or tokens_doc[x+1].type != 'LSPARENT':
                    print('Programa invalido!! - formato incorrecto')
                    break
                else:
                    tokens_doc[x].type = 'PROCEDURE'
                    x += 1
                proce = encontrarProc(tokens_doc, x)
                parametros = formatoParametro(proce)
                if parametros[0] == False:
                    print(parametros[1])
                    print('Programa incorrecto!!! - formato parametros incorrectos')
                    break
                else:
                    print(parametros[1])
                    print('Vamos bien!!')
                    
                    
                        

    
    
    
    
    
    
#for i in tokens_doc:
    #print(i)


