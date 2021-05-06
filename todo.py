from flask import Flask,render_template,redirect,url_for,request 
from flask_sqlalchemy import SQLAlchemy # SQLALCHEMY DAHİL ETTİK.

# Alltaki 3 satırı herzaman eklememiz gerek.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/berka/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    # Databaseden Veri Alma
    todos = Todo.query.all() # Bu bize bir liste dönecek
    return render_template("index.html",todos = todos)
# Todoları Tamamlama : Yani butona basınca güncelleme
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete

    db.session.commit()
    return redirect(url_for("index"))

# Databseye Veri Ekleme
@app.route("/add",methods=["POST"])
def addTodo():
    title = request.form.get("title") # Burada title değerini formdan alıyoruz.
    newTodo = Todo(title =title,complete = False ) # Classtan obje oluşturduk .yeni bir todo eklediğimiz için ve bu tamamlanmamış bir todo olduğu için false ile başlattık.
    db.session.add(newTodo) # Bu şekilde veri tabanına ekledik.
    db.session.commit()

    return redirect(url_for("index"))

# Todoları Silme
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))
# Sonra aşağıdaki gibi veri tabanında çalışması için class oluşturacaz.

class Todo(db.Model):
    # Bu şekilde veriler oluşturulur.
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(80)) # Bu şekilde title verisini yazdık. db.veritürü(max)
    complete = db.Column(db.Boolean) 

if __name__ == "__main__":
    db.create_all() # Bu şekilde veri tablolarını oluşturcak.
    app.run(debug=True)