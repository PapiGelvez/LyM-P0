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
    'not':'NOT', 'balloons':'BALLOONS', 'chips':'CHIPS', 'left':'LEFT', 'right':'RIGHT', 'around':'AROUND',
     'north':'NORTH', 'south':'SOUTH','east':'EAST', 'west':'WEST','front':'FRONT','back':'BACK'
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

directorio = "C:/Users/santi/OneDrive/Documentos/Universidad/3er semestre/LyM/P0/ejemplo github/"
#directorio = "C:/Users/garav/OneDrive/Escritorio/LYM/test/"


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

procedict = {}
commands = ['ASSIGNTOCOLONNUMBERCOMMAID', 'GOTOCOLONIDCOMMANUMBER', 'GOTOCOLONNUMBERCOMMAID', 
            'GOTOCOLONIDCOMMAID', 'GOTOCOLONNUMBERCOMMANUMBER','MOVECOLONNUMBER','TURNCOLONLEFT',
            'TURNCOLONRIGHT','TURNCOLONAROUND','FACECOLONNORTH','FACECOLONSOUTH','FACECOLONEAST',
            'FACECOLONWEST','PUTCOLONNUMBERCOMMABALLOONS','PUTCOLONNUMBERCOMMACHIPS','PUTCOLONIDCOMMABALLOONS',
            'PUTCOLONIDCOMMACHIPS','PICKCOLONNUMBERCOMMABALLOONS','PICKCOLONNUMBERCOMMACHIPS',
            'PICKCOLONIDCOMMABALLOONS','PICKCOLONIDCOMMACHIPS','MOVETOTHECOLONNUMBERCOMMAFRONT',
            'MOVETOTHECOLONNUMBERCOMMALEFT','MOVETOTHECOLONNUMBERCOMMARIGHT','MOVETOTHECOLONNUMBERCOMMABACK',
            'MOVEINDIRCOLONNUMBERCOMMANORTH','MOVEINDIRCOLONNUMBERCOMMASOUTH','MOVEINDIRCOLONNUMBERCOMMAEAST',
            'MOVEINDIRCOLONNUMBERCOMMAWEST','JUMPINDIRCOLONNUMBERCOMMANORTH','JUMPINDIRCOLONNUMBERCOMMASOUTH',
            'JUMPINDIRCOLONNUMBERCOMMAEAST','JUMPINDIRCOLONNUMBERCOMMAWEST','JUMPTOTHECOLONNUMBERCOMMAFRONT',
            'JUMPTOTHECOLONNUMBERCOMMALEFT','JUMPTOTHECOLONNUMBERCOMMARIGHT','JUMPTOTHECOLONNUMBERCOMMABACK',
            'NOPCOLON']

conditions = ['FACINGCOLONNORTH','FACINGCOLONSOUTH','FACINGCOLONEAST','FACINGCOLONWEST',
              'CANPUTCOLONNUMBERCOMMACHIPS','CANPUTCOLONNUMBERCOMMABALLOONS','CANPICKCOLONNUMBERCOMMACHIPS',
              'CANPICKCOLONNUMBERCOMMABALLOONS','CANMOVETOTHECOLONNUMBERCOMMAFRONT',
            'CANMOVETOTHECOLONNUMBERCOMMALEFT','CANMOVETOTHECOLONNUMBERCOMMARIGHT','CANMOVETOTHECOLONNUMBERCOMMABACK',
            'CANMOVEINDIRCOLONNUMBERCOMMANORTH','CANMOVEINDIRCOLONNUMBERCOMMASOUTH','CANMOVEINDIRCOLONNUMBERCOMMAEAST',
            'CANMOVEINDIRCOLONNUMBERCOMMAWEST','CANJUMPINDIRCOLONNUMBERCOMMANORTH','CANJUMPINDIRCOLONNUMBERCOMMASOUTH',
            'CANJUMPINDIRCOLONNUMBERCOMMAEAST','CANJUMPINDIRCOLONNUMBERCOMMAWEST','CANJUMPTOTHECOLONNUMBERCOMMAFRONT',
            'CANJUMPTOTHECOLONNUMBERCOMMALEFT','CANJUMPTOTHECOLONNUMBERCOMMARIGHT','CANJUMPTOTHECOLONNUMBERCOMMABACK',
            'NOTCOLON']

    
