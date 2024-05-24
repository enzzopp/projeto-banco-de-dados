
    CREATE TABLE Departamento (
        nome VARCHAR(15),
        lugar VARCHAR(15),
        id_depto INT PRIMARY KEY,
        id_professor INT
    );
    
    CREATE TABLE Curso (
        nome VARCHAR(60),
        id_curso INT PRIMARY KEY,
        id_depto INT,
        id_matriz INT
    );
    
    CREATE TABLE Disciplina (
        nome VARCHAR(15),
        semestre NUMERIC(2,0),
        id_disciplina INT PRIMARY KEY,
        id_matriz INT
    );
    
    CREATE TABLE MatrizCurricular (
        id_matriz INT PRIMARY KEY,
        id_curso INT
    );
    
    CREATE TABLE Cursa (
        ano NUMERIC(4,0) CHECK (ano > 1900 AND ano < 2100),
        nota NUMERIC(4,2) CHECK (nota >= 0 AND nota <= 10),
        semestre NUMERIC(2,0),
        id_disciplina INT,
        id_aluno INT
    );
    
    CREATE TABLE Aluno (
        id_aluno INT PRIMARY KEY,
        id_curso INT,
        nome VARCHAR(58)
    );
    
    CREATE TABLE Participa (
        id_tcc INT,
        id_professor INT,
        id_aluno INT
    );
    
    CREATE TABLE TCC (
        id_tcc INT PRIMARY KEY,
        titulo VARCHAR(15)
    );
    
    CREATE TABLE Professor (
        id_professor INT PRIMARY KEY,
        id_depto INT,
        nome VARCHAR(58)
    );
    
    CREATE TABLE Leciona (
        id_disciplina INT,
        id_professor INT,
        ano NUMERIC(4,0) CHECK (ano > 1900 AND ano < 2100),
        semestre NUMERIC(2,0)
    );
    
    ALTER TABLE Departamento
    ADD FOREIGN KEY (id_professor) REFERENCES Professor(id_professor)
    ON DELETE SET NULL;
    
    ALTER TABLE Curso
    ADD FOREIGN KEY (id_depto) REFERENCES Departamento(id_depto)
    ON DELETE SET NULL;
    
    ALTER TABLE Curso
    ADD FOREIGN KEY (id_matriz) REFERENCES MatrizCurricular(id_matriz)
    ON DELETE SET NULL;
    
    ALTER TABLE Disciplina
    ADD FOREIGN KEY (id_matriz) REFERENCES MatrizCurricular(id_matriz)
    ON DELETE SET NULL;
    
    ALTER TABLE MatrizCurricular
    ADD FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
    ON DELETE SET NULL;
    
    ALTER TABLE Cursa
    ADD FOREIGN KEY (id_disciplina) REFERENCES Disciplina(id_disciplina)
    ON DELETE SET NULL;
    
    ALTER TABLE Cursa
    ADD FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
    ON DELETE SET NULL;
    
    ALTER TABLE Aluno
    ADD FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
    ON DELETE SET NULL;
    
    ALTER TABLE Participa
    ADD FOREIGN KEY (id_tcc) REFERENCES TCC(id_tcc)
    ON DELETE SET NULL;
    
    ALTER TABLE Participa
    ADD FOREIGN KEY (id_professor) REFERENCES Professor(id_professor)
    ON DELETE SET NULL;
    
    ALTER TABLE Participa
    ADD FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
    ON DELETE SET NULL;
    
    ALTER TABLE Professor
    ADD FOREIGN KEY (id_depto) REFERENCES Departamento(id_depto)
    ON DELETE SET NULL;
    
    ALTER TABLE Leciona
    ADD FOREIGN KEY (id_disciplina) REFERENCES Disciplina(id_disciplina)
    ON DELETE SET NULL;
    
    ALTER TABLE Leciona
    ADD FOREIGN KEY (id_professor) REFERENCES Professor(id_professor)
    ON DELETE SET NULL;
    