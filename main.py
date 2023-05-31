import json
import re
import os

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Funciones de Archivos  ----------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def leer_archivo_json(nombre_file:str, key:str) -> list:
    '''
    Leera un archivo json y devolvera la lista de diccionarios
    Dicho archivo se abrirá en modo lectura únicamente y retornará la lista de héroes como una lista de diccionarios.
    Recibe por parámetro un string que indicará el nombre y extensión del archivo a leer (Ejemplo: archivo.json) y un string que representa la clve de la lista buscada
    '''
    lista = []
    with open(nombre_file, "r", encoding="utf-8") as file:  # Se abre el archivo en modo lectura, encoding="utf-8" arregla los acentos
        dict = json.load(file)      # Usando la biblioteca de json se lee el archivo y se guarda la informacion en un diccionario
        lista = dict[key]           # Se guarda la lista de diccionarios de la clave pasada por parametro
    return lista

def guardar_archivo_csv(nombre_file:str, data:str):
    '''
    .Recibe por parámetro un string que indicará el nombre con el cual se guardará el archivo junto con su extensión (ejemplo: 'archivo.csv') y 
    como segundo parámetro tendrá un string el cual será el contenido a guardar en dicho archivo. El archivo se abrira en modo escritura
    Retornara True si se pudo crear el archivo o False si no
    '''
    retorno = None
    with open(nombre_file, "w") as file:                                    # Se abre el archivo en modo escritura                   
        if file.write(data):                                                # Se escribe la informacion pasada por parametro como string
            print("\nSe creo el archivo: {0}".format(nombre_file))          # Mostrara este msj en caso que el archivo se haya podido crear
            retorno = True
        else:
            print("\nError al crear el archivo: {0}".format(nombre_file))   # Mostrara este msj en caso que el archivo no se pudo crear
            retorno = False
    return retorno

def generar_string_csv_jugador_nombre_posicion_estadisticas(jugador:dict) -> str:
    '''
    . Recibe por parámetro el jugador a guardar y crea un string con todos los datos (nombre, posicion y estadisticas) en formato csv
    . El caracter separador es la "," y el que termina la linea "\n"
    '''
    texto = "nombre,posicion,temporadas,puntos_totales,promedio_puntos_por_partido,rebotes_totales,promedio_rebotes_por_partido,promedio_asistencias_por_partido,robos_totales,bloqueos_totales,bloqueos_totales,porcentaje_tiros_de_campo,porcentaje_tiros_libres,porcentaje_tiros_triples\n"
    texto += "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(jugador["nombre"],
                                                            jugador["posicion"],
                                                            jugador["estadisticas"]["temporadas"],
                                                            jugador["estadisticas"]["puntos_totales"],
                                                            jugador["estadisticas"]["promedio_puntos_por_partido"],
                                                            jugador["estadisticas"]["rebotes_totales"],
                                                            jugador["estadisticas"]["promedio_rebotes_por_partido"],
                                                            jugador["estadisticas"]["promedio_asistencias_por_partido"],
                                                            jugador["estadisticas"]["robos_totales"],
                                                            jugador["estadisticas"]["bloqueos_totales"],
                                                            jugador["estadisticas"]["porcentaje_tiros_de_campo"],
                                                            jugador["estadisticas"]["porcentaje_tiros_libres"],
                                                            jugador["estadisticas"]["porcentaje_tiros_triples"])
    
    return texto

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# -----------------------------------------------------  Inputs  --------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def es_numero(texto:str, numero_int:bool=True) -> bool:
    '''
    Recibe un string que representa la expresión a evaluar  y un booleano que indica si debe ser un numero entero (True por defecto) o flotante (False)
    Devuelve True en caso que se trate de un número decimal y False en el caso contrario.
    '''
    retorno = False
    patron = r"^-?[0-9]+[.,]?[0-9]*$"       # + = una o mas ocurrencias | ? = cero o una ocurrencia | * = ninguna o mas ocurrencias | ^ = Empieza con | $ = Termina con
    if numero_int:                          # ^-?[0-9]+[.,]?[0-9]*$ La expresion significa: Desde que comienza, puede haber un - o no, una cantidad indeterminadas de numeros,
        patron = r"^-?[0-9]+$"              # puede haber un . o una , y puede haber o no una indeterminada cantidad de numeros. Que no porque si no hay caracter separador
    resultado = re.match(patron, texto)     # no deberia paras del primer conjunto
    if resultado:                              
        retorno = True
    return retorno

def validar_rango(numero:float,min:float,max:float) -> bool:
    '''
    Esta funcion evaluara si un numero esta  denro del rango de la lista
    Recibe el numero que se quiere validar y el minimo y el maximo que forman el rango
    Devuelve un True si esta dentro del rango o False si no
    '''
    retorno = False
    if numero >= min and numero <= max:
        retorno = True
    return retorno

def pedir_un_numero(texto_a_mostrar:str, numero_int:bool=True) -> int|float|bool:
    '''
    Esta funcion le pedira al usuario que ingrese un numero
    Recibe el texto que quiere ser mostrado en consola al momento de pedir el dato y un booleano que indica si debe ser un numero entero (True por defecto) o flotante (False)
    Devuelve el numero transformado a int o float en caso de que lo pudo tomar o z si fallo o el texto no es solo texto
    '''
    retorno = "z" # La funcion retorna 'z' porque en la evaluacion de un if el 0 se toma como False o None, esta funcion admite numeros negativos
    numero = input(texto_a_mostrar)
    if es_numero(numero, numero_int):  # En caso de que sea un numero
        if numero_int:                 # La funcion permite diferenciar int de float para que se pueda trabajar con ello de ser necesario
            retorno = int(numero)
        else:                                           # Se reemplaza la posible ',' que el usuario pueda ingresar cuando escribe un flotante porque
            retorno = float(numero.replace(",", "."))   # el float() solo admite '.'
    return retorno

def pedir_un_numero_positivo(texto_a_mostrar:str, intentos:int, numero_int:bool=True) -> int|float|bool:
    '''
    Esta funcion le pedira al usuario que ingrese un numero y lo evaluara en el rango
    Recibe: 
    .El texto que quiere ser mostrado en consola al momento de pedir el dato
    .La cantidad de intentos que se pedira el numero (El primero mas los intentos)
    .Un booleano que indica si debe ser un numero entero (True por defecto) o flotante (False)
    Devuelve el numero transformado a int o float en caso de que lo pudo tomar o "z" si fallo
    '''
    retorno = "z"               # La funcion retorna 'z' porque en la evaluacion de un if el 0 se toma como False o None, esta funcion admite numeros negativos
    for i in range(intentos):   # La funcion iterara una cantidad de veces o hasta que el usuario logre ingresar un numero
        aux_numero = pedir_un_numero(texto_a_mostrar,numero_int)        
        if aux_numero != "z" and aux_numero >= 0:           # En caso de que lo que ingreso el usuario sea un numero y mayor a 0
            retorno = aux_numero                            # Guardara en el retorno el numero ingresado para ser devuelto
            break                                           # Rompera for para finalizar la funcion
        elif aux_numero != "z":                                         # En caso de que lo que ingreso el usuario sea un numero pero no mayor a 0
            print("\nError... El numero ingresado debe ser mayor a 0")  # Mostrara el siguiente mensaje y volvera a pareguntar
        else:                                                   
            print("\nError... No se ha ingresado un numero")        # O sino quiere decir que no se ingreso un numero, dira eso y volvera a preguntar       
        if i < intentos -1:
            print("...Intente nuevamente...\n")     # Mostrara este mensaje siempre que queden intentos
    return retorno

