-- AVISO
-- Todos os dados inseridos no banco foram gerados aleatóriamente
-- As queries foram testadas em condições ideais, porém os dados recebidos podem fazer com que algumas queries não tenham resultados
-- Exemplo: Por azar ninguém conseguiu nota maior que 5 em nenhuma Matriz, portanto a query de puxar alunos formados não retornará nada
-- Acreditamos que a única query afetada por isso seja a de requisitar alunos formados
-- Caso o senhor quiser gerar novos dados, basta executar o GeradorDeDados.py e ele dará um output em TXT com novas queries de valores diferentes

-- Histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
SELECT 
    Aluno.nome AS nome_aluno,
    Disciplina.id_disciplina,
    Disciplina.nome AS nome_disciplina,
    Cursa.semestre,
    Cursa.ano,
    Cursa.nota
FROM 
    Cursa
JOIN 
    Disciplina ON Cursa.id_disciplina = Disciplina.id_disciplina
JOIN 
    Aluno ON Cursa.id_aluno = Aluno.id_aluno
WHERE 
    Aluno.id_aluno = id_aluno_desejado;


-- Histórico de disciplinas ministradas por qualquer professor, com semestre e ano:
SELECT 
    Professor.nome AS nome_professor,
    Disciplina.id_disciplina,
    Disciplina.nome AS nome_disciplina,
    Leciona.semestre,
    Leciona.ano
FROM 
    Leciona
JOIN 
    Disciplina ON Leciona.id_disciplina = Disciplina.id_disciplina
JOIN 
    Professor ON Leciona.id_professor = Professor.id_professor
WHERE 
    Professor.id_professor = id_professor_desejado;

-- Listar alunos que já se formaram (foram aprovados em todas as disciplinas de uma matriz curricular) em um determinado semestre de um ano:
-- Essa query ira mostrar todos os alunos que se formaram em uma Matriz, o ano e seu semestre de formação.
-- Para mostrar apenas de um ano ou semestre especifico, descomentar as linhas do código e alterá-lo de acordo.
SELECT
    A.id_aluno,
    A.nome AS aluno_nome,
    MAX(C.ano) AS ano_formatura,
    MAX(C.semestre) AS semestre_formatura
FROM
    Aluno A
    JOIN Cursa C ON A.id_aluno = C.id_aluno
    JOIN Disciplina D ON C.id_disciplina = D.id_disciplina
WHERE
     D.id_matriz = <id_matriz_desejado>
GROUP BY
    A.id_aluno,
    A.nome
HAVING
    MIN(C.nota) >= 5
    --AND MAX(C.ano) = 2022
    --AND MAX(C.semestre) = 5;

-- Listar todos os professores que são chefes de departamento, junto com o nome do departamento:
SELECT 
    Professor.nome AS nome_professor,
    Departamento.nome AS nome_departamento
FROM 
    Departamento
JOIN 
    Professor ON Departamento.id_professor = Professor.id_professor;

-- Saber quais alunos formaram um grupo de TCC e qual professor foi o orientador:
SELECT 
    TCC.id_tcc,
    TCC.titulo AS nome_tcc,
    Professor.nome AS nome_orientador,
    Aluno.id_aluno,
    Aluno.nome AS nome_aluno
FROM 
    Participa
JOIN 
    TCC ON Participa.id_tcc = TCC.id_tcc
JOIN 
    Professor ON Participa.id_professor = Professor.id_professor
JOIN 
    Aluno ON Participa.id_aluno = Aluno.id_aluno
ORDER BY 
    TCC.id_tcc, Aluno.nome;
