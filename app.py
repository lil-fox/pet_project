from datetime import datetime

from flask import Flask
from flask import request
from peewee import *

app = Flask(__name__)
pg_db = PostgresqlDatabase('postgres', user='postgres', password='7913024',
                           host='127.0.0.1', port=5432)


class Note(Model):
    id = PrimaryKeyField()
    text = TextField()
    date = DateField()

    class Meta:
        database = pg_db # This model uses the "people.db" database.


@app.route("/")
def root():
    return "<p>Hello, World!</p>"


@app.route("/get")
def get():
    id_ = request.args.get('id')
    if id_ == 'all':
        notes = [note for note in Note.select()]

        notes_data = ''

        for note in notes:
            notes_data += note.text + f'(ID {note.id})</br>'

        return f"<p>{notes_data}</p>"
    else:
        note = Note.select().where(Note.id == int(id_)).dicts()

        return f"<p>{note[0]['text']} (ID {note[0]['id']})</p>"


@app.route("/delete")
def delete():
    id_ = request.args.get('id')
    if id_ is not None:
        note = Note.delete_by_id(int(id_))
        return f"<p>DELETE {note}</p>"


@app.route("/create")
def create():
    text = request.args.get('text')
    note = Note(text=text, date=datetime(2024, 1, 1))
    note.save()
    if text is not None:
        return f"<p>CREATED {note.text} {note.id} </p>"