from auladatabase import AulaDatabase


class Pessoa(object):
    def __init__(self, nome) -> None:
        self.nome = nome


class Professor(Pessoa):
    def __init__(self, especialidade = None, nome = None) -> None:
        Pessoa.__init__(self, nome)
        self.especialidade = especialidade

    def __str__(self) -> str:
        return f"{self.nome}"


class Aluno(Pessoa):
    def __init__(self, matricula = 0, curso = None, periodo = 0, nome = None)-> None:
        super().__init__(nome)
        self.matricula = int(matricula)
        self.curso = curso
        self.periodo = int(periodo)

    def __str__(self) -> str:
        return f"O aluno {self.nome} detentor da matricula {self.matricula} atualmente cursando {self.curso} no periodo {self.periodo}"


class Aula:
    def __init__(self, materia = None):
        self.materia = materia
        self.professor: Professor = None
        self.alunos: list[Aluno] = []

    def getListaPresenca(self) -> str:
        lista = ''
        for aluno in self.alunos:
            lista = lista + f'''
            nome: {aluno.nome}
            matricula: {aluno.matricula}
            curso: {aluno.curso}
            periodo: {aluno.periodo}
            '''
        return lista

    def __str__(self):
        info = f"Materia: {self.materia}"
        info += f"\n    Professor: {self.professor}"
        info += f"\n    Alunos Presentes:\n {self.getListaPresenca()}"
        return info

def printAulas(aulas):
    for aula in aulas:
        print(f"Materia: {aula['materia']}")
        print(f"Professor: {aula['professor']['nome']}")
        print(f"Especialidade: {aula['professor']['especialidade']}")
        for i, aluno in enumerate(aula['alunos']):
            print(f"Aluno {i + 1}: {aluno['nome']} ({aluno['matricula']})")
            print(f"     {aluno['curso']} - {aluno['periodo']}º período")

def getAula(reqAula):
    aulas = AulaDatabase().read()
    found = False

    for aula in aulas:
        if aula['materia'] == reqAula.materia:
            reqAula.professor = Professor()
            reqAula.professor.nome = aula['professor']['nome']
            reqAula.professor.especialidade = aula['professor']['especialidade']
            for i, aluno in enumerate(aula['alunos']):
                auxAluno = Aluno()
                auxAluno.nome = aluno['nome']
                auxAluno.periodo = aluno['periodo']
                auxAluno.periodo = aluno['periodo']
                auxAluno.curso = aluno['curso']
                reqAula.alunos.append(auxAluno)

                found = True

    if found:
        return reqAula
    else:
        return None


continua = True
while continua:
    x = input("1 - Adicionar\n"
                  "2 - Remover\n"
                  "3 - Atualizar\n"
                  "4 - Ler\n"
                  "0 - Sair\n"
                  "  ->  ")
    if x.isdigit(): x = int(x)

    match x:
        case 0:
            continua = False
            break
        case 1:
            aula = Aula()
            aula.professor = Professor()
            aula.alunos = []
            aula.materia = input("Materia: ")
            aula.professor.nome = input("Nome do Professor: ")
            aula.professor.especialidade = input("Especialidade do Professor: ")

            n = int(input("Quantos alunos há na classe: "))
            for i in range(0, n):
                alunotemp = Aluno()
                alunotemp.nome = input("Nome do Aluno: ")
                alunotemp.curso = input("Curso do Aluno: ")
                alunotemp.periodo = int(input("Periodo do Aluno: "))
                alunotemp.matricula = int(input("Matricula do Aluno: "))
                aula.alunos.append(alunotemp)

            AulaDatabase().create(aula)
        case 2:
            aulas = AulaDatabase().read()
            printAulas(aulas)

            aula = Aula()
            aula.materia = input("Materia da aula que quer remover: ")
            AulaDatabase().delete(aula)

            aulas = AulaDatabase().read()
            printAulas(aulas)
        case 3:
            aulas = AulaDatabase().read()
            printAulas(aulas)

            aula = Aula()
            aula.materia = input("materia da aula que quer alterar: ")

            aula = getAula(aula)

            if aula is None:
                print("Aula não encontrada")
            else:
                aux = input("Novo professor (dê enter para deixar como está): ")
                if aux != "":
                    aula.professor.nome = aux

                aux = input("Nova especialidade (dê enter para deixar como está): ")
                if aux != "":
                    aula.professor.especialidade = aux

                AulaDatabase().update(aula)

                aulas = AulaDatabase().read()
                printAulas(aulas)

        case 4:
            aulas = AulaDatabase().read()
            printAulas(aulas)

        case _:
            print("Opção inválida")