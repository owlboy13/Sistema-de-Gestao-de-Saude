import json
from pathlib import Path
import os
import pandas as pd


FILE_BASE = Path(__file__).parent / "register_patients.json"

DELETE_BASE = Path(__file__).parent / "patients_deleted.json"


# Função para carregar Arquivo JSON (existente)
def load_json():
    try:
        with open(FILE_BASE, 'r') as file_json:
            dados = json.load(file_json)
            return dados
    except FileNotFoundError as e:
        print("Arquivo JSON não encontrado, erro:", e)


def print_bar():
    return print("--" * 30)


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
                # Verificar se nome e telefone já existem no arquivo json
                for patient in data['patients']:
                    if (patient['Nome'].lower() == self.name.strip().lower()
                        and patient["Telefone"] == self.phone.strip()):
                        print(f"\nPaciente {patient['Nome']} "
                              "já está cadastrado!")
                        return False
            else:
                data = {"patients": [], "last_id": 0}

                

            # Criando um novo registro de paciente
            data["last_id"] += 1
            new_id = data["last_id"]
            register_patients = {
                "ID": new_id,
                "Nome": self.name.strip().lower(),
                "Idade": self.age,
                "Telefone": self.phone.strip()
            }

            data["patients"].append(register_patients)

            print(f"\nID {new_id} - Cadastro de {self.name} feito com sucesso!")
            print_bar()

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

        print_bar()
        print("\n -- Estatísticas -- \n")
        print(f"\nNúmero Total de Pacientes: {len(dados['patients'])}")

        patients_ = [dado['Idade'] for dado in dados['patients']]
        media_patients = sum(patients_) / len(patients_)
        print(f"\nMédia de idade dos Pacientes: {int(media_patients)} Anos")

        min_age = min(dados['patients'], key=lambda x: x['Idade'])
        max_age = max(dados['patients'], key=lambda x: x['Idade'])

        print("\nPaciente mais novo: "
              f"{min_age['Nome']} com {min_age['Idade']} anos")
        print("\nPaciente mais velho: "
              f"{max_age['Nome']} com {max_age['Idade']} anos\n")
        
        print_bar()

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
            if person['Nome'] == input_name:
                person_find = person
                break
        print_bar()
        print("\nPaciente Encontrado:")
        for key, value in person_find.items():
            print(f"{key}: {value}")
        print_bar()

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Não Encontrado: ", e)


def list_patients():
    try:
        print_bar()
        print("\nTodos os pacientes cadastrados: \n")
        file_json = pd.read_json("register_patients.json")
        df = pd.json_normalize(file_json['patients'])
        df = pd.DataFrame(df)
        print(df)
        print_bar()
    except TypeError as e:
        print("Erro: ", e)


def del_patient():
    try:
        dados = load_json()
        dados_patients = dados['patients']
        print_bar()
        del_ = int(input("Digite o ID do Paciente que deseja excluir: ")) - 1
        for item in dados_patients:
            if item.get('ID') == del_:
                removed_patient = dados_patients.pop(del_)
                print(f"Paciente {removed_patient['Nome']}"
                      "deletado com sucesso")
                break
        # Salvar Registro de Paciente deletado
        with open(DELETE_BASE, "w", encoding='utf-8') as file2:
            json.dump(removed_patient, file2,
                      indent=2, ensure_ascii=True)
        # Salvar novo registro sem o paciente deletado
        with open(FILE_BASE, 'w', encoding='utf-8') as file:
            json.dump(dados, file, indent=2, ensure_ascii=True)
        print_bar()
    except ValueError as e:
        print("Erro ao excluir paciente", e)
    except TypeError as e:
        print("Erro de tipo:", e)


# Dados ficticios para teste
if __name__ == "__main__":

    # paciente_01 = Patients("Anderson", 32, "83999659911")
    # paciente_02 = Patients("Maria", 65, "83996565651")
    # paciente_03 = Patients("Genival", 58, "83995595541")
    # paciente_01.register()
    # paciente_02.register()
    # paciente_03.register()
    # paciente_04 = Patients("Fulano", 85, "83999559951").register()
    # paciente_05 = Patients("Cicrano", 20, "83948554466").register()


    # view_statistics()

    #find_patient()

    del_patient()