from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
from flask_mysqldb import MySQL
from . import app.


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'library'

mysql = MySQL(app)

app = Flask(__name__)
api = Api(app, version='1.0', title='Library API', description='A sample API for managing a library')

# Define the book model
book_model = api.model('Book', {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String
})

# Sample data for books in the library
books = [
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell"
    }
]

# Endpoint to get all books in the library
@api.route('/books')
class Books(Resource):
    
    @api.doc('list_books')
    @api.marshal_list_with(book_model)
    def get(self):
        '''List all books'''
        return books

    @api.doc('create_book')
    @api.expect(book_model)
    @api.marshal_with(book_model, code=201)
    def post(self):
        '''Create a new book'''
        book = api.payload
        book['id'] = len(books) + 1
        books.append(book)
        return book, 201

# Endpoint to get, update, or delete a specific book by ID
@api.route('/books/<int:id>')
@api.response(404, 'Book not found')
@api.param('id', 'The book identifier')
class Book(Resource):
    
    @api.doc('get_book')
    @api.marshal_with(book_model)
    def get(self, id):
        '''Get a book by ID'''
        book = [book for book in books if book['id'] == id]
        if len(book) == 0:
            api.abort(404, 'Book not found')
        return book[0]

    @api.doc('update_book')
    @api.expect(book_model)
    @api.marshal_with(book_model)
    def put(self, id):
        '''Update a book by ID'''
        book = [book for book in books if book['id'] == id]
        if len(book) == 0:
            api.abort(404, 'Book not found')
        book[0].update(api.payload)
        return book[0]

    @api.doc('delete_book')
    @api.response(204, 'Book deleted')
    def delete(self, id):
        '''Delete a book by ID'''
        book = [book for book in books if book['id'] == id]
        if len(book) == 0:
            api.abort(404, 'Book not found')
        books.remove(book[0])
        return '', 204

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app_name': 'Library API'}
)

# Register the Swagger UI blueprint with the Flask app
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)

# Sample data for books in the library
books = [
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell"
    }
]

# Route to get all books in the library
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

# Route to get a specific book by ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = [book for book in books if book['id'] == id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})

# Route to add a new book to the library
@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'author': request.json.get('author', '')
    }
    books.append(book)
    return jsonify({'book': book}), 201

# Route to update an existing book in the library
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = [book for book in books if book['id'] == id]
    if len(book) == 0:
        abort(404)
    if not request.json:
        abort(400)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['author'] = request.json.get('author', book[0]['author'])
    return jsonify({'book': book[0]})

# Route to delete a book from the library
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = [book for book in books if book['id'] == id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'result': True})

@app.route('/lib')
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM libraries')
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)