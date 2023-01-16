import os.path
import sys
import sqlite3

from flask import  ( Flask, g , redirect, render_template, request, session, url_for, Response )
    

from lib.tablemodel import DatabaseModel
from lib.questionmodel import QuestionModel
from lib.demodatabase import create_demo_database


# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True


class User:
    def __init__(self, id, username, password):

        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Kenan', password='KenanWW'))
users.append(User(id=2, username='Ruben', password='RubenWW'))
users.append(User(id=3, username='Maarten', password='MaartenWW'))
users.append(User(id=4, username='Aisha', password='AishaWW'))

app = Flask(__name__)
app.secret_key = 'geheimekey'

@app.before_request
def before_request():
    g.user = None


    if 'user_id' in session:
            user = [x for x in users if x.id == session['user_id']][0]
            g.user = user

## Logout route
@app.route('/uitloggen')
def logout():
    ## Remove login sessions to log user out
    session.clear()
    ## Redirect user to login page
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session.pop('user_id', None)
        
        username = request.form['username']
        password = request.form['password']
        
        user_found_list = [x for x in users if x.username == username]
        if len(user_found_list) > 0:
            user = user_found_list[0]
            if user and user.password == password:
                session['user_id'] = user.id
            return redirect(url_for('index'))
    
        return render_template ('login.html', message='Invalid username or password')
    else:
        return render_template('login.html')



@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')




# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)
qm = QuestionModel(DATABASE_FILE)

# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.
@app.route("/")
def index():
    if not g.user:
        return redirect(url_for('login'))
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )
    


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not g.user:
        return redirect(url_for('login'))
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )

# Show special characters on page
@app.route("/special_characters")
def special_characters():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.getAllSpecialCharacters()
    return render_template(
        "special_characters.html", rows=rows, columns=column_names
    )

# Show special characters on edit page
@app.route("/special_characters/edit/<id>", methods=['GET', 'POST'])
def special_characters_edit(id=None):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        id = request.form['id']
        question = request.form['question']
        qm.editSpecialCharacters(id, question)
        return redirect(url_for('special_characters'))

    id, question = qm.getSpecificQuestion(id)
    return render_template(
        "special_characters_edit.html", id=id, question=question
    )

# Show null values on page
@app.route("/null_values")
def null_values():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.getAllNullValues()
    kwargs = {
        "rows": rows,
        "columns": column_names
    }
    return render_template("null_values.html", **kwargs)


# Show null values on edit page
@app.route("/null_values/edit/<id>", methods=['GET', 'POST'])
def null_values_edit(id=None):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        id = request.form['id']
        learningGoal = int(request.form['learningGoal'])
        question = request.form['question']
        author = int(request.form['author'])
        qm.editNullValues(id, learningGoal, question, author)
        return redirect(url_for('null_values'))

    id, learningGoal, question, author = qm.getSpecificQuestionRow(id)
    kwargs = {
        "id": id,
        "learningGoal": learningGoal,
        "question": question,
        "author": author
    }
    return render_template("null_values_edit.html", **kwargs)

#export null values
@app.route("/null_values/export")
def special_characters_export():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.getAllNullValues()
    csv = ""
    for column in column_names:
        csv += f"{column};"
    csv += "\n"
    for row in rows:
        for field in row:
            csv += f"{field};"
        csv+= "\n"    

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=null_values_export.csv"})


# Show data types on page
@app.route("/data_types")
def data_types():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.getAuthors()
    kwargs = {
        "rows": rows,
        "columns": column_names
    }
    return render_template("data_types.html", **kwargs)

# Show data types on page
@app.route("/data_types/edit/<id>")
def data_types_edit(id=None):
    if not g.user:
        return redirect(url_for('login'))

    return render_template("data_types_edit.html", id=id)

@app.route("/data_types/edit/handle/<id>", methods=['GET', 'POST'])
def data_types_edit_handle(id=None):
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        id = request.form['id']
        collaborator = request.form['collaborator']
        qm.editAuthor(id, collaborator)
        return redirect(url_for('data_types'))

# Show wrong goals on a page
@app.route("/foute_leerdoelen")
def foute_leerdoelen():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.getWrongGoals()
    return render_template(
        "foute_leerdoelen.html", rows=rows, columns=column_names
    )

# Let the user edit goals
@app.route("/foute_leerdoelen/edit/<id>")
def foute_leerdoelen_edit(id=None):
    if not g.user:
        return redirect(url_for('login'))
    listofgoalID = qm.getAllGoalID()
    return render_template("foute_leerdoelen_edit.html", id=id, leerdoelen=listofgoalID)

@app.route("/foute_leerdoelen/edit/handle/<id>", methods=['GET', 'POST'])
def foute_leerdoelen_edit_handle(id=None):
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        id = request.form['id']
        collaborator = request.form['collaborator']
        qm.editWrongGoals(id, collaborator)
        return redirect(url_for('foute_leerdoelen'))

@app.route("/Spec_quest")
def specifiedquestion():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.allid()
    return render_template("vragenfilter.html",rows = rows, column_names = column_names
    )

@app.route("/Spec_quest/1")
def id1tm35():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.specifiedid1()
    return render_template("vragenfilter_specifiek1.html",rows = rows, column_names = column_names
    )

@app.route("/Spec_quest/2")
def id35tm70():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.specifiedid2()
    return render_template("vragenfilter_specifiek1.html",rows = rows, column_names = column_names
    )

@app.route("/Spec_quest/3")
def id70tm95():
    if not g.user:
        return redirect(url_for('login'))
    rows, column_names = qm.specifiedid3()
    return render_template("vragenfilter_specifiek1.html",rows = rows, column_names = column_names
    )

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)