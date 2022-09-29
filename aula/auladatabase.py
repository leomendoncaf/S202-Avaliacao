from database import Database


class AulaDatabase:
    def __init__(self):
        self._database = Database(database="Escola", collection="Aulas")

    def create(self, aula):
        prof = {"nome": aula.professor.nome,
                "especialidade": aula.professor.especialidade}
        alunos = []
        for al in aula.alunos:
            alunoTemp = {"nome": al.nome,
                         "matricula": al.matricula,
                         "curso": al.curso,
                         "periodo": al.periodo}
            alunos.append(alunoTemp)

        return self._database.collection.insert_one({"assunto": aula.assunto,
                                                     "professor": prof,
                                                     "alunos": alunos})

    def read(self):
        return self._database.collection.find({})

    def update(self, aula):
        alunos = []
        for al in aula.alunos:
            alunoTemp = {"nome": al.nome,
                         "matricula": al.matricula,
                         "curso": al.curso,
                         "periodo": al.periodo}
            alunos.append(alunoTemp)

        prof = {"nome": aula.professor.nome,
                "especialidade": aula.professor.especialidade}

        return self._database.collection.update_one(
            {"assunto": aula.assunto},
            {
                "$set": {"professor": prof,
                         "alunos": alunos},
                "$currentDate": {"lastModified": True}
            }
        )

    def delete(self, aula):
        return self._database.collection.delete_one({"assunto": aula.assunto})