def pedir_un_numero_en_rango(texto_a_mostrar:str,intentos:int, min:float, max:float, numero_int:bool=True) -> int|float|bool:
    '''
    Esta funcion le pedira al usuario que ingrese un numero y lo evaluara en el rango
    Recibe: 
    .El texto que quiere ser mostrado en consola al momento de pedir el dato
    .La cantidad de intentos que se pedira el numero (El primero mas los intentos)
    .El minimo y maximo del rango
    .Un booleano que indica si debe ser un numero entero (True por defecto) o flotante (False)
    Devuelve el numero transformado a int o float en caso de que lo pudo tomar o "z" si fallo
    '''
    retorno = "z"               # La funcion retorna 'z' porque en la evaluacion de un if el 0 se toma como False o None, esta funcion admite numeros negativos
    for i in range(intentos):   # La funcion iterara una cantidad de veces o hasta que el usuario logre ingresar un numero
        aux_numero = pedir_un_numero(texto_a_mostrar, numero_int)
        if aux_numero != "z" and validar_rango(aux_numero, min, max):       # En caso de que lo que ingreso el usuario sea un numero y este dentro del rango valido
            retorno = aux_numero                                            # Guardara en el retorno el numero ingresado para ser devuelto
            break                                                           # Rompera for para finalizar la funcion
        elif aux_numero != "z":                                             # En caso de que lo que ingreso el usuario sea un numero pero este dentro del rango valido
            print("\nError... El numero ingresado no se encuentra dentro del rango valido") # Mostrara el siguiente mensaje y volvera a pareguntar
        else:
            print("\nError... No se ha ingresado un numero")    # O sino quiere decir que no se ingreso un numero, dira eso y volvera a preguntar
        if i < intentos -1:
            print("...Intente nuevamente...\n")     # Mostrara este mensaje siempre que queden intentos
    return retorno

def pedir_una_palabra(texto_a_mostrar:str) -> str:
    '''
    Esta funcion le pedira al usuario que ingrese un string que sea todo letras sin espacios
    Recibe el texto que quiere ser mostrado en consola al momento de pedir el dato
    Devuelve el string en caso de que lo pudo tomar o -1 si fallo o el texto no es solo texto
    '''
    retorno = -1
    texto = input(texto_a_mostrar)
    if re.match(r"^[a-zA-Z ]+$", texto):    # Si lo ingresado es solo texto, letras y espacios lo retornara
        retorno = texto
    return retorno

def pedir_confirmacion(texto_a_mostrar:str) ->bool:
    '''
    Esta funcion le pedira al usuario que ingrese si elige S, SI, Y, YES para confirmar o cualquier otra tecla para continuar
    Recibe el texto a mostrar cuando se active el input
    Devuelve un bool, True si confirmo o False en caso de que haya pasado cualquier otra cosa
    '''
    retorno = False
    texto = pedir_una_palabra(texto_a_mostrar)                      # El ususario solo tiene un intento
    if texto != -1 and re.match(r"^(s|si|y|yes)$", texto, re.I):    # En caso que el texto sea valido y alguna de esas posibilidaes retorna True
        retorno = True                                              # Quiere decir que confirmo, sino devuelve False
    return retorno  

def generar_str_nombres_jugadores_re_gex(lista_jugadores:list):
    '''
    Esta funcion creara un string con todos los nombres de los jugadores para poder buscar uno por su nombre a traves de regex
    Creara un string con el siguiente formato: "^(nombre_de_los_jugadores_separados_por|)$"
    Recibe la lista de Jugadores para buscar los nombres
    Devuelve la lista de nombres formateados o -1 si fallo
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        lista_string_nombres = "^(" + lista_jugadores[0]["nombre"]  
        for jugador in lista_jugadores[1:]:                         # Se van a guardar en un string todos los nombres separados por un '|'
            lista_string_nombres += "|" + jugador["nombre"]         # para incluir en un regex y hacer la evaluacion de los nombres con eso
        lista_string_nombres += ")$"
        retorno = lista_string_nombres
    else:
        print("Error... La lista esta vacia\n")
    return retorno

def pedir_nombre_jugador(lista_jugadores:list, texto_a_mostrar:str) -> str:
    '''
    Esta funcion le pedira al usuario que ingrese el nombre de un Jugador
    Recibe la lista de Jugadores para buscar los nombres posibles y el texto a mostrar cuando se pida el nombre
    Devuelve el nombre del Jugador o un -1 si no pudo elegir
    '''
    retorno = -1
    if len(lista_jugadores) > 0:  # En caso que la lista sea mayor a 0 se ejecutara la funcion  # Funcion que generara la lista de nombres 
        lista_string_nombres = generar_str_nombres_jugadores_re_gex(lista_jugadores)            # para poder ser comparados con lo que
        intentos = 4                                                                            # ingrese el usuario
        for i in range(intentos):                                   
            texto = pedir_una_palabra(texto_a_mostrar)                          # Se pide un texto solo con letras y espacios
            if texto != -1 and re.match(lista_string_nombres, texto, re.I):     # Dentro del regex van a estar todos los nombres como opciones. Da igual mayus o minus
                retorno = texto                                                 # Si el nombre coincide guardara en el retorno el nombre ingresado para ser devuelto
                break                                                           # Lo retornara y rompera el for
            elif texto != -1:                                                   # En caso de que lo que ingreso el usuario sea un texto pero no un nombre valido
                print("\nError... El texto ingresado no es una nombre valido.") # Mostrara el siguiente mensaje y volvera a pareguntar
            else:
                print("\nEl texto contiene un caracter que no es una letra.")   # O sino quiere decir que no se ingreso un ttexto, dira eso y volvera a preguntar
            if i < intentos -1:
                    print("...Intente nuevamente...\n")    
    else:
        print("Error... La lista esta vacia\n")
        
    return retorno    

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Imprimir en consola  ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def jugador_obtener_nombre_posicion(jugador:dict) -> str:
    '''
    Esta funcion obtendra el nombre y posicion del jugador
    Recibe un jugador
    Devuelve el string formateado de la siguiente manera:
    Nombre: Michael Jordan - Posicion: Escolta
    '''
    return "Nombre: {0} - Posicion: {1}".format(jugador["nombre"], jugador["posicion"])

def mostrar_jugadores_nombre_posicion(lista_jugadores:list) -> bool:
    '''
    Mostrar la lista de todos los jugadores del Dream Team. Con el formato Nombre - Posicion
    Recibe la lista de jugadores
    Devuelve True si se pudo ejecutar o False si la lista esta vacia
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        for jugador in lista_jugadores:                         # Recorrera la lista de jugadores
            print(jugador_obtener_nombre_posicion(jugador))     # La funcion devolvera: Nombre: Michael Jordan - Posicion: Escolta 
        print()                                                 # Y sera mostrado
        retorno = True
    else:
        print("Error... La lista esta vacia\n")
    
    return retorno

