# Respuesta sin CLAUDE.md

Hay un proyecto real aquí. Voy a revisar los archivos para ver dónde encaja mejor la validación.

  Read 4 files

Con esta arquitectura (modelo Empleado + lógica en funciones.py + entrada de datos en interfaz.py), yo pondría la validación en dos capas:

1. Capa de dominio (obligatoria) — dentro de Empleado.__init__

Es la única forma de garantizar que ningún camino cree un empleado con salario negativo: ni el alta manual, ni la edición, ni la carga desde empleados.json (que hoy no pasa por ningún filtro).

class Empleado:
    def __init__(self, nombre, edad, salario, ...):
        self.salario = salario  # usa el setter de abajo
        ...

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise ValueError(f"El salario no puede ser negativo (recibido: {valor})")
        self._salario = valor

Con esto, editar_empleado_por_id (funciones.py:70) y cargar_empleado (funciones.py:33) también quedan protegidos automáticamente, sin tocarlos.

2. Capa de entrada (UX) — en interfaz.py

Para no romper el programa con un ValueError sin manejar cuando el usuario teclea algo, agregaría un _pedir_decimal especializado que reintenta:

def _pedir_salario(mensaje):
    while True:
        valor = _pedir_decimal(mensaje)
        if valor >= 0:
            return valor
        print("El salario no puede ser negativo. Intentalo de nuevo.")

Y usarlo en pedir_datos_nuevo_empleado (interfaz.py:51) y en la opción "3. Salario" de pedir_cambio_empleado (interfaz.py:104).

Por qué las dos: la del modelo es la garantía real (cierra todos los caminos, incluido el JSON); la de la interfaz es solo para que el usuario no tenga que reintentar por una excepción fea. Si solo pusieras la de interfaz.py, un dato corrupto en empleados.json seguiría colándose.


# Respuesta con CLAUDE.md

Según CLAUDE.md, esa validación es un invariante del modelo, así que va en employee.py, no en funciones.py. La regla del proyecto lo dice explícito: "validaciones de invariantes propias del modelo (ej. salario no negativo)" pertenecen a la clase Empleado.

Ahora mismo __init__ en employee.py asigna self.salario = salario sin ningún chequeo. Yo lo estructuraría así:

class Empleado:
    def __init__(self, nombre: str, edad: int, salario: float, ...):
        if salario < 0:
            raise ValueError("El salario no puede ser negativo")
        self.salario = salario
        ...

Puntos clave de por qué así:

1. Lanza excepción, no imprime nada. employee.py no puede tener print()/input(). Quien llame a Empleado(...) (típicamente agregar_empleado en funciones.py) deja que el error se propague o lo captura.
2. funciones.py no duplica la validación. agregar_empleado(datos) simplemente construye el Empleado y deja que el ValueError suba; si querés manejarlo ahí, lo envolvés en try/except ValueError y lo re-lanzas o devolvés un resultado de error — pero la regla de negativo/no-negativo vive una sola vez, en el modelo.
3. interfaz.py solo maneja la UX del error, por ejemplo:
try:
    funciones.agregar_empleado(datos)
except ValueError as e:
    print(f"Error: {e}")
   así el reintento de input y el mensaje quedan en la capa de interfaz, cumpliendo la separación de responsabilidades.

Si querés, extiendo esto para que también valide en una futura función de "editar salario" (reutilizando el mismo chequeo, quizá como método _validar_salario estático de la clase para no repetir el if en dos lugares).


# Documentacion sobre las dos respuestas:

En la respuesta con CLAUDE.md se nota la diferencia y se ve que claude si esta dentro de el proyecto ya que se ubica solo sin necesidad de darle mayor detalle
sino que el solo y respeta todo lo que se ha trabajado en el proyecto, mientras que la version sin CLAUDE.md es una respuesta mas generica 