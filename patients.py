import json
from pathlib import Path
import os


FILE_BASE = Path(__file__).parent / "register_patients.json"


# Função para carregar Arquivo JSON
def load_json():
    try:
        with open(FILE_BASE, 'r') as file_json:
            dados = json.load(file_json)
            return dados
    except FileNotFoundError as e:
        print("Arquivo JSON não encontrado, erro:", e)


class Patients:
    _name: str
    _age: int
    _phone: str = None

    def __init__(self,
                 name,
                 age,
                 phone,
                 id=0):
        self.name = name
        self.age = age
        self.phone = phone
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
        if isinstance(value, int) and value:
            self._age = value
        else:
            raise ValueError("Erro no tipo de valor da idade")

    @phone.setter
    def phone(self, value):
        if len(value) != 11:
            raise ValueError("o tamanho do número está errado")
        else:
            self._phone = value
            
    # Método para cadastrar os atributos em um arquivo json
    def register(self):
        try:
            if os.path.exists(FILE_BASE):
                # Carregar arquivo json antes de salvar novos registros
                data = load_json()
            else:
                data = {"patients": [], "last_id": 0}

            # Criando um novo registro de paciente
            data["last_id"] += 1
            new_id = data["last_id"]
            register_patients = {
                "ID": new_id,
                "name": self.name.strip().lower(),
                "age": self.age,
                "phone": self.phone.strip()
            }

            data["patients"].append(register_patients)

            with open(FILE_BASE, 'w', encoding="utf-8") as file:
                return json.dump(data, file,
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
        dados = load_json()

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


# Função para buscar paciente pelo nome
def find_patient():
    '''
        Buscar Paciente pelo nome
    '''

    input_name = input("Digite o nome do Paciente: ").lower()
    try:
        dados = load_json()

        dados_patients = dados['patients']

        person_find = None

        for person in dados_patients:
            if person['name'] == input_name:
                person_find = person
                break
        print("\nPaciente Encontrado:")
        for key, value in person_find.items():
            print(f"{key}: {value}")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Não Encontrado: ", e)


if __name__ == "__main__":
    # dados ficticios para teste
    paciente_01 = Patients("Anderson", 32, "83999659911")
    paciente_02 = Patients("Maria", 65, "83996565651")
    paciente_03 = Patients("Genival", 58, "83995595541")

    paciente_01.register()
    paciente_02.register()
    paciente_03.register()

    paciente_04 = Patients("Fulano", 85, "83999559951").register()

    view_statistics()