def mostrar_jugadores_indice_nombre_posicion(lista_jugadores:list) -> bool:
    '''
    Mostrar la lista de todos los jugadores del Dream Team. Con el formato Nombre - Posicion
    Recibe la lista de jugadores
    Devuelve True si se pudo ejecutar o False si la lista esta vacia
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        for i in range(len(lista_jugadores)):                                                       # Recorrera la lista de jugadores pero por el indice
            texto =  "{0} - {1}".format(i + 1, jugador_obtener_nombre_posicion(lista_jugadores[i])) # La funcion devolvera: Nombre: Michael Jordan - Posicion: Escolta 
            print(texto)                # El texto quedara: 1 - Nombre: Michael Jordan - Posicion: Escolta 
        print()
        retorno = True
    else:
        print("Error... La lista esta vacia\n")
    
    return retorno

def noramlizar_clave_estadistica_jugador(clave:str) -> str:
    '''
    Esta funcion normalizara las claves del diccionario de estadisticas del jugador para ser mostradas por consola. Tambien capitalizara 
    Recibe un string con la clave a normalizar
    Devuelve la clave normalizada
    '''
    lista_palabras_separadas = clave.split("_")                                 # Las claves vienen todas asi: promedio_rebotes_por_partido
    lista_palabras_separadas[0] = lista_palabras_separadas[0].capitalize()      # Capitalizara la primera palabra de la lista
    return " ".join(lista_palabras_separadas)                                   # Las juntara separadas por " ": Promedio rebotes por partido

def mostrar_estadisticas_jugador(jugador:dict):
    '''
    Esta funcion mostrara las estadisticas del jugador que se le pase por parametro
    Recibe el Jugador
    '''
    for clave,valor in jugador["estadisticas"].items():                                 # Mostrara las estadisticas del jugador aprovechando tomar clave,valor
        print("{0}: {1}".format(noramlizar_clave_estadistica_jugador(clave), valor))    # Se normaliza la clave estadistica. El texto queda "Temporadas: 19"

def mostrar_jugadores_nombre_posicion_key_estadisticas(lista_jugadores:list, key:str):
    '''
    Esta funcion mostrara la lista de Jugadores con formato nombre - posicion y una key del  diccionario esttadistica
    Recibe la lista de Jugadores y la key del dato a mostrar 
    Devuelve True si se pudo ejecutar o False si la lista esta vacia
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        for jugador in lista_jugadores:                                                             # Se obtiene nombre y posicion: Nombre: Michael Jordan - Posicion: Escolta
            print("{0} - {1}: {2}".format(jugador_obtener_nombre_posicion(jugador),                 # Se capitaliza la clave. Se muestra la estadistica del jugador. El texto queda:
                                          noramlizar_clave_estadistica_jugador(key),                # Michael Jordan - Posicion: Escolta - Promedio rebotes por partido: 30.8
                                          jugador["estadisticas"]["promedio_puntos_por_partido"]))
        retorno = True
    else:
        print("Error... La lista esta vacia\n")
    
    return retorno

def mostrar_logros_jugador(jugador:dict):
    '''
    Esta funcion mostrara los logross del jugador que se le pase por parametro
    Recibe el Jugador
    '''
    for logro in jugador["logros"]:
        print(logro)

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Funciones de ordenamiento  ------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def quick_sort_jugadores_key(lista_jugadores:list, key:str, asc_desc:bool=True) -> list:
    '''
    Esta funcion ordenara la lista de Jugadores segun una clave y segun un criterio, asecendente o descendente
    Recibe la lista de Jugadores, un string que representa la clave a buscar y un booleano que representa si asc (True, por defecto) o desc (False)
    Devolvera una nueva lista ordenada
    '''
    lista_derecha = []
    lista_izquierda = []
    if len(lista_jugadores) <= 1:
        return lista_jugadores
    else:
        pivot = lista_jugadores[0]
        for diccionario in lista_jugadores[1:]:
            if diccionario[key] > pivot[key] and asc_desc == True or diccionario[key] < pivot[key] and asc_desc == False:
                lista_derecha.append(diccionario)
            else:
                lista_izquierda.append(diccionario)
    lista_izquierda = quick_sort_jugadores_key(lista_izquierda,key,asc_desc)
    lista_izquierda.append(pivot)
    lista_derecha = quick_sort_jugadores_key(lista_derecha,key,asc_desc)
    lista_izquierda.extend(lista_derecha)
    return lista_izquierda

def quick_sort_jugadores_estadisticas_key(lista_jugadores:list, key:str, asc_desc:bool=True) -> list:
    '''
    Esta funcion ordenara la lista de Jugadores segun una clave en el diccionario de estadisticas y segun un criterio, asecendente o descendente
    Recibe la lista de Jugadores, un string que representa la clave a buscar y un booleano que representa si asc (True, por defecto) o desc (False)
    Devolvera una nueva lista ordenada
    '''
    lista_derecha = []
    lista_izquierda = []
    if len(lista_jugadores) <= 1:
        return lista_jugadores
    else:
        pivot = lista_jugadores[0]
        for jugador in lista_jugadores[1:]:
            if jugador["estadisticas"][key] > pivot["estadisticas"][key] and asc_desc == True or jugador["estadisticas"][key] < pivot["estadisticas"][key] and asc_desc == False:
                lista_derecha.append(jugador)
            else:
                lista_izquierda.append(jugador)
    lista_izquierda = quick_sort_jugadores_estadisticas_key(lista_izquierda,key,asc_desc)
    lista_izquierda.append(pivot)
    lista_derecha = quick_sort_jugadores_estadisticas_key(lista_derecha,key,asc_desc)
    lista_izquierda.extend(lista_derecha)
    return lista_izquierda

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Funciones de calculo  ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def buscar_jugador_por_nombre(lista_jugadores:list, nombre_jugador:str) -> dict:
    '''
    Esta funcion buscara un Jugador por su nombre y devolvera el diccionario
    Recibe la lista de Jugadores y el nombre del Jugador a buscar, previamente validado
    Devuelve el Jugador o False si no se pudo ejecutar
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        for jugador in lista_jugadores:                                 # Recorrera la lista de jugadores preguntando si el nombre
            if re.match(nombre_jugador, jugador["nombre"], re.I):       # que le pase por parametro coincide con el del jugador
                retorno = jugador                                       # El nombre ya esta validado, deberia estar. 
                break                                                   # Retornara el jugador cuando lo encuentre
    else:                                                               
        print("Error... La lista esta vacia\n")
    
    return retorno

def calcular_jugador_max_key_estadistica(lista_jugadores:list, key:str) -> dict:
    '''
    Recibirá por parámetro la lista de jugadores, una key (string) la cual representará el dato que deberá ser evaluado a efectos de determinar cuál es el máximo de 
    la lista. Esta funcion esta preparada para hacer los calculos en la clave["estadisticas"] del diccionario Jugador
    Retornara -1 si la lista esta vacia o el diccionario que tenga el dato más alto
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        indice_max =  0
        for i in range(1, len(lista_jugadores)): 
            if i == 0 or lista_jugadores[i]["estadisticas"][key] > lista_jugadores[indice_max]["estadisticas"][key]:
                indice_max = i
        retorno = lista_jugadores[indice_max]
    else:
        print("\nError... La lista esta vacia")
    
    return retorno

