import string
import requests
import secrets
import random

# Data Pool
LETTERS = list(string.ascii_uppercase)
NUMBERS = list(range(10))
STRING_NUMBERS = [str(i) for i in range(10)]

NAMES = []
SURNAMES = []

# Pegando nomes e sobrenomes
response = requests.get('https://randomuser.me/api/?results=25&nat=br')
data = response.json()

for user in data['results']:
    NAMES.append(user['name']['first'])
    SURNAMES.append(user['name']['last'])

# Dados padrões
NOME_DEPARTAMENTOS = ["Matemática", "Física", "Química", "Biologia", "Computação", "Estatística", "Engenharia", "Geofísica"]
NOME_CURSOS = ["Matemática", "Engenharia Elétrica", "Engenharia Química", "Biomedicina", "Ciência da Computação", "Análise de Dados", "Engenharia Cívil", "Geologia"]

# Gerando os dados completos
DEPARTAMENTOS = []
CURSOS = []
DISCIPLINAS = []
ALUNOS = []
PROFESSORES = []
TCCS = []
MATRIZ_CURRICULAR = []
CURSA = []
PARTICIPA = []
LECIONA = []

# Funções Geradoras
def generate_id(existing_ids):
    new_id = secrets.randbelow(10000)
    while new_id in existing_ids:
        new_id = secrets.randbelow(10000)
    return new_id

def generate_departamento():
    deptos = []
    for departamento in NOME_DEPARTAMENTOS:
        lugar = 'Prédio ' + ''.join(secrets.choice(LETTERS))
        id_depto = generate_id( [ [d['id_depto']] for d in deptos ] )
        deptos.append({
            'nome': departamento,
            'lugar': lugar,
            'id_depto': id_depto
        })
    return deptos

def generate_curso(deptos):
    cursos = []
    for curso in NOME_CURSOS:
        id_curso = generate_id([c['id_curso'] for c in cursos])
        id_depto = deptos[NOME_CURSOS.index(curso)]['id_depto'] 
        cursos.append({
            'nome': curso,
            'id_curso': id_curso,
            'id_depto': id_depto
        })
    return cursos

def generate_matriz_curricular(cursos):
    matrizes = []
    for curso in cursos:
        id_matriz = generate_id([m['id_matriz'] for m in matrizes])
        id_curso = curso['id_curso']
        curso['id_matriz'] = id_matriz
        matrizes.append({
            'id_matriz': id_matriz,
            'id_curso': id_curso,
        })
    return matrizes

def generate_disciplinas(matrizes):
    disciplinas = []
    for matriz in matrizes:
        for i in range(6):
            id_disciplina = generate_id([d['id_disciplina'] for d in disciplinas])
            id_matriz = matriz['id_matriz']
            nome = ''.join(secrets.choice(LETTERS) for _ in range(2)) + '-' + ''.join(secrets.choice(STRING_NUMBERS) for _ in range(4))
            semestre = secrets.randbelow(8) + 1
            disciplinas.append({
                'id_disciplina': id_disciplina,
                'id_matriz': id_matriz,
                'nome': nome,
                'semestre': semestre,
            })
    return disciplinas

# Aluno deve ser criado relacionado ao Curso e atribuido as Disciplinas da Matriz Curricular do respectivo curso
def generate_alunos(matrizes):
    alunos = []
    for matriz in matrizes:
        for i in range(5):
            id_aluno = generate_id([a['id_aluno'] for a in alunos])
            id_curso = matriz['id_curso']
            nome = random.choice(NAMES) + ' ' + random.choice(SURNAMES)
            alunos.append({
                'id_aluno': id_aluno,
                'id_curso': id_curso,
                'nome': nome,
            })
    return alunos

