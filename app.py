
from patients import Patients, view_statistics, find_patient


class App:
    def __init__(self,):
        self._name = str(input("Digite o nome completo do paciente: "))
        self._age = int(input("Digite a idade do paciente: "))
        self._phone = str(input("Digite o telefone do paciente: "))
        self.options = None


    def menu(self):
        while True:
            try:
                print("\n===SISTEMA CLÍNICA VIDA+===\n")
                self.options = int(input("""
                        \n1. Cadastrar Paciente
                        \n2. Ver Estatísticas
                        \n3. Buscar paciente
                        \n4. Listar todos os pacientes
                        \n5. Sair
                        \nEscolha uma opção: """))
            except ValueError:
                print("Digite apenas um número")

    def comands(self):
        comands_ = {
            1: lambda: Patients(self._name, self._age, self._phone),
            2: lambda: view_statistics(),
            3: lambda: find_patient(),
            4: lambda: 

        }