def calcular_jugador_min_key_estadistica(lista_jugadores:list, key:str) -> dict:
    '''
    Recibirá por parámetro la lista de jugadores, una key (string) la cual representará el dato que deberá ser evaluado a efectos de determinar cuál es el minimo de 
    la lista. Esta funcion esta preparada para hacer los calculos en la clave["estadisticas"] del diccionario Jugador
    Retornara -1 si la lista esta vacia o el diccionario que tenga el dato más alto
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        indice_min =  0
        for i in range(1, len(lista_jugadores)):
            if i == 0 or lista_jugadores[i]["estadisticas"][key] < lista_jugadores[indice_min]["estadisticas"][key]:
                indice_min = i
        retorno =  lista_jugadores[indice_min]
    else:
        print("\nError... La lista esta vacia")
    return retorno
    
def calcular_max_min_key_estadistica(lista_jugadores:list, key:str, max_min:bool=True) -> dict:
    '''
    .Recibira la lista de jugadores, un string que representa la key del dato a calcular y un valor bool que puede tomar los valores 
    "True" (por defecto) para maximo o "False" para minimo para elegir que calcular
    La funcion esta preparada para trabjar los datos en la clave ["estadistica"] del diccionario Jugador
    .Busca el maximo o minimo
    .Retorna -1 si la lista esta vacia o el diccionario que cumpla la condicion
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        if max_min:
            retorno = calcular_jugador_max_key_estadistica(lista_jugadores, key)
        else:
            retorno = calcular_jugador_min_key_estadistica(lista_jugadores, key)
    else:
        print("\nError... La lista esta vacia")

    return retorno

def calcular_mostrar_jugador_max_min_key_estadisticas(lista_jugadores:list, texto_a_mostrar:str, key:str, max_min:bool=True) -> bool:
    '''
    Esta funcion calculara y mostrara el jugador con mayor o menor cantidad de la key pasada por parametro y lo mostrara por consola.
    Recibe: 
    .La lista de Jugadores
    .El texto que se mostrara al momento de mostrar el jugador que cumple el criterio con el siguiente formato:
    "\nEl/los Jugador/es con mayor/menor cantidad la key (de robos totales) es/son:"
    .La key dentro del diccionario estadistica dentro del diccionario jugador para ser calculada y mostrada
    .Un booleano que indica si se calculara el maximo (True, por defecto) o el minimo (False)
    Devuelve False si fallo o True si la funcion se ejecuto
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        jugador_max_min = calcular_max_min_key_estadistica(lista_jugadores, key, max_min)       # Calculara el jugador maximo o minimo dependiendo de lo pasado por parametro
        if jugador_max_min != -1:                                                               # Si es un jugador valido 
            print(texto_a_mostrar)                                                              # Imprimira el texto pasado por parametro
            for jugador in lista_jugadores:                                                     # Y recorrera la lista de jugadores preguntando si el valor de la estadistica pasada como key
                if jugador["estadisticas"][key] == jugador_max_min["estadisticas"][key]:        # es igual a la del jugador que se esta iterando lo mostrara por pantalla
                    print(jugador_obtener_nombre_posicion(jugador))                             # Con el siguiente formato: Nombre: Michael Jordan - Posicion: Escolta
            print("Con una cantidad de:", jugador_max_min["estadisticas"][key])                 # Mostrara el valor de la estadistica
        retorno = True
    else:
        print("\nError... La lista esta vacia")

    return retorno

def calcular_mostrar_jugadores_promedio_key_mayor_menor_valor_ingresado(lista_jugadores:list, key:str, texto_input:str, mayor_menor:bool=True) -> bool:
    '''
    Esta funcion calculara y mostrara los jugadores que tengan un promedio en la key pedida mayor o menor al numero ingresado por el usuario
    Recibe:  
    .La lista de Jugadores
    .Un string que representara la key del dato a buscar
    .Un string que sera el texto mostrado por pantalla cuando se pida el numero
    .Un booleando que indica si se mostraran los mayores (True, por defecto) al numero ingresado o los menores (False) 
    Devuelve False si fallo o True si la funcion se ejecuto
    '''
    retorno = False
    flag = False
    lista_aux = []
    if len(lista_jugadores) > 0:
        numero_ingresado = pedir_un_numero_positivo(texto_input, 4, False)      # Pedira un numero positivo
        if numero_ingresado != "z":    # La funcion retorna 'z' porque en la evaluacion de un if el 0 se toma como False o None, esta funcion admite numeros negativos             
            print("\nEl {0} ingresado es: {1}".format(noramlizar_clave_estadistica_jugador(key),numero_ingresado))
            if mayor_menor:     
                # Se hara una lista con los jugadores que superen el numero ingresado
                lista_aux = buscar_jugadores_key_estadistica_mayor_menor_numero_ingresado(lista_jugadores, key, numero_ingresado)   
                # Se evaluara si esa lista esta vacia y se mostraran los mensajes correspondientes
                flag = evaluar_lista_vacia(lista_aux, "\nLos jugadores que lo superan son:", "\nNo hay jugadores por encima del numero ingresado")
            else:
                # Se hara una lista con los jugadores que esten debajo del numero ingresado
                lista_aux = buscar_jugadores_key_estadistica_mayor_menor_numero_ingresado(lista_jugadores, key, numero_ingresado, False) 
                # Se evaluara si esa lista esta vacia y se mostraran los mensajes correspondientes
                flag = evaluar_lista_vacia(lista_aux, "\nLos jugadores que estan por debajo son:", "\nNo hay jugadores por debajo del numero ingresado")
            if flag:                                                                # En caso que la lista no este vacia el flag estara en True y mostrara los jugadores
                mostrar_jugadores_nombre_posicion_key_estadisticas(lista_aux, key)  # Ejemplo:  Michael Jordan - Posicion: Escolta - Promedio rebotes por partido: 30.8
        else:
            print("...Sera devuelto al menu...")
        retorno = True
    else:
        print("\nError... La lista esta vacia")

    return retorno

def buscar_jugadores_key_estadistica_mayor_menor_numero_ingresado(lista_jugadores:list, key:str, valor_ingresado:float, mayor_menor:bool=True) -> list:
    '''
    Esta funcion buscara los jugadores que esten por encima o debajo del valor pasado por parametro y los guardara en una lista
    Recibe:  
    .La lista de Jugadores
    .Un string que representara la key del dato a buscar
    .El numero que servira de parametro para elegir
    .Un booleando que indica si se buscaran los mayores (True, por defecto) al numero ingresado o los menores (False) 
    Devuelve la lista de jugadores
    '''
    lista_aux = []
    if len(lista_jugadores) > 0:
        if mayor_menor:
            for jugador in lista_jugadores:
                if jugador["estadisticas"][key] >= valor_ingresado:
                    lista_aux.append(jugador)
        else:
            for jugador in lista_jugadores:
                if jugador["estadisticas"][key] <= valor_ingresado:
                    lista_aux.append(jugador)     
    else:
        print("\nError... La lista esta vacia")

    return lista_aux

def evaluar_lista_vacia(lista_personajes:list, mensaje_1:str, mensaje_2:str) -> bool:
    '''
    Esta funcion evaluara si la lista generada de personajes esta vacia o no. Imprimira un mensaje pasado por parametro dependiendo del resultado 
    y devuelve True o False segun corresponda
    Recibe:  
    .La lista de Jugadores
    .Un string que sera el texto mostrado por pantalla en caso que el tamaño de la lista sea mayor a 0
    .Un string que sera el texto mostrado por pantalla en caso que el tamaño de la lista sea igual a 0
    Devuelve True si el tamaño de la lista es mayor a 0 o False si es igual a 0
    '''
    retorno = False
    if len(lista_personajes) > 0:
        print(mensaje_1)
        retorno = True
    else:
        print(mensaje_2)
    return retorno

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Funciones del menu  -------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def mostrar_guardar_estadisticas_jugador_por_indice(lista_jugadores:list) -> bool:
    '''
    Esta funcion pedira un indice de Jugador al usuario para mostrar todas sus estadisticas y las guardara en un archivo si el usuario quiere
    Recibe la lista de jugadores
    Devuelve True si se pudo ejecutar la funcion o False si la lista esta vacia
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        mostrar_jugadores_indice_nombre_posicion(lista_jugadores) # Muestra los jugadores en el siguiente formato: 1 - Nombre: Michael Jordan - Posicion: Escolta 
        indice_jugador = pedir_un_numero_en_rango("Ingrese el indice del Jugador que quiere mostrar: ", 4, 1, len(lista_jugadores)) #Pide un numero dentro de ese rango
        if indice_jugador != "z": #En caso que sea un numero valido se le restara 1 para respetar los indices de cada jugador real en la lista
            indice_jugador -= 1
            print()
            print(jugador_obtener_nombre_posicion(lista_jugadores[indice_jugador]), "\n")   # Imprime el jugador seleccionado en el siguiente formato: Nombre: Michael Jordan - Posicion: Escolta 
            mostrar_estadisticas_jugador(lista_jugadores[indice_jugador])                   # Imprime las estadisticas del jugador
            print("\n¿Quiere guardar el jugador en un archivo?")
            # Pregunta si quiere guardar el jugador en un archivo y de confirmar lo hace
            if pedir_confirmacion("Ingrese [s-si-y-yes] para confirmar o cualquier otra tecla para continuar: "):
                # Crea un Archivo con el siguiente nombre formateado con el nombre del jugador   
                nombre_archivo = "C:\Python\Dram_Team_Parcial1\estadisticas_{0}.csv".format(lista_jugadores[indice_jugador]["nombre"])
                # Se formatean las estadisticas del jugador en un texto y se escribe en un archivo .csv
                guardar_archivo_csv(nombre_archivo, generar_string_csv_jugador_nombre_posicion_estadisticas(lista_jugadores[indice_jugador]))
            else:
                print("\n... Los datos no se han guardado ...\n")
            retorno = True
        else:
            print("... Ha realizado muchos intentos, Sera devuelto al menu ...\n")
    else:
        print("Error... La lista esta vacia\n")
    return retorno

