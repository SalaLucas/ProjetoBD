CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    matricula VARCHAR(8) NOT NULL UNIQUE,
    curso VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    img bytea,
    is_admin BOOLEAN DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL
);
  
CREATE TABLE IF NOT EXISTS professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    departamento_id INT NOT NULL,
    CONSTRAINT fk_departamento_id
    FOREIGN KEY (departamento_id)
    REFERENCES departamentos (id)
);
  
CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    departamento_id INT NOT NULL,
    CONSTRAINT fk_departamento_id
    FOREIGN KEY (departamento_id)
    REFERENCES departamentos (id)
);  
  
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comentario VARCHAR(250),
    aluno_id INT,
    turma_id INT,
    CONSTRAINT fk_aluno_id
    FOREIGN KEY (aluno_id)
    REFERENCES alunos (matricula),
    CONSTRAINT fk_turma_id
    FOREIGN KEY (turma_id)
    REFERENCES turma (numero)
);
  
CREATE TABLE IF NOT EXISTS turma (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INT NOT NULL UNIQUE,
    materia_id INT,
    professor_id INT,
    CONSTRAINT fk_materia_id
    FOREIGN KEY (materia_id)
    REFERENCES materias (id),
    CONSTRAINT fk_professor_id
    FOREIGN KEY (professor_id)
    REFERENCES professores (id)
);

CREATE TABLE IF NOT EXISTS denuncia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report VARCHAR(250),
    avaliacao_id INT,
    CONSTRAINT fk_avaliacao_id
    FOREIGN KEY (avaliacao_id)
    REFERENCES avaliacoes (id)
);

CREATE VIEW vw_turma AS
    SELECT professores.nome AS professor_nome, materias.nome AS materia_nome, turma.numero AS turma_numero, turma.id AS id
    FROM professores
    JOIN materias ON professores.departamento_id = materias.departamento_id
    JOIN turma ON materias.id = turma.materia_id;


CREATE TRIGGER deleta_denuncia
AFTER DELETE ON avaliacoes
FOR EACH ROW
BEGIN
    DELETE FROM denuncia WHERE avaliacao_id = OLD.id;
END;