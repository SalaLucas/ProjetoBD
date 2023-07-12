import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()

cur.execute("INSERT INTO departamentos (nome) VALUES ('CIC'), ('FIS'), ('BIO')"
            )
cur.execute("""INSERT INTO professores (nome,departamento_id) VALUES 
             ('Caleb',1), ('Yago',2), ('Ruan',3)""")
cur.execute("""INSERT INTO materias (nome,departamento_id) VALUES 
             ('APC',1), ('FIS1',2), ('GEN',3)""")
cur.execute("""INSERT INTO turma (numero,materia_id,professor_id) VALUES 
             (12,1,1), (25,2,2), (35,3,3)""")
cur.execute("""INSERT INTO materias (nome,departamento_id) VALUES 
             ('APC',1), ('FIS1',2), ('Ruan',3)""")

with open("aluno.png", "rb") as f:
    lucas = f.read()

with open("aluno.png", "rb") as f:
    eduardo = f.read()

with open("aluno.png", "rb") as f:
    licas = f.read()

cur.execute("""INSERT INTO alunos (email,matricula,curso,senha, img,is_admin) VALUES 
             ('lucas@gmail.com','12345678','cic','123',?,1), 
             ('eduardo@gmail.com','12345679','cic','123',?,0), 
             ('licas@gmail.com','12345479','cic','123',?,0)""", (lucas,eduardo,licas))

cur.execute("""INSERT INTO avaliacoes (comentario,aluno_id,turma_id) VALUES 
             ('Gostei',1,1), 
             ('Podia ser melhor',2,2), 
             ('O professor deu pizza nota 10', 3, 3)""")

cur.execute("""INSERT INTO denuncia (report,avaliacao_id) VALUES 
             ('Nao podia nao',2), 
             ('Achei toxico',1), 
             ('Nao como pizza', 3)""")

connection.commit()
connection.close()