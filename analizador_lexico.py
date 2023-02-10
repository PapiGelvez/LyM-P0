import ply.lex as lex
import re
import codecs
import os
import sys

"""reservadas = ['ROBOT_R', 'VARS', 'PROCS', 'ASSIGNTO', 'GOTO', 'MOVE', 'TURN', 'FACE', 'PUT', 'PICK', 'MOVETOTHE', 'MOVEINDIR',
            'JUMPTOTHE', 'JUMPINDIR', 'NOP', 'IF', 'WHILE', 'THEN', 'ELSE', 'DO', 'REPEAT', 'FACING', 'CANPUT', 'CANPICK',
            'CANMOVEINDIR', 'CANJUMPINDIR', 'CANMOVETOTHE', 'CANJUMPTOTHE', 'NOT', 'NORTH', 'EAST', 'SOUTH', 'WEST']"""

tokens =  [
    'ID', 'NUMBER', 'LSPARENT', 'RSPARENT', 'COMMA', 'SEMICOLON', 'COLON', 'VERTICALBAR'    
]


reservadas = {
    'ROBOT_R':'ROBOT_R', 'VARS':'VARS', 'PROCS':'PROCS', 'assignTo':'ASSIGNTO', 'goto':'GOTO', 'move':'MOVE',
    'turn':'TURN', 'face':'FACE', 'put':'PUT', 'pick':'PICK', 'moveToThe':'MOVETOTHE', 'moveInDir':'MOVEINDIR',
    'jumpToThe':'JUMPTOTHE', 'jumpInDir':'JUMPINDIR', 'nop':'NOP', 'if':'IF', 'while':'WHILE', 'then':'THEN',
    'else':'ELSE', 'do':'DO', 'repeat':'REPEAT', 'facing':'FACING', 'canPut':'CANPUT', 'canPick':'CANPICK',
    'canMoveInDir':'CANMOVEINDIR', 'canJumpInDir':'CANJUMPINDIR', 'canMoveToThe':'CANMOVETOTHE', 'canJumpToThe':'CANJUMPTOTHE',
    'not':'NOT', 'north':'NORTH','east':'EAST','south':'SOUTH','west':'WEST'
}

tokens = tokens + list(reservadas.values())

 

t_ignore = ' \t\r'
t_LSPARENT = r'\['
t_RSPARENT = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_VERTICALBAR = r'\|'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    #t.type = reservadas.get(t.value, 'ID')
    #t.value = t.value.upper()
    if t.value.upper() in reservadas.values():
        t.value = t.value.upper()
        t.type = t.value

    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Existen caracteres ilegales dentro del código ingresado '%s'" % t.value[0])
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

directorio = "C:/Users/santi/OneDrive/Documentos/Universidad/3er semestre/LyM/P0/test/"


archivo = buscarFicheros(directorio)
test = directorio + archivo
fp = codecs.open(test, "r", "utf-8")
cadena = fp.read()
fp.close()

analizador = lex.lex()

analizador.input(cadena)

while True:
    tok = analizador.token()
    if not tok: break
    print(tok)