def mostrar_logros_jugador_por_nombre(lista_jugadores:list) -> bool:
    '''
    Esta funcion pedira al usuario que ingrese el nombre del Jugador que quiere ver los logros y los mostrara por consola
    Recibe la lista de Juagadores
    Devuelve True si se pudo ejecutar la funcion o False si la lista esta vacia
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        mostrar_jugadores_nombre_posicion(lista_jugadores) # Muestra los jugadores en el siguiente formato: Nombre: Michael Jordan - Posicion: Escolta 
        nombre_jugador = pedir_nombre_jugador(lista_jugadores, "Ingrese el nombre del Jugador que quiere ver los logros: ") # Pide el nombre del jugador validado
        if nombre_jugador != -1:                                                    # En caso que sea un nombre valido
            jugador = buscar_jugador_por_nombre(lista_jugadores, nombre_jugador)    # Busca el jugador por el nombre
            print()
            print(jugador_obtener_nombre_posicion(jugador))                         # Imprime el jugador seleccionado en el siguiente formato: Nombre: Michael Jordan - Posicion: Escolta 
            mostrar_logros_jugador(jugador)                                         # Mostrara los logros del jugador del nombre ingresado
            retorno = True
        else:
            print("... Ha realizado muchos intentos, Sera devuelto al menu ...\n")
    else:
        print("Error... La lista esta vacia\n")
    return retorno

def mostrar_si_jugador_es_miembro_salon_fama(lista_jugadores:list) -> bool:
    '''
    Esta funcion pedira al usuario que ingrese el nombre del Jugador y el programa respondera si uno de sus logros es ser miembro de la fama del baloncesto
    Recibe la lista de Juagadores
    Devuelve True si se pudo ejecutar la funcion o False si la lista esta vacia
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        mostrar_jugadores_nombre_posicion(lista_jugadores)  # Muestra los jugadores en el siguiente formato: Nombre: Michael Jordan - Posicion: Escolta 
        nombre_jugador = pedir_nombre_jugador(lista_jugadores, "Ingrese el nombre del Jugador: ")   # Pide el nombre del jugador validado
        if nombre_jugador != -1: # En caso que sea un nombre valido
            jugador = buscar_jugador_por_nombre(lista_jugadores, nombre_jugador)            # Buscara el jugador del nombre ingresado
            if "Miembro del Salon de la Fama del Baloncesto" in jugador["logros"]:          # En caso que el logro pertenezca a la lista de logros del jugador
                print("\nEl Jugador es Miembro del Salon de la Fama del Baloncesto")        # Mostrara este mensaje
            else:
                print("\nEl Jugador no es Miembro del Salon de la Fama del Baloncesto")     # Sino mostrara este mensaje
            retorno = True
        else:
            print("... Ha realizado muchos intentos, Sera devuelto al menu ...\n")
    else:
        print("Error... La lista esta vacia\n")
    return retorno

