from flask import Flask, request, Response
from spyne import Application, rpc, ServiceBase, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Definimos el servicio SOAP
class CalculadoraServicio(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def sumar(ctx, x, y):
        return x + y

    @rpc(Integer, Integer, _returns=Integer)
    def restar(ctx, x, y):
        return x - y

# Configuramos la aplicación SOAP
soap_app = Application(
    [CalculadoraServicio],
    'soap.ejemplo.calculadora',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Creamos la aplicación Flask
app = Flask(__name__)

# Asociamos el servicio SOAP a Flask
soap_service = WsgiApplication(soap_app)

@app.route('/')
def inicio():
    return (
        "Servicio SOAP funcionando. "
        "Accede a /soap para usar el servicio o a /soap/wsdl para obtener el WSDL."
    )

@app.route('/soap', methods=['POST'])
def soap():
    # Procesa solicitudes SOAP (POST)
    return Response(
        soap_service(request.environ, start_response=lambda *args: None),
        content_type='text/xml; charset=utf-8'
    )

@app.route('/soap/wsdl', methods=['GET'])
def wsdl():
    # Genera un WSDL dinámico o estático
    wsdl_url = "http://127.0.0.1:5000/soap"
    wsdl_template = f"""<?xml version="1.0"?>
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/"
             xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
             xmlns:tns="soap.ejemplo.calculadora"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema"
             name="CalculadoraServicio"
             targetNamespace="soap.ejemplo.calculadora">
  <types>
    <schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="soap.ejemplo.calculadora">
      <element name="sumar">
        <complexType>
          <sequence>
            <element name="x" type="xsd:int"/>
            <element name="y" type="xsd:int"/>
          </sequence>
        </complexType>
      </element>
      <element name="sumarResponse">
        <complexType>
          <sequence>
            <element name="resultado" type="xsd:int"/>
          </sequence>
        </complexType>
      </element>
      <element name="restar">
        <complexType>
          <sequence>
            <element name="x" type="xsd:int"/>
            <element name="y" type="xsd:int"/>
          </sequence>
        </complexType>
      </element>
      <element name="restarResponse">
        <complexType>
          <sequence>
            <element name="resultado" type="xsd:int"/>
          </sequence>
        </complexType>
      </element>
    </schema>
  </types>
  <message name="sumarRequest">
    <part name="parameters" element="tns:sumar"/>
  </message>
  <message name="sumarResponse">
    <part name="parameters" element="tns:sumarResponse"/>
  </message>
  <message name="restarRequest">
    <part name="parameters" element="tns:restar"/>
  </message>
  <message name="restarResponse">
    <part name="parameters" element="tns:restarResponse"/>
  </message>
  <portType name="CalculadoraServicioPortType">
    <operation name="sumar">
      <input message="tns:sumarRequest"/>
      <output message="tns:sumarResponse"/>
    </operation>
    <operation name="restar">
      <input message="tns:restarRequest"/>
      <output message="tns:restarResponse"/>
    </operation>
  </portType>
  <binding name="CalculadoraServicioBinding" type="tns:CalculadoraServicioPortType">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="sumar">
      <soap:operation soapAction="sumar"/>
      <input>
        <soap:body use="literal"/>
      </input>
      <output>
        <soap:body use="literal"/>
      </output>
    </operation>
    <operation name="restar">
      <soap:operation soapAction="restar"/>
      <input>
        <soap:body use="literal"/>
      </input>
      <output>
        <soap:body use="literal"/>
      </output>
    </operation>
  </binding>
  <service name="CalculadoraServicio">
    <port name="CalculadoraServicioPort" binding="tns:CalculadoraServicioBinding">
      <soap:address location="{wsdl_url}"/>
    </port>
  </service>
</definitions>"""
    return Response(wsdl_template, content_type='text/xml; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True)
