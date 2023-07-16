from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_session import Session
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aLoasc@42%1jnklacs'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_student(student_email):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alunos WHERE email = ?',
                        (student_email,)).fetchone()
    conn.close()
    return post

def get_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM avaliacoes WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    return post


@app.route('/', methods=('GET', 'POST'))
def loginStudent():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if not email:
            flash('Digite seu email')
        elif not senha:
            flash('Digite sua senha')
        else:
            aluno = get_student(email)
            if aluno == None:
                flash('Usuario ou senha invalido')
            elif aluno['senha'] != senha:
                flash('Usuario ou senha invalido')
            else:
                #usar session
                session['matricula'] = aluno['matricula']
                session['email'] = aluno['email']
                session['admin'] = aluno['is_admin']
                return redirect(url_for('home'))

    return render_template('loginStu.html')

@app.route('/reg', methods=('GET', 'POST'))
def registerStudent():
    if request.method == 'POST':

        email = request.form['email']
        senha = request.form['senha']
        curso = request.form['curso']
        matricula = request.form['matricula']
        conn = get_db_connection()
        conn.execute('INSERT INTO alunos (email, senha, curso, matricula) VALUES (?, ?, ?, ?)',
        (email, senha, curso, matricula))
        conn.commit()
        conn.close()

        session['matricula'] = matricula
        session['email'] = email
        session['admin'] = 0

        return redirect(url_for('home'))

    return render_template('regStu.html')

@app.route('/home', methods=('GET', 'POST'))
def home():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM avaliacoes').fetchall()
    conn.close()
    return render_template('home.html', posts=posts, admin=session['admin'])


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':

        content = request.form['avaliacao']

        conn = get_db_connection()
        conn.execute('UPDATE avaliacoes SET comentario = ?'
                        ' WHERE id = ?',
                        (content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template('editAva.html', post=post)

@app.route('/createAva', methods=('GET', 'POST'))
def createAva():
    
    if request.method == 'POST':

        turma = request.form['turma']
        content = request.form['avaliacao']

        conn = get_db_connection()
        conn.execute('INSERT INTO avaliacoes (turma_id, comentario, aluno_id) VALUES (?, ?, ?)',
                        (turma, content,session['matricula']))
        conn.commit()
        conn.close()
        

    return render_template('createAva.html')

@app.route('/<int:id>/delete', methods=('POST','GET'))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM avaliacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/<int:id>/deleteRep', methods=('POST','GET'))
def deleteRep(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM avaliacoes WHERE id = (SELECT avaliacao_id FROM denuncia WHERE id= ?)', (id,))
    conn.execute('DELETE FROM denuncia WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))



@app.route('/denuncias', methods=('GET', 'POST'))
def report():
    aluno = get_student(session['email'])
    if(aluno == None):
        redirect(url_for('home'))

    if(aluno['is_admin'] == 0):
        return redirect(url_for('home'))

    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM denuncia').fetchall()
    conn.close()
    return render_template('denuncias.html', posts=posts)

@app.route('/<int:id>/denuncia', methods=('POST','GET'))
def denuncia(id):


    if request.method == 'POST':

        coment = request.form['denuncia']

        conn = get_db_connection()
        conn.execute('INSERT INTO denuncia (report, avaliacao_id) VALUES (?, ?)',
                        (coment, id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template('denunciar.html')

@app.route('/alunos', methods=('GET', 'POST'))
def alunos():
    atual = get_student(session['email'])
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM alunos').fetchall()
    conn.close()
    return render_template('alunos.html', posts=posts,is_admin=atual['is_admin'])

@app.route('/<int:id>/deleteAlu', methods=('POST','GET'))
def deleteAlu(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM alunos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('alunos'))


@app.route('/createTur', methods=('GET', 'POST'))
def createTur():
    
    if request.method == 'POST':

        numero = request.form['numero']
        professor = request.form['professor']
        materia = request.form['materia']

        conn = get_db_connection()
        conn.execute('INSERT INTO turma (numero, materia_id, professor_id) VALUES (?, ?, ?)',
                        (numero, professor,materia))
        conn.commit()
        conn.close()
        
    return render_template('createTur.html')

@app.route('/turmas', methods=('GET', 'POST'))
def turmas():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM vw_turma').fetchall()
    conn.close()
    return render_template('turmas.html', posts=posts)

@app.route('/<int:id>/editTur', methods=('GET', 'POST'))
def editTur(id):
    post = get_post(id)
    if request.method == 'POST':

        numero = request.form['numero']
        professor = request.form['numero']

        conn = get_db_connection()
        conn.execute('UPDATE turma SET numero = ?, professor_id = ?'
                        ' WHERE id = ?',
                        (numero,professor, id))
        conn.commit()
        conn.close()
        return redirect(url_for('turmas'))
    return render_template('editTur.html')

@app.route('/<int:id>/deleteTur', methods=('POST','GET'))
def deleteTur(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM turma WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('turmas'))

@app.route('/createProf', methods=('GET', 'POST'))
def createProf():
    
    if request.method == 'POST':

        nome = request.form['nome']
        depart = request.form['departamento']

        conn = get_db_connection()
        conn.execute('INSERT INTO professores (nome, departamento_id) VALUES (?, ?)',
                        (nome, depart))
        conn.commit()
        conn.close()
        

    return render_template('createProf.html')

@app.route('/professores', methods=('GET', 'POST'))
def professores():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM professores').fetchall()
    conn.close()
    return render_template('professores.html', posts=posts)

@app.route('/<int:id>/editProf', methods=('GET', 'POST'))
def editProf(id):
    post = get_post(id)
    if request.method == 'POST':
        nome = request.form['nome']
        depart = request.form['departamento']
        conn = get_db_connection()
        conn.execute('UPDATE professores SET nome = ?, departamento_id = ?'
                        ' WHERE id = ?',
                        (nome, depart, id))
        conn.commit()
        conn.close()
        return redirect(url_for('professores'))
    return render_template('editProf.html')

@app.route('/<int:id>/deleteProf', methods=('POST','GET'))
def deleteProf(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM professores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('professores'))