def encontrarProc(lista, pos):
    respuesta = []
    nume = 0
    if lista[pos].type == 'LSPARENT':
        while pos < len(lista):
            if lista[pos].type != 'RSPARENT':
                pos += 1
                nume += 1
                respuesta.append(lista[pos])
            else:
                return respuesta, nume
        else:
            return None

def formatoParametro(lista, procedure):
    y = 0
    ids = 0
    parametros = []
    tipo = ''
    if lista[y].type == 'VERTICALBAR':
        parametros.append(lista[y])
        y += 1
        while tipo != 'VERTICALBAR':
            parametros.append(lista[y])
            tipo = lista[y].type
            y += 1
            if y == len(lista)-1:
                return False
    z = 1
    barB = False
    while parametros[z].type != 'VERTICALBAR':
        if parametros[z].type =='ID' or parametros[z].type == 'COMMA':
            if parametros[z].type =='ID':
                ids += 1
                if parametros[z-1].type != 'COMMA':
                    if parametros[z-1].type == 'VERTICALBAR' and barB == False:
                        barB = True
                    else:
                        return False
                else:
                    z += 1
            else:
                if parametros[z-1].type != 'ID' or parametros[z+1].type != 'ID':
                    return False
                else:
                    z += 1
            if z == len(parametros)-1:
                return False
            else:
                z+=1
        else:
            return False
    else:
        procedict[procedure] = ids
        return True
    
def creaCommands(dict):
    number = 'NUMBER'
    coma = 'COMMA'
    colon = 'COLON'
    for i in dict:
        x = ''
        z = i.key.type
        x = x + z + colon
        pos = 0
        while pos < i.value:
            x = x + number + coma
        else:
            x = x + number
        if x not in commands:
            commands.append(x)


def commandsExist(string):
    if string in commands:
        return True
    else:
        return False

def formatoInstructions(lista):
    barsQ = 0
    instruct = []
    
    for i in lista:
        if barsQ == 2:
            instruct.append(i)
        if i.type == 'VERTICALBAR':
            barsQ += 1
    respuesta = True
    command = ''
    q = 0
    for i in instruct:
        if i.type != 'SEMICOLON':
            command = command + i.type
            if i.type == 'IF':
                if formatIf(instruct, q) != True:
                    respuesta = False
            elif i.type == 'WHILE':
                if formatWhile(instruct, q) != True:
                    respuesta = False
            elif i.type == 'REPEAT':
                if formatRepeat(instruct, q) != True:
                    respuesta = False
        else:
            respuesta = commandsExist(command)
            if respuesta == False:
                respuesta = False
            else:
                command = ''    
        q += 1
    return respuesta, len(lista)

def formatCommands(lista):
    respuesta = True
    command = ''
    q = 0
    for i in lista:
        if i.type != 'SEMICOLON':
            command = command + i.type
            if i.type == 'IF':
                if formatIf(lista, q) != True:
                    respuesta = False
            elif i.type == 'WHILE':
                if formatWhile(lista, q) != True:
                    respuesta = False
            elif i.type == 'REPEAT':
                if formatRepeat(lista, q) != True:
                    respuesta = False
        else:
            respuesta = commandsExist(command)
            if respuesta == False:
                respuesta = False
            else:
                command = ''    
        q += 1
    return respuesta, len(lista)

primer_id = False

