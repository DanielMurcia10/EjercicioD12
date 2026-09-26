# CLAUDE.md — Gestión de Empleados

## Descripción del proyecto
Sistema de gestión de empleados (CRUD: alta, baja, edición, listado).

## Arquitectura de archivos (roles fijos — no mezclar)
- `employee.py` — SOLO la clase `Employee` (o `Empleado`): atributos (__init__, self.nombre, self.puesto, self.salario, etc.) y métodos propios del objeto (ej. `to_dict()`, `__str__`). Sin lógica de menú, sin input().
- `funciones.py` — Lógica de negocio: crear, buscar, actualizar, eliminar empleados; validaciones; guardar/cargar en disco (JSON). Recibe datos ya validados o los valida aquí, pero NUNCA usa input() ni print() de menú — solo retorna valores o lanza excepciones.
- `interfaz.py` — Toda la interacción con el usuario: menús, input(), prints de opciones. Llama a las funciones de `funciones.py`, nunca contiene lógica de negocio propia.
- `main.py` — Punto de entrada. Importa `interfaz.py` y arranca el programa. Nada de lógica aquí más que el arranque.

## Reglas de código
- NUNCA poner `input()` fuera de `interfaz.py` — si aparece en `employee.py` o `funciones.py`, bloquea pytest al importar.
- Toda función en `funciones.py` debe ser testeable de forma aislada (recibe parámetros, retorna resultado; no depende de que el usuario escriba nada).
- Persistencia: [definir aquí — JSON en un archivo `empleados.json`, o el formato que estés usando].
- Validaciones de datos (ej. salario no negativo, campos no vacíos) van en `funciones.py`, no repetidas en `interfaz.py`.

## Tests
- pytest sobre `funciones.py` y `employee.py` (los que no dependen de input()).
- Comando: `pytest`

## Comandos
- Ejecutar el programa: `python main.py`

## Entorno
- Mac (zsh). Si la ruta tiene espacios, usar comillas al hacer `cd`.

## Estilo
- Español en nombres de dominio (empleado, puesto, salario), inglés en términos técnicos genéricos.