import os
import sqlite3
from flask import Flask, request, jsonify, Response, redirect, url_for, render_template
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__,template_folder='template', static_folder='static')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app.config['MONGO_URI'] = 'mongodb://localhost/cenabast'
mongo_connection = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET'])
def posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/mensaje', methods=['POST'])
def setMensaje():
    ##recibo el json completo desde postman
    request_data = request.get_json(True)
    ##obtengo el parametro message y se los asigno a mensaje
    #message = request_data['message']
    #titulo = request_data['titulo']
    #subtitulo = request_data['subtitulo']
    #bajada  = request_data['bajada']
    ##inserto el mensaje a la collecion example 
    id = mongo_connection.db.example.insert(request_data)

    response = {
        'id' : str(id),
        'message' : "El mensaje es {}.".format(request_data),
        'code' : 201
    }
    return response

@app.route('/mensajes', methods=['GET'])
def getMensajes():
    ##busco todos los mensajes a la collecion example 
    mensajes = mongo_connection.db.example.find()
    response = json_util.dumps(mensajes)
    return Response(response, mimetype='application/json')

@app.route('/mensaje/<id>', methods=['GET'])
def getMensaje(id):

    ##busco el mensaje en la collecion por Id 
    mensaje = mongo_connection.db.example.find_one({
        '_id' : ObjectId(id),
    })

    response = json_util.dumps(mensaje)
    return Response(response, mimetype='application/json')

@app.route('/mensaje/<id>', methods=['DELETE'])
def deleteMensaje(id):

    ##Elimino el mensaje en la collecion con id 
    mongo_connection.db.example.delete_one({
        '_id' : ObjectId(id),
    })
    response = jsonify({
        'id' : str(id),
        'message' : 'El mensaje'+ str(id) +'ha sido eliminado' ,
        'code' : 200
    })
    return response

@app.route('/mensaje/<id>', methods=['PUT'])
def putMensaje(id):
    ##recibo el json completo desde postman fuerzo a True para que reciba un json
    request_data = request.get_json(True)
    #print(json_util.dumps(request_data))
    print(request_data)

    message = request_data['message']
    titulo = request_data['titulo']
    subtitulo = request_data['subtitulo']
    bajada  = request_data['bajada']
    ##Actualizo el mensaje de la collecion con id 
    mongo_connection.db.example.update_one({
        '_id' : ObjectId(id)
    },{"$set":{
           'message': message,
           'titulo': titulo,
           'subtitulo': subtitulo,
           'bajada' : bajada
        }
    })

    response = jsonify({
        'id' : str(id),
        'message' : 'El mensaje'+ str(id) +'ha sido actualizado' ,
        'code' : 200
    })
    return response

####################EXAMPLES#########################

@app.route('/SetProductos', methods=['POST'])
def setProducto():
    language = request.args.get('language')

    return '''<h1>The language value is: {}</h1>'''.format(language)

@app.route('/query-example')
def query_example():
    # obtengo los parametros desde request GET
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
        #obtengo los parametros desde el formulario
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

    ##recibo el request json completo desde postman
    #request_data = request.get_json()
    ##inserto el json completo tal cual a mingo
    #id = mongo_connection.db.example.insert(request_data)

    ##recibo el json completo desde postman
    request_data = request.get_json()
    ##obtengo el parametro message y se los asigno a mensaje
    mensaje = request_data['message']
    ##inserto el mensaje a la collecion example 
    id = mongo_connection.db.example.insert({
        'message' : mensaje,
    })

    response = {
        'id' : str(id),
        'message' : "El mensaje es {}.".format(mensaje),
        'code' : 201
    }
    return response

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

@app.route('/ofertas')
def ofertar():
    return '<h1>Hello, World Ofertas!</h1>'

@app.route('/distribuciones')
def distribuciones():
    return '<h1>Hello, World Distrubuciones!</h1>'

@app.route('/rfc')
def rfc():
    return '<h1>Hello, World r!</h1>'    


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message':'Resource not found!'
    }
    return message


if __name__ == '__main__':
    app.run('0.0.0.0',5000, debug=True)