def calcular_mostrar_jugador_con_mas_logros(lista_jugadores:list) ->bool:
    '''
    Esta funcion calculara y mostrara cual es el jugador con mas logros y lo mostrara en consola
    Retornara False si no pudo ejecutarse o True si pudo
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        indice_max = 0
        for i in range(1, len(lista_jugadores)):
            if len(lista_jugadores[i]["logros"]) > len(lista_jugadores[i]["logros"]):     # Se busca el jugador con la Maxima cantidad de logros
                indice_max = i
        print("\nEl jugador con mas logros es:\n")                                          
        print(jugador_obtener_nombre_posicion(lista_jugadores[indice_max]))                         # Muestra los jugadores en el siguiente formato: Nombre: Michael Jordan - Posicion: Escolta 
        print("Cantidad de logros: {0}\n".format(len(lista_jugadores[indice_max]["logros"])))       # Muestra la cantidad de logros del jugador
        mostrar_logros_jugador((lista_jugadores[indice_max]))                                       # Muestra los logros del jugador
        retorno = True
    else:
        print("\nError... La lista esta vacia")
    
    return retorno

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Funciones generacion del menu  --------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def imprimir_menu():
    '''
    Imprimira el menu principal de la funcion en pantalla
    '''
    print("\n1. Mostrar la lista de todos los jugadores del Dream Team")
    print("2. Mostrar estadicticas de un Jugador seleccionado por Indice")
    print("3. Buscar un Jugador por nombre y mostrar sus logros")
    print("4. Mostrar los Jugadores ordenados de forma ascendente segun su promedio de puntos por partido")
    print("5. Buscar un Jugador por nombre y mostrar si pertenece al Salon de la Fama")
    print("6. Mostrar el Jugador con mayor cantidad de rebotes totales")
    print("7. Mostrar el Jugador con mayor porcentaje de tiros de campo")
    print("8. Mostrar el Jugador con mayor cantidad de asistencias totales")
    print("9. Mostrar los Jugador con mayor promedio de puntos por partido a partir de un numero ingresado")
    print("10. Mostrar los Jugador con mayor promedio de rebotes por partido a partir de un numero ingresado")
    print("11. Mostrar los Jugador con mayor promedio de asisetncias por partido a partir de un numero ingresado")
    print("12. Mostrar el Jugador con mayor cantidad de robos totales")
    print("13. Mostrar el Jugador con mayor cantidad de bloqueos totales")
    print("14. Mostrar los Jugador con mayor porcentaje de tiros libres a partir de un numero ingresado")
    print("15. Mostrar los Jugadores segun el promedio de puntos por partido excluyendo el jugador que menos tenga")
    print("16. Mostrar el Jugador con mas Logros")
    print("17. Mostrar los Jugador con mayor porcentaje de tiros triples a partir de un numero ingresado")
    print("18. Mostrar el Jugador con mayor cantidad de temporadas")
    print("19. Mostrar los Jugador con mayor porcentaje de tiros de campo a partir de un numero ingresado, ordenados por posicion en la cancha")
    print("20. Punto Bonus")
    print("21. Mostrar la cantidad de jugadores por posicion")
    print("22. Mostrar la lista de Jugadores ordanada de forma descendente por la cantidad de All-Star")
    print("23. Mostrar los Jugadores con mas estadistica de cada una")
    print("24. Salir del programa\n")

def pedir_opcion_menu_principal_numero(texto_a_mostrar:str,intentos:int,min:int,max:int):
    '''
    .Imprimira el menu de opciones, pedira la opcion y validara que sea una letra
    .Recibe el texto a mostrar cuando pide la opcion, la catidad de intentos que tendra el usuario, el minimo y el maximo que corresponda a las opciones disponibles
    .En caso de ser valida, devolvera la opcion sino devolvera -1
    '''
    retorno = -1
    imprimir_menu()
    retorno = pedir_un_numero_en_rango(texto_a_mostrar,intentos,min,max)
    
    return retorno
    
def dream_team_app(lista_jugadores:list):
    '''
    .Funcion principal que desplegara  el menu de opciones y  ejecutaralas funciones
    .Recibe la lista de jugadores
    .Funcion principal del programa que se encargara de la ejecucion de las funciones del menu
    '''
    while True:
        opcion = pedir_opcion_menu_principal_numero("Ingrese la opcion: ",6,1,24)
        print()
        match opcion:
            case 1:
                mostrar_jugadores_nombre_posicion(lista_jugadores)
            case 2:
                mostrar_guardar_estadisticas_jugador_por_indice(lista_jugadores)
            case 3:
                mostrar_logros_jugador_por_nombre(lista_jugadores)
            case 4:
                aux_lista = quick_sort_jugadores_estadisticas_key(lista_jugadores, "promedio_puntos_por_partido")
                mostrar_jugadores_nombre_posicion_key_estadisticas(aux_lista, "promedio_puntos_por_partido")
            case 5:
                mostrar_si_jugador_es_miembro_salon_fama(lista_jugadores)
            case 6:
                calcular_mostrar_jugador_max_min_key_estadisticas(lista_jugadores, "El Jugador con mayor cantidad de rebotes totales es:\n", "rebotes_totales")
            case 7:
                calcular_mostrar_jugador_max_min_key_estadisticas(lista_jugadores, "El Jugador con mayor porcentaje de tiros de campo es:\n", "porcentaje_tiros_de_campo")
            case 8:
                calcular_mostrar_jugador_max_min_key_estadisticas(lista_jugadores, "El Jugador con mayor cantidad de asistencias totales es:\n", "asistencias_totales")
            case 9:
                aux_lista = quick_sort_jugadores_estadisticas_key(lista_jugadores, "promedio_puntos_por_partido")
                calcular_mostrar_jugadores_promedio_key_mayor_menor_valor_ingresado(aux_lista, "promedio_puntos_por_partido", 
                                                        "Ingrese el promedio de puntos por partido minimo que deben tener los jugadores (el maximo es 30.1): ")
            case 10:
                aux_lista = quick_sort_jugadores_estadisticas_key(lista_jugadores, "promedio_rebotes_por_partido")
                calcular_mostrar_jugadores_promedio_key_mayor_menor_valor_ingresado(aux_lista, "promedio_rebotes_por_partido", 
                                                        "Ingrese el promedio de rebotes por partido minimo que deben tener los jugadores (el maximo es 11.7): ")
            case 11:
                aux_lista = quick_sort_jugadores_estadisticas_key(lista_jugadores, "promedio_asistencias_por_partido")
                calcular_mostrar_jugadores_promedio_key_mayor_menor_valor_ingresado(aux_lista, "promedio_asistencias_por_partido", 
                                                        "Ingrese el promedio de asistencias por partido minimo que deben tener los jugadores (el maximo es 11.2): ")
            case 12:
                calcular_mostrar_jugador_max_min_key_estadisticas(lista_jugadores, "El Jugador con mayor cantidad de robos totales es:\n", "robos_totales")
            case 13:
                calcular_mostrar_jugador_max_min_key_estadisticas(lista_jugadores, "El Jugador con mayor cantidad de bloqueos totales es:\n", "bloqueos_totales")
            case 14:
                aux_lista = quick_sort_jugadores_estadisticas_key(lista_jugadores, "porcentaje_tiros_libres")
                calcular_mostrar_jugadores_promedio_key_mayor_menor_valor_ingresado(aux_lista, "porcentaje_tiros_libres", 
                                                        "Ingrese el porcentaje de tiros libres minimo que deben tener los jugadores (el maximo es 88.6): ")
            case 15:
                aux_lista = quick_sort_jugadores_estadisticas_key(lista_jugadores, "promedio_puntos_por_partido", False)
                mostrar_jugadores_nombre_posicion_key_estadisticas(aux_lista[:-1], "promedio_puntos_por_partido")
            case 16:
                calcular_mostrar_jugador_con_mas_logros(lista_jugadores)
            case 17:
                aux_lista = quick_sort_jugadores_estadisticas_key(lista_jugadores, "porcentaje_tiros_triples")
                calcular_mostrar_jugadores_promedio_key_mayor_menor_valor_ingresado(aux_lista, "porcentaje_tiros_triples", 
                                                        "Ingrese el porcentaje de tiros triples minimo que deben tener los jugadores (el maximo es 45.5): ")
            case 18:
                calcular_mostrar_jugador_max_min_key_estadisticas(lista_jugadores, "Los Jugadores con mayor cantidad de temporadas son:\n", "temporadas")
            case 19:
                aux_lista = quick_sort_jugadores_key(lista_jugadores, "posicion")
                calcular_mostrar_jugadores_promedio_key_mayor_menor_valor_ingresado(aux_lista, "porcentaje_tiros_de_campo", 
                                                        "Ingrese el porcentaje de tiros de campo minimo que deben tener los jugadores (el maximo es 54): ")
            case 20:
                guardar_calcular_ranking_dream_team(lista_jugadores)
            case 21:
                print("\nCantidad de Jugadores por posicion:\n")
                mostrar_cantidad_jugadores_key(lista_jugadores, "posicion")
            case 22:
                print("\nLista de jugadores ordenada por cantidad de All-Star:\n")
                mostrar_ordenar_jugadores_cantidad_all_stars(lista_jugadores)
            case 23:
                print("\nLos Jugadores con mas estadistica de cada una son:\n")
                mostrar_calcular_mejor_jugador_cada_estadistica(lista_jugadores)
            case 24:
                if pedir_confirmacion("Esta seguro que quiere salir del programa? Ingrese [s-si-y-yes] para confirmar o cualquier otra tecla para seguir en el programa: "):
                    break
                else:
                    print("... Sera devuelto al menu ...")
            case _:
                print("... Ha realizado muchos intentos, intente denuevo mas tarde ...")
                break
        
        input("\n...Presione 'enter' para continuar...  ")
        os.system("cls")
    print("\n\n... Gracias por utilizar el programa. Hasta luego ...")

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Funciones punto bonus  ----------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def obtener_diccionario_nombres_jugadores(lista_jugadores:list) -> dict:
    '''
    Esta función itera la lista de jugadores creando un diccionario donde cada clave sera el nombre de un jugador
    Cada jugador, a su vez, tendra un diccionario
    Recibe por parámetro la lista de jugadores
    Devuelve el diccionario de diccionarios o -1 si no se pudo ejecutar
    '''
    retorno = -1
    diccionario_nombres = {}
    if len(lista_jugadores) > 0:
        for jugador in lista_jugadores:                         # Itera la lista de jugadores
            if jugador["nombre"] not in diccionario_nombres:    # En caso que el nombre del jugador no sea clave del diccionario la agrega
                diccionario_nombres[jugador["nombre"]] = {}     # El valor de la nueva clave, que es el nombre del jugador, sera un diccionario
        retorno = diccionario_nombres                           # En ese diccionario se guardara el ranking de cada uno
    else:
        print("\nError... La lista esta vacia")
    return retorno

def set_ranking_jugador_key(lista_jugadores:list, diccionario_jugadores:dict, key:str):
    '''
    Esta funcion seteara el puesto en el ranking de la key pasada por parametro de cada jugador
    Recibe la lista de jugadores, el diccionario con los nombres como clave y la key del ranking a setear
    Retornara False si no pudo ejecutarse o True si pudo
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        aux_lista_jugadores = quick_sort_jugadores_estadisticas_key(lista_jugadores, key, False)  # Ordena la lista segun la key en orden descendente
        for i in range(len(aux_lista_jugadores)):                   # Itera la lista de jugadores por indice
            for clave in diccionario_jugadores:                     # Itera el diccionario de jugadores para obtener el nombre de cada uno que es la clave
                if aux_lista_jugadores[i]["nombre"] == clave:       # Si el nombre del jugador buscado por indice es igual al de la clave
                    diccionario_jugadores[clave][key] = i + 1       # Agregara al diccionario ranking dentro del diccionario de jugadores por nombre
        retorno = True                                              # una nueva clave, la estadistica, con valor i + 1 para guardar el ranking arrancando por 1
    else:
        print("\nError... La lista esta vacia")
    
    return retorno

