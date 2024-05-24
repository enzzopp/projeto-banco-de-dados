# Sistema de Gestão de Faculdade - Ciência da Computação FEI

Este repositório contém o projeto final da disciplina de Banco de Dados do curso de Ciência da Computação no Centro Universitário FEI. O objetivo do projeto é desenvolver um sistema para gerenciar uma faculdade, abrangendo desde a estrutura dos departamentos e cursos até a alocação de alunos e professores.

## Descrição do Projeto

O sistema de gestão de faculdade abrange as seguintes funcionalidades e estruturas:

- **Departamentos:** A faculdade possui 8 departamentos.
- **Cursos:** Cada departamento oferece 1 curso, totalizando 8 cursos.
- **Matriz Curricular:** Cada curso possui 1 matriz curricular composta por 6 disciplinas.
- **Alunos:** Cada curso possui 5 alunos.
- **Professores:** Cada departamento possui 3 professores, sendo um deles o chefe do departamento. Cada professor leciona 2 disciplinas do curso.
- **Trabalho de Conclusão de Curso (TCC):** Existem 4 grupos de TCC, cada um composto por 5 alunos e orientado por 1 professor.

## Tecnologias Utilizadas

- **SGBD:** CockroachDB
- **Linguagem de Programação:** Python
- **Linguagem de Consulta:** SQL

## Instruções

1. Clone este repositório:
    ```bash
    git clone https://github.com/enzzopp/projeto-banco-de-dados.git
2. Navegue até o diretório do projeto:
    ```bash
    cd projeto-banco-de-dados
    ```
3. Execute os seguintes arquivos SQL para criar e popular o banco de dados no Cockroach:
    ```bash
    createSchema.sql
    dataInsertion.sql
    ```
4. Execute as queries a partir do arquivo SQL::
    ```bash
    queries.sql
    ```
5. Execute os scripts Python para gerar dados de teste (OPCIONAL):
    ```bash
    python dataGenerator.py
    ```
## Diagrama de Relacionamento

Este é o diagrama de relacionamento das tabelas do banco de dados usando Mermaid.

```mermaid
erDiagram
    Departamento {
        INT id_depto PK
        INT id_professor FK
        VARCHAR nome
        VARCHAR lugar
    }
    
    Curso {
        INT id_curso PK
        INT id_depto FK
        INT id_matriz FK
        VARCHAR nome
    }
    
    Disciplina {
        INT id_disciplina PK
        INT id_matriz FK
        VARCHAR nome
        NUMERIC semestre
    }
    
    MatrizCurricular {
        INT id_matriz PK
        INT id_curso FK
    }
    
    Cursa {
        INT id_disciplina FK
        INT id_aluno FK
        NUMERIC ano
        NUMERIC nota
        NUMERIC semestre
    }
    
    Aluno {
        INT id_aluno PK
        INT id_curso FK
        VARCHAR nome
    }
    
    Participa {
        INT id_tcc FK
        INT id_professor FK
        INT id_aluno FK
    }
    
    TCC {
        INT id_tcc PK
        VARCHAR titulo
    }
    
    Professor {
        INT id_professor PK
        INT id_depto FK
        VARCHAR nome
    }
    
    Leciona {
        INT id_disciplina FK
        INT id_professor FK
        NUMERIC ano
        NUMERIC semestre
    }

    Departamento ||--o{ Professor : "id_professor"
    Departamento ||--o{ Curso : "id_depto"
    Curso ||--o{ MatrizCurricular : "id_matriz"
    MatrizCurricular ||--o{ Disciplina : "id_matriz"
    MatrizCurricular ||--o{ Curso : "id_curso"
    Disciplina ||--o{ Cursa : "id_disciplina"
    Aluno ||--o{ Cursa : "id_aluno"
    Curso ||--o{ Aluno : "id_curso"
    TCC ||--o{ Participa : "id_tcc"
    Professor ||--o{ Participa : "id_professor"
    Aluno ||--o{ Participa : "id_aluno"
    Departamento ||--o{ Professor : "id_depto"
    Disciplina ||--o{ Leciona : "id_disciplina"
    Professor ||--o{ Leciona : "id_professor"
```

## Contribuidores

- [Enzo Pacheco Porfirio - 24.122.003-7](https://github.com/enzzopp)
- [Gabriel Destro - 24.122.059-9](https://github.com/httpDerpyy)
