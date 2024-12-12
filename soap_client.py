from zeep import Client

# URL to the WSDL (adjust the localhost and port if needed)
wsdl = 'http://localhost:5000/?wsdl'

# Create the SOAP client
client = Client(wsdl=wsdl)

# Test the add operation
result = client.service.add(5, 3)
print(f"Addition Result: 5 + 3 = {result}")

# Test the subtract operation
result = client.service.subtract(10, 4)
print(f"Subtraction Result: 10 - 4 = {result}")
