from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"

@app.route('/')
def hello():
    return "Hello!"

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'name': book.book_name, 'author': book.author, 'Publisher': book.publisher}
        output.append(book_data)
    return {"books": output}
@app.route('/books/<id>')
def get_book(id):
    book= Book.query.get_or_404(id)
    return {"name":Book.book_name, "Author":Book.author, "Publisher": Book.publisher}

@app.route('/books', methods=['POST'])
def add_book(id):
    book=Book(name= request.json['name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id':Book.id}

@app.route('/books', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Not found"}
    db.session.add(book)
    db.session.commit()
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)