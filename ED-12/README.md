# PREGUNTA COMPLEJA 

la pregunta compleja que se le ha hecho a Claude sin Claude.md fue la siguiente: 
"¿Dónde debería validar que el salario de un empleado no sea negativo, y cómo estructurarías esa función?"

A lo que Claude respondio lo siguiente: 

Según las reglas del proyecto, la validación va en funciones.py (nunca en interfaz.py, y nunca en employee.py).

Yo lo estructuraría como una función separada que valida y lanza excepción, no que imprima nada:

def validar_salario(salario):
    if salario < 0:
        raise ValueError("El salario no puede ser negativo")

Y la llamaría desde los puntos donde se crea o edita un empleado, que ya existen en tu funciones.py:

def agregar_empleado(datos):
    validar_salario(datos["salario"])
    global siguiente_id
    nuevo_empleado = Empleado(id=siguiente_id, **datos)
    ...

def editar_empleado_por_id(empleado, campo, valor):
    if campo == "salario":
        validar_salario(valor)
        empleado.salario = valor
    ...

interfaz.py es quien captura el ValueError con try/except y hace el print() del mensaje de error al usuario — así la validación queda testeable de forma aislada con pytest (validar_salario(-100) → debe lanzar ValueError) sin depender de input().

Nota aparte: vi que funciones.py ya importa interfaz y llama interfaz._pedir_entero(...) y print(...) dentro de buscar_empleado_por_id() — esto rompe la regla de "nunca input()/print() de menú en funciones.py" y puede darte problemas al testear con pytest (importar funciones importaría interfaz, que a su vez espera interacción). ¿Quieres que lo revise/corrija también?

# SE REDACTA EL CLAUDE.md completo y despues se le hace la misma pregunta a claude

y esta fue su respuesta: 

En este proyecto la validación va en funciones.py (según las reglas de CLAUDE.md: las validaciones no se repiten en interfaz.py, y funciones.py no puede usar print()/input() de menú — solo retorna o lanza excepciones).

Estructura recomendada:

# funciones.py
def validar_salario(salario):
    if salario < 0:
        raise ValueError("El salario no puede ser negativo")

Y se invoca en los dos puntos donde el salario cambia:

def agregar_empleado(datos):
    validar_salario(datos["salario"])
    ...

def editar_empleado_por_id(empleado, campo, valor):
    if campo == "salario":
        validar_salario(valor)
        empleado.salario = valor
    ...

interfaz.py solo captura la excepción y la muestra:

try:
    funciones.agregar_empleado(datos)
except ValueError as e:
    print(f"Error: {e}")

Así queda testeable de forma aislada (validar_salario(-100) debe lanzar ValueError, sin tocar input()).

Aparte, de paso vi que buscar_empleado_por_id en funciones.py:51-60 sí usa input()/print() a través de interfaz._pedir_entero y print() — eso rompe la regla de CLAUDE.md y hace que ese archivo no sea testeable de forma aislada. ¿Quieres que lo corrija también?

# Analisis de las dos respuestas:

Sin CLAUDE.md hay una respuesta mas generica, no es mala pero puede no tomar en cuenta lo que es la arquitectura en si del proyecto
y hay que ponerlo un poco mas en contexto.

Pero ahora con CLAUDE.md, lo toma en cuenta para brindar una respuesta y en base a lo que contiene CLAUDE.md da una respuesta y posibles
soluciones.