from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/cenabast'

mongo_connection = PyMongo(app)

@app.route('/SetProductos', methods=['POST'])
def setProducto():
    language = request.args.get('language')

    return '''<h1>The language value is: {}</h1>'''.format(language)

@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)

# allow both GET and POST requests
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''

# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    """language = None
    framework = None
    python_version = None
    example = None
    boolean_test = None

    if request_data:
        if 'language' in request_data:
            language = request_data['language']

        if 'framework' in request_data:
            framework = request_data['framework']

        if 'version_info' in request_data:
            if 'python' in request_data['version_info']:
                python_version = request_data['version_info']['python']

        if 'examples' in request_data:
            if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                example = request_data['examples'][0]

        if 'boolean_test' in request_data:
            boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)
    """
    return '<h1>Hello, World! Mensaje : {}</h1>'.format(request_data['message']) 

@app.route('/', methods = ['GET'])
def index():
    return { 'message': '<h1>Hello, World!</h1>' }

@app.route('/productos', methods = ['GET'])
def getProductos():
    return '<h1>Hello, World! Productos</h1>'

@app.route('/productos/<Id>', methods = ['GET'])
def getProducto(Id):
    return '<h1>Hello, World Producto Id:{}!</h1>'.format(Id)



@app.route('/proveedores')
def proveedores():
    return '<h1>Hello, World Proveedores!</h1>'

@app.route('/clientes')
def clientes():
    return '<h1>Hello, World! clientes!</h1>'

@app.route('/ofertar')
def ofertar():
    return '<h1>Hello, World Ofertas!</h1>'

@app.route('/distribuciones')
def distribuciones():
    return '<h1>Hello, World Distrubuciones!</h1>'

@app.route('/rfc')
def rfc():
    return '<h1>Hello, World r!</h1>'    

if __name__ == '__main__':
    app.run('0.0.0.0',5000, debug=True)