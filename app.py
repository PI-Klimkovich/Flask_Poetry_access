import uuid
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks_lesson_18.db'
db = SQLAlchemy(app)

# https://www.youtube.com/playlist?list=PL0lO_mIqDDFXiIQYjLbncE9Lb6sx8elKA
# ===== При запуске python в терминале =====
# БД сохраняется в папке instance.
# В командной строке пишем:
# >>>from app import app, db
# >>>app.app_context().push()
# >>>db.create_all()
# >>>exit()


class Note(db.Model):
    uuid = db.Column(db.String(36), primary_key=True,  default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note %r>' % self.uuid


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/notes')
def posts():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('notes.html', notes=notes)


@app.route('/about_note/<uuid>')
def post_about(uuid):
    note = Note.query.get(uuid)
    return render_template('note_about.html', note=note)


@app.route('/notes/<uuid>')
def post_detail(uuid):
    note = Note.query.get(uuid)
    return render_template('note_detail.html', note=note)


@app.route('/notes/<uuid>/delete')
def post_delete(uuid):
    note = Note.query.get_or_404(uuid)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/notes')
    except:
        return "При удалении записи произошла ошибка"


@app.route('/notes/<uuid>/update', methods=['POST', 'GET'])
def post_update(uuid):
    note = Note.query.get(uuid)
    if request.method == 'POST':
        note.title = request.form['title']
        note.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/notes')
        except:
            return "При редактировании заметки произошла ошибка"
    else:

        return render_template('note_update.html', note=note)


@app.route('/create_note', methods=['POST', 'GET'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        note = Note(title=title, text=text)

        try:
            db.session.add(note)
            db.session.commit()
            print(note.uuid)
            return redirect(url_for('post_about', uuid=note.uuid))
        except:
            return "При добавлении заметки произошла ошибка"
    else:
        return render_template('create_note.html')


@app.route('/note_access', methods=['POST', 'GET'])
def note_access():
    if request.method == 'POST':
        uuid = request.form['uuid']
        print(uuid)
        try:
            note = Note.query.get(uuid)
            print(note.uuid)
            return redirect(url_for('post_detail', uuid=note.uuid))
        except:
            return "Не верный id"
    else:
        return render_template('note_access.html')


if __name__ == "__main__":
    app.run(debug=True)  # 'debug=True' - для отслеживания ошибок при тестировании
