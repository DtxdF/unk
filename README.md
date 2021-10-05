# unk
Simplemente una API modular usando tornado

# Agregar un nuevo recurso
Es demasiado fácil agregar un nuevo recurso para que nuestros clientes lo consuman. Simplemente es necesario seguir los siguientes pasos:

* Primero, es necesario crear la estructura del recurso, y sus métodos. En aras a la simplicación, crearemos un '*Hello world*' típico:

**applications/hello.py**
```python
from applications import mainHandler

class helloHandler(mainHandler.JsonHandler):
	async def get(self):
		self.write("Hello, world!")
```

* Segundo, se deberá importar en [__init__.py](applications/__init__.py):

```bash
echo "from . import hello" >> applications/__init__.py
```

* Tercero, ahora se creará la URL en [app.py](app.py):

```
...
		(rf"/v{version}/hello", applications.hello.helloHandler)
...
```

***Nota***: No es necesario, pero sí recomendable colocar la versión, y si es de agrado personal, se puede craer un alias que apunte a la versión más reciente de ese recurso.

* Cuato y último. Ya listo lo anterior, simplemente se levanta el servidor.

# Consumiendo el recurso

En el lado del servidor se ejecuta [main.py](main.py) y listo, aunque lo más probable es que se quiera exponer la API a todo el mundo, así que se deberá ejecutar del siguiente modo:

```bash
python main.py --lhost=0.0.0.0
```

Claro está que directamente se puede realizar lo anterior desde [files/settings.ini](files/settings.ini).


Ahora desde el lado del cliente es posible ver la respuesta:

```bash
curl http://localhost:8080/v1.0/hello
Hello, world!
```

# Personalizando el mensaje

Resulta que deseamos personalizar el mensaje para que no sea tan estática la interacción. Pues es posible gracias a la configuración:

**files/settings.ini**
```
[hello_service]
message=¡Hola, mundo!
```

**applications/hello.py**
```python
import config
from applications import mainHandler

__name__ = "hello_service"
settings = config.settings[__name__]

class helloHandler(mainHandler.JsonHandler):
	async def get(self):
		self.write(settings["message"])
```

Lo que verá el cliente será:

```bash
curl http://localhost:8080/v1.0/hello
¡Hola, mundo!
```

# Interactuando con el usuario

La configuración solo fue una forma demostrativa, en la vida real queremos recibir y dependiendo de ésto, enviar una respuesta. Es tan simple como lo siguiente:

```python
from applications import mainHandler

class helloHandler(mainHandler.JsonHandler):
	async def get(self):
		message = self.get_query_argument("message")

		self.write(message)
```

Entonces, el cliente ahora, si desea, puede enviar un mensaje personalizado usando el método GET:

```bash
curl 'http://localhost:8080/v1.0/hello?message=Hello!'
Hello!
```

# Todo es JSON

Siguiente el ejemplo anterior, si el cliente olvida especificar el parámetro `message`, entonces recibirá una linda respuesta:

```json
{
  "status_code": 400,
  "message": "`message` is required"
}
```

También pasará algo similar si se envía en un formato no correcto, o en otras palabras, si no es JSON:

# Un ejemplo más avanzado

¿Qué tal una pequeña calculadora?

```python
import tornado.web
from applications import mainHandler

operations = {
	"sum" : lambda x, y: x + y,
	"sub" : lambda x, y: x - y,
	"mul" : lambda x, y: x * y,
	"div" : lambda x, y: x / y
}

class calcHandler(mainHandler.JsonHandler):
	async def post(self):
		operation_type = self.get_json_argument(
			"operation"
		)

		valid_func = None
		if (operation_type == "div"):
			valid_func = lambda v: v > 0

		operation = operations.get(operation_type)
		if operation is None:
			raise tornado.web.HTTPError(400, "La operación no existe")

		x = self.get_json_argument(
			"x",
			value_type=int
		)

		y = self.get_json_argument(
			"y",
			value_type=int,
			valid_func=valid_func
		)

		self.write_template({
			"result" : operation(x, y)
		})
```

* Sumar:

```bash
curl http://localhost:8080/v1.0/calc -X POST -d '{"x" : 2, "y" : 2, "operation" : "sum"}'
{"status_code": 200, "result": 4}
```

* Restar:

```bash
curl http://localhost:8080/v1.0/calc -X POST -d '{"x" : 2, "y" : 2, "operation" : "sub"}'
{"status_code": 200, "result": 0}
```

* Multiplicar:

```bash
curl http://localhost:8080/v1.0/calc -X POST -d '{"x" : 2, "y" : 2, "operation" : "mul"}'
{"status_code": 200, "result": 4}
```

* Dividir:

```bash
curl http://localhost:8080/v1.0/calc -X POST -d '{"x" : 2, "y" : 2, "operation" : "div"}'
{"status_code": 200, "result": 1.0}
```

# TODO

- [ ] Documentarlo mejor
- [x] Personalizar los encabezados globales
- [ ] Separar cada archivo de configuración por cada recurso

\~ DtxdF
