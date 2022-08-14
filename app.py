import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tododb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    task_description = db.Column(db.String(300))
    email_address = db.Column(db.String(300))
    priority_level=db.Column(db.Integer)
    deadline = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route('/base', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome'))

    todo_list = Todo.query.all()
    #Convert to CSV

    import csv
    import sqlite3

    conn = sqlite3.connect('tododb.sqlite')
    cursor = conn.cursor()
    cursor.execute("select * from todo;")
    with open("out.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    conn.close()
    with open('out.csv', 'r') as f_in, open('out.txt', 'w') as f_out:
        # 2. Read the CSV file and store in variable
        content = f_in.read()
        # 3. Write the content into the TXT file
        f_out.write(content)

    os.remove('out.csv')
    return render_template("home.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    task_description = request.form.get("task_description")
    email_address = request.form.get("email_address")
    priority_level= request.form.get("priority_level")
    deadline= request.form.get("deadline")

    new_todo = Todo(title=title,task_description=task_description, email_address=email_address, priority_level=priority_level,
                    deadline=deadline, complete=False)

    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