def generate_cursa(alunos, disciplinas, cursos):
    cursa = []
    for aluno in alunos:
        for disciplina in disciplinas:
            matriz_aluno = [ curso for curso in cursos if curso.get('id_curso') == aluno['id_curso'] ][0]
            if matriz_aluno['id_matriz'] == disciplina['id_matriz']:
                cursa.append({
                    'id_disciplina': disciplina['id_disciplina'],
                    'id_aluno': aluno['id_aluno'],
                    'semestre': disciplina['semestre'],
                    'ano': (2020 + ((disciplina['semestre'] - 1) // 2)) ,
                    'nota': round(random.uniform(0, 10), 2),
                }) 
    return cursa

# Criar 3 professores por departamento, sendo o primeiro o chefe do departamento, cada professor leciona 2 disciplinas do curso.
def generate_professores(deptos):
    professores = []
    for depto in deptos:
        for i in range(3):
            id_professor = generate_id([p['id_professor'] for p in professores])
            id_depto = depto['id_depto']
            nome = random.choice(NAMES) + ' ' + random.choice(SURNAMES)
            professores.append({
                'id_professor': id_professor,
                'id_depto': id_depto, 
                'nome': nome,
            })
            # Torna o primeiro professor chefe do departamento
            if not ('id_professor' in depto):
                depto['id_professor'] = id_professor
    return professores

def generate_leciona(professores, cursos, matrizes, disciplinas):
    leciona = []
    for professor in professores:      
        # Encontrar disciplinas que podem ser lecionadas por esse professor
        curso_professor = [curso for curso in cursos if curso.get('id_depto') == professor['id_depto']][0]
        matriz_professor = [matriz for matriz in matrizes if matriz.get('id_curso') == curso_professor.get('id_curso')][0]
        disciplinas_professor = [disciplina for disciplina in disciplinas if disciplina.get('id_matriz') == matriz_professor.get('id_matriz')]

        # Atribuir ao professor duas disciplinas para lecionar
        lecionando = 0
        for disciplina in disciplinas_professor:
            if lecionando >= 2:
                break
            if not disciplina.get('lecionada'):
                leciona.append({
                    'id_disciplina': disciplina['id_disciplina'],
                    'id_professor': professor['id_professor'],
                    'ano': random.randint(2020, 2024),
                    'semestre': disciplina['semestre']
                })
                disciplina['lecionada'] = True
                lecionando += 1
    return leciona
          
# Seram 4 grupos de TCC, cursados cada por 5 alunos e orientado por 1 professor
def generate_TCC():
    tcc = []
    for i in range(4):
        tcc.append({
            'id_tcc': generate_id([t['id_tcc'] for t in tcc]),
            'titulo': 'Projeto ' + ''.join( secrets.choice(LETTERS) for n in range(3))
        })
    return tcc

def generate_participa(tccs, alunos, professores):
    participa = []
    for tcc in tccs:
        # Escolhe 1 professor para ser orientador do TCC
        professor_atribuido = None 
        for professor in professores:
            if not (professor.get('orientaTCC')):
                professor_atribuido = professor
                professor['orientaTCC'] = True
                break

        # Escolhe 5 alunos para participar do TCC
        alunos_atribuidos = 0
        for aluno in alunos:
            if alunos_atribuidos >= 5:
                break
            if not (aluno.get('fazTCC')):
                participa.append({
                    'id_tcc': tcc['id_tcc'],
                    'id_professor': professor_atribuido['id_professor'],
                    'id_aluno': aluno['id_aluno'],
                })
                alunos_atribuidos += 1
                aluno['fazTCC'] = True
    return participa


DEPARTAMENTOS = generate_departamento()
CURSOS = generate_curso(DEPARTAMENTOS)
MATRIZES = generate_matriz_curricular(CURSOS)
DISCIPLINAS = generate_disciplinas(MATRIZES)
ALUNOS = generate_alunos(MATRIZES)
CURSA = generate_cursa(ALUNOS, DISCIPLINAS, CURSOS)
PROFESSORES = generate_professores(DEPARTAMENTOS)
LECIONA = generate_leciona(PROFESSORES, CURSOS, MATRIZES, DISCIPLINAS)
TCC = generate_TCC()
PARTICIPA = generate_participa(TCC, ALUNOS, PROFESSORES)

file = open("dataInsertion.txt", "a", encoding="utf-8")

# # Inserindo dados no banco
# Função para inserir dados na tabela Departamento
def insert_departamentos(departamentos):
    query = "INSERT INTO Departamento (nome, lugar, id_depto) VALUES (%s, %s, %s)"
    for depto in departamentos:
        file.write(query % (depto['nome'], depto['lugar'], depto['id_depto']) + "\n")
    
# Função para inserir dados na tabela Curso
def insert_cursos(cursos):
    query = "INSERT INTO Curso (nome, id_curso, id_depto) VALUES (%s, %s, %s)"
    for curso in cursos:
        file.write(query % (curso['nome'], curso['id_curso'], curso['id_depto']) + "\n")
    
# Função para inserir dados na tabela MatrizCurricular
def insert_matriz_curricular(matriz_curricular):
    query = "INSERT INTO MatrizCurricular (id_matriz, id_curso) VALUES (%s, %s)"
    for matriz in matriz_curricular:
        file.write(query % (matriz['id_matriz'], matriz['id_curso']) + "\n")
    
# Função para inserir dados na tabela Disciplina
def insert_disciplinas(disciplinas):
    query = "INSERT INTO Disciplina (nome, semestre, id_disciplina, id_matriz) VALUES (%s, %s, %s, %s)"
    for disciplina in disciplinas:
        file.write(query % (disciplina['nome'], disciplina['semestre'], disciplina['id_disciplina'], disciplina['id_matriz']) + "\n")
    
# Função para inserir dados na tabela Aluno
def insert_alunos(alunos):
    query = "INSERT INTO Aluno (id_aluno, nome, id_curso) VALUES (%s, %s, %s)"
    for aluno in alunos:
        file.write(query % (aluno['id_aluno'], aluno['nome'], aluno['id_curso']) + "\n")
    
# Função para inserir dados na tabela Professor
def insert_professores(professores):
    query = "INSERT INTO Professor (id_professor, nome, id_depto) VALUES (%s, %s, %s)"
    for professor in professores:
        file.write(query % (professor['id_professor'], professor['nome'], professor['id_depto']) + "\n")
    
# Função para inserir dados na tabela TCC
def insert_tccs(tccs):
    query = "INSERT INTO TCC (id_tcc, titulo) VALUES (%s, %s)"
    for tcc in tccs:
        file.write(query % (tcc['id_tcc'], tcc['titulo']) + "\n")
    
# Função para inserir dados na tabela Cursa
def insert_cursa(cursa):
    query = "INSERT INTO Cursa (ano, semestre, nota, id_disciplina, id_aluno) VALUES (%s, %s, %s, %s, %s)"
    for cursa in cursa:
        file.write(query % (cursa['ano'], cursa['semestre'], cursa['nota'], cursa['id_disciplina'], cursa['id_aluno']) + "\n")
    
# Função para inserir dados na tabela Participa
def insert_participa(participa):
    query = "INSERT INTO Participa (id_tcc, id_professor, id_aluno) VALUES (%s, %s, %s)"
    for participa in participa:
        file.write(query % (participa['id_tcc'], participa['id_professor'], participa['id_aluno']) + "\n")
    
# Função para inserir dados na tabela Leciona
def insert_leciona(leciona):
    query = "INSERT INTO Leciona (ano, semestre, id_disciplina, id_professor) VALUES (%s, %s, %s, %s)"
    for leciona in leciona:
        file.write(query % (leciona['ano'], leciona['semestre'], leciona['id_disciplina'], leciona['id_professor']) + "\n")
    
# Atualiza os dados do Departamentos para inserir o id_professor como foreign key
def update_departamento_with_professor(departamentos):
    query = "UPDATE Departamento SET id_professor = %s WHERE id_depto = %s"
    for depto in departamentos:
        # Verifica se o departamento possui um id_professor
        if 'id_professor' in depto:
            file.write(query % (depto['id_professor'], depto['id_depto']) + "\n")
    
def update_cursos_with_matriz(cursos):
    query = "UPDATE Curso SET id_matriz = %s WHERE id_curso = %s"
    for curso in cursos:
        if 'id_matriz' in curso:
            file.write(query % (curso['id_matriz'], curso['id_curso']) + "\n")
    

# Inserindo os dados na ordem correta para garantir a integridade referencial
insert_departamentos(DEPARTAMENTOS)
insert_cursos(CURSOS)
insert_matriz_curricular(MATRIZES)
insert_disciplinas(DISCIPLINAS)
insert_professores(PROFESSORES)
insert_alunos(ALUNOS)
insert_cursa(CURSA)
insert_tccs(TCC)
insert_participa(PARTICIPA)
insert_leciona(LECIONA)
update_departamento_with_professor(DEPARTAMENTOS)
update_cursos_with_matriz(CURSOS)

# Fechando o arquivo
file.close()

print("Dados criados com sucesso")