def armar_ranking_dream_team(lista_jugadores:list) -> dict:
    '''
    Esta funcion sseteara las posiciones en el ranking de cada jugador luego de crear el diccionario con los nombres de cada jugador
    Retornara False si no pudo ejecutarse o el diccionario con el ranking
    '''
    retorno = False
    diccionario_jugadores = {}
    if len(lista_jugadores) > 0:
        diccionario_jugadores = obtener_diccionario_nombres_jugadores(lista_jugadores)          # Se crea el diccionario de jugadores con sus nombres como clave
        set_ranking_jugador_key(lista_jugadores, diccionario_jugadores, "puntos_totales")       # Se setea el puesto de cada jugador en el ranking de puntos
        set_ranking_jugador_key(lista_jugadores, diccionario_jugadores, "rebotes_totales")      # Se setea el puesto de cada jugador en el ranking de rebotes
        set_ranking_jugador_key(lista_jugadores, diccionario_jugadores, "asistencias_totales")  # Se setea el puesto de cada jugador en el ranking de asistencias
        set_ranking_jugador_key(lista_jugadores, diccionario_jugadores, "robos_totales")        # Se setea el puesto de cada jugador en el ranking de robos
        retorno = diccionario_jugadores
    else:
        print("\nError... La lista esta vacia")
    
    return retorno

def formatear_ranking_csv(diccionario_jugadores:dict) -> str:
    '''
    . Recibe por parámetro el diccionario de jugadores y crea un string con todos los datos en formato csv
    . El caracter separador es la "," y el que termina la linea "\n"
    '''
    texto = "Jugador,Puntos,Rebotes,Asistencias,Robos\n"
    for nombre,diccionario_ranking in diccionario_jugadores.items():
        texto += "{0},{1},{2},{3},{4}\n".format(nombre, diccionario_ranking["puntos_totales"], diccionario_ranking["rebotes_totales"],
                                                diccionario_ranking["asistencias_totales"], diccionario_ranking["robos_totales"])
    return texto

