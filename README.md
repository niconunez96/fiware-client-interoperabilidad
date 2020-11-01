# Cliente de fiware para la catedra de Interoperabilidad de la facultad UTN FRM


## Descripción

FiwareClient es un programa que se encarga de leer los datos enviados al puerto serie.
Estos datos pueden provenir de un Arduino, una vez procesado los datos estos se envian
al servidor fiware para poder guardarlos y usarlos para realizar consultas, graficas, etc.

## Como correr el proyecto

### Linux

- Crear un virtual environment con `python3 -m venv env`
- Activar el virtual environment `source env/bin/activate`
- Si es la primera vez, instalar las dependencias `pip install -r requirements.txt`
- Correr el programa `python main.py`
- Cuando ya no se utilice el programa correr `deactivate` para desactivar el virtual environment