def formatIf(list, pos):
    condition = ''
    if list[pos].type == 'IF':
        pos += 1
        if list[pos].type == 'COLON':
            pos += 1
            while list[pos].type != 'THEN':
                if pos < len(list):
                    condition = condition + list[pos].type
                    pos += 1
                else:
                    return False
            else:
                if condition not in conditions:
                    return False
                else:
                    condition = ''
                    pos += 1
            if list[pos].type != 'COLON':
                return False
            else:
                pos += 1
            if list[pos].type != 'LSPARENT':
                return False
            else:
                pos += 1
            while list[pos].type != 'RSPARENT':
                if pos < len(list):
                    condition = condition + list[pos].type
                    pos += 1
                else:
                    return False
            else:
                if condition not in commands:
                    return False
                else:
                    condition = ''
                    pos += 1
            if list[pos].type != 'ELSE':
                return False
            else:
                pos += 1
            if list[pos].type != 'COLON':
                return False
            else:
                pos += 1
            while list[pos].type != 'RSPARENT':
                if pos < len(list):
                    condition = condition + list[pos].type
                    pos += 1
                else:
                    return False
            else:
                if condition not in commands:
                    return False
                else:
                    condition = ''
                    return True
            
def formatWhile(list, pos):
    condition = ''
    if list[pos].type == 'WHILE':
        pos += 1
        if list[pos].type == 'COLON':
            pos += 1
            while list[pos].type != 'DO':
                if pos < len(list):
                    condition = condition + list[pos].type
                    pos += 1
                else:
                    return False
            else:
                if condition not in conditions:
                    return False
                else:
                    condition = ''
                    pos += 1
            if list[pos].type != 'COLON':
                return False
            else:
                pos += 1
            if list[pos].type != 'LSPARENT':
                return False
            else:
                pos += 1
            while list[pos].type != 'RSPARENT':
                if pos < len(list):
                    condition = condition + list[pos].type
                    pos += 1
                else:
                    return False
            else:
                if condition not in commands:
                    return False
                else:
                    condition = ''
                    return True

def formatRepeat(list, pos):
    condition = ''
    if list[pos].type == 'REPEAT':
        pos += 1
        if list[pos].type == 'COLON':
            pos += 1
        if list[pos].type != 'NUMBER' or list[pos].type != 'ID':
            return False
        else:
            pos += 1
        if list[pos].type != 'LSPARENT':
            return False
        else:
            pos += 1
            while list[pos].type != 'RSPARENT':
                if pos < len(list):
                    condition = condition + list[pos].type
                    pos += 1
                else:
                    return False
            else:
                if condition not in commands:
                    return False
                else:
                    condition = ''
                    return True


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
                if tokens_doc[x] == 'ID':
                    if tokens_doc[x+1].type == 'LSPARENT':
                        x += 1
                        tokens_doc[x-1].type = 'PROCEDURE'
                        proce = encontrarProc(tokens_doc, x)
                        parametros = formatoParametro(proce[0], tokens_doc[x-1])
                        inst = formatoInstructions(proce[0])
                        creaCommands(procedict)
                        if parametros == False or inst[0] == False:
                            print('Programa incorrecto!!! - formato parametros incorrectos')
                            break
                        else:
                            x += inst[1]
                    else:
                        print('ERROR')
                        break
                else:
                    x+=1
                    if tokens_doc[x].type == 'LSPARENT':
                        x += 1
                        while tokens_doc[x].type != 'SEMICOLON':
                            lst = []
                            lst.append(tokens_doc[x])
                            x += 1
                        else:
                            if formatCommands(lst) == False:
                                print('ERROR')
                                break
                            else:
                                x += 1
                    if x == len(tokens_doc)-1:
                        if tokens_doc[x].type == 'RSPARENT':
                            print('SINTAXIS CORRECTA')
                            break
                        else:
                            print('ERROR')
                            break
                    else:
                        print('ERROR')
                        break
                            
                                
                        
                        
                    
                
                
                
                    
            
                    
                    
                        

    
    
    
    