def guardar_calcular_ranking_dream_team(lista_jugadores:list) -> bool:
    '''
    Esta funcion creara y guardara el ranking de jugadores de la siguiente forma 
    Jugador         - Puntos - Rebotes - Asistencias - Robos
    Michael Jordan  -   1    -    1    -     1       -   2
    Recibe la lista de jugadores
    Retornara False si no pudo ejecutarse o el diccionario con el ranking
    '''
    retorno = False
    diccionario_jugadores = {}
    if len(lista_jugadores) > 0:
        diccionario_jugadores = armar_ranking_dream_team(lista_jugadores)
        nombre_archivo = "C:\Python\Dram_Team_Parcial1\Ranking.csv"
        guardar_archivo_csv(nombre_archivo, formatear_ranking_csv(diccionario_jugadores))
        retorno = True
    else:
        print("\nError... La lista esta vacia")
    
    return retorno

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------  Funciones ejercicion extra  ------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def obtener_lista_de_key_jugadores(lista_jugadores:list, key:str) -> set:
    '''
    . Esta función itera la lista de jugadores guardando las posiciones de los Jugadores en una lista
    . Recibe por parámetro la lista de jugadores y un string que representará el tipo de dato/key a buscar
    . Devuelve un set de datos o -1 si fallo
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        lista_aux = []
        for jugador in lista_jugadores:
            aux = jugador[key]
            lista_aux.append(aux)
            retorno = set(lista_aux)
    else:
        print("\nError... La lista esta vacia")    

    return retorno

def obtener_cantidad_jugadores_key(lista_jugadores:list, set_datos_posiciones:set, key:str) -> dict:
    '''
    Esta funcion iterara el set de posiciones y creara un diccionario con cada variable del set como key y el valor de cada una sera un contador
    A su vez recorrera la lista de jugadores, evaluara la clave que da origen al set de datos y en caso de que el valor corresponda guardara aumentara
    en uno el contador. Si el diccionario fue creado se inicializa en 1
    Recibe la lista de jugadores, el set de datos con las posiciones, la key, en este caso de posiciones
    Esta función retornará un diccionario con cada variedad como key y una lista de diccionarios como valor, o -1 si fallo
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        diccionario_contador = {}
        for tipo in set_datos_posiciones:
            if tipo not in diccionario_contador:
                diccionario_contador[tipo] = 1
            for jugador in lista_jugadores:           
                if jugador[key] == tipo:
                    diccionario_contador[tipo] += 1
        retorno = diccionario_contador
    else:
        print("\nError... La lista esta vacia")  

    return retorno

def mostrar_cantidad_jugadores_key(lista_jugadores:list, key:str):
    '''
    Esta funcion contara la cantidad de jugadores por posicion y lo mostrara en pantalla
    Recibe la lista de jugadores y la key del tipo que se quiere contar
    Devuelve False si fallo o True si se ejecuto
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        set_datos_posiciones = obtener_lista_de_key_jugadores(lista_jugadores, key)
        diccionario_posiciones = obtener_cantidad_jugadores_key(lista_jugadores, set_datos_posiciones, key)
        for posicion,cantidad in diccionario_posiciones.items():
            print("{0}: {1}".format(posicion,cantidad))
        retorno = True  
    else:
        print("\nError... La lista esta vacia")  
        
    return retorno

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def calcular_cantidad_all_stars(lista_jugadores:list) ->list:
    '''
    Esta funcion calculara la cantidad de all stars que tiene cada jugador y creara una lista de jugadores con clave nombre y clave cantidad de all stars
    Recibe la lista de jugadores
    Devuelve -1 si fallo o la lista si se ejecuto
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        lista_all_star = []
        for jugador in lista_jugadores:
            for logro in jugador["logros"]:
                if re.search(r"all-star", logro, re.I) and re.search(r"[0-9]+", logro):
                    diccionario_aux = {}
                    diccionario_aux["nombre"] = jugador["nombre"]
                    diccionario_aux["cant_all_stars"] = int(logro[:2])
                    lista_all_star.append(diccionario_aux)
                    break
        retorno = lista_all_star
    else:
        print("\nError... La lista esta vacia")  
        
    return retorno  

def mostrar_ordenar_jugadores_cantidad_all_stars(lista_jugadores:list):
    '''
    Esta funcion ordenara la cantidad de jugadores por cantidad de all stars que tengan
    Recibe la lista de jugadores y la key del tipo que se quiere contar
    Devuelve False si fallo o True si se ejecuto
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        lista_nombre_cantallstar = calcular_cantidad_all_stars(lista_jugadores)
        lista_nombre_cantallstar = quick_sort_jugadores_key(lista_nombre_cantallstar, "cant_all_stars", False)
        for jugador in lista_nombre_cantallstar:
            print("{0}: {1}".format(jugador["nombre"], jugador["cant_all_stars"]))
        retorno = True  
    else:
        print("\nError... La lista esta vacia")  
        
    return retorno    

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
def obtener_lista_de_key_jugadores_estadistica(lista_jugadores:list) -> set:
    '''
    . Esta función itera la lista de jugadores guardando en una lista las distintas claves de estadistica, recorre todos los jugadores
    por si no todos tienen todo
    . Recibe por parámetro la lista de jugadores y un string que representará el tipo de dato/key a buscar
    . Devuelve un set de datos o -1 si fallo
    '''
    retorno = -1
    if len(lista_jugadores) > 0:
        lista_aux = []
        for jugador in lista_jugadores:
            for estadistica in jugador["estadisticas"]:
                lista_aux.append(estadistica)
        retorno = set(lista_aux)
    else:
        print("\nError... La lista esta vacia")    

    return retorno

def mostrar_calcular_mejor_jugador_cada_estadistica(lista_jugadores:list):
    '''
    Esta funcion ordenara la cantidad de jugadores por cantidad de all stars que tengan
    Recibe la lista de jugadores y la key del tipo que se quiere contar
    Devuelve False si fallo o True si se ejecuto
    '''
    retorno = False
    if len(lista_jugadores) > 0:
        set_claves_estadistica = obtener_lista_de_key_jugadores_estadistica(lista_jugadores)
        for clave in set_claves_estadistica:
            jugador = calcular_jugador_max_key_estadistica(lista_jugadores, clave)
            if re.search(r"promedio", clave, re.I):
                print("El mayor {0} es para: {1} con: {2}".format(noramlizar_clave_estadistica_jugador(clave), jugador["nombre"], jugador["estadisticas"][clave]))
            else:
                print("La mayor cantidad de {0} es para: {1} con: {2}".format(noramlizar_clave_estadistica_jugador(clave), jugador["nombre"], jugador["estadisticas"][clave]))
        retorno = True  
    else:
        print("\nError... La lista esta vacia")  
        
    return retorno    

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------------------------ #

nombre_archivo_json = "C:\Python\Dram_Team_Parcial1\dt.json"
lista_jugadores = leer_archivo_json(nombre_archivo_json, "jugadores")
dream_team_app(lista_jugadores)
