import json
from employee import Empleado #llama a employee.py que es donde esta la clase Empleado 
import interfaz

lista_empleados = [] #lista en donde se guardaran los empleados 
siguiente_id = 1 #contador inicializado en 1


def obtener_empleado_por_id(id_buscado): #funcion que busca al empleado por medio de su ID
    print(len(lista_empleados))
    for empleado in lista_empleados:
        if empleado.id == id_buscado:
            return empleado
    return None

# 1. Agregar empleado
def agregar_empleado(datos):
    global siguiente_id
    nuevo_empleado = Empleado(id=siguiente_id, **datos)
    lista_empleados.append(nuevo_empleado)
    guardar_empleado()
    siguiente_id += 1
    return nuevo_empleado

#funcion para generar y guardar los empleados en un archivo json 
def guardar_empleado():
    datos = [vars(e) for e in lista_empleados]
    with open("empleados.json", "w") as archivo:
        json.dump(datos, archivo, indent=2)


#funcion para cargar los empleados del archivo json
def cargar_empleado():
    global siguiente_id
    try:
        with open("empleados.json", "r") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return

    for dato in datos:
        empleado = Empleado(**dato)
        lista_empleados.append(empleado)

    if lista_empleados:
        siguiente_id = max(e.id for e in lista_empleados) + 1



# 2. Buscar empleado por ID
def buscar_empleado_por_id():
    id_buscado = interfaz._pedir_entero("\nIngresa el ID del empleado a buscar: ")
    empleado = obtener_empleado_por_id(id_buscado)

    if empleado is None:
        print(f"\nNo se encontro ningun empleado con ID {id_buscado}.\n")
        return

    print("\n-- Empleado encontrado --")
    print(empleado)


# 3. Editar empleado por ID
def editar_empleado_por_id(empleado, campo, valor):
    if campo == "nombre":
        empleado.nomnbre = valor
    elif campo == "edad":
        empleado.edad = valor
    elif campo == "salario":
        empleado.salario = valor
    elif campo == "rol":
        empleado.rol = valor
    elif campo == "email":
        empleado.email = valor
    elif campo == "horas_por_dia":
        empleado.horas_por_dia = valor
    elif campo == "vacaciones_anuales":
        empleado.vacaciones_anuales = valor
    elif campo == "bonos":
        empleado.bonos = valor
    elif campo == "recibe_comision":
        empleado.recibe_comision = valor
    elif campo == "comision":
        empleado.recibe_comision, empleado.porcentaje_comision = valor


# 4. Eliminar empleado por ID
def eliminar_empleado_por_id(empleado):
    lista_empleados.remove(empleado)
    guardar_empleado()


# 5. Mostrar empleados por departamento 
def mostrar_empleados_por_departamento(rol_buscado):
    rol_buscado = rol_buscado.lower()
    return [e for e in lista_empleados if e.rol.lower() == rol_buscado]


# 7. Calculos de salario, bonos y comisiones
PORCENTAJE_DESCUENTO = 0.10  # 10% de descuentos (ej. ISSS, AFP, etc.)


def calcular_descuentos(empleado):
    return empleado.salario * PORCENTAJE_DESCUENTO


def calcular_salario_neto(empleado):
    descuentos = calcular_descuentos(empleado)
    return (empleado.salario - descuentos) + empleado.bonos + calcular_comision(empleado)


def calcular_comision(empleado):
    if not empleado.recibe_comision:
        return 0.0
    return empleado.salario * (empleado.porcentaje_comision / 100)