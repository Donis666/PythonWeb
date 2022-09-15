from ast import Delete
from crypt import methods
from email.policy import default
from flask import Flask, request
from flask_cors import CORS
from flask.views import MethodView
from models import Book

from extension import db,cors

app = Flask(__name__)
cors.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    Book.init_db()


@app.route('/')
def hello_world():
    return 'Hellp World'


class BookApi(MethodView):

    def get(self,book_id):
        if not book_id:
            books = Book.query.all()
            results = [
                {
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_prize': book.book_prize,
                    'book_number': book.book_number,
                    'book_publisher': book.book_publisher,
                    'author':book.author
                }
                for book in books
            ]

            return {
                'status':'success',
                'message':'data query success!',
                'results':results
            }

        book = Book.query.get(book_id)
        results = {
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_prize': book.book_prize,
                    'book_number': book.book_number,
                    'book_publisher': book.book_publisher,
                    'author':book.author
                }    

        return {
                'status':'success',
                'message':'data query success!',
                'results':results
            }

    def put(self,book_id):
        # to make modification of the data

        book: Book = Book.query.get(book_id)
        book.book_type = request.json.get('book_type')
        book.book_name = request.json.get('book_name')
        book.book_prize = request.json.get('book_prize')
        book.book_number = request.json.get('book_number')
        book.book_publisher = request.json.get('book_publisher')
        book.book_type = request.json.get('book_type')
        book.author = request.json.get('author')

        db.session.commit() #commit the change? 
        return {
            'status':'success',
            'message': 'successfully change the data! '
        }

    def delete(self,book_id):
        book:Book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return  {
            'status':'success',
            'message':"successfully delete the data"
        }
    
    def post(self):
        form = request.json 
        book = Book()
        book.book_number = form.get('book_number')
        book.book_name = form.get('book_name')
        book.book_type = form.get('book_type')
        book.book_prize = form.get('book_prize')
        book.author = form.get('author')
        book.book_publisher = form.get('book_publisher')
        db.session.add(book)
        db.session.commit()

        return {
            'status': 'success',
            'message': 'successfully add the data'
        }





    


    

book_view = BookApi.as_view('book_api')
app.add_url_rule('/books/',defaults = {'book_id':None}, view_func=book_view, methods=["GET", ])
app.add_url_rule('/books/', view_func=book_view, methods=['POST', ])
app.add_url_rule('/books/<int:book_id>',view_func=book_view, methods = ["GET","DELETE","PUT", ])

if __name__ == '__main__':
    app.run(debug=True)