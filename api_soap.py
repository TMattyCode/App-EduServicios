'''from flask import Flask, request, Response
from flask_cors import CORS
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Define el servicio SOAP
class CursoService(ServiceBase):
    cursos = {
        "L": "lenguaje",
        "M": "matematicas"
    }

    @rpc(Unicode, _returns=Unicode)
    def getCursoPorCodigo(ctx, codigo):
        print("Código recibido:", codigo)
        return CursoService.cursos.get(codigo, "Curso no encontrado")

# App SOAP
soap_app = Application(
    [CursoService],
    tns='edu.servicios.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# App Flask + CORS para envolver SOAP
flask_app = Flask(__name__)
CORS(flask_app, resources={r"/soap*": {"origins": "*"}})

@flask_app.route('/')
def inicio():
    return "Servidor SOAP activo en /soap"

# Permitir OPTIONS para preflight
@flask_app.route('/soap', methods=['OPTIONS'])
def options_soap():
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

# Conectar Flask con Spyne
flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
    '/soap': WsgiApplication(soap_app)
})

if __name__ == '__main__':
    print("API SOAP corriendo en http://localhost:8000/soap")
    run_simple('0.0.0.0', 8000, flask_app)'''

# Separacion

'''from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/soap", methods=["POST"])
def soap():
    xml = request.data.decode("utf-8")
    print("XML recibido:", xml)

    # Extraer código simple (para tareas o demos)
    start = xml.find("<codigo>") + len("<codigo>")
    end = xml.find("</codigo>")
    codigo = xml[start:end]

    respuesta = "matematicas" if codigo == "M" else "Curso no encontrado"

    soap_response = f"""<?xml version="1.0"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <getCursoPorCodigoResponse>
          <getCursoPorCodigoResult>{respuesta}</getCursoPorCodigoResult>
        </getCursoPorCodigoResponse>
      </soap:Body>
    </soap:Envelope>"""

    return Response(soap_response, content_type="text/xml")

app.run(port=8000)'''

from flask import Flask, request, Response

app = Flask(__name__)

# Habilita CORS globalmente (opcional pero útil para Live Server)
@app.after_request
def aplicar_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, SOAPAction"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

# Diccionario de cursos
cursos = {
    "CS101": "lenguaje",
    "CS102": "matematicas"
}

# Ruta para manejar SOAP
@app.route("/soap", methods=["POST", "OPTIONS"])
def soap_endpoint():
    if request.method == "OPTIONS":
        return Response(status=200)

    xml = request.data.decode("utf-8")
    print("XML recibido:\n", xml)

    # Extraer <codigo> del XML recibido
    if "<codigo>" in xml:
        start = xml.find("<codigo>") + len("<codigo>")
        end = xml.find("</codigo>")
        codigo = xml[start:end].strip()
    else:
        codigo = ""

    # Buscar el curso
    resultado = cursos.get(codigo, "Curso no encontrado")

    # Crear respuesta en formato SOAP
    soap_response = f"""<?xml version="1.0"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <getCursoPorCodigoResponse>
                <getCursoPorCodigoResult>{resultado}</getCursoPorCodigoResult>
            </getCursoPorCodigoResponse>
        </soap:Body>
    </soap:Envelope>"""

    return Response(soap_response, content_type="text/xml")

if __name__ == "__main__":
    print("API SOAP corriendo en http://localhost:8000/soap")
    app.run(debug=True,port=8000)