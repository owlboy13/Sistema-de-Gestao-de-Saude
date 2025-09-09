import json
from pathlib import Path
import os


FILE_BASE = Path(__file__).parent / "register_patients.json"


class Patients:
    def __init__(self,
                 name: str,
                 age: int,
                 phone: str,
                 data={"patients": [],
                       "last_id": 0},
                 id=0):
        self._name = name
        self._age = age
        self._phone = phone
        self._data = data
        self._id = id

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def phone(self):
        return self._phone

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value:
            self._name = value
        else:
            raise ValueError("Erro no tipo de valor do nome")

    @age.setter
    def age(self, value):
        if isinstance(value, str) and value:
            self._age = value
        else:
            raise ValueError("Erro no tipo de valor da idade")

    @phone.setter
    def phone(self, value):
        if isinstance(value, str) and value:
            self._phone = value
        else:
            raise ValueError("Erro no tipo de valor do telefone")

    # Método para cadastrar os atributos em um arquivo json
    def register(self):
        try:
            self._data["last_id"] += 1
            new_id = self._data["last_id"]
            register_patients = {
                "ID": new_id,
                "name": self.name.strip(),
                "age": self.age,
                "phone": self.phone.strip()
            }

            self._data["patients"].append(register_patients)

            with open(FILE_BASE, 'w', encoding="utf-8") as file:
                return json.dump(self._data, file,
                                 ensure_ascii=False, indent=2)

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print("Erro ao tentar registrar paciente no json: ", e)


# Função para Carregar o json e exibir as estatisticas exigidas
def view_statistics():
    '''
        o Número total de pacientes cadastrados
        o Idade média dos pacientes
        o Paciente mais novo e mais velho
    '''
    try:
        if os.path.exists(FILE_BASE):
            with open(FILE_BASE, 'r') as file_json:
                dados = json.load(file_json)

        print(f"\nNúmero Total de Pacientes: {dados['last_id']}")

        patients_ = [dado['age'] for dado in dados['patients']]
        media_patients = sum(patients_) / len(patients_)
        print(f"\nMédia de idade dos Pacientes: {int(media_patients)} Anos")

        min_age = min(dados['patients'], key=lambda x: x['age'])
        max_age = max(dados['patients'], key=lambda x: x['age'])

        print("\nPaciente mais novo: "
              f"{min_age['name']} com {min_age['age']} anos")
        print("\nPaciente mais velho: "
              f"{max_age['name']} com {max_age['age']} anos")

    except Exception as e:
        print("Erro ao exibir as estatísticas: ", e)

def find_patient(name):
    '''
        Buscar Paciente pelo novo
    '''
    pass



if __name__ == "__main__":

    paciente_01 = Patients("Anderson Luiz", 32, "83996208929")
    paciente_02 = Patients("Maria", 65, "8399656565")
    paciente_03 = Patients("Genival", 58, "83995595954")

    paciente_01.register()
    paciente_02.register()
    paciente_03.register()

    view_statistics()